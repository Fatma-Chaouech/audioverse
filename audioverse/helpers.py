import os
import pinecone
import time
import openai
import streamlit as st
from elevenlabs.api import Voices
from audioverse.utils import (
    get_file_if_path_exists,
    save_dict_to_json,
    read_txt_file,
    read_pdf_file,
    read_epub_file,
)


def get_file_content(file):
    file_contents = None
    if file is not None:
        file_type = file.type
        if "text" in file_type:
            file_contents = read_txt_file(file)
        elif "pdf" in file_type:
            file_contents = read_pdf_file(file)
        elif "epub" in file_type:
            file_contents = read_epub_file(file)
    return file_contents


def get_voices_info():
    voice_types = get_file_if_path_exists("voices/voice_types.json")
    if not voice_types:
        voices = Voices.from_api()
        voice_types = [{"name": voice.name, "labels": voice.labels} for voice in voices]
        save_dict_to_json(voice_types, "voice_types.json")
    return voice_types


def change_cloning_state():
    st.session_state.clone_voice = not st.session_state.clone_voice


def get_sound_effects_embeddings(folder_path):
    files = os.listdir(folder_path)
    dimension = None
    embedded_effects = []
    for file in files:
        file_name = ' '.join(os.path.splitext(file)[0].split('_'))
        embedding = generate_embeddings(file_name)
        embedded_effects.append((file_name, embedding))
        if not dimension:
            dimension = len(embedding)
        time.sleep(20)
        print("Processed: " + file_name)
    return embedded_effects, dimension


def query_model(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]},
        ],
        temperature=0.2,
    )
    return completion.choices[0].message["content"]


def generate_embeddings(input):
    response = openai.Embedding.create(model="text-embedding-ada-002", input=input)
    try:
        embedding = response["data"][0]["embedding"]
        return embedding
    except KeyError:
        print("Error: " + str(response["error"]))


def find_most_similar_effect(description, index):
    description_embedding = generate_embeddings(description)
    results = index.query(vector=description_embedding, top_k=1)["matches"]
    try:
        return results[0]["id"]
    except:
        raise KeyError("No similar sound effect found. The results are: ", results)
