import random
from typing import List

from audioverse.pinecone_utils import find_most_similar_effect


def update_chunk_sfx(word, chunk, sfx, sound_effects, index):
    idx_opening_bracket, idx_closing_bracket = brackets_position(word)

    if idx_opening_bracket != -1 and idx_closing_bracket == -1:
        chunk += word[:idx_opening_bracket] + "- - - - - - - - - - - -\n- - - - - - - - - - - -"
        sfx += word[idx_opening_bracket:]

    elif idx_opening_bracket == -1 and idx_closing_bracket != -1:
        sfx += word[: idx_closing_bracket - 1]
        sound_effects.append(find_most_similar_effect(sfx[1:-1], index))
        sfx = ""
        chunk += word[idx_closing_bracket + 1 :]
    elif idx_opening_bracket != -1 and idx_closing_bracket != -1:
        chunk += (
            word[:idx_opening_bracket]
            + "- - - - - - - - - - - -\n- - - - - - - - - - - -"
            + word[idx_closing_bracket + 1 :]
        )
        sound_effects.append(
            find_most_similar_effect(
                word[idx_opening_bracket + 1 : idx_closing_bracket], index
            )
        )
    elif sfx != "":
        sfx += word
    else:
        chunk += word
    return chunk, sfx, sound_effects


def brackets_position(word):
    idx_opening_bracket = word.find("[")
    idx_closing_bracket = word.find("]")

    return idx_opening_bracket, idx_closing_bracket


def input_to_chunks(input_text):
    return [x.strip() for x in input_text.split("\n\n") if x.strip() != ""]


def chunked_text_from_paragraphs(paragraphs: List[str], chunk_size=100) -> List[str]:
    return "\n\n".join(
        [
            " ".join(paragraphs[i : i + chunk_size])
            for i in range(0, len(paragraphs), chunk_size)
        ]
    )


def get_random_excerpt(content):
    split_book = input_to_chunks(content)
    return split_book[random.randint(0, len(split_book) - 1)]
