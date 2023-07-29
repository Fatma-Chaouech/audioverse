from elevenlabs.api import Voices
from audioverse.utils import (
    get_file_if_path_exists,
    save_dict_to_json,
)
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


def get_voices_info():
    voice_types = get_file_if_path_exists("voices/voice_types.json")
    if not voice_types:
        voices = Voices.from_api()
        voice_types = [{"name": voice.name, "labels": voice.labels} for voice in voices]
        save_dict_to_json(voice_types, "voice_types.json")
    return voice_types
