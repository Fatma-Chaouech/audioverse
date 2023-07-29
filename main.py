import os
from dotenv import load_dotenv
import streamlit as st
import openai
from elevenlabs.api import Voices
from elevenlabs import generate, play
from audioverse.prompts import VoiceCategoryPrompt
from audioverse.utils import (
    get_file_if_path_exists,
    save_dict_to_json,
)
from audioverse.helpers import get_file_content


def get_voices_info():
    voice_types = get_file_if_path_exists("voice_types.json")
    if not voice_types:
        voices = Voices.from_api()
        voice_types = [{"name": voice.name, "labels": voice.labels} for voice in voices]
        save_dict_to_json(voice_types, "voice_types.json")
    return voice_types


def query_model(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]},
        ],
        temperature=0.2,
    )
    return completion.choices[0].message["content"]


def preprare_ui():
    uploaded_file = st.file_uploader(
        "Upload your book", type=["txt", "pdf", "epub"], key="file_uploader"
    )

    if st.button("Upload Book"):
        return uploaded_file.name, get_file_content(uploaded_file)

    return None, None


def run(filename, content):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    voice_types = get_voices_info()
    template = VoiceCategoryPrompt()
    actor_name = query_model(template(voice_types, content))
    print("GPT has chosen {} for the voice actor...".format(actor_name))
    audio = generate(content, voice=actor_name)
    print("Audio generated...")
    play(audio)
    st.download_button(
        label="Save Audiobook", data=audio, file_name=filename, mime="audio/mp3"
    )


if __name__ == "__main__":
    name, content = preprare_ui()
    if content:
        print("File uploaded...")
        run(name, content)
