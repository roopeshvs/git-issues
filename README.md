## GitIssues

Manage all your git issues from the CLI.

Uses [GitHub REST API v3](https://docs.github.com/en/rest) to make the API calls.

### Installation

Install From PyPI

`pip install git-issues`

### How to Use?

#### Login

Login Using Personal Access Token.
If you do not have a Personal Access Token, create one at `https://github.com/settings/tokens`

`git-issues login -t <token>`

If a token is not given during the time of command, a prompt will be issued.

#### List Issues Of A Repository

`git-issues list -r <repo>`

By default, 