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

Modify the utility to keep track of changes in all the patches included in the PR in the following manner:

- Get a list of all the patches in the PR
- before force pushing:
    - For each patch generate a difference between the local version and the remote version
    - store the patch locally, following a standardized naming convention
- force push
- Add the difference per patch in the PR comment

## Disadvantges And Solutions
The problem with this approach is it can generate large comments, if the changes are extensive.

It would be better to be able to upload these patches to the PR comment somehow, but it seems like the github CLI doesn't allow for that. It'll have to be done manually, which is an option.

To remedy this disadvantage, don't provided the -p and the -R command line arguments but provide the -k argument. This will keep the patches around. They can be manually added to the PR comment afterwards.

Another solution to this problem is to create a repository in the owner's github account which will hold the patch files. A link to these patch files can be added into the comment. This seems to be the most reasonable approach.

The following command can show the list of commits in the PR in JSON format. This can then be parsed and used in creating a difference between local and remote changes
```
gh pr view <PR> -R <target repo> --json commits
  
Available fields:
  additions
  assignees
  author
  baseRefName
  body
  changedFiles
  closed
  closedAt
  comments
  commits
  createdAt
  deletions
  files
  headRefName
  headRepository
  headRepositoryOwner
  id
  isCrossRepository
  isDraft
  labels
  maintainerCanModify
  mergeCommit
  mergeStateStatus
  mergeable
  mergedAt
  mergedBy
  milestone
  number
  potentialMergeCommit
  projectCards
  reactionGroups
  reviewDecision
  reviewRequests
  reviews
  state
  statusCheckRollup
  title
  updatedAt
  url
```
The patches will need to be named consistently, such that when the same set of patches are updated, the patches in the github repository will be updated as well. This way we don't have to maintain many files. We can then execute a clean up regularly, which will delete all the patches associated with a specific PR, if the PR has been closed.
