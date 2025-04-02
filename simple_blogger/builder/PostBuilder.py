from ..poster.Post import Post

class PostBuilder():
    def __init__(self, message_builder=None, media_builder=None):
        self.message_builder = message_builder
        self.media_builder = media_builder

    def build(self, force_rebuild=False):
        return Post(
            self.message_builder.build(force_rebuild=force_rebuild) if self.message_builder else None,
            self.media_builder.build(force_rebuild=force_rebuild) if self.media_builder else None
        )