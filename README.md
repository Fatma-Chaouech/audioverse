# AudioVerse - Breathe Life Into Your Books! 📚🌱

[![Contributors](https://img.shields.io/github/contributors/Fatma-Chaouech/audioverse)](https://github.com/Fatma-Chaouech/audioverse/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/Fatma-Chaouech/audioverse)](https://github.com/Fatma-Chaouech/audioverse/network/members)
[![Stars](https://img.shields.io/github/stars/Fatma-Chaouech/audioverse)](https://github.com/Fatma-Chaouech/audioverse/stargazers)
[![License](https://img.shields.io/github/license/Fatma-Chaouech/audioverse)](https://github.com/Fatma-Chaouech/audioverse/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/Fatma-Chaouech/audioverse)](https://github.com/Fatma-Chaouech/audioverse/issues)

![cover](./docs/cover.png)

Are you tired of reading books the traditional way? 😩 Experience a whole new world of literary immersion with [AudioVerse](https://audioverse.streamlit.app/)! 🎧📚 AudioVerse allows you to effortlessly transform any written material into captivating audiobooks, complete with customizable language, cloned voices, and exciting sound effects. 🌟🎙️💥

## Table of Contents
- [AudioVerse - Breathe Life Into Your Books! 📚🌱](#audioverse---breathe-life-into-your-books-)
  - [Table of Contents](#table-of-contents)
  - [🌟 Why AudioVerse?](#-why-audioverse)
  - [👀 Sneak Peek - Demo](#-sneak-peek---demo)
  - [🛠️ Technologies That Power Us](#️-technologies-that-power-us)
  - [🏭 Architecture Snapshot](#-architecture-snapshot)
  - [💻 Installation](#-installation)
  - [👩‍💻 Usage](#-usage)
  - [👋 Meet Our Team](#-meet-our-team)
    - [Fatma "PinkPanther" Chaouech](#fatma-pinkpanther-chaouech)
    - [Mohamed Nour "RedLion" Bessadok](#mohamed-nour-redlion-bessadok)
  - [🚀 Features and Challenges](#-features-and-challenges)
    - [🎟️ Features in the Pipeline](#️-features-in-the-pipeline)
    - [🔍 Challenges to Tackle](#-challenges-to-tackle)
  - [🙌 How You Can Contribute](#-how-you-can-contribute)

## 🌟 Why AudioVerse?

Get ready to transform your reading experience! With AudioVerse, you're not just reading – you're immersing yourself in a symphony of words, emotions, and soundscapes. Here's what makes us unique:

- **Effortless Conversion:** No more boring texts! Convert your favorite books into mesmerizing audiobooks with just a click.

- **Voice of Your Choice:** Pick the narrator that resonates with your soul. Our automatic voice selection makes every story come alive.

- **Your Personal Touch:** Want your audiobook to sound like you? Engage our personalized voice cloning for a one-of-a-kind listening adventure.

- **Sound Effects Magic:** Get ready for an immersive journey! We automatically integrate sound effects to elevate your storytelling experience.

## 👀 Sneak Peek - Demo
Here are some generated examples:

| Text          | Voice Name          | Cloning Voice Sample           | Generated Audio 🔊 |
| :------------ | :-----------------: | :-----------------------------: | :----------------: |
| With an unsettling urgency, the figure checked their phone, the device casting a dim glow on their features. A call interrupted the solitude... | Andrew Huberman | ![Voice](./docs/hubermanlab.mp3) | ![Generated](docs/andrew.mp3) |
| Brunson, a hefty fellow, was far from bashful when it came to throwing his weight around. One fateful day, ... | Dynamically Selected Voice | ❌ | ![Generated](docs/brunson.mp3) |

Curious to see how the magic works? Check out our demo [here](https://github.com/Fatma-Chaouech/audioverse/assets/69005550/3d25a540-393d-4a3e-b799-a8d9826c74b9), or try it yourself on our [Demo Website](https://audioverse.streamlit.app/).



## 🛠️ Technologies That Power Us
- **ElevenLabs**
- **OpenAI** 
- **Streamlit** 
- **Pinecone** 

## 🏭 Architecture Snapshot
![architecture](docs/architecture.png)

## 💻 Installation
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

## 👩‍💻 Usage
1. Run streamlit server
    ```
    streamlit run app.py
    ```
2. Open your web browser and navigate to [http://localhost:8501](http://localhost:8501)
3. Follow the Guiding Form
4. Give our magic a moment to weave its spell
5. Download your audiobook

## 👋 Meet Our Team

🎉 We're the dynamic duo behind the scenes, shaping AudioVerse with passion, innovation, and a sprinkle of quirkiness! 🎙️🛠️

### Fatma "PinkPanther" Chaouech
🧠 **Role:** Builder Extraordinaire

If you ever spot a trail of code leading to awesomeness, it's likely Fatma's work. As a software engineering student with a builder's mentality, she thrives on turning ideas into vibrant projects. With an unwavering belief in open source magic, she's constantly weaving creativity and code. Interested in the AI-neuroscience blend, she's bridging the gap between machines and minds.

🌐 **Connect:** [Github](https://github.com/Fatma-Chaouech) | [LinkedIn](https://www.linkedin.com/in/fatma-chaouech/) | [Twitter](https://twitter.com/FatmaChaouech_) (or X?)

🐾 **Fun Fact:** She's known as the "PinkPanther" – a fusion of her love for mystery and a dash of pink flair.

### Mohamed Nour "RedLion" Bessadok
🧐 **Role:** Problem Solving Guru

Meet the mind that navigates the labyrinth of challenges – Mohamed is the Sherlock of our team. With a knack for critical thinking, he's our puzzle solver, spotting issues before they even think of hiding. When not crafting solutions in code, he's crafting strategic moves on a chessboard. Dune by Frank Herbert holds his heart, and horses are his favorite ride.

🌐 **Connect:** [Github](https://github.com/Mohamed-Nour-Bessadok) | [LinkedIn](https://www.linkedin.com/in/mohamed-nour-bessadok-34446b251/)

♟️ **Fun Fact:** He's a chess aficionado, and just like a grandmaster, he's always a few steps ahead.

## 🚀 Features and Challenges 

We're on a journey to create the ultimate audiobook experience with AudioVerse. While we've come a long way, there are still exciting features to be built and challenges to overcome. We believe in the power of community collaboration, and we invite you to join us on this adventure!

### 🎟️ Features in the Pipeline

- **Enhanced Narrator Variety:** Elevate the storytelling experience by seamlessly switching between different voices, perfect for dialogues and diverse characters within the same audiobook.

- **Language Magic:** Expand language support to bring audiobooks to a global audience. Unleash the magic of storytelling in multiple languages!

- **Add File Parsers:** We currently support pdfs and txt files. We're working to enhance compatibility by adding support for additional file formats.

### 🔍 Challenges to Tackle 

- **Optimizing Audiobook Generation Pipeline:** The audiobook generation process takes a significant amount of time as the size of the book increases. We're exploring ways to optimize this process, whether by reducing the number of calls made to OpenAI and ElevenLabs or by experimenting with alternative models like Stability AI or Meta's models.

- **Enriching Sound Effects:** Currently, the accuracy of sound effect insertion varies due to a limited database. We're on a mission to create a comprehensive sound effects library, categorized by topics. Additionally, we're exploring the use of text-to-sound models to generate unique and accurate sound effects.

- **PDF Parsing Improvements:** We've encountered challenges with PDF parsing using the current library. We're actively investigating alternative parsers to ensure accurate and reliable text extraction from PDF files.

## 🙌 How You Can Contribute

If you're passionate about any of the features or challenges mentioned above, or if you have your own ideas to bring to the table, we welcome your contributions!

Here's how you can get involved:

1. **Fork the Repository:** Start by forking our repository to your GitHub account.

2. **Create a Branch:** Create a new branch for your contributions, ensuring that your work doesn't interfere with the main codebase.

3. **Make Your Magic:** Work on your chosen feature or challenge, keeping in mind best coding practices.

4. **Submit a Pull Request:** Once your code is ready, submit a pull request. We'll review your work and provide feedback.

5. **Celebrate Collaboration:** By contributing, you're becoming a part of the AudioVerse community. Your contributions make a real impact!

**Join us on this exciting journey of innovation and creativity. Let's turn words into symphonies together!** 🎶🚀
