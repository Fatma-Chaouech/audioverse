from elevenlabs import clone
import streamlit as st


def clone_voice():
    # Name input
    name = st.text_input("Name of the New Voice", "")

    # Description input (optional)
    description = st.text_area("Description (Optional)", "")

    # Audio files uploader
    st.write("Upload Audio Files for Cloning:")
    files = st.file_uploader("Select audio files", type=["mp3", "wav"], accept_multiple_files=True)

    # Optional labels (key-value pair)
    st.write("Optional Labels (Key-Value Pairs):")
    labels = {}
    key_input = st.text_input("Label Key", "")
    value_input = st.text_input("Label Value", "")
    if st.button("Add Label"):
        if key_input and value_input:
            labels[key_input] = value_input
            key_input = ""
            value_input = ""

    # Clone Button
    if st.button("Clone Voice"):
        if name and files:
            # Call the clone function here
            new_voice = clone(name=name, description=description, files=files, labels=labels)
            st.success("Voice Cloned Successfully!")
            st.write("New Voice Details:")
            st.write("Name:", new_voice.name)
            st.write("Description:", new_voice.description)
            st.write("Labels:", new_voice.labels)


if __name__ == "__main__":
    clone_voice()

