# AudioVerse
![cover](./docs/cover.jpeg)
Are you tired of reading books the traditional way? 😩 Experience a whole new world of literary immersion with [AudioVerse](https://audioverse.streamlit.app/)! 🎧📚 AudioVerse allows you to effortlessly transform any written material into captivating audiobooks, complete with customizable language, cloned voices, and exciting sound effects. 🌟🎙️💥

Join the auditory adventure now! 🚀🎶 AudioVerse: Breathe Life Into Your Books! 📚💨

## Features
* Convert books to audiobooks with a single click
* Automatic voice selection for the perfect narration
* Personalized voice cloning for a unique listening experience
* Automatic integration of sound effects for immersive storytelling

## Technologies
* ElevenLabs
* OpenAI
* Streamlit
* Pinecone

## Demo
![demo](https://github.com/Fatma-Chaouech/audioverse/assets/69005550/3d25a540-393d-4a3e-b799-a8d9826c74b9)

## Usage
1. Clone the repository
    ```
    git clone https://github.com/Fatma-Chaouech/audioverse.git
    ```
2. Create a virtual environment
   ```
   cd audioverse
   python -m venv myenv
   ```
3. Activate the virtual environment
    ```
    # on Windows  
    myenv\Scripts\activate

    # on macOS and Linux
    source myenv/bin/activate
    ```
5. Install the dependencies
    ```
    pip install -r requirements.txt
    ```
6. Install [ffmpeg](https://www.videoproc.com/resource/how-to-install-ffmpeg.htm) if you don't already have it
   ```
   # On Linux
   sudo apt update
   sudo apt install ffmpeg
   ```
7. Create a .env file (see the [.env.template](./.env.template))
