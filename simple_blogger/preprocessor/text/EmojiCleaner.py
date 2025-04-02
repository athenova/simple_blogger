import emoji
from .ITextProcessor import ITextProcessor

class EmojiCleaner(ITextProcessor):        
    def process(self, message:str)->str:
        return emoji.replace_emoji(message)