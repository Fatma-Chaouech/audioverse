import os
import re
import time
import pinecone
from elevenlabs.api import Voices
from audioverse.utils import (
    get_file_if_path_exists,
    save_dict_to_json,
)
from audioverse.utils import (
    read_txt_file,
    read_pdf_file,
    read_epub_file,
    generate_embeddings,
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


def get_sound_effects_embeddings(folder_path):
    files = os.listdir(folder_path)
    dimension = None
    embedded_effects = []
    for file in files:
        file_name = os.path.splitext(file)[0]
        embedding = generate_embeddings(file_name)
        embedded_effects.append((file_name, embedding))
        if not dimension:
            dimension = len(embedding)
        time.sleep(20)
        print("Processed: " + file_name)
    return embedded_effects, dimension


def get_pinecone_index(index_name):
    if index_name in pinecone.list_indexes():
        return pinecone.Index(index_name)
    return None


def embeddings_to_pinecone(id_embeddings, index):
    index.upsert(id_embeddings)

def extract_sound_effects_from_text(text):
    pattern = r"\[([^]]+)\]"
    matches = re.findall(pattern, text)
    return matches
