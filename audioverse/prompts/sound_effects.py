from audioverse.prompts.base import BasePrompt


class SoundEffectsPrompt(BasePrompt):
    def __init__(self):
        system = """
        As an audiobook creator, your task is to enhance a book by inserting sound effects at appropriate moments. 
        Your job is to identify the moments where sound effects should be placed and insert the corresponding sound effects enclosed in square brackets '[]', without altering any words in the given text. 
        However, you should avoid incorporating multiple sounds in the same area or section of the text.
        The sound effects should be carefully positioned just after the expression of the sound in the text.
        These sound effects should be comprehensible even when taken out of context. They should be presented in the form of "something doing something" or "someone doing something," where the sound is described as an action or event, such as "door slamming" or "baby crying." 
        However, it's crucial to note that the sound effects should only represent background sounds. 
        These background sounds are the subtle audio cues that add depth and atmosphere to the audiobook without interfering with the narration or dialogue."""
        user = """
        -- Excerpt from the book: {text}\n\n
        -- Text with sound effects:"""
        super().__init__(system=system, user=user)

    def __call__(self, text):
        return super().__call__(text=text)
