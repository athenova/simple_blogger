from simple_blogger.uploader.VkUploader import VkUploader
from simple_blogger.preprocessor.text import SerialProcessor, MarkdownCleaner, IdentityProcessor
from simple_blogger.poster import IPoster, Post
import os, vk

class VkPoster(IPoster):
    def __init__(self, token_name='VK_BOT_TOKEN', group_id=None, uploader=None, processor=None, **_):
        token = os.environ.get(token_name)
        self.group_id = group_id or os.environ.get('VK_REVIEW_GROUP_ID')
        self.api = vk.API(token, v='5.199')
        self.uploader = uploader or VkUploader(group_id=self.group_id)
        self.processor = SerialProcessor([MarkdownCleaner(), processor or IdentityProcessor()])
            
    def post(self, post:Post, group_id=None, processor=None, **_):
        processor = processor or IdentityProcessor()
        group_id = group_id or self.group_id
        if post.media and post.message:
            image_address = self.uploader.upload_photo(file=post.media, group_id=group_id)
            caption = post.get_real_message(SerialProcessor([self.processor, processor]))
            self.api.wall.post(owner_id=f"-{group_id}", from_group=1, message=caption, attachments=f"{image_address}")
        else:
            if post.media:
                image_address = self.uploader.upload_photo(file=post.media, group_id=group_id)
                self.api.wall.post(owner_id=f"-{group_id}", from_group=1, attachments=f"{image_address}")
            if post.message:
                caption = post.get_real_message(SerialProcessor([self.processor, processor]))
                self.api.wall.post(owner_id=f"-{group_id}", from_group=1, message=caption)

class VkVideoPoster(VkPoster):
    def post(self, post:Post, group_id=None, processor=None, **_):
        processor = processor or IdentityProcessor()
        group_id = group_id or self.group_id
        if post.media and post.message:
            video_address = self.uploader.upload_video(file=post.media, group_id=group_id)
            caption = post.get_real_message(SerialProcessor([self.processor, processor]))
            self.api.wall.post(owner_id=f"-{group_id}", from_group=1, message=caption, attachments=f"{video_address}")
        else:
            if post.media:
                video_address = self.uploader.upload_video(file=post.media, group_id=group_id)
                self.api.wall.post(owner_id=f"-{group_id}", from_group=1, attachments=f"{video_address}")
            if post.message:
                caption = post.get_real_message(SerialProcessor([self.processor, processor]))
                self.api.wall.post(owner_id=f"-{group_id}", from_group=1, message=caption)