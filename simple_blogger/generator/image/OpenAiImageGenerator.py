from .ImageGenerator import ImageGenerator
from openai import OpenAI
import requests
import os
from io import BytesIO
from ...builder.File import File

class OpenAiImageGenerator(ImageGenerator):
    def __init__(self, api_key_name ='OPENAI_API_KEY', model_name='dall-e-3'):
        self.api_key = os.environ.get(api_key_name)
        self.model_name=model_name

    def generate(self, prompt, **_):
        client = OpenAI(api_key=self.api_key)
        image_url = client.images.generate(
            model = self.model_name,
            prompt = prompt,
            size = "1024x1024",
            quality = "standard",
            n = 1                
        ).data[0].url
        response = requests.get(image_url)
        return File('png', BytesIO(response.content))