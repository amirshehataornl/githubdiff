# Overview
After creating a Pull Request (PR) in github, the PR can be updated by doing a force push into your local branch. However, github doesn't maintain revisions of the PR. This makes reviewing code changes difficult, as there is no way to know what changed between one revision of the PR to the next.

## Exact Steps
This utility:
* gets the top level difference between local and remote repo for the current branch.
* Creates a patch with the difference.
* Uploads it to an automatically generated repository in the user's github account named: gh_diff_<username>.
* If the -f option is given, then force push the changes in the current git working directory to update the PR.
* Add a comment to the PR in the provided target repository with a link to the patch file.
   * Tag everyone who had commented on the PR to the comment, to notify them of the update

This makes it easier for reviewers to see the changes which the updated PR brings.

# Usage
```
Always execute script from the top of a git repository
usage: gitcommit [-h] [-p PR] [-R REPO] [-d] [-v] [-k] [-f]

options:
  -h, --help            show this help message and exit
  -p PR, --pr PR        Pull Request Number
  -R REPO, --repo REPO  Target Github repository
  -d, --dry-run         Do a dry run
  -v, --verbose         Verbose mode
  -k, --keep            Keep Patch
  -f, --force           Force Push Change
  ```


# TODO
This utility only generates a top level difference between local and remote changes.
It can not create a difference per commit. This can only be done by adding a change-id to the git comment similar to gerrit.

However at present it is better than what exits in github.
