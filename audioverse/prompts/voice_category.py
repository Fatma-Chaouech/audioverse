class VoiceCategoryPrompt:
    def __init__(self):
        self.prompt = """
        System: As an audiobook creator, your task is to select the most suitable voice actor for a specific part of the book, based on the provided voice actors' descriptions and the excerpt from the book. 
        Your role is to only return the name of the chosen voice actor, not any other text.\n\n
        User: 
        -- voice actors and their descriptions: {voices}
        -- Excerpt from the book: {text}\n\n
        Chosen voice actor:"""
    
    def __call__(self, voices, text):
        return self.prompt.format(voices=voices, text=text)
