from .SenderBase import *
from .TelegramSender import *
from .InstagramSender import *
from .VkSender import *
from io import StringIO
# from .DeepSeekGenerator import *

def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()

Markdown.output_formats["plain"] = unmark_element