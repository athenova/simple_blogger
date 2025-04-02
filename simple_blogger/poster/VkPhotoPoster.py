from ..uploader.VkUploader import VkUploader
import os
import vk
from .IPoster import IPoster
from .Post import Post
from ..preprocessor.text.SerialProcessor import SerialProcessor
from ..preprocessor.text.MarkdownCleaner import MarkdownCleaner
from ..preprocessor.text.IdentityProcessor import IdentityProcessor

class VkPhotoPoster(IPoster):
    def __init__(self, token_name='VK_BOT_TOKEN', group_id=None, uploader=None, custom_processor=IdentityProcessor(), **_):
        token = os.environ.get(token_name)
        self.group_id = group_id or os.environ.get('VK_REVIEW_GROUP_ID')
        self.api = vk.API(token, v='5.199')
        self.uploader = uploader or VkUploader(group_id=self.group_id)
        self.processor = SerialProcessor([MarkdownCleaner(), custom_processor])
            
    def post(self, post:Post, group_id=None, custom_processor=IdentityProcessor(), **_):
        group_id = group_id or self.group_id
        if post.media and post.message:
            image_address = self.uploader.upload_photo(post.get_real_media(), group_id=group_id)
            caption = post.get_real_message(SerialProcessor([self.processor, custom_processor]))
            self.api.wall.post(owner_id=f"-{group_id}", from_group=1, message=caption, attachments=f"{image_address}")
        else:
            if post.media:
                image_address = self.uploader.upload_photo(post.get_real_media(), group_id=group_id)
                self.api.wall.post(owner_id=f"-{group_id}", from_group=1, attachments=f"{image_address}")
            if post.message:
                caption = post.get_real_message(SerialProcessor([self.processor, custom_processor]))
                self.api.wall.post(owner_id=f"-{group_id}", from_group=1, message=caption)