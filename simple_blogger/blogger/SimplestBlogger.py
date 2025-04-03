from simple_blogger.builder import PostBuilder
from simple_blogger.poster import IPoster
from simple_blogger.generator.yandex import YandexTextGenerator, YandexImageGenerator
from datetime import datetime, timedelta

class SimplestBlogger():
    def __init__(self, builder:PostBuilder, posters:list[IPoster], force_rebuild=False):
        self.builder = builder
        self.posters = posters
        self.force_rebuild = force_rebuild

    def post(self, **__):
        post = self.builder.build(force_rebuild=self.force_rebuild)
        for poster in self.posters:
            poster.post(post=post)

    def _check_date(self, task, days_before=0):
        date = datetime.now() - timedelta(days=days_before)
        return task['date'] == date.strftime('%Y-%m-%d')
    
    def _system_prompt(self):
        return 'Ты - известный блоггер с 1000000 подписчиков'

    def _message_generator(self):
        return YandexTextGenerator(system_prompt=self._system_prompt())
    
    def _image_prompt_generator(self):
        return YandexTextGenerator(system_prompt=self._system_prompt())
    
    def _image_generator(self):
        return YandexImageGenerator()
    