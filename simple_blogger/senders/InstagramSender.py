from simple_blogger.senders.SenderBase import SenderBase
from simple_blogger.uploaders.S3Uploader import S3Uploader
import os
import requests
from PIL import Image
from markdown import Markdown

class InstagramSender(SenderBase):
    def __init__(self, channel_token_name='IG_BOT_TOKEN', channel_id=None, uploader=None, tags=None, **kwargs):
        super().__init__(tags=tags,**kwargs)
        self.uploader = S3Uploader() if uploader is None else uploader
        self.channel_token = os.environ.get(channel_token_name)
        self.channel_id = self.me()['id'] if channel_id is None else channel_id
        self.md = Markdown(output_format="plain")
        self.md.stripTopLevelTags = False

    def send(self, text_file_name=None, image_file_name=None, tags=None, **_):
        if os.path.exists(image_file_name) and os.path.exists(text_file_name):
            temp_image_name = self.png2jpg(image_file_name)
            image_url = self.uploader.upload(temp_image_name)
            caption_markdown = open(text_file_name, 'rt', encoding='UTF-8').read()
            caption = self._add_tags(text=self.md.convert(caption_markdown), tags=tags)     
            post = self.create_post(self.channel_id, image_url=image_url, caption=caption)
            self.publish(self.channel_id, post['id'])

    def png2jpg(self, image_file_name):
        file_name, _ = os.path.splitext(image_file_name)
        output_file_name = f"{file_name}.jpg"
        if not os.path.exists(output_file_name):
            png_image = Image.open(image_file_name)
            jpg_image = png_image.convert("RGB")
            jpg_image.save(output_file_name)
        return output_file_name
       
    def me(self):
        payload = { 'fields': ['user_id', 'username'], 'access_token': self.channel_token }
        user_url = "https://graph.instagram.com/v22.0/me"
        response = requests.get(user_url, params=payload).json()
        return response

    def create_post(self, account_id, image_url, caption):
        payload = { 'image_url': image_url, 'access_token': self.channel_token, 'caption': caption }
        crate_image_url = f"https://graph.instagram.com/v22.0/{account_id}/media"
        response = requests.post(crate_image_url, params=payload).json()
        return response

    def publish(self, account_id, creation_id):
        payload = { 'creation_id': creation_id, 'access_token': self.channel_token }
        crate_image_url = f"https://graph.instagram.com/v22.0/{account_id}/media_publish"
        response = requests.post(crate_image_url, params=payload).json()
        return response
