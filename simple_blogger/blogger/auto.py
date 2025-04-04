from simple_blogger.blogger.basic import SimpleBlogger
from datetime import date, timedelta

class AutoBlogger(SimpleBlogger):
    def __init__(self, posters, first_post_date=None, force_rebuild=True, index=None):
        self.first_post_date=first_post_date or date.today()
        super().__init__(posters=posters, force_rebuild=force_rebuild, index=index)

    def _check_task(self, task, tasks, days_before=0):
        check_date = date.today() + timedelta(days=days_before)
        days_diff = check_date - self.first_post_date
        return task["day"] == days_diff.days % len(tasks)
    