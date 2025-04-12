from simple_blogger.blogger.basic import SimpleBlogger, CommonBlogger
from simple_blogger.blogger import AutoBlogger

class AutoSimpleBlogger(SimpleBlogger, AutoBlogger):
    def __init__(self, posters, first_post_date=None, index=None):
        AutoBlogger.__init__(self, first_post_date)
        SimpleBlogger.__init__(self, posters, index)

class AutoCommonBlogger(CommonBlogger, AutoBlogger):
    def __init__(self, posters, first_post_date=None, index=None):
        AutoBlogger.__init__(self, first_post_date)
        CommonBlogger.__init__(self, posters, index)