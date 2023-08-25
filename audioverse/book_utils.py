import random
import re
from typing import List


def extract_sound_effects_from_text(text):
    pattern = r"\[([^]]+)\]"
    matches = re.findall(pattern, text)
    return matches


def input_to_chunks(input_text):
    return [x.strip() for x in input_text.split("\n\n") if x.strip() != ""]


def chunk_and_remove_sfx(text):
    chunks_with_sfx = text.split("[")
    chunks_without_sfx = []

    for chunk_sfx in chunks_with_sfx:
        index_closing_bracket = chunk_sfx.find("]")

        if index_closing_bracket != -1:
            remaining_chunk = chunk_sfx[index_closing_bracket + 1 :]
            if remaining_chunk != "":
                chunks_without_sfx.append(remaining_chunk)
        else:
            chunks_without_sfx.append(chunk_sfx)

    return chunks_without_sfx


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
