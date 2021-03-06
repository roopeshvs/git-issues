## GitIssues

Manage all your git issues from the CLI.

Uses [GitHub REST API v3](https://docs.github.com/en/rest) to make the API calls.

### Installation

Install From PyPI

`pip install gitissues`

### Commands

Commands  |  Description
----------|---------------
close   | close an issue on a github repo
comment | create a new comment on a github issue
create  | create an issue on a github repo
list    | list issues of a github repo
lock    | lock an issue
login   | gets token and stores it in a file only the user can access
reopen  | reopen an issue on a github repo
unlock  | unlock an issue
update  | update an issue on a github repo


Get more help on commands from the command-line with the `--help` option.

This application requires the use of a GitHub Personal Access Token to Authorize.

If you do not have a Personal Access Token, create one at [https://github.com/settings/tokens](https://github.com/settings/tokens)

To login, run the command

`gitissues login -t <token>`

If the repository is not specified as a command option where required, 
looks for a GITHUB_PROJECT environment variable that should contain the repository 
name in the format `username/repo`

If the GITHUB_PROJECT variable name does not exist and if the current working directory
is a github repository, the command takes this as the repository to work on.

### Known Limitations

1. In the current state of Github REST API, it is not possible to delete an issue.

2. GitHub's REST API v3 considers every pull request an issue, but not every issue is a pull request. For this reason, "Issues" endpoints may return both issues and pull requests in the response. Pull requests can be identified by the pull_request key in response. Hence, right now, the number of issues returned varies as the pull requests are removed from the response till a workaround is found.
