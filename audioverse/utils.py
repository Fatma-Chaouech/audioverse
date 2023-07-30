import json
import os
import re
import shutil
from moviepy.editor import concatenate_audioclips, AudioFileClip
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


def copy_file_with_new_name(source_dir, source_filename, destination_dir, new_filename):
    source_path = os.path.join(source_dir, source_filename)
    destination_path = os.path.join(destination_dir, new_filename)
    shutil.copy(source_path, destination_path)


def clear_directory(directory):
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
            chunks_without_sfx.append(chunk_sfx[index_closing_bracket + 1 :])
        else:
            chunks_without_sfx.append(chunk_sfx)

    return chunks_without_sfx


def contruct_audiobook(input_dir):
    voice_files = sorted(
        [
            os.path.join(input_dir, f)
            for f in os.listdir(input_dir)
            if f.startswith("voice")
        ]
    )
    voice_files = [AudioFileClip(x) for x in voice_files]
    sfx_files = sorted(
        [
            os.path.join(input_dir, f)
            for f in os.listdir(input_dir)
            if f.startswith("sfx")
        ]
    )
    sfx_files = [AudioFileClip(x) for x in sfx_files]
    clips = []
    for i in range(len(voice_files)):
        if i >= len(sfx_files):
            clips.append(voice_files[i])
        else:
            clips.extend([voice_files[i], sfx_files[i]])
    audiobook = concatenate_audioclips(clips)

    temp = os.path.join(input_dir, "final.mp3")
    audiobook.write_audiofile(temp, codec="mp3")
    with open(temp, "rb") as file:
        audio_bytes = file.read()
    return audio_bytes
