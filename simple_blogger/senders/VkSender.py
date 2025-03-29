from simple_blogger.senders.SenderBase import SenderBase
from simple_blogger.uploaders.VkUploader import VkUploader
import os
from markdown import Markdown
import vk

class VkSender(SenderBase):
    def __init__(self, app_id=None, secret=None, group_id=None, login=None, password=None, uploader=None, tags=None, **kwargs):
        super().__init__(tags=tags,**kwargs)
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
        self.group_id = os.environ.get('VK_GROUP_ID') if group_id is None else group_id
        self.uploader = VkUploader(group_id=group_id, api=self.api) if uploader is None else uploader
        self.md = Markdown(output_format="plain")
        self.md.stripTopLevelTags = False
            
    def send(self, text_file_name=None, image_file_name=None, group_id=None, tags=None, **_):
        group_id = self.group_id if group_id is None else group_id
        if os.path.exists(image_file_name) and os.path.exists(text_file_name):
            image_address = self.uploader.upload(image_file_name)
            caption_markdown = open(text_file_name, 'rt', encoding='UTF-8').read()
            caption = self._add_tags(text=self.md.convert(caption_markdown), tags=tags)     
            self.api.wall.post(owner_id=f"-{group_id}", from_group=1, message=caption, attachments=f"{image_address}")
        elif os.path.exists(image_file_name):
            image_address = self.uploader.upload(image_file_name)
            self.api.wall.post(owner_id=f"-{group_id}", from_group=1, attachments=f"{image_address}")
        elif os.path.exists(text_file_name):
            caption_markdown = open(text_file_name, 'rt', encoding='UTF-8').read()
            caption = self._add_tags(text=self.md.convert(caption_markdown), tags=tags)     
            self.api.wall.post(owner_id=f"-{group_id}", from_group=1, message=caption)

    