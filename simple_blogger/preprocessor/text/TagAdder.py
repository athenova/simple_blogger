from .ITextProcessor import ITextProcessor

class TagAdder(ITextProcessor):
    def __init__(self, tags:list[str]):
        self.tags = tags

    def process(self, message:str)->str:
        text_lower = message.lower()
        delimiter = '\n\n'
        for tag in self.tags:
            if not tag.lower() in text_lower:
                message += f"{delimiter}{tag}"
                delimiter = ' '
        return message