import os
import time
import openai
import streamlit as st
from dotenv import load_dotenv
from elevenlabs import generate, clone, save
from audioverse.audio_manager.audio import construct_audiobook
from audioverse.book_utils import (
    chunk_and_remove_sfx,
    extract_sound_effects_from_text,
    get_random_excerpt,
)
from audioverse.database.pinecone import PineconeVectorDB
from audioverse.helpers import (
    change_cloning_state,
    delete_cloned_voice,
    get_file_content,
    get_sound_effects_embeddings,
    choose_voice,
)

from audioverse.layout import clone_section_layout, welcome_layout
from audioverse.openai_utils import query_model
from audioverse.pinecone_utils import find_most_similar_effect
from audioverse.prompts.sound_effects import SoundEffectsPrompt
from audioverse.utils import (
    clear_directory,
    copy_file_with_new_name,
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
        try:
            run(uploaded_file, voice_name, description, files)
        except Exception as e:
            print(e)
            st.error("Error: Please upload a valid file.")


def initialize_app():
    pinecone_api_key, pinecone_environment = initialize_api_keys()
    index = initialize_vector_db(pinecone_api_key, pinecone_environment)
    return index


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


def generate_audio(sfx_split, voice, sound_effects, index, temp_dir):
    progress_bar = st.progress(0, text="Audio 0/{}".format(len(sfx_split)))

    for idx2, subparagraph in enumerate(sfx_split):
        # send the audio to elevenlabs
        audio = generate(subparagraph, voice=voice)

        # store it
        save(audio=audio, filename=temp_dir + f"/voice{0}_{idx2}.mp3")

        if len(sound_effects) == 0:
            time.sleep(20)

        # get the corresponding sound effect, if there still is one
        if idx2 < len(sound_effects):
            similar_effect = find_most_similar_effect(sound_effects[idx2], index)

            if similar_effect:
                # store that sound effect
                copy_file_with_new_name(
                    "./sounds",
                    similar_effect + ".mp3",
                    temp_dir,
                    str(f"sfx{0}_{idx2}.mp3"),
                )
            else:
                copy_file_with_new_name(
                    "./sounds",
                    "silence.mp3",
                    temp_dir,
                    str(f"sfx{0}_{idx2}.mp3"),
                )
            if idx2 != len(sfx_split) - 1:
                # sleep to avoid rate limit
                time.sleep(20)

        progress_bar.progress(
            (idx2 + 1) / len(sfx_split),
            text="Audio {}/{}".format(idx2 + 1, len(sfx_split)),
        )


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
def run(uploaded_file, voice_name, description, files):
    with st.spinner("Processing..."):
        index = initialize_app()
        content = get_file_content(uploaded_file)
        filename = uploaded_file.name
        temp_dir, clone_dir = initialize_directories()

        # if cloning is not selected, let gpt choose
        if not files:
            excerpt_book = get_random_excerpt(content)
            voice = choose_voice(excerpt_book)
            print("GPT has chosen the voice of", voice)

        # if cloning is selected, get the voice clone
        else:
            filenames = dump_streamlit_files(files, clone_dir, voice_name)
            voice = clone(name=voice_name, description=description, files=filenames)

    # prepare the sound effects template
    template = SoundEffectsPrompt()
    with st.spinner("Generating audio... This might take a while."):
        # get the sound effects
        split_with_sfx = query_model(template(content))
        sound_effects = extract_sound_effects_from_text(split_with_sfx)

        st.toast("Extracted sound effects!", icon="🎉")

        # split the paragraph by the sound effect, and remove them
        sfx_split = chunk_and_remove_sfx(split_with_sfx)
        generate_audio(sfx_split, voice, sound_effects, index, temp_dir)

    with st.spinner("Constructing the audiobook..."):
        audiobook = construct_audiobook(temp_dir)

    st.toast("Audiobook generated!", icon="🎉")
    st.balloons()

    clear_directory(temp_dir)
    delete_cloned_voice(files, voice)
    download_audiobook(audiobook, filename)


if __name__ == "__main__":
    prepare_app()
