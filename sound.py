import os
import openai
import time
from dotenv import load_dotenv
from audioverse.prompts import SoundEffectsPrompt
from audioverse.vector_db.pinecone import PineconeVectorDB
from audioverse.helpers import (
    generate_embeddings,
    get_sound_effects_embeddings,
    query_model,
)
from audioverse.utils import (
    extract_sound_effects_from_text,
    input_to_chunks,
    chunk_and_remove_sfx,
)


def initialize_api_keys():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
    return pinecone_api_key, pinecone_environment


def find_most_similar_effect(description, index):
    description_embedding = generate_embeddings(description)
    results = index.query(vector=description_embedding, top_k=1)["matches"][0]
    return results["id"]
    


if __name__ == "__main__":
    pinecone_api_key, pinecone_environment = initialize_api_keys()
    index_name = "sound-effects-index"
    vector_db = PineconeVectorDB(pinecone_api_key, pinecone_environment)
    index = vector_db.get_pinecone_index(index_name)
    if not index:
        embedded_effects, dimension = get_sound_effects_embeddings("./sounds")
        index = vector_db.create_pinecone_index(index_name, dimension=dimension)
        vector_db.embeddings_to_pinecone(embedded_effects, index)

    print("Preparing prompt...")
    book = """It was a rainy day. Alice was laying on her bed, when suddenly she heard craking noise. She looked out of the window and saw a tree falling down. She was scared and ran to her mother. Her mother told her that it was just a thunderstorm.\n\n
    Alice did not believe it was a thunderstorm, she thought it was a monster. She went to her room and closed the door. She was scared and did not know what to do. She heard a loud noise and saw a monster coming out of the tree. She screamed and ran to her mother. Her mother told her that it was just a thunderstorm.\n\n
    """
    split_book = input_to_chunks(book)
    template = SoundEffectsPrompt()
    for split in split_book:
        split_with_sfx = query_model(template(split))
        print("Refactored book: ", split_with_sfx)
        sound_effects = extract_sound_effects_from_text(split_with_sfx)
        refactored_split = chunk_and_remove_sfx(split_with_sfx)
        print("Extracted sound effects: ", sound_effects)
        for sound_effect in sound_effects:
            similar_effect = find_most_similar_effect(sound_effect, index)
            print(
                f"The most similar sound effect to '{sound_effect}' is: {similar_effect}"
            )
            time.sleep(15)
