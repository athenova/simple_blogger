import os
import requests
import vk

class VkUploader():
    def __init__(self, app_id=None, secret=None, group_id=None, login=None, password=None, api=None):
        if api is None:
            app_id = os.environ.get('VK_APP_ID') if app_id is None else app_id
            secret = os.environ.get('VK_SECRET_KEY') if secret is None else secret
            login = os.environ.get('VK_BOT_LOGIN') if login is None else login
            password = os.environ.get('VK_BOT_PASSWORD') if password is None else password
            token = os.environ.get('VK_BOT_TOKEN')
            v = '5.199'
            self.api = vk.API(token, v=v)
            try:
                _ = self.api.account.getInfo()
            except Exception as e:
                self.api = vk.DirectUserAPI(user_login=login, user_password=password, client_id=app_id, client_secret=secret, scope='photos,wall', v=v)
                os.environ["VK_BOT_TOKEN"] = self.api.access_token
        else:
            self.api = api
        self.group_id = os.environ.get('VK_GROUP_ID') if group_id is None else group_id


    def upload(self, image_file_name):
        response = self.api.photos.getWallUploadServer(group_id=self.group_id)
        upload_url = response["upload_url"]
        files = {'photo': open(image_file_name, 'rb') }
        response = requests.post(url=upload_url, files=files).json()
        response = self.api.photos.saveWallPhoto(group_id=self.group_id
                                                , photo=response["photo"]
                                                , server=response["server"]
                                                , hash=response["hash"])
        return f"photo{response[0]['owner_id']}_{response[0]['id']}"
