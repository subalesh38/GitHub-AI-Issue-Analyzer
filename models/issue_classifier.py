from transformers import pipeline

# Zero-shot classification pipeline
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

LABELS = ["bug", "feature request", "documentation", "question", "other"]

def classify_issue(title: str, body: str):
    """
    Classify a GitHub issue into predefined categories
    """
    text = title + " " + body

    result = classifier(text, LABELS)

    return {
        "label": result["labels"][0],
        "confidence": round(float(result["scores"][0]), 2)
    }
