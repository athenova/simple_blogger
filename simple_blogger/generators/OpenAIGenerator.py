from openai import OpenAI
import requests
import os
from PIL import Image
from .GeneratorBase import GeneratorBase

class OpenAIGenerator(GeneratorBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class OpenAITextGenerator(OpenAIGenerator):
    def __init__(self, **kwargs):
        kwargs.setdefault("model_name", "chatgpt-4o-latest")
        super().__init__(**kwargs)

    def gen_content(self, system_prompt, user_prompt, output_file_name, force_regen=False):
        if force_regen or not os.path.exists(output_file_name):
            client = OpenAI()
            text = client.chat.completions.create(
                        model=self.model_name,
                        messages=[
                            { "role": "system", "content": system_prompt },
                            { "role": "user", "content": user_prompt },
                        ]
                    ).choices[0].message.content
            open(output_file_name, 'wt', encoding="UTF-8").write(text)
        

class OpenAIImageGenerator(OpenAIGenerator):
    def __init__(self, **kwargs):
        kwargs.setdefault('model_name', 'dall-e-3')
        super().__init__(**kwargs)

    def gen_content(self, prompt, output_file_name, force_regen=False, remove_temp_file=True):
        file_name, _ = os.path.splitext(output_file_name)
        temp_file_name = f"{file_name}.webp"

        if force_regen or (not os.path.exists(temp_file_name) and not os.path.exists(output_file_name)):
            client = OpenAI()
            image_url = client.images.generate(
                model = self.model_name,
                prompt = prompt,
                size = "1024x1024",
                quality = "standard",
                n = 1                
            ).data[0].url
            response = requests.get(image_url)
            with open(temp_file_name, 'wb') as f:
                f.write(response.content)

        if os.path.exists(temp_file_name) and (force_regen or not os.path.exists(output_file_name)):
            webp_image = Image.open(temp_file_name)
            png_image = webp_image.convert("RGBA")
            png_image.save(output_file_name)
            if remove_temp_file: os.remove(temp_file_name)