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
from simple_blogger.senders.TelegramSender import TelegramSender

class CommonBlogger():
    def __init__(self
                 , review_chat_id=None
                 , production_chat_id=None
                 , first_post_date=datetime.today() + timedelta(days=1)
                 , days_to_review=timedelta(days=1)
                 , days_between_posts=timedelta(days=1)
                 , text_generator=DeepSeekTextGenerator()
                 , image_generator=OpenAIImageGenerator()
                 , topic_word_limit=300
                 , project_name=None
                 , blogger_bot_token_name='BLOGGER_BOT_TOKEN'
                 , shuffle_tasks=True
                 , send_text_with_image=False
                 , reviewer=None
                 , senders=None
                 , image_prompt_char_limit=4000
                 , alt_image_count = 1
                 ):
        review_chat_id = os.environ.get('TG_REVIEW_CHANNEL_ID') if review_chat_id is None else review_chat_id
        self.reviewer = TelegramSender(channel_id = review_chat_id
                                       , send_text_with_image=send_text_with_image) if reviewer is None else reviewer
        self.project_name = project_name if project_name is not None else os.path.basename(os.getcwd())
        production_chat_id = production_chat_id if production_chat_id is not None else f"@{self.project_name}"
        self.senders = [ TelegramSender(channel_token_name=blogger_bot_token_name
                                        , channel_id=production_chat_id
                                        , send_text_with_image=send_text_with_image) ] if senders is None else senders
        self.topic_word_limit = topic_word_limit
        self.files_dir = f"./files"
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
        self.shuffle_tasks = shuffle_tasks
        self.image_prompt_char_limit = image_prompt_char_limit
        self.alt_image_count = alt_image_count

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
                        task = self._task_converter(item)
                        task['index'] = i + index_start
                        tasks.append(task)
                    processed_file = f"{self.processed_dir}/{file}"
                    os.rename(input_file, processed_file)

            if self.shuffle_tasks:
                year = datetime.today().year
                random.seed(year)
                random.shuffle(tasks)

            self._task_post_processor(tasks, self.first_post_date, self.days_between_posts)

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
        folder_name = glob.escape(f"{self.data_dir}/{self._get_category_folder(task).replace('/', ',')}")
        if not os.path.exists(folder_name): os.mkdir(folder_name)
        folder_name = glob.escape(f"{folder_name}/{self._get_topic_folder(task).replace('/', ',')}")
        if not os.path.exists(folder_name): os.mkdir(folder_name)
        return folder_name

    def gen_image(self, task, type='topic', force_regen=False):
        attr_name = f"{type}_image"
        folder_name = self.__init_task_dir(task)
        if attr_name in task:
            image_file_name = f"{folder_name}/{type}.png"
            image_prompt = task[attr_name]
            self.image_generator.gen_content(image_prompt, image_file_name, force_regen=force_regen)
        attr_name = f"{type}_image_prompt"
        if attr_name in task:
            image_prompt_file_name = f"{folder_name}/{type}_image_prompt.txt"
            image_prompt = open(image_prompt_file_name, 'rt', encoding='UTF-8').read()
            for i in range(self.alt_image_count):
                image_file_name = f"{folder_name}/{type}_{i+1}.png"
                self.image_generator.gen_content(image_prompt, image_file_name, force_regen=force_regen)
   
    def gen_text(self, task, type='topic', force_regen=False):
        text_suffixes = ['text', 'prompt']
        folder_name = self.__init_task_dir(task)
        for suffix in text_suffixes:
            attr_name = f"{type}_{suffix}"
            if attr_name in task:
                text_file_name = f"{folder_name}/{type}.txt"
                text_prompt = self._preprocess_text_prompt(task[attr_name])
                self.text_generator.gen_content(self._system_prompt(task), text_prompt, text_file_name, force_regen)
        attr_name = f"{type}_image_prompt"
        if attr_name in task:
            text_file_name = f"{folder_name}/{type}_image_prompt.txt"
            text_prompt = self._preprocess_text_prompt(task[attr_name])
            self.text_generator.gen_content(self._system_prompt(task), text_prompt, text_file_name, force_regen)

    def review(self, type='topic', force_image_regen=False, force_text_regen=False, index=0):
        task=self.__prepare(type, image_gen=True, text_gen=True, days_offset=self.days_to_review
                  , force_image_regen=force_image_regen, force_text_regen=force_text_regen, index=index)
        self.__send(task=task,type=type,sender=self.reviewer)

    def send(self, type='topic', image_gen=False, text_gen=False, days_offset=None
             , force_image_regen=False, force_text_regen=False, index=0, **kwargs):
        task=self.__prepare(type=type, image_gen=image_gen, text_gen=text_gen, days_offset=days_offset
             , force_image_regen=force_image_regen, force_text_regen=force_text_regen, index=index)
        for sender in self.senders:
            self.__send(task=task, type=type, sender=sender, **kwargs)

    def __prepare(self, type, image_gen=False, text_gen=False, days_offset=None
                  , force_image_regen=False, force_text_regen=False, index=0):
        tasks = json.load(open(self.tasks_file, 'rt', encoding='UTF-8'))
        task = self._task_extractor(tasks, days_offset=days_offset, index=index)
        if task is not None:
            try:
                if text_gen: self.gen_text(task, type=type, force_regen=force_text_regen)
                if image_gen: self.gen_image(task, type=type, force_regen=force_image_regen)
            except Exception as e:
                self.reviewer.send_error(str(e))
        return task
    
    def __send(self, task, type, sender, **kwargs):
        if task is not None:
            folder_name = self.__init_task_dir(task)
            image_file_name = f"{folder_name}/{type}.png"
            text_file_name = f"{folder_name}/{type}.txt"
            try:
                sender.send(text_file_name, image_file_name, **kwargs)
            except Exception as e:
                self.reviewer.send_error(str(e))

    def __init_simple(self):
        ideas_file = f"{self.ideas_dir}/{self.project_name}.json"
        if not os.path.exists(ideas_file):
            simple_ideas = self._example_task_creator()
            json.dump(simple_ideas, open(ideas_file, 'wt', encoding='UTF-8'), indent=4, ensure_ascii=False)

    def _example_task_creator(self):
        return [ { "topic": "Post topic", "category": "Post Category" } ]

    def _system_prompt(self, _):
        return f'You are a famous blogger with {1_000_000} followers'

    def _task_converter(self, idea):
        return { 
                "topic": idea['topic'],
                "category": f"{idea['category']}",
                "topic_image": f"Draw a picture, inspired by '{idea['topic']}' from '{idea['category']}'",
                "topic_text": f"Write about '{idea['topic']}' from '{idea['category']}', use less than {self.topic_word_limit} words",
                "topic_image_prompt": f"Write a prompt to generate picture about '{idea['topic']}' from '{idea['category']}', use less than {self.image_prompt_char_limit} symbols",
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
