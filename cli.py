import os
import click
import requests
from pprint import pprint
import configparser
from utilities import authenticate, get_config_path, get_token, is_logged_in, get_repo


@click.group()
def cli():
    pass

@cli.command()
@click.option("-t", "--token", help="personal access token unique to you. Requires repo, read:org permissions")
@click.option("-r", "--repo", help="default repo if no repo is specified in other commands", envvar="GITHUB_PROJECT")
def login(token, repo):
    """git-issues - manage all your issues at one place"""
    config = configparser.ConfigParser()
    config['github-user'] = {'token':token}
    with open(get_config_path(), 'w') as configfile:
        config.write(configfile)


@cli.command()
@click.option("-r", "--repo", default=None)
def list(repo):
    authenticate()
    token = get_token()
    repo = get_repo(repo)
    r = requests.get(f"https://api.github.com/repos/{repo}/issues", headers = {"Authorization": f"token {token}"})
    if str(r.status_code).startswith("2"):
        issues_len = len(r.json())
        if issues_len > 0:
            print(f"Showing {issues_len} Open Issues")
            pprint(r.json())
        else:
            print("No Open Issues Found.")
    else:
        print("An error occurred fetching API from GitHub. Status Code : {r.status_code}")

@cli.command()
@click.option("-r", "--repo", default=None)
def create(repo):
    authenticate()
    token = get_token()
    

if __name__ == '__main__':
    cli()