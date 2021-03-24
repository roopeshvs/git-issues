import click
import configparser
from .utils import authenticate, get_config_path, get_token, get_repo
from tabulate import tabulate
from .classes import GitHubRepo, GitHubIssue


@click.group()
def cli():
    """
    A command line interface to manage all your git issues at one place
    """
    pass

@cli.command()
@click.option("-t", "--token", help="personal access token unique to you. Requires repo, read:org permissions")
def login(token):
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
@click.option("-r", "--repo", help = "github repository in format username/repo", default=None)
@click.option("-t", "--title", help = "issue title", default=None)
@click.option("-b", "--body", help = "description of the issue", default=None)
@click.option("-l", "--labels", help = "issue labels. add multiple labels by specifying the option again.", default=None, multiple=True)
@click.option("-a", "--assignees", help = "users to assign. add multiple usernames by specifying the option again.", default=None, multiple=True)
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
@click.option("-r", "--repo", help = "github repository in format username/repo", default=None)
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
@click.option("-r", "--repo", help = "github repository in format username/repo", default=None)
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
@click.option("-b", "--body", help = "comment body", default=None)
@click.option("-r", "--repo", help = "github repository in format username/repo", default=None)
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
@click.argument("number", type=int)
@click.option("-r", "--repo", help = "github repository in format username/repo", default=None)
@click.option("-t", "--title", help = "issue title", default=None)
@click.option("-b", "--body", help = "description of the issue", default=None)
@click.option("-s", "--state", help = "state of the issue. can be one of open or closed", type=click.Choice(['open', 'closed'], case_sensitive=False), default=None)
@click.option("-l", "--labels", help = "issue labels. add multiple labels by specifying the option again.", default=None, multiple=True)
@click.option("-a", "--assignees", help="users to assign. add multiple usernames by specifying the option again.", default=None, multiple=True)
def update(number, repo, title, body, state, labels, assignees):
    """
    update an issue on a github repo
    """
    authenticate()
    token = get_token()
    repo = get_repo(repo)
    issue = GitHubIssue({'number':number, 'title':title, 'body':body, 'labels':labels, 'assignees':assignees, 'state':state})
    issue.update_issue(repo, token)

@cli.command()
@click.option("-r", "--repo", help = "github repository in format username/repo", default=None)
@click.option("-s", "--state", help = "state of the issue. can be one of open, closed or all",
                type=click.Choice(['open', 'closed', 'all'], case_sensitive=False), default='open')
@click.option("-a", "--author", help="filter by author", default=None)
def list(repo, state, author):
    """
    list issues of a github repo
    """
    authenticate()
    token = get_token()
    repo = get_repo(repo)
    git_repo = GitHubRepo(repo, token)
    git_repo.print_table(state, author)

@cli.command()
@click.argument("number", type=int)
@click.option("-r", "--repo", help = "github repository in format username/repo", default=None)
@click.option("-l", "--lock-reason", help="reason to lock the issue", 
                type=click.Choice(['off topic', 'too heated', 'resolved', 'spam'], case_sensitive=False), default=None)
def lock(number, repo, lock_reason):
    """
    lock an issue. requires push access.
    must provide one of the reasons for lock
    - off topic, too heated, resolved, spam
    """
    if lock_reason is None:
        lock_reason = click.prompt("A lock reason must be specified. Lock Reason",
                                    type=click.Choice(['off topic', 'too heated', 'resolved', 'spam'], case_sensitive=False))
    authenticate()
    token = get_token()
    repo = get_repo(repo)
    issue = GitHubIssue({'number':number})
    issue.lock_issue(lock_reason, repo, token)


@cli.command()
@click.argument("number", type=int)
@click.option("-r", "--repo", help = "github repository in format username/repo", default=None)
def unlock(number, repo):
    """
    unlock an issue.
    requires push access.
    """
    authenticate()
    token = get_token()
    repo = get_repo(repo)
    issue = GitHubIssue({'number':number})
    issue.unlock_issue(repo, token)

if __name__ == '__main__':
    cli()