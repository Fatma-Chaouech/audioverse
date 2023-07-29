import streamlit as st
from audioverse.utils import (
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
