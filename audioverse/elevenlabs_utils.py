from audioverse.prompts import voice_category
from audioverse.utils import get_file_if_path_exists, save_dict_to_json


def get_voices_info():
    voice_types = get_file_if_path_exists("voices/voice_types.json")
    if not voice_types:
        voices = voice_category.from_api()
        voice_types = [{"name": voice.name, "labels": voice.labels} for voice in voices]
        save_dict_to_json(voice_types, "voice_types.json")
    return voice_types


def delete_voice(voice):
    voice.delete()


def get_available_languages():
    return [
        "English",
        "Portuguese (Brazilian)",
        "Portuguese (other)",
        "Japanese",
        "Chinese",
        "German",
        "French",
        "Korean",
        "Italian",
        "Indonesian",
        "Dutch",
        "Turkish",
        "Polish",
        "Swedish",
        "Bulgarian",
        "Romanian",
        "Arabic",
        "Czech",
        "Greek",
        "Finnish",
        "Croatian",
        "Malay",
        "Slovak",
        "Danish",
        "Tamil",
        "Ukrainian",
    ]
