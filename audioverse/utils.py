import json
import os
import re
from tika import parser
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


def extract_sound_effects_from_text(text):
    pattern = r"\[([^]]+)\]"
    matches = re.findall(pattern, text)
    return matches


def input_to_chunks(input_text):
    return [x.strip() for x in input_text.split("\n\n") if x.strip() != ""]


def chunk_and_remove_sfx(text):
    chunks_with_sfx = text.split("[")
    chunks_without_sfx = []

    for chunk_sfx in chunks_with_sfx:
        index_closing_bracket = chunk_sfx.find("]")

        if index_closing_bracket != -1:
            chunks_without_sfx.append(chunk_sfx[index_closing_bracket + 1 :])
        else:
            chunks_without_sfx.append(chunk_sfx)

    return chunks_without_sfx
