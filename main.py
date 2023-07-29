import os
from dotenv import load_dotenv
import openai
from elevenlabs.api import Voices
from audioverse.prompts import VoiceCategoryPrompt
from audioverse.utils import get_file_if_path_exists, save_dict_to_json


def get_voices_info():
    voice_types = get_file_if_path_exists("voice_types.json")
    voice_ids = get_file_if_path_exists("voice_ids.json")
    if not voice_types or not voice_ids:
        voices = Voices.from_api()
        voice_types = [{"name": voice.name, "labels": voice.labels} for voice in voices]
        voice_ids = {voice.name: voice.voice_id for voice in voices}
        save_dict_to_json(voice_types, "voice_types.json")
        save_dict_to_json(voice_ids, "voice_ids.json")
    return voice_types, voice_ids


def query_model(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]},
        ],
    )
    return completion.choices[0].message['content']


def run():
    load_dotenv()
    voice_types, voice_ids = get_voices_info()
    template = VoiceCategoryPrompt()
    text = """
        Amelia tiptoed through the dense foliage of the ancient forest, her heart pounding with excitement and a hint of fear. The moss-covered trees towered above her, their gnarled branches forming an intricate canopy that filtered the sunlight. As she ventured deeper, the air seemed to hum with an otherworldly energy.
        Amongst the shadows, Amelia caught a glimpse of a mysterious figure, tall and ethereal, moving gracefully between the trees. His voice was a soothing melody that seemed to resonate with the very essence of the forest. He spoke of forgotten tales and whispered secrets of the woodland creatures. Amelia felt drawn to him, a curious enchantment wrapping around her like a delicate vine.
        In that moment, she knew she had found the perfect guide to explore the secrets of the forest.
        """
    actor_name = query_model(template(voice_types, text))
    actor_id = voice_ids[actor_name]
    print('GPT has chosen {} for the voice actor'.format(actor_name))


if __name__ == "__main__":
    run()
