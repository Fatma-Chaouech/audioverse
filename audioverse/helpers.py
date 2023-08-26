import os
import streamlit as st
from audioverse.lock_manager import embedding_lock_manager, gpt_lock_manager
from audioverse.book_utils import chunked_text_from_paragraphs
from audioverse.elevenlabs_utils import delete_voice, get_voices_info
from audioverse.openai_utils import generate_embeddings, query_model
from audioverse.prompts.voice_category import VoiceCategoryPrompt
from audioverse.utils import (
    clear_directory,
    copy_file_with_new_name,
    remove_directory,
    read_txt_file,
    read_pdf_file,
    read_epub_file,
    dump_streamlit_file,
)
from decorators import start_end_decorator, timing_decorator


def get_file_content(streamlit_file):
    try:
        file_contents = None
        tmp_dir = "tmp"
        if streamlit_file is not None:
            file_type = streamlit_file.type
            if "text" in file_type:
                file_contents = read_txt_file(streamlit_file)
            elif "pdf" in file_type:
                tmp_path = os.path.join(tmp_dir, "book.pdf")
                dump_streamlit_file(streamlit_file, tmp_path)
                pragraphs = read_pdf_file(tmp_path)
                file_contents = chunked_text_from_paragraphs(pragraphs)
            elif "epub" in file_type:
                tmp_path = os.path.join(tmp_dir, "book.epub")
                dump_streamlit_file(streamlit_file, tmp_path)
                pragraphs = read_epub_file(tmp_path)
                file_contents = chunked_text_from_paragraphs(pragraphs)
        return file_contents
    except:
        return None
    finally:
        clear_directory(tmp_dir)
        remove_directory(tmp_dir)


def change_cloning_state():
    st.session_state.clone_voice = not st.session_state.clone_voice


def get_sound_effects_embeddings(folder_path):
    files = os.listdir(folder_path)
    dimension = None
    embedded_effects = []
    for file_ in files:
        file_name = " ".join(os.path.splitext(file_)[0].split("_"))
        try:
            with embedding_lock_manager:
                embedding = generate_embeddings(file_name)
        except Exception as e:
            print('Exception in get_sound_effects_embeddings', e)
            embedding_lock_manager.force_release()
        embedded_effects.append((file_name, embedding))
        if not dimension:
            dimension = len(embedding)

    return embedded_effects, dimension


@start_end_decorator
@timing_decorator
def store_sound_effects(sound_effects, directory):
    for idx, sfx in enumerate(sound_effects):
        if sfx:
            copy_file_with_new_name(
                "./sounds",
                sfx + ".mp3",
                directory,
                str(f"sfx{0}_{idx}.mp3"),
            )
        else:
            copy_file_with_new_name(
                "./sounds",
                "silence.mp3",
                directory,
                str(f"sfx{0}_{idx}.mp3"),
            )


def delete_cloned_voice(files, voice):
    if files:
        delete_voice(voice)


def choose_voice(excerpt_book):
    voice_types = get_voices_info()
    template = VoiceCategoryPrompt()
    try:
        with gpt_lock_manager:
            voice = query_model(template(voices=voice_types, text=excerpt_book))
    except Exception as e:
        print('Exception in choose voice', e)
        gpt_lock_manager.force_release()
    return voice
