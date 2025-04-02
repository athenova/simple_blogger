from openai import OpenAI
import os
from io import StringIO
from .TextGenerator import TextGenerator
from ...builder.File import File

class OpenAiTextGenerator(TextGenerator):
    def __init__(self, system_prompt, api_key_name ='OPENAI_API_KEY', model_name='chatgpt-4o-latest'):
        super().__init__(system_prompt=system_prompt)
        self.api_key = os.environ.get(api_key_name)
        self.model_name=model_name

    def generate(self, prompt, **_):
        client = OpenAI(api_key=self.api_key)
        text = client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        { "role": "system", "content": self.system_prompt },
                        { "role": "user", "content": prompt },
                    ]
                ).choices[0].message.content
        return File('txt', StringIO(text))