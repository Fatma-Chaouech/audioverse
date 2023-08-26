from audioverse.prompts.base import BasePrompt


class VoiceCategoryPrompt(BasePrompt):
    def __init__(self):
        system = """
        As an audiobook creator, your task is to select the most suitable voice actor for a specific part of the book, based on the provided voice actors' descriptions and the excerpt from the book. 
        Your role is to return only the name of the chosen voice actor, not any other text.
        If there isn't enough information to make a decision, just answer 'Rachel'"""
        user = """
        -- voice actors and their descriptions: {voices}
        -- Excerpt from the book: {text}\n\n
        Chosen voice actor:"""
        super().__init__(system=system, user=user)

    def __call__(self, voices, text):
        return super().__call__(voices=voices, text=text)
