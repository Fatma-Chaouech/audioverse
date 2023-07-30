import os
from dotenv import load_dotenv
import streamlit as st
import openai
from elevenlabs import generate, play, clone
from audioverse.prompts import VoiceCategoryPrompt
from audioverse.helpers import get_file_content, get_voices_info, change_cloning_state, query_model
from audioverse.layout import welcome_layout, clone_section_layout


def preprare_ui():
    st.session_state.clone_voice = False
    welcome_layout()
    uploaded_file = st.file_uploader(
        "Upload your book", type=["txt", "pdf", "epub"], key="file_uploader"
    )

    clone_voice = st.checkbox(
        "Clone Voice", key="clone_checkbox", on_change=change_cloning_state
    )
    if clone_voice:
        name, description, files = clone_section_layout()

    if st.button("Upload Book", type="primary", use_container_width=True):
        run(
            uploaded_file.name,
            get_file_content(uploaded_file),
            name,
            description,
            files,
        )


def run(filename, content, name, description, files):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not files:
        voice_types = get_voices_info()
        template = VoiceCategoryPrompt()
        voice = query_model(template(voice_types, content))
        print("GPT has chosen {} for the voice actor...".format(voice))
    else:
        filenames = []
        for idx, file_ in enumerate(files):
            filenames.append("voices/{}_{}".format(name, idx))
            with open(filenames[idx], "wb") as f:
                f.write(file_.getbuffer())
        voice = clone(name=name, description=description, files=filenames)
    audio = generate(content, voice=voice)
    print("Audio generation...")
    play(audio)
    st.download_button(
        label="Save Audiobook", data=audio, file_name=filename, mime="audio/mp3"
    )


if __name__ == "__main__":
    preprare_ui()
