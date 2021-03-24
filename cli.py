import click
import configparser
from utilities import authenticate, get_config_path, get_token, get_repo, parse_issues, fetch_issues
from tabulate import tabulate
from classes import GitHubRepo, GitHubIssue


@click.group()
def cli():
    pass

@cli.command()
@click.option("-t", "--token", help="personal access token unique to you. Requires repo, read:org permissions")
def login(token, repo):
    """
    gets token and stores it in a file only the user can access
    """
    if token is None:
        token = click.prompt("Tip: You can generate your personal access token at https://github.com/settings/tokens\nToken", hide_input=True)
    config = configparser.ConfigParser()
    config['github-user'] = {'token': token}
    with open(get_config_path(), 'w') as configfile:
        config.write(configfile)


@cli.command()
@click.option("-r", "--repo", default=None)
@click.option("-t", "--title", default=None)
@click.option("-b", "--body", default=None)
@click.option("-l", "--labels", default=None, multiple=True)
@click.option("-a", "--assignees", default=None, multiple=True)
def create(repo, title, body, labels, assignees):
    """
    create an issue on a github repo
    """
    authenticate()
    token = get_token()
    repo = get_repo(repo)
    issue = GitHubIssue({'title':title, 'body':body, 'labels':labels, 'assignees':assignees})
    issue.create_issue(repo, token)

    
@cli.command()
@click.argument("number", type=int)
@click.option("-r", "--repo", default=None)
def close(repo, number):
    """
    close an issue on a github repo
    """
    authenticate()
    token = get_token()
    repo = get_repo(repo)
    issue = GitHubIssue({'number':number})
    issue.close_issue(repo, token)


@cli.command()
@click.argument("number", type=int)
@click.option("-r", "--repo", default=None)
def reopen(repo, number):
    """
    reopen an issue on a github repo
    """
    authenticate()
    token = get_token()
    repo = get_repo(repo)
    issue = GitHubIssue({'number':number})
    issue.reopen_issue(repo, token)


@cli.command()
@click.argument("number", type=int)
@click.option("-b", "--body", default=None)
@click.option("-r", "--repo", default=None)
def comment(body, repo, number):
    """
    create a new comment on a github issue
    """
    authenticate()
    token = get_token()
    repo = get_repo(repo)
    issue = GitHubIssue({'number':number})
    issue.create_comment(body, repo, token)


@cli.command()
@click.option("-r", "--repo", default=None)
@click.option("-s", "--state", type=click.Choice(['open', 'closed', 'all'], case_sensitive=False), default='open')
def list(repo, state):
    """
    list issues of a github repo
    """
    authenticate()
    token = get_token()
    repo = get_repo(repo)
    git_repo = GitHubRepo(repo, token)
    git_repo.print_table(state)


if __name__ == '__main__':
    cli()