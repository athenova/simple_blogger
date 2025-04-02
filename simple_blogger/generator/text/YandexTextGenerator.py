from .TextGenerator import TextGenerator
from yandex_cloud_ml_sdk import YCloudML
import os
from io import StringIO
from ...builder.File import File

class YandexTextGenerator(TextGenerator):
    def __init__(self, system_prompt, folder_id=None, model_name='yandexgpt', model_version='latest'):
        super().__init__(system_prompt=system_prompt)
        self.folder_id=folder_id or os.environ.get('YC_FOLDER_ID')
        self.model_name=model_name
        self.model_version=model_version

    def generate(self, prompt, **_):
        sdk = YCloudML(folder_id=self.folder_id)
        model = sdk.models.completions(model_name=self.model_name, model_version=self.model_version)
        text = model.run([
                        { "role": "system", "text": self.system_prompt },
                        { "role": "user", "text": prompt },
                    ]
                ).alternatives[0].text
        return File('txt', StringIO(text))