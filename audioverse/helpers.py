import os
import time
import openai
import streamlit as st
from elevenlabs.api import Voices
from audioverse.utils import (
    clear_directory,
    get_file_if_path_exists,
    remove_directory,
    save_dict_to_json,
    read_txt_file,
    read_pdf_file,
    read_epub_file,
    dump_file,
)


def get_file_content(streamlit_file):
    try:
        file_contents = None
        tmp_dir = "tmp"
        if streamlit_file is not None:
            file_type = streamlit_file.type
            if "text" in file_type:
                file_contents = read_txt_file(streamlit_file)
            elif "pdf" in file_type:
                tmp_path = os.path.join(tmp_dir, "book.pdf")
                dump_file(streamlit_file, tmp_path)
                file_contents = read_pdf_file(tmp_path)
            elif "epub" in file_type:
                tmp_path = os.path.join(tmp_dir, "book.epub")
                dump_file(streamlit_file, tmp_path)
                file_contents = read_epub_file(tmp_path)
        return file_contents
    except:
        return None
    finally:
        clear_directory(tmp_dir)
        remove_directory(tmp_dir)


def get_voices_info():
    voice_types = get_file_if_path_exists("voices/voice_types.json")
    if not voice_types:
        voices = Voices.from_api()
        voice_types = [{"name": voice.name, "labels": voice.labels} for voice in voices]
        save_dict_to_json(voice_types, "voice_types.json")
    return voice_types


def change_cloning_state():
    st.session_state.clone_voice = not st.session_state.clone_voice


def delete_voice(voice):
    voice.delete()


def get_sound_effects_embeddings(folder_path):
    files = os.listdir(folder_path)
    dimension = None
    embedded_effects = []
    for file in files:
        file_name = " ".join(os.path.splitext(file)[0].split("_"))
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
        if results[0]["score"] >= 0.8:
            return results[0]["id"]
        else:
            return None
    except:
        raise KeyError("No similar sound effect found. The results are: ", results)
