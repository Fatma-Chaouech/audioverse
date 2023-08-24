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
from ebooklib import epub, ITEM_DOCUMENT
from langchain.document_loaders import UnstructuredEPubLoader, UnstructuredPDFLoader


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


def read_txt_file(streamlit_file: object) -> str:
    """
    This function reads a text file and returns its content.

    Args:
        streamlit_file (str): The text file to be read.

    Returns:
        str: The content of the text file.
    """
    return streamlit_file.getvalue().decode("utf-8")


def read_pdf_file(path: str) -> str:
    """
    This function reads a PDF file, extracts the text from all pages, and divides the content into chunks of paragraphs.

    Args:
        streamlit_file (object): The PDF file to be read.

    Returns:
        str: A string where each chunk represents a paragraph from the PDF.
    """
    paragraphs = [
        doc.page_content
        for doc in UnstructuredPDFLoader(path, mode="elements").load()
        if doc.page_content.endswith(".")
    ]
    return "\n\n".join(
        [" ".join(paragraphs[i : i + 100]) for i in range(0, len(paragraphs), 100)]
    )


def dump_file(streamlit_file: object, path: str):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, "wb") as f:
        f.write(streamlit_file.getvalue())


def read_epub_file(path: str):
    paragraphs = [
        doc.page_content
        for doc in UnstructuredEPubLoader(path, mode="elements").load()
        if doc.page_content.endswith(".")
    ]
    return "\n\n".join(
        [" ".join(paragraphs[i : i + 100]) for i in range(0, len(paragraphs), 100)]
    )


def copy_file_with_new_name(source_dir, source_filename, destination_dir, new_filename):
    source_filename = source_filename.replace(" ", "_")
    source_path = os.path.join(source_dir, source_filename)
    destination_path = os.path.join(destination_dir, new_filename)
    shutil.copy(source_path, destination_path)


def clear_directory(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            os.remove(os.path.join(directory, filename))


def remove_directory(directory):
    if os.path.exists(directory):
        os.rmdir(directory)


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
