import concurrent.futures
import os
import openai
import streamlit as st
from dotenv import load_dotenv
from elevenlabs import generate, clone
from elevenlabs import save
from audioverse.lock_manager import gpt_lock_manager
from audioverse.audio_manager.audio import construct_audiobook
from audioverse.book_utils import get_random_excerpt, update_chunk_sfx
from audioverse.database.pinecone import PineconeVectorDB
from audioverse.helpers import (
    change_cloning_state,
    delete_cloned_voice,
    get_file_content,
    get_sound_effects_embeddings,
    choose_voice,
    store_sound_effects,
)

from audioverse.layout import clone_section_layout, welcome_layout
from audioverse.openai_utils import stream_query_model
from audioverse.prompts.sound_effects import SoundEffectsPrompt
from audioverse.utils import (
    clear_directory,
    create_directory_if_not_exists,
    dump_streamlit_files,
)
from audioverse.decorators import start_end_decorator, timing_decorator


def prepare_app():
    welcome_layout()
    st.session_state.clone_voice = False
    uploaded_file = st.file_uploader("Upload your book", type=["txt", "pdf", "epub"])

    clone_voice = st.checkbox("Clone Voice", on_change=change_cloning_state)
    voice_name, description, files = (
        clone_section_layout() if clone_voice else (None, None, None)
    )
    if uploaded_file and st.button(
        "Upload Book", type="primary", use_container_width=True
    ):
        run(uploaded_file, voice_name, description, files)


def initialize_api_keys():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
    return pinecone_api_key, pinecone_environment


def initialize_directories():
    temp_dir = "./voices/generated"
    clone_dir = "./voices/clone"
    create_directory_if_not_exists(temp_dir)
    create_directory_if_not_exists(clone_dir)
    return temp_dir, clone_dir


@start_end_decorator
@timing_decorator
def initialize_vector_db(pinecone_api_key, pinecone_environment):
    index_name = "sound-effects-index"
    vector_db = PineconeVectorDB(pinecone_api_key, pinecone_environment)
    if not vector_db.has_index(index_name):
        embedded_effects, dimension = get_sound_effects_embeddings("./sounds")
        index = vector_db.create_pinecone_index(index_name, dimension)
        vector_db.embeddings_to_pinecone(embedded_effects)
    elif not vector_db.has_embeddings(index_name):
        index = vector_db.get_pinecone_index()
        embedded_effects, dimension = get_sound_effects_embeddings("./sounds")
        vector_db.embeddings_to_pinecone(embedded_effects)
    else:
        index = vector_db.get_pinecone_index()
    return index


def download_audiobook(audiobook, filename):
    audio_filename = filename.replace(" ", "_").split(".")[0] + ".mp3"
    st.download_button(
        label="Save Audiobook",
        data=audiobook,
        file_name=audio_filename,
        mime="audio/mp3",
    )


@start_end_decorator
@timing_decorator
def get_text_sfx(prompt, index):
    sound_effects, chunk, sfx = [], "", ""
    try:
        with gpt_lock_manager:
            stream = stream_query_model(prompt)
    except Exception as e:
        print("Exception in get_text_sfx", e)
        gpt_lock_manager.force_release()

    for word in stream:
        chunk, sfx, sound_effects = update_chunk_sfx(
            word, chunk, sfx, sound_effects, index
        )
    return chunk, sound_effects


@start_end_decorator
@timing_decorator
def get_voice(files, clone_dir, voice_name, description, content):
    # if cloning is not selected, let gpt choose
    if not files:
        excerpt_book = get_random_excerpt(content)
        voice = choose_voice(excerpt_book)
        print("GPT has chosen the voice of", voice)

    # if cloning is selected, get the voice clone
    else:
        filenames = dump_streamlit_files(files, clone_dir, voice_name)
        voice = clone(name=voice_name, description=description, files=filenames)
    return voice


@start_end_decorator
@timing_decorator
def generate_audio(chunk, voice, temp_dir):
    audio = generate(chunk, voice=voice)
    save(audio=audio, filename=temp_dir + f"/voice.mp3")


@timing_decorator
def run(uploaded_file, voice_name, description, files):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        pinecone_api_key, pinecone_environment = initialize_api_keys()
        future_index = executor.submit(
            initialize_vector_db, pinecone_api_key, pinecone_environment
        )
        content = get_file_content(uploaded_file)
        filename = uploaded_file.name
        temp_dir, clone_dir = initialize_directories()
        template = SoundEffectsPrompt()
        sound_effects, chunk = [], ""

        with st.spinner("Generating audio... This might take a while."):
            future_voice = executor.submit(
                get_voice, files, clone_dir, voice_name, description, content
            )

            # wait to get the index
            index = future_index.result()

            future_text_sfx = executor.submit(
                get_text_sfx, template(text=content), index
            )

            # wait for both tasks to complete
            voice = future_voice.result()
            chunk, sound_effects = future_text_sfx.result()

            future_storing = executor.submit(
                store_sound_effects, sound_effects, temp_dir
            )
            future_generating = executor.submit(generate_audio, chunk, voice, temp_dir)

            # wait for both tasks to complete
            future_storing.result()
            future_generating.result()

    with st.spinner("Constructing the audiobook..."):
        audiobook = construct_audiobook(temp_dir)

    st.toast("Audiobook generated!", icon="🎉")
    st.balloons()

    clear_directory(temp_dir)
    delete_cloned_voice(files, voice)
    download_audiobook(audiobook, filename)


if __name__ == "__main__":
    prepare_app()
