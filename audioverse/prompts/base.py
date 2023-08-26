class BasePrompt:
    def __init__(self, system, user):
        self.system = system
        self.user = user
    
    def __call__(self, **kwargs):
        return {
            "system": self.system,
            "user": self.user.format(**kwargs),
        }

