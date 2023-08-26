from audioverse.openai_utils import generate_embeddings
from audioverse.lock_manager import embedding_lock_manager


def find_most_similar_effect(description, index):
    try:
        with embedding_lock_manager:
            description_embedding = generate_embeddings(description)
    except Exception as e:
        print('EXception in find_most_similar_effect', e)
        embedding_lock_manager.force_release()
    results = index.query(vector=description_embedding, top_k=1)["matches"]
    try:
        if results[0]["score"] >= 0.8:
            return results[0]["id"]
        else:
            return None
    except:
        raise KeyError("No similar sound effect found. The results are: ", results)
