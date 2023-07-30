import pinecone
import os
import openai
import time
from dotenv import load_dotenv

# time.sleep(21) needed

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone.init(api_key=pinecone_api_key, environment="us-west1-gcp-free")


def generate_embeddings(name):
    response = openai.Embedding.create(model="text-embedding-ada-002", input=name)
    try:
        embedding = response["data"][0]["embedding"]
    except KeyError:
        print("Error: " + str(response["error"]))
        embedding = None
    return embedding


def store_sound_effects(folder_path):
    files = os.listdir(folder_path)
    effect_embeddings = []
    effect_names = []
    for file in files:
        file_name = os.path.splitext(file)[0]
        embedding = generate_embeddings(file_name)
        if embedding:
            effect_names.append(file_name)
            effect_embeddings.append(embedding)
    index_name = "sound-effects-index"
    pinecone.create_index(index_name, dimension=len(effect_embeddings[0]))
    index = pinecone.Index(index_name)
    index.upsert(effect_names, effect_embeddings)
    return index_name


def choose_effect_prompt():
    prompt = "Choose a sound effect:Rain "
    return prompt


def find_most_similar_effect(description, index_name):
    description_embedding = generate_embeddings(description)
    if description_embedding:
        results = pinecone.query(index_name, description_embedding, top_k=1)
        most_similar_effect = results[0].id
        return most_similar_effect
    else:
        return None


if __name__ == "__main__":
    folder_path = "./sounds"
    indexname = store_sound_effects(folder_path)
    prompt = choose_effect_prompt()
    while True:
        description = input(prompt)
        if description.lower() == "exit":
            break
        similar_effect = find_most_similar_effect(description, indexname)
        if similar_effect:
            print(
                f"The most similar sound effect to '{description}' is: {similar_effect}"
            )
        else:
            print("No similar sound effect found for the given description.")
