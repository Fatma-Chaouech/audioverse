# AudioVerse
Breathe life into your books.


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