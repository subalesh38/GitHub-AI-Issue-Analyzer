def predict_priority(title: str, body: str, issue_type: str):
    """
    Predict issue priority: low / medium / high
    """

    text = (title + " " + body).lower()

    high_priority_keywords = [
        "crash", "error", "fail", "urgent", "broken",
        "exception", "bug", "security", "data loss"
    ]

    score = 0

    # Rule 1: Issue type
    if issue_type == "bug":
        score += 2
    elif issue_type == "feature request":
        score += 1

    # Rule 2: Keywords
    for word in high_priority_keywords:
        if word in text:
            score += 1

    # Rule 3: Description length
    if len(body) > 300:
        score += 1

    # Final decision
    if score >= 4:
        return "high"
    elif score >= 2:
        return "medium"
    else:
        return "low"
