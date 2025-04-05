import os, requests, vk
from simple_blogger.generator import File

class VkUploader():
    def __init__(self, token_name='VK_BOT_TOKEN', group_id=None):
        token = os.environ.get(token_name)
        self.group_id = group_id or os.environ.get('VK_REVIEW_GROUP_ID')
        self.api = vk.API(token, v='5.199')

    def upload_photo(self, file:File, group_id=None):
        group_id = group_id or self.group_id
        response = self.api.photos.getWallUploadServer(group_id=group_id)
        upload_url = response["upload_url"]
        files = {'photo': (f"photo.{file.ext}", file.get_file(), file.get_content_type() ) }
        response = requests.post(url=upload_url, files=files).json()
        response = self.api.photos.saveWallPhoto(group_id=self.group_id
                                                , photo=response["photo"]
                                                , server=response["server"]
                                                , hash=response["hash"])
        return f"photo{response[0]['owner_id']}_{response[0]['id']}"
