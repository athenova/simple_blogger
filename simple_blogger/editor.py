import os, json, random, math
from datetime import timedelta, date, datetime

class Editor():
    def __init__(self, root_folder='./files', multiple_projects=False, shuffle_tasks=True):
        self.root_folder=root_folder
        self.data_dir=f"{self.root_folder}/data"
        self.ideas_dir=f"{self.root_folder}/ideas"
        self.backlog_file=f"{self.root_folder}/backlog.json"
        self.projects_dir=f"{self.root_folder}/projects"
        self.tasks_file=f"{self.projects_dir}/in_progress.json"
        self.multiple_projects=multiple_projects
        self.shuffle_tasks=shuffle_tasks

    def init_project(self):
        if not os.path.exists(self.root_folder): os.mkdir(self.root_folder)
        if not os.path.exists(self.data_dir): os.mkdir(self.data_dir)
        if not os.path.exists(self.ideas_dir): os.mkdir(self.ideas_dir)
        if not os.path.exists(self.projects_dir): os.mkdir(self.projects_dir)

    def create_simple(self, first_post_date=None, days_between_posts=1):
        project_tasks=self._load_project_tasks()
        self._shuffle_if_needed(project_tasks=project_tasks)
        self._set_dates(project_tasks=project_tasks, first_post_date=first_post_date, days_between_posts=days_between_posts)
        self._save_tasks(project_tasks=project_tasks)

    def create_auto(self, first_post_date=None, days_between_posts=1):
        project_tasks=self._load_project_tasks()
        self._shuffle_if_needed(project_tasks=project_tasks)
        self._set_days(project_tasks=project_tasks, first_post_date=first_post_date, days_between_posts=days_between_posts)
        self._save_tasks(project_tasks=project_tasks)

    def create_between(self, first_post_date, last_post_date, exclude_weekends=True):
        project_tasks=self._load_project_tasks()
        self._shuffle_if_needed(project_tasks=project_tasks)
        self._set_dates_between(project_tasks, first_post_date, last_post_date, exclude_weekends)
        self._save_tasks(project_tasks=project_tasks)

    def _set_dates_between(self, project_tasks, first_post_date, last_post_date, exclude_weekends):
        first_post_date = datetime.fromordinal(first_post_date.toordinal())
        last_post_date = datetime.fromordinal(last_post_date.toordinal())
        for i, tasks in enumerate(project_tasks):
            curr_date = first_post_date + timedelta(days=math.trunc(i/2))
            d = (last_post_date - curr_date).days / len(tasks)
            days_between_posts = timedelta(days = d)
            for task in tasks:
                if exclude_weekends:
                    if curr_date.weekday() == 6: curr_date += timedelta(days=1)
                    if curr_date.weekday() == 5: curr_date += timedelta(days=-1)
                task["date"] = curr_date.strftime("%Y-%m-%d")
                curr_date += days_between_posts

    def _load_project_tasks(self):
        project_tasks=[]
        tasks=[]
        for root, _, files in os.walk(self.ideas_dir, ):
            for i, file in enumerate(files):
                input_file = f"{root}/{file}"
                data = json.load(open(input_file, "rt", encoding="UTF-8"))
                for idea in data:
                    task = idea
                    task['index'] = i
                    tasks.append(task)
                if self.multiple_projects:
                    project_tasks.append(tasks)
                    tasks=[]
        if not self.multiple_projects:
            project_tasks.append(tasks)
        return project_tasks
    
    def _save_tasks(self, project_tasks):
        for i, tasks in enumerate(project_tasks):
            tasks_file=f"{self.projects_dir}/in_progress{'' if i==0 else i}.json"
            json.dump(tasks, open(tasks_file, 'wt', encoding='UTF-8'), indent=4, ensure_ascii=False)

    def _shuffle_if_needed(self, project_tasks):
        if self.shuffle_tasks:
            year = date.today().year
            for tasks in project_tasks:
                random.seed(year)
                random.shuffle(tasks)

    def _set_dates(self, project_tasks, first_post_date=None, days_between_posts=1):
        first_post_date = first_post_date or date.today()
        days_between_posts = timedelta(days=days_between_posts)
        for tasks in project_tasks:
            curr_date = first_post_date
            for task in tasks:
                task["date"] = curr_date.strftime("%Y-%m-%d")
                curr_date += days_between_posts

    def _set_days(self, project_tasks, days_between_posts=1):
        for tasks in project_tasks:
            day=0
            for task in tasks:
                task["day"] = day
                day += days_between_posts

