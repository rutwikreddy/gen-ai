import os
import re
import time
import json
import argparse
from typing import List, Dict, Any
from src.utils.join_lineage_eval_pipeline import *

def main():
    parser = argparse.ArgumentParser(description="Join Lineage Eval Pipeline")
    parser.add_argument("--repo_url", type=str, help="GitHub repo url to scan")
    parser.add_argument("--eval", action="store_true", help="Run example evaluation suite")
    parser.add_argument("--branch", type=str, default="main")
    parser.add_argument("--model", type=str, default="llama3.2")
    args = parser.parse_args()

    if args.eval:
        run_evaluation_suite()
    elif args.repo_url:
        run_pipeline_for_repo(args.repo_url, branch=args.branch, llm_model=args.model)
    else:
        print("Provide --repo_url or --eval. Use -h for help.")

if __name__ == "__main__":
    main()