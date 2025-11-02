# 🧩 Join Lineage Evaluation Pipeline

A **LangGraph + LangChain + LangSmith** powered pipeline that automatically scans a GitHub repository, extracts **SQL and DataFrame joins**, traces **PySpark temp view lineage**, and evaluates model performance with **observability metrics**.

---

## 🚀 Features

- 🔍 **GitHub Code Scanner** — clones and parses `.py`, `.sql`, `.scala`, `.ipynb` files.
- 🤖 **LLM-Powered Join Extraction** — uses Ollama (e.g., `llama3.2`) to detect SQL and Spark DataFrame joins.
- 🧩 **Lineage Resolution** — maps temp views to their underlying source tables.
- 🌐 **LangGraph DAG Orchestration** — modular pipeline (load → extract joins → lineage → resolve).
- 📊 **LangSmith Observability** — trace, span, and latency logging for each stage.
- 🧪 **Evaluation Suite** — built-in ground-truth evaluator (Precision, Recall, F1).

---

## 🏗️ Architecture Overview

```mermaid
graph TD
  A[GitHub Loader] --> B[Join Extractor (LLM)]
  A --> C[Temp View Lineage Extractor]
  B --> D[Lineage Resolver]
  C --> D
  D --> E[Resolved Join Output]
```

---

## ⚙️ Installation

1. Clone this repo or download the script:

```bash
curl -O https://your-download-url/join_lineage_eval_pipeline.py
```

2. Install dependencies:

```bash
pip install langchain langchain-community langgraph langsmith langchain-ollama
```

3. (Optional) Configure environment variables for observability:

```bash
export LANGCHAIN_API_KEY="your_langchain_api_key"
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_PROJECT="join-lineage-observability"
```

4. Ensure Ollama is running locally and the model (e.g., `llama3.2`) is available:

```bash
ollama pull llama3.2
```

---

## 🧠 Usage

### 🔹 Run on a GitHub repo

```bash
python join_lineage_eval_pipeline.py --repo_url https://github.com/your-org/your-repo
```

This will:
- Clone the repo
- Extract SQL/DataFrame joins
- Resolve PySpark temp tables to base tables
- Print all resolved joins as JSON

### 🔹 Run Evaluation Suite

```bash
python join_lineage_eval_pipeline.py --eval
```

This will:
- Use example evaluation data (`EXAMPLE_DATA`)
- Run the full pipeline for each case
- Compute Precision, Recall, and F1

Example output:

```bash
[eval] Metrics: {'precision': 0.91, 'recall': 0.86, 'f1': 0.88}
```

---

## 🧩 Example Output

```json
[
  {
    "type": "INNER",
    "source_objects": ["orders", "customers"],
    "join_keys": ["orders.customer_id = customers.id"],
    "join_style": "SQL"
  },
  {
    "type": "LEFT",
    "source_objects": ["transactions", "payments"],
    "join_keys": ["transactions.id = payments.txn_id"],
    "join_style": "DataFrame"
  }
]
```

---

## 🧪 Evaluation Metrics

| Metric | Description |
|--------|--------------|
| **Precision** | % of extracted joins that are correct |
| **Recall** | % of true joins that were detected |
| **F1** | Combined precision-recall measure |
| **Latency** | Time taken per repo (tracked in LangSmith) |
| **Lineage Accuracy** | % of temp views correctly resolved |

---

## 🧱 File Structure

```
join_lineage_eval_pipeline.py   # main pipeline and evaluation harness
README.md                       # this file
```

---

## 🔭 Future Enhancements

- Integrate **LangSmith auto-benchmarking** for version comparison  
- Export resolved joins to S3 or a metadata catalog (Glue / Hive)  
- Add **Graph visualization** of join lineage  
- Extend to **dbt** and **Snowflake SQL scripts**  

---

## 🧑‍💻 Author

**Rutwik Thamira**  
Data Engineering & GenAI Solutions | Banking & LLM Frameworks
