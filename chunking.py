import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def identify_onomatopoeia_sounds(book):
    deli = "you are an insane linguist with 20years experience in literature, each time you see a onomatopoeia sounds you can't help but put it between []"
    prompt = f"Do what you will\n\ntext:{book}\n\n refactored text:"
    messages = [
        {"role": "system", "content": deli},
        {"role": "user", "content": prompt},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        temperature=0.1,
    )
    identified_sounds = response["choices"][0]["message"]["content"]
    return identified_sounds


def split_book(book):
    paragraphs = book.split("\n\n")
    return paragraphs


book = """Amidst the clash of swords, a thunderous "clang" rang through the air. "Crack!" went the breaking wood, and the knights charged, "thud, thud, thud," their armored boots striking the ground. The crowd roared with a resounding "cheers," and the blacksmith's hammer went "clang, clang, clang" in the village.

In the forest, "snap" went the twigs, and a haunting "hoo-hoo" called from above. Through the dense foliage, "rustle, rustle," went the mysterious creatures. As the storm approached, "rumble" echoed across the sky, and the raindrops went "tap, tap, tap" on the cobblestone streets.

In the midst of it all, "haha," laughed the merry tavern-goers, and the bards sang "ballad, ballad" of heroes' quests. The church bells tolled, "dong, dong," and the monks chanted "hum, hum" their ancient prayers.

The symphony of Eloria, a land of "clash, clang, crack," and "snap, rustle, rumble," "cheers, haha, ballad," filled the air. In this medieval realm, onomatopoeia expressions painted a vivid canvas of sound, weaving tales of valor and wonder that echoed through time."""
identified_sounds = identify_onomatopoeia_sounds(book)

print(split_book(identified_sounds))
