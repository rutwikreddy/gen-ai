"""
join_lineage_eval_pipeline.py

A self-contained pipeline that:
- Loads a GitHub repo (via GitLoader)
- Extracts JOINs (SQL + DataFrame) using an LLM (Ollama)
- Extracts PySpark temp view lineage
- Resolves lineage (replace temp views with their source tables)
- Builds a LangGraph DAG to orchestrate the workflow
- Adds LangSmith tracing & simple custom metrics
- Provides a minimal evaluation harness (example dataset + evaluator)

Notes / placeholders:
- Set LANGCHAIN_API_KEY / LANGCHAIN_TRACING_V2 / other env vars externally.
- This file intentionally uses placeholders for API keys and repo URLs.
- Adjust models, repo_url, and dataset paths as needed.

Usage:
    python join_lineage_eval_pipeline.py --repo_url https://github.com/your-org/your-repo

Outputs:
- Prints resolved joins to stdout
- (Optional) Hook into LangSmith / Prometheus as desired

"""

import os
import re
import time
import json
import argparse
from typing import List, Dict, Any

# LangChain / LangGraph / LangSmith imports
try:
    from langchain_community.document_loaders import GitLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_ollama import OllamaLLM
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    from langgraph.graph import Graph, StateGraph, END
    from langgraph.nodes import TransformNode
    # LangSmith tracing - import best-effort (placeholder if not installed)
    from langsmith import client as ls_client, traceable
except Exception as e:
    # Provide informative message when modules are unavailable.
    print("Warning: One or more Lang* libraries are not installed or importable.")
    print("Install required packages to run the pipeline: langchain, langchain-community, langgraph, langsmith, langchain-ollama")
    print("Error detail:", e)
    # Continue — the script can still be inspected or saved even if imports fail.

# -----------------------------
# Helper utilities
# -----------------------------
def safe_json_loads(s: str):
    try:
        return json.loads(s)
    except Exception:
        return []

def is_temp_name(name: str) -> bool:
    n = (name or "").lower()
    temp_patterns = ["tmp_", "temp_", "stg_", "cte_", "#", "_tmp", "_join", "_merged", "_intermediate"]
    return any(p in n for p in temp_patterns)

# -----------------------------
# 1) GitHub Loader Node
# -----------------------------
def github_loader_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    repo_url = state.get("repo_url")
    branch = state.get("branch", "main")
    file_exts = state.get("file_exts", (".py", ".sql", ".scala", ".ipynb"))
    print(f"[load_repo] Loading repo: {repo_url} branch={branch}")
    loader = GitLoader(
        clone_url=repo_url,
        repo_path="repo_clone",
        branch=branch,
        file_filter=lambda f: f.endswith(file_exts)
    )
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    return {"docs": docs, "chunks": chunks}

# -----------------------------
# 2) Join Extractor Node (LLM)
# -----------------------------
JOIN_PROMPT = PromptTemplate(
    input_variables=["code", "file"],
    template=(
        "You are a data engineering code analyzer.\n"
        "Extract all JOIN operations (SQL or DataFrame) from the following code.\n"
        "Return a JSON array where each element has: file, type, source_objects, join_keys, condition, join_style.\n"
        "If no joins found, return an empty list.\n\n"
        "Code from {file}:\n{code}"
    )
)

def join_extractor_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    chunks = state.get("chunks", [])
    print(f"[extract_joins] Running join extraction on {len(chunks)} chunks")
    llm = OllamaLLM(model=state.get("llm_model", "llama3.2"))
    chain = LLMChain(llm=llm, prompt=JOIN_PROMPT)
    all_joins = []
    for c in chunks:
        file_name = c.metadata.get("source", "unknown")
        try:
            response = chain.run({"code": c.page_content, "file": file_name})
            parsed = safe_json_loads(response)
            if isinstance(parsed, list):
                all_joins.extend(parsed)
        except Exception as e:
            print(f"[extract_joins] Warning: LLM call failed for {file_name}: {e}")
    print(f"[extract_joins] Found {len(all_joins)} raw joins (unfiltered)")
    return {"joins": all_joins}

# -----------------------------
# 3) TempView Lineage Extractor Node
# -----------------------------
TEMP_VIEW_RE = re.compile(r'(\w+)\.createOrReplace(?:Global)?TempView\(["\']([\w_]+)["\']\)', re.IGNORECASE)

def tempview_lineage_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    docs = state.get("docs", [])
    lineage: Dict[str, List[str]] = {}
    print(f"[extract_lineage] Scanning {len(docs)} documents for temp view creation")
    for doc in docs:
        code = getattr(doc, "page_content", "") or ""
        matches = TEMP_VIEW_RE.findall(code)
        for df_name, temp_name in matches:
            # Attempt to discover sources used to build df_name
            sources = re.findall(rf'{re.escape(df_name)}\s*=\s*spark\.read\.(?:table|format|parquet).*?["\']([\w_]+)["\']', code, re.IGNORECASE)
            if not sources:
                # look for join patterns like df_x = df_a.join(df_b, ...)
                join_matches = re.findall(rf'{re.escape(df_name)}\s*=\s*(\w+)\.join\((\w+)', code)
                if join_matches:
                    sources = [src for pair in join_matches for src in pair]
            lineage[temp_name.lower()] = list(dict.fromkeys(sources))
    print(f"[extract_lineage] Discovered {len(lineage)} temp view lineage mappings")
    return {"lineage_map": lineage}

