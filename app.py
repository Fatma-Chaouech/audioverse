import os
import random
import time
from dotenv import load_dotenv
import streamlit as st
import openai
from elevenlabs import generate, play, clone, save
from audioverse.prompts import VoiceCategoryPrompt
from audioverse.prompts.sound_effects import SoundEffectsPrompt
from audioverse.layout import welcome_layout, clone_section_layout
from audioverse.vector_db.pinecone import PineconeVectorDB
from audioverse.audio.audio import contruct_audiobook
from audioverse.utils import (
    chunk_and_remove_sfx,
    clear_directory,
    copy_file_with_new_name,
    create_directory_if_not_exists,
    extract_sound_effects_from_text,
    input_to_chunks,
)
from audioverse.helpers import (
    get_file_content,
    get_voices_info,
    change_cloning_state,
    query_model,
    get_sound_effects_embeddings,
    find_most_similar_effect,
)


def initialize_app():
    pinecone_api_key, pinecone_environment = initialize_api_keys()
    index_name = "sound-effects-index"
    vector_db = PineconeVectorDB(pinecone_api_key, pinecone_environment)
    index = vector_db.get_pinecone_index(index_name)
    return index_name, vector_db, index


def initialize_api_keys():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
    return pinecone_api_key, pinecone_environment


def preprare_ui():
    st.session_state.clone_voice = False
    welcome_layout()
    uploaded_file = st.file_uploader("Upload your book", type=["txt", "pdf"])

    clone_voice = st.checkbox(
        "Clone Voice", key="clone_checkbox", on_change=change_cloning_state
    )
    if clone_voice:
        voice_name, description, files = clone_section_layout()
    else:
        voice_name, description, files = None, None, None

    if st.button(
        "Upload Book",
        type="primary",
        use_container_width=True,
        disabled=uploaded_file is None,
    ):
        content = get_file_content(uploaded_file)
        if content:
            run(
                uploaded_file.name,
                content,
                voice_name,
                description,
                files,
            )
        else:
            st.error("Please upload a valid txt or pdf file.")


def run(filename, content, voice_name, description, files):
    audio_filename = filename.replace(" ", "_").split(".")[0] + ".mp3"
    with st.spinner("Processing..."):
        index_name, vector_db, index = initialize_app()
        temp_dir = "./voices/generated"
        clone_dir = "./voices/clone"
        create_directory_if_not_exists(temp_dir)
        create_directory_if_not_exists(clone_dir)

        # generate sound effects embeddings
        if not vector_db.has_embeddings():
            embedded_effects, dimension = get_sound_effects_embeddings("./sounds")
            if not vector_db.has_index():
                index = vector_db.create_pinecone_index(index_name, dimension=dimension)
            vector_db.embeddings_to_pinecone(embedded_effects, index)

        # split the book into paragraphs
        split_book = input_to_chunks(content)

        # choose voice based on random excerpt, if cloning is not selected
        excerpt_book = split_book[random.randint(0, len(split_book) - 1)]
        if not files:
            voice_types = get_voices_info()
            template = VoiceCategoryPrompt()
            voice = query_model(template(voice_types, excerpt_book))
            print("GPT has chosen {} for the voice actor...".format(voice))

        # get the voice, if cloning is selected
        else:
            filenames = []
            for idx, file_ in enumerate(files):
                filenames.append(clone_dir + "/{}_{}".format(voice_name, idx))
                with open(filenames[idx], "wb") as f:
                    f.write(file_.getbuffer())
            voice = clone(name=voice_name, description=description, files=filenames)

        # prepare the sound effects template
        template = SoundEffectsPrompt()

        # for each paragraph
    with st.spinner("Generating audio... This may take a while."):
        # get the sound effects
        split_with_sfx = query_model(template(content))
        sound_effects = extract_sound_effects_from_text(split_with_sfx)
        print("Extracted sound effects: ", sound_effects)
        st.toast("Extracted sound effects!", icon="🎉")

        # split the paragraph by the sound effect, and remove them
        sfx_split = chunk_and_remove_sfx(split_with_sfx)

        progress_bar = st.progress(0, text="Audio 0/{}".format(len(sfx_split)))

        # for each subparagraph
        for idx2, subparagraph in enumerate(sfx_split):
            # send the audio to elevenlabs
            audio = generate(subparagraph, voice=voice)

            # store it
            save(audio=audio, filename=temp_dir + f"/voice{0}_{idx2}.mp3")

            # get the corresponding sound effect, if there still is one
            print(f"{idx2}")
            if len(sound_effects) == 0:
                time.sleep(20)

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

    with st.spinner("Constructing the audiobook..."):
        audiobook = contruct_audiobook(temp_dir)

    print("Audio generation...")
    st.toast("Audiobook generated!", icon="🎉")
    st.balloons()
    # play(audiobook)
    clear_directory(temp_dir)
    st.download_button(
        label="Save Audiobook",
        data=audiobook,
        file_name=audio_filename,
        mime="audio/mp3",
    )


if __name__ == "__main__":
    try:
        preprare_ui()
    except Exception as e:
        st.error(e)
        clear_directory("./voices/generated")
