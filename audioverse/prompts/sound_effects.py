class SoundEffectsPrompt:
    def __init__(self):
        self.system = """
        As an audiobook creator, your task is to enhance a book by inserting sound effects at appropriate moments. 
        Your job is to identify the moments where sound effects should be placed and insert the corresponding sound effects enclosed in square brackets '[]', without altering any words in the given text. 
        The sound effects should be carefully positioned just after the expression of the sound in the text."""
        self.user = """
        -- Excerpt from the book: {text}\n\n
        -- Text with sound effects:"""

    def __call__(self, text):
        return {
            "system": self.system,
            "user": self.user.format(text=text),
        }
