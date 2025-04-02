from markdown import Markdown

class MarkdownCleaner():
    def __init__(self):
        self.md = Markdown(output_format="plain")
        self.md.stripTopLevelTags = False

    def process(self, message:str)->str:
        return self.md.convert(message)