# -----------------------------
# 4) Lineage Resolver Node
# -----------------------------
def lineage_resolver_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    joins = state.get("joins", [])
    lineage_map = state.get("lineage_map", {})
    print(f"[resolve_lineage] Resolving {len(joins)} joins using lineage_map of size={len(lineage_map)}")

    def expand_sources(srcs: List[str]):
        expanded = []
        for s in srcs:
            if not s:
                continue
            s_lower = s.lower()
            if s_lower in lineage_map:
                expanded.extend(lineage_map[s_lower])
            else:
                expanded.append(s)
        # remove temps and dedupe
        expanded = [e for e in expanded if not is_temp_name(e)]
        return list(dict.fromkeys(expanded))

    resolved = []
    for j in joins:
        sources = j.get("source_objects", []) or []
        resolved_sources = expand_sources(sources)
        j["source_objects"] = resolved_sources
        resolved.append(j)
    print(f"[resolve_lineage] Produced {len(resolved)} resolved joins")
    return {"resolved_joins": resolved}

# -----------------------------
# Observability / Tracing helpers (LangSmith client)
# -----------------------------
# We wrap node functions with traceable if available; otherwise noop wrappers.
def maybe_traceable(name):
    try:
        return traceable(name=name)
    except Exception:
        # fallback no-op decorator
        def _noop(f):
            return f
        return _noop

# -----------------------------
# Build LangGraph Graph
# -----------------------------
def build_graph():
    print("[build_graph] Building LangGraph DAG")
    graph = StateGraph()
    graph.add_node("load_repo", TransformNode(func=maybe_traceable("load_repo")(github_loader_tool)))
    graph.add_node("extract_joins", TransformNode(func=maybe_traceable("extract_joins")(join_extractor_tool)))
    graph.add_node("extract_lineage", TransformNode(func=maybe_traceable("extract_lineage")(tempview_lineage_tool)))
    graph.add_node("resolve_lineage", TransformNode(func=maybe_traceable("resolve_lineage")(lineage_resolver_tool)))

    graph.add_edge("load_repo", "extract_joins")
    graph.add_edge("load_repo", "extract_lineage")
    graph.add_edge("extract_joins", "resolve_lineage")
    graph.add_edge("extract_lineage", "resolve_lineage")
    graph.add_edge("resolve_lineage", END)

    return Graph(graph)

# -----------------------------
# Minimal evaluator helper
# -----------------------------
def flatten_joins(joins: List[Dict[str, Any]]):
    """Simplify joins to tuples for comparison"""
    out = []
    for j in joins:
        t = (j.get("type", "").lower() if j.get("type") else "unknown")
        objs = tuple(sorted([s.lower() for s in j.get("source_objects", [])]))
        out.append((t, objs))
    return sorted(out)

def compute_metrics(examples: List[Dict[str, Any]], predictions: List[Dict[str, Any]]):
    """Compute precision / recall / f1 over a small dataset."""
    y_true = []
    y_pred_bool = []
    for ex, pred in zip(examples, predictions):
        gt = flatten_joins(ex["expected_output"]["joins"])
        pr = flatten_joins(pred.get("joins", pred.get("resolved_joins", [])))
        for j in gt:
            y_true.append(j)
            y_pred_bool.append(j in pr)
    precision = sum(y_pred_bool) / len(y_pred_bool) if y_pred_bool else 0.0
    recall = sum(y_pred_bool) / len(y_true) if y_true else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}

# -----------------------------
# Example evaluation dataset (small)
# -----------------------------
EXAMPLE_DATA = [
    {
        "input": {"repo_url": "https://github.com/example/repo1"},
        "expected_output": {
            "joins": [
                {
                    "type": "INNER",
                    "source_objects": ["orders", "customers"],
                    "join_keys": ["orders.customer_id = customers.id"],
                    "join_style": "SQL"
                }
            ]
        }
    },
    # Add more examples as needed
]

# -----------------------------
# CLI / Main
# -----------------------------
def run_pipeline_for_repo(repo_url: str, branch: str = "main", llm_model: str = "llama3.2"):
    graph = build_graph()
    initial_state = {
        "repo_url": repo_url,
        "branch": branch,
        "llm_model": llm_model
    }
    final_state = graph.invoke(initial_state)
    # final_state contains 'resolved_joins' (from our DAG)
    resolved = final_state.get("resolved_joins", [])
    print(json.dumps(resolved, indent=2))
    return resolved

def run_evaluation_suite():
    print("[eval] Running evaluation suite on example dataset")
    predictions = []
    for ex in EXAMPLE_DATA:
        repo_url = ex["input"]["repo_url"]
        preds = run_pipeline_for_repo(repo_url)
        predictions.append({"resolved_joins": preds, "joins": preds})
    metrics = compute_metrics(EXAMPLE_DATA, predictions)
    print("[eval] Metrics:", metrics)
    return metrics


