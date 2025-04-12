from simple_blogger.blogger.basic import SimpleBlogger, CommonBlogger
from simple_blogger.blogger import FiniteBlogger

class FiniteSimpleBlogger(SimpleBlogger, FiniteBlogger):
    def __init__(self, posters, index=None):
        SimpleBlogger.__init__(self, posters, index)

class FiniteCommonBlogger(CommonBlogger, FiniteBlogger):
    def __init__(self, posters, index=None):
        CommonBlogger.__init__(self, posters, index)