from abc import ABC, abstractmethod

class ITextProcessor(ABC):
    @abstractmethod
    def process(self, message:str)->str:
        """ Message preprocess method """