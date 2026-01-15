import requests

GITHUB_API_BASE = "https://api.github.com"

def fetch_issues(owner: str, repo: str, state: str = "open"):
    """
    Fetch issues from a GitHub repository
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues"
    params = {
        "state": state,
        "per_page": 30
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception("Failed to fetch issues")

    issues = response.json()

    # Remove pull requests (GitHub treats PRs as issues)
    clean_issues = [
        {
            "id": issue["id"],
            "title": issue["title"],
            "body": issue["body"] or "",
            "url": issue["html_url"]
        }
        for issue in issues if "pull_request" not in issue
    ]

    return clean_issues
