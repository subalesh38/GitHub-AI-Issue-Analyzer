from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def find_similar_issues(issues, threshold=0.75, max_results=10):
    texts = [
        issue["title"] + " " + issue["body"]
        for issue in issues
    ]

    embeddings = model.encode(texts)
    similarity_matrix = cosine_similarity(embeddings)

    duplicates = []

    for i in range(len(issues)):
        for j in range(i + 1, len(issues)):
            score = similarity_matrix[i][j]
            if score > threshold:
                duplicates.append({
                    "issue_1": issues[i]["title"],
                    "issue_2": issues[j]["title"],
                    "similarity": round(float(score), 2)
                })

    # Sort by similarity score
    duplicates.sort(key=lambda x: x["similarity"], reverse=True)

    return duplicates[:max_results]
