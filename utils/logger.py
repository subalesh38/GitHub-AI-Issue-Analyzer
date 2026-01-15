import json
import os
from datetime import datetime
from pathlib import Path

# Create data directory structure
DATA_DIR = Path("data")
LOGS_DIR = DATA_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def log_analysis(owner: str, repo: str, results: dict):
    """
    Log analysis results to a JSON file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{owner}_{repo}_{timestamp}.json"
    filepath = LOGS_DIR / filename
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "repository": f"{owner}/{repo}",
        "results": results
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(log_entry, f, indent=2, ensure_ascii=False)
    
    # Also append to summary log
    summary_file = DATA_DIR / "analysis_summary.jsonl"
    summary_entry = {
        "timestamp": datetime.now().isoformat(),
        "repository": f"{owner}/{repo}",
        "total_issues": results.get("total_issues", 0),
        "duplicates_found": results.get("duplicates_found", 0)
    }
    
    with open(summary_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(summary_entry) + '\n')
    
    return filename

def get_analysis_history(limit: int = 10):
    """
    Get recent analysis history
    """
    summary_file = DATA_DIR / "analysis_summary.jsonl"
    
    if not summary_file.exists():
        return []
    
    with open(summary_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Get last N lines
    recent_lines = lines[-limit:]
    
    return [json.loads(line) for line in recent_lines]

def get_total_analyses():
    """
    Get total number of analyses performed
    """
    summary_file = DATA_DIR / "analysis_summary.jsonl"
    
    if not summary_file.exists():
        return 0
    
    with open(summary_file, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)
