import os
import json
import random
import glob
import telebot
from datetime import date
from datetime import datetime
from datetime import timedelta
from simple_blogger.generators.OpenAIGenerator import OpenAIImageGenerator
from simple_blogger.generators.DeepSeekGenerator import DeepSeekTextGenerator

class CommonBlogger():
    def __init__(self
                 , review_chat_id
                 , production_chat_id=None
                 , first_post_date=datetime.today() + timedelta(days=1)
                 , days_to_review=timedelta(days=1)
                 , days_between_posts=timedelta(days=1)
                 , text_generator=DeepSeekTextGenerator()
                 , image_generator=OpenAIImageGenerator()
                 , topic_word_limit=300
                 , project_name=None
                 , working_dir=None
                 , system_prompt=None
                 , task_converter=None
                 , catagory_folder_getter=None
                 , topic_folder_getter=None
                 , blogger_bot_token_name='BLOGGER_BOT_TOKEN'
                 , shuffle_tasks=True
                 , task_post_processor=None
                 , task_extractor=None
                 , example_task_creator=None
                 , send_text_with_image=False
                 , preprocess_text_prompt=None
                 ):
        self.review_chat_id = review_chat_id
        self.project_name = project_name if project_name is not None else os.path.basename(os.getcwd())
        self.production_chat_id = production_chat_id if production_chat_id is not None else f"@{self.project_name}"
        self.working_dir = working_dir if working_dir is not None else '.'
        self.topic_word_limit = topic_word_limit
        self.files_dir = f"{self.working_dir}/files"
        self.data_dir = f"{self.files_dir}/data"
        self.ideas_dir = f"{self.files_dir}/ideas"
        self.processed_dir = f"{self.files_dir}/processed"
        self.tasks_file = f"{self.files_dir}/in_progress.json"
        self.backlog_file = f"{self.files_dir}/backlog.json"
        self.first_post_date = first_post_date
        self.days_to_review = days_to_review
        self.days_between_posts = days_between_posts
        self.text_generator = text_generator
        self.image_generator = image_generator
        self.example_task_creator = example_task_creator if example_task_creator is not None else self._example_task_creator
        self.task_converter = task_converter if task_converter is not None else self._task_converter
        self.system_prompt = system_prompt if system_prompt is not None else self._system_prompt
        self.catagory_folder_getter = catagory_folder_getter if catagory_folder_getter is not None else self._get_category_folder
        self.topic_folder_getter = topic_folder_getter if topic_folder_getter is not None else self._get_topic_folder
        self.task_post_processor = task_post_processor if task_post_processor is not None else self._task_post_processor
        self.task_extractor = task_extractor if task_extractor is not None else self._task_extractor
        self.preprocess_text_prompt = preprocess_text_prompt if preprocess_text_prompt is not None else self._preprocess_text_prompt
        self.blogger_bot_token_name = blogger_bot_token_name
        self.shuffle_tasks = shuffle_tasks
        self.send_text_with_image = send_text_with_image

    def init_project(self):
        if not os.path.exists(self.files_dir): os.mkdir(self.files_dir)
        if not os.path.exists(self.data_dir): os.mkdir(self.data_dir)
        if not os.path.exists(self.ideas_dir): os.mkdir(self.ideas_dir)
        if not os.path.exists(self.processed_dir): os.mkdir(self.processed_dir)
        self.__init_simple()
        
    def push(self):
        if not os.path.exists(self.tasks_file):
            if os.path.exists(self.backlog_file):
                tasks = json.load(open(self.backlog_file, "rt", encoding="UTF-8"))
                index_start = max(tasks, key=lambda task: task['index'])['index'] + 1
            else:
                tasks = []
                index_start = 1
            for root, _, files in os.walk(self.ideas_dir, ):
                for i, file in enumerate(files):
                    input_file = f"{root}/{file}"
                    data = json.load(open(input_file, "rt", encoding="UTF-8"))
                    for item in data:
                        task = self.task_converter(item)
                        task['index'] = i + index_start
                        tasks.append(task)
                    processed_file = f"{self.processed_dir}/{file}"
                    os.rename(input_file, processed_file)

            if self.shuffle_tasks:
                year = datetime.today().year
                random.seed(year)
                random.shuffle(tasks)

            self.task_post_processor(tasks, self.first_post_date, self.days_between_posts)

            json.dump(tasks, open(self.tasks_file, 'wt', encoding='UTF-8'), indent=4, ensure_ascii=False)
            if os.path.exists(self.backlog_file):
                os.remove(self.backlog_file)

            print(f"{len(tasks)} tasks created")
        else: 
            print("Tasks already exist, revert before push")
    
    def revert(self):
        if os.path.exists(self.tasks_file):
            backlog = []
            in_progress = json.load(open(self.tasks_file, "rt", encoding="UTF-8"))
            for task in in_progress:
                if task['date'] > datetime.today().strftime('%Y-%m-%d'):
                    backlog.append(task)
            json.dump(backlog, open(self.backlog_file, 'wt', encoding='UTF-8'), indent=4, ensure_ascii=False)
            os.remove(self.tasks_file)
            print(f"{len(backlog)} tasks reverted")
        else: 
            print("Nothing to revert")

    def __init_task_dir(self, task):
        folder_name = glob.escape(f"{self.data_dir}/{self.catagory_folder_getter(task).replace('/', ',')}")
        if not os.path.exists(folder_name): os.mkdir(folder_name)
        folder_name = glob.escape(f"{folder_name}/{self.topic_folder_getter(task).replace('/', ',')}")
        if not os.path.exists(folder_name): os.mkdir(folder_name)
        return folder_name

    def gen_image(self, task, type='topic', force_regen=False):
        attr_name = f"{type}_image"
        if attr_name in task:
            folder_name = self.__init_task_dir(task)
            image_file_name = f"{folder_name}/{type}.png"
            image_prompt = task[attr_name]
            self.image_generator.gen_content(image_prompt, image_file_name, force_regen=force_regen)
   
    def gen_text(self, task, type='topic', force_regen=False):
        attr_name = f"{type}_prompt"
        if attr_name in task:
            folder_name = self.__init_task_dir(task)
            text_file_name = f"{folder_name}/{type}.txt"
            text_prompt = self.preprocess_text_prompt(task[attr_name])
            self.text_generator.gen_content(self.system_prompt(task), text_prompt, text_file_name, force_regen)

    def review(self, type='topic', force_image_regen=False, force_text_regen=False, index=0):
        self.send(type, image_gen=True, text_gen=True, chat_id=self.review_chat_id, days_offset=self.days_to_review
                  , force_image_regen=force_image_regen, force_text_regen=force_text_regen, index=index)

    def send(self, type='topic', image_gen=False, text_gen=False, chat_id=None, days_offset=None
             , force_image_regen=False, force_text_regen=False, index=0):
        chat_id = chat_id if chat_id is not None else self.production_chat_id
        tasks = json.load(open(self.tasks_file, 'rt', encoding='UTF-8'))
        task = self.task_extractor(tasks, days_offset, index)
        if task is not None:
            try:
                if image_gen: self.gen_image(task, type, force_regen=force_image_regen)
                if text_gen: self.gen_text(task, type, force_regen=force_text_regen)
            except Exception as e:
                self.__send_error(str(e))
            self.__send(task, type, chat_id)

    def __send(self, task, type, chat_id):
        folder_name = self.__init_task_dir(task)
        image_file_name = f"{folder_name}/{type}.png"
        text_file_name = f"{folder_name}/{type}.txt"
        try:
            bot = telebot.TeleBot(os.environ.get(self.blogger_bot_token_name))
            if self.send_text_with_image and os.path.exists(image_file_name) and os.path.exists(text_file_name):
                bot.send_photo(chat_id=chat_id
                               , photo=open(image_file_name, 'rb')
                               , caption=open(text_file_name, 'rt', encoding='UTF-8').read()
                               , parse_mode="Markdown")
            else:
                if os.path.exists(image_file_name):
                    bot.send_photo(chat_id=chat_id
                                   , photo=open(image_file_name, 'rb')
                                   , disable_notification=True)

                if os.path.exists(text_file_name):
                    bot.send_message(chat_id=chat_id
                                     , text=open(text_file_name, 'rt', encoding='UTF-8').read()
                                     , parse_mode="Markdown")
        except Exception as e:
            self.__send_error(str(e))

    def __send_error(self, message):
        bot = telebot.TeleBot(os.environ.get(self.blogger_bot_token_name))
        bot.send_message(chat_id=self.review_chat_id, text=message)

    def __init_simple(self):
        ideas_file = f"{self.ideas_dir}/{self.project_name}.json"
        if not os.path.exists(ideas_file):
            simple_ideas = self.example_task_creator()
            json.dump(simple_ideas, open(ideas_file, 'wt', encoding='UTF-8'), indent=4, ensure_ascii=False)

    def _example_task_creator(self):
        return [ { "topic": "Post topic", "category": "Post Category" } ]

    def _system_prompt(self, _):
        return f'You are a famous blogger with {1_000_000} followers'

    def _task_converter(self, item):
        return { 
                "topic": item['topic'],
                "category": f"{item['category']}",
                "topic_image": f"Draw a picture, inspired by '{item['topic']}' from '{item['category']}'",
                "topic_prompt": f"Write about '{item['topic']}' from '{item['category']}', use less than {self.topic_word_limit} words",
            }
    
    def _get_category_folder(self, task):
        return task['category']
                
    def _get_topic_folder(self, task):
        return task['topic']

    def _task_post_processor(self, tasks, first_post_date, days_between_posts):
        curr_date = first_post_date
        for task in tasks:
            task["date"] = curr_date.strftime("%Y-%m-%d")
            curr_date += days_between_posts

    def _task_extractor(self, tasks, days_offset=None, index=0):
        days_offset = days_offset if days_offset is not None else timedelta(days=0)
        check_date = date.today() + days_offset
        today_tasks = list(filter(lambda task: task["date"] == check_date.strftime('%Y-%m-%d'), tasks))
        return today_tasks[index] if len(today_tasks) > index else None
    
    def _preprocess_text_prompt(self, prompt):
        return prompt
