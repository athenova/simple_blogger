from simple_blogger.blogger.basic.cached import CachedSimpleBlogger, CachedCommonBlogger
from simple_blogger.blogger import FiniteBlogger

class CachedFiniteSimpleBlogger(CachedSimpleBlogger, FiniteBlogger):
    def __init__(self, posters, force_rebuild=True, index=None):
        CachedSimpleBlogger.__init__(self, posters, force_rebuild, index)

class CachedFiniteCommonBlogger(CachedCommonBlogger, FiniteBlogger):
    def __init__(self, posters, force_rebuild=True, index=None):
        CachedCommonBlogger.__init__(self, posters, force_rebuild, index)   
    