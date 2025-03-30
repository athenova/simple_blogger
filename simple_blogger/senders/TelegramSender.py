from simple_blogger.senders.SenderBase import *
import os
import telebot

class TelegramSender(SenderBase):
    def __init__(self, channel_token_name=None, channel_id=None, tags=None, **kwargs):
        super().__init__(tags=tags, **kwargs)
        channel_token_name ='TG_BOT_TOKEN' if channel_token_name is None else channel_token_name
        self.bot_token = os.environ.get(channel_token_name)
        self.channel_id = os.environ.get('TG_REVIEW_CHANNEL_ID') if channel_id is None else channel_id
        self.bot = telebot.TeleBot(self.bot_token)

    def send(self, text_file_name=None, image_file_name=None, chat_id=None, tags=None, **_):
        chat_id = self.channel_id if chat_id is None else chat_id
        if self.send_alternatives is SendAlternatives.FirstOnly:
            file_name, ext = os.path.splitext(image_file_name)
            image_file_name = f"{file_name}_1{ext}"
        if self.send_alternatives is SendAlternatives.All:
            raise NotImplementedError()
        if self.send_text_with_image and os.path.exists(image_file_name) and os.path.exists(text_file_name): 
            self.bot.send_photo(chat_id=chat_id
                            , photo=open(image_file_name, 'rb')
                            , caption=self._add_tags(text=open(text_file_name, 'rt', encoding='UTF-8').read(), tags=tags)
                            , parse_mode="Markdown")
        else:
            if os.path.exists(image_file_name):
                self.bot.send_photo(chat_id=chat_id
                                , photo=open(image_file_name, 'rb')
                                , disable_notification=True)

            if os.path.exists(text_file_name):
                self.bot.send_message(chat_id=chat_id
                                    , text=self._add_tags(text=open(text_file_name, 'rt', encoding='UTF-8').read(), tags=tags)
                                    , parse_mode="Markdown")
    
    def send_error(self, message):
        self.bot.send_message(chat_id=self.channel_id, text=message)