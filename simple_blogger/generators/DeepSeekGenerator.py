from openai import OpenAI
import os
from .GeneratorBase import GeneratorBase

class DeepSeekGenerator(GeneratorBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token_name ='DEEPSEEK_API_KEY'
        self.base_url='https://api.deepseek.com'

class DeepSeekTextGenerator(DeepSeekGenerator):
    def __init__(self, **kwargs):
        kwargs.setdefault('model_name', 'deepseek-chat')
        super().__init__(**kwargs)

    def gen_content(self, system_prompt, user_prompt, output_file_name, force_regen=False):
        if force_regen or not os.path.exists(output_file_name):
            client = OpenAI(api_key=os.environ.get(self.token_name), base_url=self.base_url)
            text = client.chat.completions.create(
                        model=self.model_name,
                        messages=[
                            { "role": "system", "content": system_prompt },
                            { "role": "user", "content": user_prompt },
                        ]
                    ).choices[0].message.content
            open(output_file_name, 'wt', encoding="UTF-8").write(text)
