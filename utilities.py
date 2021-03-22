import os
import sys
import configparser
from subprocess import check_output


def get_config_path():
    if sys.platform == "linux" or sys.platform == "linux2":
        pass
    elif sys.platform == "win32":
        return os.path.join(os.environ['APPDATA'], 'credentials.ini')

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
        click.echo("Use the login command to login first. You will need a Personal Access Token to login.")
        exit()
        
def get_token():
    if is_logged_in():
        config_file = get_config_path()
        config = configparser.ConfigParser()
        config.read(config_file)
        return config['github-user']['token']
    
def get_repo(repo):
    if repo:
        repo = repo
    if not repo:
        repo = os.environ.get("GITHUB_PROJECT", None)
    if not repo:
        if check_output(["git", "branch"]) != 0:
            print("No git repository specified. You can specify it in three ways.\n1. with -r option\n2. GITHUB_PROJECT env variable\n3. Run the command in a git repository")
            exit()
        else:
            print(check_output(["git", "config", "--get", "remote.origin.url"]))
    return repo
