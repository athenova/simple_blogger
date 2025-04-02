from .ImageGenerator import ImageGenerator
from yandex_cloud_ml_sdk import YCloudML
import os
from io import BytesIO
from ...builder.File import File

class YandexImageGenerator(ImageGenerator):
    def __init__(self, folder_id=None, model_name='yandex-art', model_version='latest'):
        super().__init__()
        self.folder_id=folder_id or os.environ.get('YC_FOLDER_ID')
        self.model_name=model_name
        self.model_version=model_version

    def generate(self, prompt, **_):
        sdk = YCloudML(folder_id=self.folder_id)
        model = sdk.models.image_generation(self.model_name)
        operation = model.run_deferred(prompt)
        result = operation.wait()
        return File('jpg', BytesIO(result.image_bytes))