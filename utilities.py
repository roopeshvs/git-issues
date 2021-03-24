"""
utilities.py
contain general utility functions
"""
import os
import sys
import configparser
from subprocess import check_output, DEVNULL
from classes import APIException
import requests
from datetime import datetime
import json
import timeago


def get_config_path():
    if sys.platform == "linux" or sys.platform == "linux2":
        return os.path.join(os.path.expanduser('~'), '.git-issues-credentials')
    elif sys.platform == "win32":
        return os.path.join(os.path.expanduser('~'), 'git-issues-credentials.ini')

def is_logged_in():
    config_file = get_config_path()
    config = configparser.ConfigParser()
    config.read(config_file)
    if 'github-user' in config.sections():
        if config['github-user']['token']:
            return True
    return False

def authenticate():
    if is_logged_in():
        pass
    else:
        print("Use the login command to login first. You will need a Personal Access Token to login.")
        exit()
        
def get_token():
    if is_logged_in():
        config_file = get_config_path()
        config = configparser.ConfigParser()
        config.read(config_file)
        return config['github-user']['token']
    
def get_repo(repo):
    """
    retrieves the repo for a command to work on.
    priority:
    1. --repo option
    2. Environment Variable: GITHUB_PROJECT
    3. git remote of CWD if it is a git repository. 
    """
    if repo:
        repo = repo
    if not repo:
        repo = os.environ.get("GITHUB_PROJECT", None)
    if not repo:
        if check_output(["git", "branch"]) == b"fatal: not a git repository (or any of the parent directories): .git":
            print("No git repository specified. You can specify it in three ways.\n1. with -r option\n2. GITHUB_PROJECT env variable\n3. Run the command in a git repository")
            exit()
        else:
            output = check_output(["git", "remote", "show", "origin"], stderr=DEVNULL).decode('utf=8')
            line = output.split("\n")[1]
            url_split = line.split("/")
            repo = "/".join(url_split[-2:])[:-4]
    return repo