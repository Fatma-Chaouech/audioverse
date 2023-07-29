import streamlit as st


def welcome_layout():
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>🎧 Welcome to AudioVerse! 📚</h1>
            <p style="font-size: 18px; color: #555555;">Breathe Life Into Your Books!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def clone_section_layout():
    st.subheader("Voice Cloning")
    name = st.text_input(
        "Name of the New Voice",
        "",
        disabled=st.session_state.clone_voice,
    )
    description = st.text_area(
        "Description (Optional)",
        "",
        disabled=st.session_state.clone_voice,
    )
    files = st.file_uploader(
        "Select audio files",
        type=["mp3", "wav"],
        accept_multiple_files=True,
        disabled=st.session_state.clone_voice,
    )
    return name, description, files
