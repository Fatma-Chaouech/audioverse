from audioverse.openai_utils import generate_embeddings


def find_most_similar_effect(description, index):
    description_embedding = generate_embeddings(description)
    results = index.query(vector=description_embedding, top_k=1)["matches"]
    try:
        if results[0]["score"] >= 0.8:
            return results[0]["id"]
        else:
            return None
    except:
        raise KeyError("No similar sound effect found. The results are: ", results)
