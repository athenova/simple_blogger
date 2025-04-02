from ..IGeneratorBase import IGeneratorBase

class TextGenerator(IGeneratorBase):
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt

    def generate(self, prompt, **_):
        return prompt