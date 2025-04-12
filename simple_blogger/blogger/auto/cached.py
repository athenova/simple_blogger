from simple_blogger.blogger.basic.cached import CachedSimpleBlogger, CachedCommonBlogger
from simple_blogger.blogger import AutoBlogger

class CachedAutoSimpleBlogger(CachedSimpleBlogger, AutoBlogger):
    def __init__(self, posters, first_post_date=None, force_rebuild=True, index=None):
        AutoBlogger.__init__(self, first_post_date)
        CachedSimpleBlogger.__init__(self, posters, force_rebuild, index)

class CachedAutoCommonBlogger(CachedCommonBlogger, AutoBlogger):
    def __init__(self, posters, first_post_date=None, force_rebuild=True, index=None):
        AutoBlogger.__init__(self, first_post_date)
        CachedCommonBlogger.__init__(self, posters, force_rebuild, index)   
    