from simple_blogger.builder import PostBuilder
from simple_blogger.poster import IPoster
from simple_blogger.generator.yandex import YandexTextGenerator, YandexImageGenerator
from simple_blogger.builder.task import TaskExtractor
from abc import abstractmethod
from datetime import date, timedelta
import json

class SimplestBlogger():
    def __init__(self, builder:PostBuilder, posters:list[IPoster]):
        self.builder = builder
        self.posters = posters

    def post(self, **__):
        post = self.builder.build()
        for poster in self.posters:
            poster.post(post=post)
    
    def _system_prompt(self):
        return 'Ты - известный блоггер с 1000000 подписчиков'

    def _message_generator(self):
        return YandexTextGenerator(system_prompt=self._system_prompt())
    
    def _image_generator(self):
        return YandexImageGenerator()
    
class ProjectBlogger(SimplestBlogger):
    def __init__(self, posters, index=None):
        self.index = index
        super().__init__(self._builder(), posters)

    def _message_prompt_constructor(self, task):
        return f"Напиши пост на тему {task['topic']} из области '{task['category']}', используй не более 100 слов, используй смайлики"
    
    def root_folder(self):
        return './files'
    
    def _tasks_file_path(self):
        return f"{self.root_folder()}/projects/in_progress{(self.index or '')}.json"
    
    def _load_tasks(self):
        return json.load(open(self._tasks_file_path(), "rt", encoding="UTF-8"))
    
    def _check_task(self, task, days_before=0, **_):
        check_date = date.today() + timedelta(days=days_before)
        return task['date'] == check_date.strftime('%Y-%m-%d')
    
    def _task_extractor(self, tasks):
        return TaskExtractor(tasks=tasks, check=self._check_task)           
    
    def print_current_task(self):
        tasks = self._load_tasks()
        task_extractor = self._task_extractor(tasks)
        task = task_extractor.build()
        print(f"system: {self._system_prompt()}")
        print(f"message: {self._message_prompt_constructor(task)}")
        return task
    
    @abstractmethod
    def _builder(self):
        """"""

class CachedBlogger(ProjectBlogger):
    def __init__(self, force_rebuild=False):
        self.force_rebuild = force_rebuild
    
    def _path_constructor(self, task):
        return f"{task['category']}/{task['topic']}"
    
    def _data_folder(self):
        return f"{self.root_folder()}/data"
    
    def print_current_task(self):
        task = super().print_current_task()
        print(f"path: {self._path_constructor(task)}")
        return task

class AutoBlogger(ProjectBlogger):
    def __init__(self, first_post_date=None):
        self.first_post_date = first_post_date or date.today()

    def _check_task(self, task, tasks, days_before=0):
        check_date = date.today() + timedelta(days=days_before)
        days_diff = check_date - self.first_post_date
        return task["day"] == days_diff.days % len(tasks)