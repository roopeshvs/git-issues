"""
issue.py
contains classes, attributes, and methods pertaining to a single issue.
"""
import requests
import json
from pprint import pprint
from colour import COLOR
from datetime import datetime
import timeago
from tabulate import tabulate

class GitHubRepo:
    def __init__(self, repo, token):
        self.owner = repo.split('/')[0]
        self.name = repo.split('/')[1]
        self.issues = []
        issues = self.fetch_issues('all', token)
        for issue in self.parse_issues(issues):               # parse_issues is a generator that returns a dictionary of attributes for every issue
            issue_obj = GitHubIssue(issue)
            self.issues.append(issue_obj)
        
    
    def fetch_issues(self, state, token):
        r = requests.get(f"https://api.github.com/repos/{self.owner}/{self.name}/issues?state={state}", 
                                headers = {"Authorization": f"token {token}"})
        if r.status_code == 200:
            if len(r.json()) == 0:
                print(f"There are no {state if state != 'all' else ''} issues in {self.repo}")    
                exit()
            return r.json()
        else:
            raise APIException(f"Error Fetching API. Status Code: {r.status_code}")
    
    def parse_issues(self, issues):
        for issue in issues:
            number = issue['number']
            title = issue['title']
            body = issue['body']
            labels = [issue['labels'][i]['name'] for i in range(len(issue['labels']))] if len(issue['labels']) > 0 else None
            time_obj = datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            time_diff = datetime.utcnow() - time_obj
            time_str = 'about ' + timeago.format(time_diff)
            assignees = [issue['assignees'][i]['login'] for i in range(len(issue['assignees']))] if len(issue['assignees']) > 0 else None
            author = issue['user']['login']
            state = issue['state']
            yield {'number': number, 'title': title, 'body': body, 'labels': labels, 'time_str' : time_str,
                    'assignees': assignees, 'author': author, 'state': state}
        
    def print_table(self, state):
        table = []
        for issue in self.issues:
            if state == 'all' or issue.state == state:
                table.append(issue.get_table_attrs())
        table = tabulate(table, tablefmt="github")
        print(table)

class GitHubIssue:
    def __init__(self, *args):
        attr = {}
        if args:
            attr = args[0]
        self.number = attr.get('number', None)
        self.title = attr.get('title', None)
        self.body = attr.get('body', None)
        self.labels = attr.get('labels', None)
        self.created = attr.get('time_str', None)
        self.assignees = attr.get('assignees', None)
        self.author = attr.get('author', None)
        self.state = attr.get('state', None)

    def get_table_attrs(self):
        labels = ", ".join([item for item in self.labels]) if self.labels is not None else None
        return [
            f"{COLOR['GREEN']}{self.number}{COLOR['ENDC']}" if self.state == 'open' else f"{COLOR['RED']}{self.number}{COLOR['ENDC']}", 
            self.title, 
            f"{COLOR['BLUE']}{labels}{COLOR['ENDC']}" if self.labels is not None else None,
            self.created
        ]
    
    def create_issue(self, repo, token):
        data = {'title':self.title, 'body': self.body, 'labels': self.labels, 'assignees':self.assignees}
        json_data = json.dumps(data)
        response = requests.post(f"https://api.github.com/repos/{repo}/issues", 
                        headers = {"Authorization": f"token {token}",
                                    "accept": "application/vnd.github.v3+json"},
                        data = json_data
        )
        if response.status_code == 201:
            print(f"Created issue in {repo}\n")
            print(f"{response.json()['html_url']}")
        else:
            print(f"An API error occured in creating issue. Status Code: {response.status_code}")
    
    def close_issue(self, repo, token):
        data = {'state': 'closed'}
        json_data = json.dumps(data)
        response = requests.patch(f"https://api.github.com/repos/{repo}/issues/{self.number}", 
                        headers = {"Authorization": f"token {token}",
                                    "accept": "application/vnd.github.v3+json"},
                        data = json_data
        )
        if response.status_code == 200:
            print(f"Closed issue #{self.number} in {repo}\n")
            print(f"{response.json()['html_url']}")
        else:
            print(f"An API error occured in closing issue. Status Code: {response.status_code}")
    
    def reopen_issue(self, repo, token):
        data = {'state': 'open'}
        json_data = json.dumps(data)
        response = requests.patch(f"https://api.github.com/repos/{repo}/issues/{self.number}", 
                        headers = {"Authorization": f"token {token}",
                                    "accept": "application/vnd.github.v3+json"},
                        data = json_data
        )
        if response.status_code == 200:
            print(f"Reopened issue #{self.number} in {repo}\n")
            print(f"{response.json()['html_url']}")
        else:
            print(f"An API error occured in reopening issue. Status Code: {response.status_code}")
    
    def create_comment(self, body, repo, token):
        data = {'body': body}
        json_data = json.dumps(data)
        response = requests.post(f"https://api.github.com/repos/{repo}/issues/{self.number}/comments", 
                        headers = {"Authorization": f"token {token}",
                                    "accept": "application/vnd.github.v3+json"},
                        data = json_data
        )
        if response.status_code == 201:
            print(f"Added new comment in issue #{self.number} in {repo}\n")
            print(f"{response.json()['html_url']}")
        else:
            print(f"An API error occured in creating comment. Status Code: {response.status_code}")
        
    

class APIException(Exception):
    pass