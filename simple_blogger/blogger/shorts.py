from simple_blogger.builder import PostBuilder
from simple_blogger.blogger.basic import CommonBlogger
from simple_blogger.generator.video.basic import ImageSequenceGenerator
from simple_blogger.builder.shorts import ShortsBuilder
from simple_blogger.generator.subs import SubsGenerator
from simple_blogger.generator.speech.yandex import YandexSpeechGenerator
from simple_blogger.builder.task import TaskExtractor
from simple_blogger.cache.file_system import FileCache
from simple_blogger.builder.prompt import TaskPromptBuilder, ContentBuilderPromptBuilder
from simple_blogger.builder.content import CachedContentBuilder, ContentBuilder
import json

class DurationConstructor():
    def __init__(self, duration):
        self.duration=duration

    def get_duration(self):
        return self.duration

class ShortsBlogger(CommonBlogger):
    def __init__(self, posters, image_count=5, force_rebuild=False, index=None):
        self.image_count=image_count
        super().__init__(posters=posters, force_rebuild=force_rebuild, index=index)
        
    def _speech_generator(self):
        return YandexSpeechGenerator()
        
    def _builder(self):
        tasks = json.load(open(self._tasks_file_path(), "rt", encoding="UTF-8"))
        task_extractor = TaskExtractor(tasks=tasks, check=self._check_task)
        message_builder = CachedContentBuilder(
                            task_builder=task_extractor,
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
                        )
        audio_builder=CachedContentBuilder(
                            task_builder=task_extractor,
                            path_constructor=self._path_constructor,
                            builder=ContentBuilder(
                                generator=self._speech_generator(), 
                                prompt_builder=ContentBuilderPromptBuilder(content_builder=message_builder)
                            ),
                            force_rebuild=self.force_rebuild,
                            filename="audio",
                            cache=FileCache(root_folder=self._data_folder())
                        )
        duration_constructor=DurationConstructor(22) 
        
        subs_builder=CachedContentBuilder(
                        task_builder=task_extractor,
                        path_constructor=self._path_constructor,
                        builder=ContentBuilder(
                            generator=SubsGenerator(duration_constructor=duration_constructor.get_duration), 
                            prompt_builder=ContentBuilderPromptBuilder(content_builder=message_builder)
                        ),
                        force_rebuild=self.force_rebuild,
                        filename="subs",
                        cache=FileCache(root_folder=self._data_folder(), is_binary=False)                            
                    )        
        image_prompt_builder=ContentBuilderPromptBuilder(
                                content_builder=CachedContentBuilder(
                                    task_builder=task_extractor,
                                    path_constructor=self._path_constructor,
                                    builder=ContentBuilder(
                                        generator=self._image_prompt_generator(), 
                                        prompt_builder=TaskPromptBuilder(
                                            task_builder=task_extractor,
                                            prompt_constructor=self._image_prompt_prompt_constructor
                                        )),
                                    force_rebuild=self.force_rebuild,
                                    filename="image_prompt",
                                    cache=FileCache(root_folder=self._data_folder(), is_binary=False)
                                )
                            )
        video_buidler = CachedContentBuilder(
                            task_builder=task_extractor,
                            path_constructor=self._path_constructor,
                            builder=ContentBuilder(
                                generator=ImageSequenceGenerator(self._image_generator(), duration_constructor=duration_constructor.get_duration, image_count=self.image_count),
                                prompt_builder=image_prompt_builder,
                            ),
                            force_rebuild=self.force_rebuild,
                            cache=FileCache(root_folder=self._data_folder()),
                            filename="video"
                        )
        
        media_buidler = CachedContentBuilder(
                            task_builder=task_extractor,
                            path_constructor=self._path_constructor,
                            builder=ShortsBuilder(audio_builder=audio_builder, subs_builder=subs_builder, video_builder=video_buidler),
                            force_rebuild=self.force_rebuild,
                            cache=FileCache(root_folder=self._data_folder()),
                            filename="media"
                        )

        builder = PostBuilder(
            message_builder=message_builder,
            media_builder=media_buidler
        )
        return builder