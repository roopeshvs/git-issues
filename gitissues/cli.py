import click
import configparser
from .utils import authenticate, get_config_path, get_token, get_repo_name
from tabulate import tabulate
from .classes import Github, GithubIssue


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
    gets token from the user to perform authenticated api calls
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
    repository = get_repo_name(repo)

    g = Github(token)
    repo = g.get_repo(repository)
    issue = repo.create_issue(title=title, body=body, labels=labels, assignees=assignees)
    print(f"Issue #{issue.number} Created Successfully in {repository}\n\n{issue.html_url}")

    
@cli.command()
@click.argument("number", type=int)
@click.option("-r", "--repo", help = "github repository in format username/repo", default=None)
def close(repo, number):
    """
    close an issue on a github repo
    """
    authenticate()
    token = get_token()
    repository = get_repo_name(repo)

    g = Github(token)
    repo = g.get_repo(repository)
    issues = repo.get_issues()
    for issue in issues:
        if issue.number == number:
            issue.close_issue()
            print(f"Issue #{issue.number} Closed Successfully in {repository}\n\n{issue.html_url}")

    if len(issues) == 0:
        print("Please enter a valid issue number")

@cli.command()
@click.argument("number", type=int)
@click.option("-r", "--repo", help = "github repository in format username/repo", default=None)
def reopen(repo, number):
    """
    reopen an issue on a github repo
    """
    authenticate()
    token = get_token()
    repository = get_repo_name(repo)

    g = Github(token)
    repo = g.get_repo(repository)
    issues = repo.get_issues(params={'state':'closed'})
    for issue in issues:
        if issue.number == number:
            issue.reopen_issue()
            print(f"Issue #{issue.number} Reopened Successfully in {repository}\n\n{issue.html_url}")

    if len(issues) == 0:
        print("Please enter a valid issue number")

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
    repository = get_repo_name(repo)

    if body == None:
        body = click.prompt("Issue comment requires a body.\nComment")

    g = Github(token)
    repo = g.get_repo(repository)
    issues = repo.get_issues(params={'state':'all'})
    for issue in issues:
        if issue.number == number:
            comment = issue.create_comment(body=body)
            print(f"Comment created in issue #{issue.number} in {repository}\n\n{comment['html_url']}")

    if len(issues) == 0:
        print("Please enter a valid issue number")

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
    repository = get_repo_name(repo)
    
    g = Github(token)
    repo = g.get_repo(repository)
    issues = repo.get_issues(params={'state':'all'})
    
    for issue in issues:
        if issue.number == number:
            issue.update_issue(title=title, body=body, labels=labels, assignees=assignees, state=state)
            print(f"Issue #{issue.number} updated successfully in {repository}\n\n{issue.html_url}")
    
    if len(issues) == 0:
        print("Please enter a valid issue number")

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
    repository = get_repo_name(repo)

    g = Github(token)
    repo = g.get_repo(repository)
    table = []
    issues = repo.get_issues(params={'state':state, 'creator':author})

    for issue in issues:
        table.append(issue.get_table_attrs())

    if len(issues) == 0:
        print(f"No {'open' if state == 'all' else ''} issues found in {repository}.")
    print(tabulate(table))

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
    repository = get_repo_name(repo)

    g = Github(token)
    repo = g.get_repo(repository)
    issues = repo.get_issues(params={'state':'all'})

    for issue in issues:
        if issue.number == number:
            issue.lock_issue(lock_reason=lock_reason)
            print(f"Issue #{issue.number} Locked in {repository}")

    if len(issues) == 0:
        print("Please enter a valid issue number")

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
    repository = get_repo_name(repo)

    g = Github(token)
    repo = g.get_repo(repository)
    issues = repo.get_issues(params={'state':'all'})

    for issue in issues:
        if issue.number == number:
            issue.unlock_issue()
            print(f"Issue #{issue.number} unlocked in {repository}")
    
    if len(issues) == 0:
        print("Please enter a valid issue number")

if __name__ == '__main__':
    cli()