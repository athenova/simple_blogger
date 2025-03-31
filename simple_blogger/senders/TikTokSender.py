from simple_blogger.senders.SenderBase import *
import os
from markdown import Markdown
import requests

class TikTokSender(SenderBase):
    def __init__(self, access_token_name='TT_ACCESS_TOKEN', review_mode=True, tags=None, **kwargs):
        super().__init__(tags=tags,**kwargs)
        self.token = os.environ.get(access_token_name)
        self.md = Markdown(output_format="plain")
        self.md.stripTopLevelTags = False
        self.review_mode = review_mode

    def _review(self, video_file_name=None, access_token_name=None, tags=None, **_):
        token = self.token if access_token_name is None else os.environ.get(access_token_name)
        init_url = 'https://open.tiktokapis.com/v2/post/publish/inbox/video/init/'
        headers = {
            'Authorization': f"Bearer {token}",
            'Content-Type': 'application/json; charset=UTF-8'
        }
        video_size = os.path.getsize(video_file_name)
        body = {
            'source_info': {
                'source': 'FILE_UPLOAD',
                'video_size': video_size,
                'chunk_size': video_size,
                'total_chunk_count': 1
            }
        }
        response = requests.post(url=init_url, json=body, headers=headers)
        upload_url = response.json()['data']['upload_url']
        headers = {
            'Content-Type': 'video/mp4',
            'Content-Range' : f"bytes 0-{video_size-1}/{video_size}",
            'Content-Length': f"{video_size}",
        }
        requests.put(url=upload_url, headers=headers, data=open(video_file_name, 'rb'))

    def _send(self, text_file_name=None, video_file_name=None, access_token_name=None, tags=None, **_):
        token = self.token if access_token_name is None else os.environ.get(access_token_name)
        init_url = 'https://open.tiktokapis.com/v2/post/publish/video/init/'
        headers = {
            'Authorization': f"Bearer {token}",
            'Content-Type': 'application/json; charset=UTF-8'
        }
        video_size = os.path.getsize(video_file_name)
        body = {
            'post_info' : {
                'privacy_level': 'SELF_ONLY',
                'title': self.md.convert(open(text_file_name, 'rt', encoding='UTF-8').read()), 
                'is_aigc': True,
            }, 
            'source_info': {
                'source': 'FILE_UPLOAD',
                'video_size': video_size,
                'chunk_size': video_size,
                'total_chunk_count': 1
            }
        }
        response = requests.post(url=init_url, json=body, headers=headers)
        upload_url = response.json()['data']['upload_url']
        headers = {
            'Content-Type': 'video/mp4',
            'Content-Range' : f"bytes 0-{video_size-1}/{video_size}",
            'Content-Length': f"{video_size}",
        }
        requests.put(url=upload_url, headers=headers, data=open(video_file_name, 'rb'))   

    def send(self, text_file_name=None, image_file_name=None, access_token_name=None, tags=None, **kwargs):
        file_name, _ = os.path.splitext(image_file_name)
        video_file_name = f"{file_name}.mp4"
        if self.review_mode:
            self._review(video_file_name=video_file_name, access_token_name=access_token_name, tags=tags, **kwargs)
        else:
            self._send(text_file_name=text_file_name, video_file_name=video_file_name, access_token_name=access_token_name, tags=tags, **kwargs) 