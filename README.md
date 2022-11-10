# Overview
After creating a Pull Request (PR) in github, the PR can be updated by doing a force push into your local branch. However, github doesn't maintain revisions of the PR. This makes reviewing code changes difficult, as there is no way to know what changed between one revision of the patch to another.

This utility creates a patch which contains the revision changes before force pushing into the owner's branch. It then adds a comment to the PR containing the generated patch.

This makes it easier for reviewers to see the changes which the updated PR brings.

## Exact Steps
- Generate a patch using "git diff". This will contain the changes to be committed
- "git add" files to be committed
- "git commit" files
- if the -f options is given then force push into the github repo
- If a PR and a target github repository are specified then add a comment to the PR which contains the patch generated in the first step 

# Usage
```
usage: gitcommit.py [-h] [-a] [-f] [-p PR] [-R REPO] [-d] [-v] [-k]

options:
  -h, --help            show this help message and exit
  -a, --amend           amend a git commit
  -f, --force           Do a force push
  -p PR, --pr PR        Pull Request Number
  -R REPO, --repo REPO  Target Github repository
  -d, --dry-run         Do a dry run
  -v, --verbose         Verbose mode
  -k, --keep            Keep Patch
  ```


# TODO
This utility only works for changes to the tip of the patch list.

Modify the utility to keep track of changes in all the patches included in the PR
