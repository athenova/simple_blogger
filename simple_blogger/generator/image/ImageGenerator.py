from PIL import Image
from io import BytesIO
from ..IGeneratorBase import IGeneratorBase


class ImageGenerator(IGeneratorBase):
    def __init__(self):
        pass

    def generate(self, *_, **__):
        stream = BytesIO()
        Image.new(mode='RGBA', size=(1,1), color=1).save(stream)
        return stream.getbuffer()
    
class ImagePromptGenerator(ImageGenerator):
    def __init__(self, image_generator, image_prompt_builder):
        self.image_generator= image_generator
        self.image_prompt_builder=image_prompt_builder

    def generate(self, user_prompt, force_rebuild=False, **_):
        prompt_file=self.image_prompt_builder.build(user_prompt, force_rebuild=force_rebuild)
        return self.image_generator.generate(prompt=prompt_file.file.read())
