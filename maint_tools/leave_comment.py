from argparse import ArgumentParser
from os import environ
from github import Github, Auth

parser = ArgumentParser()
parser.add_argument("repo")
parser.add_argument("number", type=int)

args = parser.parse_args()

# using an access token
auth = Auth.Token(environ["GITHUB_TOKEN"])

# Public Web Github
g = Github(auth=auth)

repo = g.get_repo(args.repo)
issue = repo.get_issue(args.number)

issue.create_comment("This is a comment")
