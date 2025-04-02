from .ITextProcessor import ITextProcessor

class SerialProcessor(ITextProcessor):
    def __init__(self, processors:list[ITextProcessor]):
        self.processors = processors

    def process(self, message:str)->str:
        for processor in self.processors:
            message = processor.process(message=message)
        return message