from ..uploader.S3Uploader import S3Uploader
import os
import requests
from .IPoster import IPoster
from .Post import Post
from ..preprocessor.text.SerialProcessor import SerialProcessor
from ..preprocessor.text.MarkdownCleaner import MarkdownCleaner
from ..preprocessor.text.IdentityProcessor import IdentityProcessor

class IgPhotoPoster(IPoster):
    def __init__(self, account_token_name='IG_BOT_TOKEN', account_id=None, uploader=S3Uploader(), custom_processor=IdentityProcessor(), **_):
        self.uploader = uploader
        self.account_token = os.environ.get(account_token_name)
        self.account_id = account_id or self.me()['id']
        self.processor = SerialProcessor([MarkdownCleaner(), custom_processor])
            
    def post(self, post:Post, custom_processor=IdentityProcessor(), **_):
        if post.media and post.message:
            image_url = self.uploader.upload(post.get_real_media(), extra_args={ 'ContentType': post.get_content_type() })
            caption = post.get_real_message(SerialProcessor([self.processor, custom_processor]))
            post = self.create_post(self.account_id, image_url=image_url, caption=caption)
            self.publish(self.account_id, post['id'])

    def me(self):
        payload = { 'fields': ['user_id', 'username'], 'access_token': self.account_token }
        user_url = "https://graph.instagram.com/v22.0/me"
        response = requests.get(user_url, params=payload).json()
        return response

    def create_post(self, account_id, image_url, caption):
        payload = { 'image_url': image_url, 'access_token': self.account_token, 'caption': caption }
        crate_image_url = f"https://graph.instagram.com/v22.0/{account_id}/media"
        response = requests.post(crate_image_url, params=payload).json()
        return response

    def publish(self, account_id, creation_id):
        payload = { 'creation_id': creation_id, 'access_token': self.account_token }
        crate_image_url = f"https://graph.instagram.com/v22.0/{account_id}/media_publish"
        response = requests.post(crate_image_url, params=payload).json()
        return response
