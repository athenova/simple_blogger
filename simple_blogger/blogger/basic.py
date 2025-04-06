from simple_blogger.builder import PostBuilder
from simple_blogger.poster import IPoster
from simple_blogger.generator.yandex import YandexTextGenerator, YandexImageGenerator
from simple_blogger.builder.task import TaskExtractor
from simple_blogger.cache.file_system import FileCache
from simple_blogger.builder.prompt import TaskPromptBuilder, ContentBuilderPromptBuilder
from simple_blogger.builder.content import CachedContentBuilder, ContentBuilder
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
    
class SimpleBlogger(SimplestBlogger):
    def __init__(self, posters, force_rebuild=False, index=None):
        self.index=index
        self.force_rebuild=force_rebuild
        super().__init__(builder=self._builder(), posters=posters)

    def _path_constructor(self, task):
        return f"{task['category']}/{task['topic']}/{self._topic()}"
    
    def _message_prompt_constructor(self, task):
        return f"Напиши пост на тему {task['topic']} из области '{task['category']}', используй не более 100 слов, используй смайлики"
    
    def _image_prompt_constructor(self, task):
        return f"Нарисуй рисунок, вдохновленный темой {task['topic']} из области '{task['category']}'"
    
    def _topic(self):
        return 'topic'
    
    def root_folder(self):
        return './files'

    def _data_folder(self):
        return f"{self.root_folder()}/data"
    
    def _tasks_file_path(self):
        return f"{self.root_folder()}/projects/in_progress{(self.index or '')}.json"
    
    def _check_task(self, task, days_before=0, **_):
        check_date = date.today() + timedelta(days=days_before)
        return task['date'] == check_date.strftime('%Y-%m-%d')

    def _builder(self):
        tasks = json.load(open(self._tasks_file_path(), "rt", encoding="UTF-8"))
        task_extractor = TaskExtractor(tasks=tasks, check=self._check_task)
        builder = PostBuilder(
            message_builder=CachedContentBuilder(
                task_builder=task_extractor,
                path_constructor=self._path_constructor,
                force_rebuild=self.force_rebuild,
                builder=ContentBuilder(
                    generator=self._message_generator(), 
                    prompt_builder=TaskPromptBuilder(
                            task_builder=task_extractor,
                            prompt_constructor=self._message_prompt_constructor
                        )
                    ),
                cache=FileCache(root_folder=self._data_folder(), is_binary=False),
                filename=f"text"
            ),
            media_builder=CachedContentBuilder(
                task_builder=task_extractor,
                path_constructor=self._path_constructor,
                force_rebuild=self.force_rebuild,
                builder=ContentBuilder(
                    generator=self._image_generator(),
                    prompt_builder=TaskPromptBuilder(
                            task_builder=task_extractor,
                            prompt_constructor=self._image_prompt_constructor
                        )
                    ),
                cache=FileCache(root_folder=self._data_folder()),
                filename=f"image"
            )
        )
        return builder
    
class CommonBlogger(SimpleBlogger):
    def __init__(self, posters, force_rebuild=False):
        super().__init__(posters=posters, force_rebuild=force_rebuild)
        
    def _image_prompt_prompt_builder(self, task):
        return f"Напиши промпт для генерации изображения на тему '{task['topic']}' из области '{task['category']}'"
    
    def _image_prompt_generator(self):
        return YandexTextGenerator(system_prompt=self._system_prompt())
    
    def _builder(self):
        tasks = json.load(open(self._tasks_file_path(), "rt", encoding="UTF-8"))
        task_extractor = TaskExtractor(tasks=tasks, check=self._check_task)
        builder = PostBuilder(
            message_builder=CachedContentBuilder(
                path_constructor=self._path_constructor,
                builder=ContentBuilder(
                    generator=self._message_generator(), 
                    prompt_builder=TaskPromptBuilder(
                            task_builder=task_extractor,
                            prompt_constructor=self._message_prompt_constructor
                        )
                ),
                force_rebuild=self.force_rebuild,
                cache=FileCache(root_folder=self._data_folder(), is_binary=False),
                filename="text"
            ),
            media_builder=CachedContentBuilder(
                path_constructor=self._path_constructor,
                builder=ContentBuilder(
                    generator=self._image_generator(),
                    prompt_builder=ContentBuilderPromptBuilder(
                        content_builder=CachedContentBuilder(
                            task_builder=task_extractor,
                            path_constructor=self._path_constructor,
                            builder=ContentBuilder(
                                generator=self._image_prompt_generator(), 
                                prompt_builder=TaskPromptBuilder(
                                    task_builder=task_extractor,
                                    prompt_constructor=self._image_prompt_prompt_builder
                                )),
                            force_rebuild=self.force_rebuild,
                            filename="image_prompt",
                            cache=FileCache(root_folder=self._data_folder(), is_binary=False)
                        )
                    )
                ),
                force_rebuild=self.force_rebuild,
                cache=FileCache(root_folder=self._data_folder()),
                filename="image"
            )
        )
        return builder
    
    

    