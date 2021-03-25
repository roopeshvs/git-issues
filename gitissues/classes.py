"""
classes.py
contains all classes. all api calls happen here.
"""
import requests
import json
from .colour import COLOR
from datetime import datetime
import timeago
from tabulate import tabulate

class Github:
    def __init__(self, token):
        self.token = token
        self.path = None
    
    def request(self, method, path, params = None, data = None):
        url = "https://api.github.com" + path
        if params:
            url += "?"
            for key,value in params.items():
                if value != None:
                    url += f"{key}={value}"

        if data:
            data = json.dumps(data)

        headers = {"Authorization": f"token {self.token}",
                   "accept": "application/vnd.github.v3+json"}

        response = requests.request(method, url, 
                                    headers=headers,
                                    data = data)

        if response.status_code > 299:
            raise APIException(f"An API Exception has occured.\
                                \nStatus Code: {response.status_code}\nResponse: {response.text}")
        elif response.status_code == 204:
            return

        return response.json()

    def get_repo(self, name):
        self.path = f"/repos/{name}"
        data = self.request("GET", self.path)
        return GithubRepo(self, data)
        
        
class GithubRepo:
    def __init__(self, github, data):
        self.data = data
        self.github = github

    def get_issues(self, params=None):
        path = f"{self.github.path}/issues"
        data = self.github.request("GET", path, params = params)
        return [GithubIssue(self.github, d) for d in data]
    
    def create_issue(self, title, body=None, labels=None, assignees=None):
        data = locals()                                         # Get a dictionary of local values. At this point, all arguments of the function.
        del data['self']
        data = {k:v for k,v in data.items() if v is not None}

        path = f"{self.github.path}/issues"
        data = self.github.request("POST", path, data = data)
        return GithubIssue(self.github, data)
        
class GithubIssue:
    def __init__(self, github, data):
        self.github = github
        self.number = data['number']
        self.title = data['title']
        self.body = data['body']
        self.labels = [data['labels'][i]['name'] for i in range(len(data['labels']))] if len(data['labels']) > 0 else None
        time_obj = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        time_diff = datetime.utcnow() - time_obj
        self.created = 'about ' + timeago.format(time_diff)
        self.assignees = [data['assignees'][i]['login'] for i in range(len(data['assignees']))] if len(data['assignees']) > 0 else None
        self.author = data['user']['login']
        self.state = data['state']
        self.html_url = data['html_url']

    def get_table_attrs(self):
        labels = ", ".join([item for item in self.labels]) if self.labels is not None else None
        return [
            f"{COLOR['GREEN']}{self.number}{COLOR['ENDC']}" if self.state == 'open' else f"{COLOR['RED']}{self.number}{COLOR['ENDC']}", 
            self.title, 
            f"{COLOR['BLUE']}{labels}{COLOR['ENDC']}" if self.labels is not None else None,
            self.created
        ]

    def close_issue(self):
        data = {'state': 'closed'}
        path = f"{self.github.path}/issues/{self.number}"
        self.github.request("PATCH", path, data = data)
    
    def reopen_issue(self):
        data = {'state': 'open'}
        path = f"{self.github.path}/issues/{self.number}"
        self.github.request("PATCH", path, data = data)

    def update_issue(self, title, body=None, labels=None, assignees=None, state=None):
        data = locals()
        del data['self']
        data = {k:v for k,v in data.items() if v is not None}

        path = f"{self.github.path}/issues/{self.number}"
        self.github.request("PATCH", path, data = data)
    
    def create_comment(self, body):
        data = {'body': body}
        path = f"{self.github.path}/issues/{self.number}/comments"
        comment = self.github.request("POST", path, data = data)
        return comment
    
    def lock_issue(self, lock_reason):
        data = {'lock_reason': lock_reason}
        path = f"{self.github.path}/issues/{self.number}/lock"
        self.github.request("PUT", path, data = data)

    def unlock_issue(self):
        path = f"{self.github.path}/issues/{self.number}/lock"
        self.github.request("DELETE", path)

class APIException(Exception):
    pass