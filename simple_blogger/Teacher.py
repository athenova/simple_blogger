from simple_blogger import CommonBlogger
from itertools import groupby
from datetime import timedelta
import math

class Teacher(CommonBlogger):
    def __init__(self, last_post_date, **kwargs):
        self.last_post_date = last_post_date
        kwargs.setdefault('shuffle_tasks', False)
        super().__init__(**kwargs)

    def _example_task_creator(self):
        return [ { "topic": "Post topic", "author": "Topic author", "category": "Post Category" } ]

    def _task_converter(self, idea):
        return { 
                "topic": f"{idea['author']}. {idea['topic']}" if 'author' in idea else idea['topic'],
                "category": f"{idea['category']}",
                "topic_image": f"Draw a picture, inspired by '{idea['topic']}' from '{idea['category']}'",
                "topic_text": f"Write about '{idea['topic']}' from '{idea['category']}', use less than {self.topic_word_limit} words",
            }

    def _task_post_processor(self, tasks, first_post_date, *_):
        f = lambda x: x['index']
        for index, group in groupby(sorted(tasks, key=f), f):
            category_tasks = list(group)
            curr_date = first_post_date + timedelta(days=math.trunc((index-1)/2))
            d = (self.last_post_date - curr_date).days / len(category_tasks)
            days_between_posts = timedelta(days = d)
            for task in category_tasks:
                if curr_date.weekday() == 6: curr_date += timedelta(days=1)
                if curr_date.weekday() == 5: curr_date += timedelta(days=-1)
                task["date"] = curr_date.strftime("%Y-%m-%d")
                curr_date += days_between_posts
        tasks.sort(key=lambda x: x['date'])
