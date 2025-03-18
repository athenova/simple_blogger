from simple_blogger.generators.GeneratorBase import GeneratorBase
from yandex_cloud_ml_sdk import YCloudML
from PIL import Image
import os

class YandexGenerator(GeneratorBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.folder_id = kwargs['folder_id'] if 'folder_id' in kwargs else os.environ.get('YC_FOLDER_ID')
        self.model_version = kwargs['model_version'] if 'model_version' in kwargs else "latest"

class YandexTextGenerator(YandexGenerator):
    def __init__(self, **kwargs):
        kwargs.setdefault("model_name", "yandexgpt")
        kwargs.setdefault("model_version", "latest")
        super().__init__(**kwargs)

    def gen_content(self, system_prompt, user_prompt, output_file_name, force_regen=False):
        if force_regen or not os.path.exists(output_file_name):
            sdk = YCloudML(folder_id=self.folder_id)
            model = sdk.models.completions(model_name=self.model_name, model_version=self.model_version)
            text = model.run([
                            { "role": "system", "text": system_prompt },
                            { "role": "user", "text": user_prompt },
                        ]
                    ).alternatives[0].text
            open(output_file_name, 'wt', encoding="UTF-8").write(text)

class YandexImageGenerator(YandexGenerator):
    def __init__(self, **kwargs):
        kwargs.setdefault("model_name", "yandex-art")
        kwargs.setdefault("model_version", "latest")
        super().__init__(**kwargs)

    def gen_content(self, prompt, output_file_name, force_regen=False, remove_temp_file=True):
        file_name, _ = os.path.splitext(output_file_name)
        temp_file_name = f"{file_name}.jpg"

        if force_regen or (not os.path.exists(temp_file_name) and not os.path.exists(output_file_name)):
            sdk = YCloudML(folder_id=self.folder_id)
            model = sdk.models.image_generation(self.model_name)
            operation = model.run_deferred(prompt)
            result = operation.wait()
            open(temp_file_name, 'wb').write(result.image_bytes)

        if os.path.exists(temp_file_name) and (force_regen or not os.path.exists(output_file_name)):
            jpeg_image = Image.open(temp_file_name)
            png_image = jpeg_image.convert("RGBA")
            png_image.save(output_file_name)
            if remove_temp_file: os.remove(temp_file_name)
