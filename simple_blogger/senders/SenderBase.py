from datetime import timedelta

class SenderBase():
    def __init__(self
                #  , days_to_review=timedelta(days=1)
                 , send_text_with_image=True
                 , tags=None
                #  , force_image_regen=False
                #  , force_text_regen=False
                 ):
        # self.days_to_review = days_to_review
        self.send_text_with_image = send_text_with_image
        self.tags = [] if tags is None else tags
        # self.force_image_regen = force_image_regen
        # self.force_text_regen = force_text_regen
        pass

    def _add_tags(self, text, tags, **_):
        result = text
        text_lower = text.lower()
        delimiter = '\n\n'
        for tag in self.tags if tags is None else tags:
            if not tag.lower() in text_lower:
                result += f"{delimiter}{tag}"
                delimiter = ' '
        return result