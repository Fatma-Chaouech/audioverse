class SoundEffectsPrompt:
    def __init__(self):
        self.system = """
        As an audiobook creator, your task is to go through a book and insert sound effects at the appropriate places.
        You have to return to your boss the same text that he gave you, but filled with sound effects between '[]'.
        You should not change any word of the given text, just insert the sound effects."""
        self.user = """
        -- Excerpt from the book: {text}\n\n
        Text with sound effects:"""

    def __call__(self, text):
        return {
            "system": self.system,
            "user": self.user.format(text=text),
        }
