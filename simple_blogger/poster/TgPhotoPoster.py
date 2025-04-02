from simple_blogger.senders.SenderBase import *
import os
import telebot
from .Post import Post
from .IPoster import IPoster
from ..preprocessor.text.SerialProcessor import SerialProcessor
from ..preprocessor.text.IdentityProcessor import IdentityProcessor

class TgPhotoPoster(IPoster):
    def __init__(self, bot_token_name='TG_BOT_TOKEN', chat_id=None, custom_processor=IdentityProcessor(), send_text_with_image=True, **_):
        self.bot_token = os.environ.get(bot_token_name)
        self.chat_id = chat_id or os.environ.get('TG_REVIEW_CHAT_ID')
        self.send_text_with_image = send_text_with_image
        self.bot = telebot.TeleBot(self.bot_token)
        self.processor = custom_processor

    def post(self, post:Post, chat_id=None, custom_processor=IdentityProcessor(), **_):
        chat_id = chat_id or self.chat_id
        if self.send_text_with_image and post.media and post.message:
            self.bot.send_photo(chat_id=chat_id, photo=post.get_real_media(), caption=post.get_real_message(SerialProcessor([self.processor, custom_processor])), parse_mode="Markdown")
        else:
            if post.media:
                self.bot.send_photo(chat_id=chat_id, photo=post.get_real_media(), disable_notification=True)
            if post.message:
                self.bot.send_message(chat_id=chat_id, text=post.get_real_message(SerialProcessor([self.processor, custom_processor])), parse_mode="Markdown")
    
    def post_error(self, message):
        self.bot.send_message(chat_id=self.chat_id, text=message)