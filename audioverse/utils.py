import json
import os
import openai
from tika import parser
import streamlit as st
from ebooklib import epub, ITEM_DOCUMENT


def save_dict_to_json(dictionnary, path):
    with open(path, "w") as f:
        json.dump(dictionnary, f, indent=4)


def get_file_if_path_exists(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None


def read_txt_file(file):
    return file.getvalue().decode("utf-8")


def read_pdf_file(file):
    raw_text = parser.from_buffer(file.read())
    return raw_text["content"]


def read_epub_file(file):
    book = epub.read_epub(file)
    text = ""
    for item in book.get_items():
        if item.get_type() == ITEM_DOCUMENT:
            text += item.get_body_content().decode("utf-8")
    return text


def change_cloning_state():
    st.session_state.clone_voice = not st.session_state.clone_voice


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
