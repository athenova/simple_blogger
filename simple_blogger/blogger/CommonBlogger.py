from simple_blogger.blogger.SimpleBlogger import SimpleBlogger
from simple_blogger.builder import PostBuilder
from simple_blogger.builder.content import ContentBuilder, CachedContentBuilder
from simple_blogger.cache.file_system import FileCache
from simple_blogger.builder.path import TaskPathBuilder
from simple_blogger.builder.prompt import TaskPromptBuilder, ContentBuilderPromptBuilder
import json

class CommonBlogger(SimpleBlogger):
    def __init__(self, posters, force_rebuild=False):
        super().__init__(posters=posters, force_rebuild=force_rebuild)
        
    def _image_prompt_prompt_builder(self, task):
        return f"Напиши промпт для генерации изображения по тему '{task['topic']}' из области '{task['category']}'"
    
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
                filename="text"
            ),
            media_builder=CachedContentBuilder(
                path_builder=path_builder,
                builder=ContentBuilder(
                    generator=self._image_generator(),
                    prompt_builder=ContentBuilderPromptBuilder(
                        content_builder=CachedContentBuilder(
                            path_builder=path_builder,
                            builder=ContentBuilder(
                                generator=self._image_prompt_generator(), 
                                prompt_builder=TaskPromptBuilder(
                                    tasks=tasks,
                                    check=self._check_date,
                                    prompt_builder=self._image_prompt_prompt_builder
                                )),
                            filename="image_prompt",
                            cache=FileCache(root_folder=self._data_folder(), is_binary=False)
                        )
                    )
                ),
                cache=FileCache(root_folder=self._data_folder()),
                filename="image"
            )
        )
        return builder
    
    
