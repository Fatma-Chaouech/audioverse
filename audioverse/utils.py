import json
import os
from typing import List
import shutil
from langchain.document_loaders import UnstructuredEPubLoader, UnstructuredPDFLoader


def save_txt_to_file(text, path):
    with open(path, "w") as f:
        f.write(text)


def dump_streamlit_file(streamlit_file: object, path: str):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, "wb") as f:
        f.write(streamlit_file.getvalue())


def dump_streamlit_files(files: List[object], directory: str, name: str):
    filenames = []
    for idx, file_ in enumerate(files):
        filenames.append(directory + "/{}_{}".format(name, idx))
        with open(filenames[idx], "wb") as f:
            f.write(file_.getbuffer())
    return filenames


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


def read_pdf_file(path: str) -> List[str]:
    """
    This function reads a PDF file, extracts the text from all pages, and divides the content into chunks of paragraphs.

    Args:
        path (str): The path to the PDF file to be read.

    Returns:
        List[str]: A list of strings where each string represents a sentence from the PDF.
    """
    return [
        doc.page_content
        for doc in UnstructuredPDFLoader(path, mode="elements").load()
        if doc.page_content.endswith(".")
    ]


def read_epub_file(path: str) -> List[str]:
    """
    This function reads an EPUB file, extracts the text from all pages, and divides the content into chunks of paragraphs.

    Args:
        path (str): The path to the EPUB file to be read.

    Returns:
        List[str]: A list of strings where each string represents a sentence from the EPUB.
    """
    return [
        doc.page_content
        for doc in UnstructuredEPubLoader(path, mode="elements").load()
        if doc.page_content.endswith(".")
    ]


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
