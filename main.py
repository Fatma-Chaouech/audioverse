import os
from dotenv import load_dotenv
import streamlit as st
import openai
from elevenlabs.api import Voices
from elevenlabs import generate, play, save
from audioverse.prompts import VoiceCategoryPrompt
from audioverse.utils import (
    get_file_if_path_exists,
    save_dict_to_json,
)
from audioverse.helpers import get_file_content


def get_voices_info():
    voice_types = get_file_if_path_exists("voice_types.json")
    voice_ids = get_file_if_path_exists("voice_ids.json")
    if not voice_types or not voice_ids:
        voices = Voices.from_api()
        voice_types = [{"name": voice.name, "labels": voice.labels} for voice in voices]
        voice_ids = {voice.name: voice.voice_id for voice in voices}
        save_dict_to_json(voice_types, "voice_types.json")
        save_dict_to_json(voice_ids, "voice_ids.json")
    return voice_types, voice_ids


def query_model(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]},
        ],
    )
    return completion.choices[0].message["content"]


def preprare_ui():
    uploaded_file = st.file_uploader("Upload your book", type=["txt", "pdf", "epub"])

    if st.button("Send File"):
        return get_file_content(uploaded_file)


def run(content):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    voice_types, voice_ids = get_voices_info()
    template = VoiceCategoryPrompt()
    actor_name = query_model(template(voice_types, content))
    # actor_id = voice_ids[actor_name]
    print("GPT has chosen {} for the voice actor".format(actor_name))
    audio = generate(content, voice=actor_name)
    play(audio)
    save(audio, "./generated/book_test.mp3")


if __name__ == "__main__":
    content = preprare_ui()
    if content:
        run(content)
