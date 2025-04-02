from .IContentBuilder import IContentBuilder

class ContentBuilder(IContentBuilder):
    def __init__(self, generator, prompt=None):
        self.generator = generator
        self.prompt = prompt

    def build(self, prompt=None, force_rebuild=False):
        return self.generator.generate(prompt or self.prompt, force_rebuild=force_rebuild)