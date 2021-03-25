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
