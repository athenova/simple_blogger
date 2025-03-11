from datetime import timedelta
from datetime import datetime
from simple_blogger import SimpleBlogger

class Journalist(SimpleBlogger):
    def _example_task_creator(self):
        return [ { "topic": "Post Topic", "category": "Post Category" } ]
      
    def _task_converter(self, item):
        return { 
                "category": f"{item['category']}",
                "category": f"{item['category']}",
                "topic_image": f"Draw a picture, inspired by '{item['topic']}' from domain '{item['category']}'",
                "topic_prompt": f"Write about '{item['topic']}' from domain '{item['category']}', use less than {self.topic_word_limit} words",
            }
    
    def _get_category_folder(self, task):
        return task['category']
                
    def _get_topic_folder(self, task):
        return task['topic']

    def _task_post_processor(self, tasks, *_):
        for i, task in enumerate(tasks):
            task["day"] = i

    def _task_extractor(self, tasks, days_offset=None, **_):
        days_offset = days_offset if days_offset is not None else timedelta(days=0)
        check_date = datetime.today() + days_offset
        days_diff = check_date - self.first_post_date
        for task in tasks:
            if task["day"] == days_diff.days % len(tasks): return task
        return None