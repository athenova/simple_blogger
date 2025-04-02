from .ITextProcessor import ITextProcessor

class IdentityProcessor(ITextProcessor):        
    def process(self, message:str)->str:
        return message