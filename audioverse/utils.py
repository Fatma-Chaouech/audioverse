"""
audioverse/utils.py

This module contains utility functions for the Audioverse project.

Functions:
    save_dict_to_json(dictionnary, path): Save a dictionary to a JSON file.
    get_file_if_path_exists(path): Return the content of a file if the file exists.
    create_directory_if_not_exists(directory): Create a directory if it does not exist.
    read_txt_file(streamlit_file): Read a text file and return its content.
    read_pdf_file(streamlit_file): Read a PDF file and return the text from each page.
    read_epub_file(path): Read an EPUB file and return its text content.
    copy_file_with_new_name(source_dir, source_filename, destination_dir, new_filename): Copy a file to a new location with a new name.
    clear_directory(directory): Delete all files in a directory.
    extract_sound_effects_from_text(text): Extract sound effects from a text.
    input_to_chunks(input_text): Split a text into chunks.
    chunk_and_remove_sfx(text): Split a text into chunks and remove sound effects.
"""

import json
import os
import io
from pypdf import PdfReader
import re
import shutil
from typing import List
from ebooklib import epub, ITEM_DOCUMENT


def save_txt_to_file(text, path):
    with open(path, "w") as f:
        f.write(text)


def save_dict_to_json(dictionnary, path):
    with open(path, "w") as f:
        json.dump(dictionnary, f, indent=4)


def get_file_if_path_exists(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None


def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def read_txt_file(streamlit_file):
    """
    This function reads a text file and returns its content.

    Args:
        streamlit_file (str): The text file to be read.

    Returns:
        str: The content of the text file.
    """
    return streamlit_file.getvalue().decode("utf-8")


def read_pdf_file(streamlit_file: object) -> list:
    """
    This function reads a PDF file, extracts the text from all pages, and divides the content into chunks of paragraphs.

    Args:
        streamlit_file (object): The PDF file to be read.

    Returns:
        List[str]: A list of strings where each string represents a chunk of paragraphs from the PDF.
    """

    with io.BytesIO(streamlit_file.getvalue()) as open_pdf_file:
        reader = PdfReader(open_pdf_file)
        paragraphs = "\n".join([page.extract_text() for page in reader.pages]).split(".\n")

    # put back the periods
    formatted_paragraphs = [para.replace('\n', ' ').strip() + "." for para in paragraphs if para.strip()]

    return "\n\n".join(formatted_paragraphs)


def read_epub_file(path):
    book = epub.read_epub(path)
    text = ""
    for item in book.get_items():
        if item.get_type() == ITEM_DOCUMENT:
            text += item.get_body_content().decode("utf-8")
    return text


def copy_file_with_new_name(source_dir, source_filename, destination_dir, new_filename):
    source_filename = source_filename.replace(" ", "_")
    source_path = os.path.join(source_dir, source_filename)
    destination_path = os.path.join(destination_dir, new_filename)
    shutil.copy(source_path, destination_path)


def clear_directory(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            os.remove(os.path.join(directory, filename))


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
            remaining_chunk = chunk_sfx[index_closing_bracket + 1 :]
            if remaining_chunk != "":
                chunks_without_sfx.append(remaining_chunk)
        else:
            chunks_without_sfx.append(chunk_sfx)

    return chunks_without_sfx
