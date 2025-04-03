from simple_blogger.blogger.SimplestBlogger import SimplestBlogger
from simple_blogger.builder.path import TaskPathBuilder
from simple_blogger.builder import PostBuilder
from simple_blogger.cache.file_system import FileCache
from simple_blogger.builder.prompt import TaskPromptBuilder
from simple_blogger.builder.content import CachedContentBuilder, ContentBuilder
import json

class SimpleBlogger(SimplestBlogger):
    def __init__(self, posters, force_rebuild=False):
        super().__init__(builder=self._builder(), posters=posters, force_rebuild=force_rebuild)

    def _path_builder(self, task):
        return f"{task['category']}/{task['topic']}/{self._topic()}"
    
    def _message_prompt_builder(self, task):
        return f"Напиши пост на тему {task['topic']} из области '{task['category']}', используй не более 100 слов, используй смайлики"
    
    def _image_prompt_builder(self, task):
        return f"Нарисуй рисунок, вдохновленный темой {task['topic']} из области '{task['category']}'"
    
    def _topic(self):
        return 'topic'
    
    def _root_folder(self):
        return './files'

    def _data_folder(self):
        return f"{self._root_folder()}/data"
    
    def _tasks_file_path(self):
        return f"{self._root_folder()}/in_progress.json"

    def _builder(self):
        tasks = json.load(open(self._tasks_file_path(), "rt", encoding="UTF-8"))
        path_builder=TaskPathBuilder(
            tasks=tasks, 
            check=self._check_date, 
            path_builder=self._path_builder
        )
        builder = PostBuilder(
            message_builder=CachedContentBuilder(
                path_builder=path_builder,
                builder=ContentBuilder(
                    generator=self._message_generator(), 
                    prompt_builder=TaskPromptBuilder(
                            tasks=tasks,
                            check=self._check_date,
                            prompt_builder=self._message_prompt_builder
                        )
                    ),
                cache=FileCache(root_folder=self._data_folder(), is_binary=False),
                filename=f"text"
            ),
            media_builder=CachedContentBuilder(
                path_builder=path_builder,
                builder=ContentBuilder(
                    generator=self._image_generator(),
                    prompt_builder=TaskPromptBuilder(
                            tasks=tasks,
                            check=self._check_date,
                            prompt_builder=self._image_prompt_builder
                        )
                    ),
                cache=FileCache(root_folder=self._data_folder()),
                filename=f"image"
            )
        )
        return builder
        