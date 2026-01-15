from fastapi import FastAPI
from services.github_service import fetch_issues
from models.similarity_model import find_similar_issues
from models.issue_classifier import classify_issue
from models.priority_predictor import predict_priority
from utils.logger import log_analysis, get_analysis_history, get_total_analyses

app = FastAPI(
    title="GitHub AI Issue Analyzer",
    description="AI-powered analysis of GitHub issues",
    version="1.0"
)

@app.get("/")
def root():
    return {"message": "GitHub AI Issue Analyzer is running"}

@app.get("/analyze/{owner}/{repo}")
def analyze_issues(owner: str, repo: str):
    issues = fetch_issues(owner, repo)

    if len(issues) < 1:
        return {"message": "No issues found"}

    for issue in issues:
        classification = classify_issue(issue["title"], issue["body"])
        priority = predict_priority(
            issue["title"],
            issue["body"],
            classification["label"]
        )

        issue["classification"] = classification
        issue["priority"] = priority

    duplicates = find_similar_issues(issues)

    results = {
        "total_issues": len(issues),
        "duplicates_found": len(duplicates),
        "issues": issues,
        "duplicates": duplicates
    }
    
    # Log the analysis results
    log_analysis(owner, repo, results)
    
    return results

@app.get("/history")
def analysis_history(limit: int = 10):
    """
    Get recent analysis history
    """
    return {
        "history": get_analysis_history(limit),
        "total_analyses": get_total_analyses()
    }

@app.get("/stats")
def analysis_stats():
    """
    Get analysis statistics
    """
    return {
        "total_analyses": get_total_analyses(),
        "message": "Analysis logging is active"
    }
