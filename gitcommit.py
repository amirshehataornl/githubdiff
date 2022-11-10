#!/usr/bin/env python3

# get the git difference
#   git diff --cached
#    write output in temporary file "tmp.patch"
#    encompass the output in `` to make it look like code in the git hub
#    commit message
# run git commit with the parameters passed in
#   git commit <parameters>
# if the user requests a force push:
#   git push -f -u origin <branch>
# If a PR is provided then assume ofiwg/libfabric unless another one is
# given by the user
#   write a comment into the PR with the diff:
#       gh pr comment <PR> -F /path/to/tmp.patch -R <REPO>
#

import sys, git, yaml, os, argparse, subprocess
from datetime import datetime
from command import Command

ypref = {}
dry_run = False
verbose = False
timeout = 1000
default_commit_msg =                                                          \
"\n# Please enter the commit message for your changes. Lines starting\n"    \
"# with '#' will be ignored, and an empty message aborts the commit.\n"       \
"#\n"                                                                         \
"# On branch %s\n"                                                            \
"#\n"                                                                         \
"# Changes to be committed:\n"                                                \
"%s\n"                                                                        \
"#\n"                                                                         \
"# Untracked files:\n"                                                        \
"%s\n"                                                                        \
"# ------------------------ >8 ------------------------\n"                    \
"# Do not modify or remove the line above.\n"                                 \
"# Everything below it will be ignored.\n"                                    \
"%s\n"

class YamlDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(YamlDumper, self).increase_indent(flow, False)

def git_add_files(repo, files):
    global dry_run
    global verbose

    if len(files) > 0:
        cmd = Command("git add %s" % (" ".join(files)), fake=dry_run, verbose=verbose)
    else:
        files = [ item.a_path for item in repo.index.diff(None) ]
        cmd = Command("git add %s" % (" ".join(files)), fake=dry_run, verbose=verbose)
    rc, output = cmd.exec_cmd()
    if rc:
        print("Failed to add files")
        exit(1)

def git_commit(repo, amend, files, diff):
    global dry_run
    global verbose
    global ypref
    global default_commit_msg

    untracked = repo.untracked_files
    newuntracked = []
    for f in untracked:
        newuntracked.append("#    modified:   " + f)

    concatun = '\n'.join(newuntracked)

    newfiles = []
    for f in files:
        newfiles.append("#    " + f)

    concatf = '\n'.join(newfiles)

    commit_msg_f = os.path.join(ypref['path'], "COMMIT_MSG")
    with open(commit_msg_f, 'w') as f:
        if amend:
            master = repo.head.reference
            f.write(master.commit.message)
        f.write(default_commit_msg % (repo.active_branch.name, concatf, concatun, diff))

    try:
        subprocess.call(ypref['editor']+" "+ commit_msg_f, shell=True)
    except:
        print("Failed to find an editor")
        exit(1)

    with open(commit_msg_f, 'r') as f:
        commit_msg = f.readlines()

    newcommit = []
    for line in commit_msg:
        if '#' in line and ">8" not in line:
            continue
        newcommit.append(line)

    commit_msg = ''.join(newcommit)

    if amend:
        cmd = Command('git commit --amend -v -m "%s"' % (commit_msg),
                       fake=dry_run, verbose=verbose)
    else:
        cmd = Command('git commit -v -m "%s"' % (commit_msg),
                       fake=dry_run, verbose=verbose)
    rc, output = cmd.exec_cmd()
    if rc:
        print("Failed to commit changes")
        exit(1)

def git_force_push(remote, branch):
    global dry_run
    global verbose

    cmd = Command("git push -f -u %s %s" % (remote, branch), fake=dry_run, verbose=verbose)
    rc, output = cmd.exec_cmd()
    if rc:
        print("Failed to commit changes")
        exit(1)

def gh_add_comment(filename, pr, target):
    global dry_run
    global verbose

    cmd = Command("gh pr comment %d -R %s -F %s" %
            (pr, target, filename), fake=dry_run, verbose=verbose)
    rc, output = cmd.exec_cmd()
    if rc:
        print("Failed to add comment to github PR %d" % (pr))
        exit(1)

def print_help(parser):
    print("Always execute script from the top of a git repository")
    parser.print_help()

if __name__ == '__main__':
    # Load Preferences if it exists. Or create one if it doesn't
    path = os.path.dirname(os.path.abspath(__file__))
    pref = os.path.join(path, "gitcommit.pref")
    if not os.path.exists(pref):
        ypref = {'editor': 'vim', 'path': path}
        with open(pref, 'w') as f:
            f.write(yaml.dump(ypref, Dumper=YamlDumper, indent=2, sort_keys=False))
    with open(pref, 'r') as f:
        ypref = yaml.load(f, Loader=yaml.FullLoader)

    argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--amend", help = "amend a git commit",
                        nargs='?', const=1, type=int)
    parser.add_argument("-p", "--pr", help = "Pull Request Number", type=int)
    parser.add_argument("-R", "--repo", help = "Target Github repository",
                        nargs='?', const="ofiwg/libfabric")
    parser.add_argument("-f", "--force", help = "Do a force push", action="store_true")
    parser.add_argument("-d", "--dry-run", help = "Do a dry run", action="store_true")
    parser.add_argument("-v", "--verbose", help = "Verbose mode", action="store_true")
    parser.add_argument("-k", "--keep", help = "Keep Patch", action="store_true")
    #parser.add_argument("-k", "--keep", help = "Keep Patch", nargs='?', const=0, type=int)

    if len(argv) == 0:
        print_help(parser)
        exit()

    args = parser.parse_known_args()

    repo = git.Repo('.git')
    if not repo.is_dirty(untracked_files=True):
        print("GIT repository has no changes")
        exit(1)

    date = datetime.now()
    filename = "%d-%d-%d-%d-%d-%d-%d.patch" % \
        (date.year, date.month, date.day, date.hour,
         date.minute, date.second, date.microsecond)
    diff = repo.git.diff()
    with open(filename, 'w') as f:
        f.write('```')
        f.write(diff)
        f.write('```')
        f.write('\n')

    dry_run = args[0].dry_run
    verbose = args[0].verbose

    if len(args[1]) <= 0:
        files = [ item.a_path for item in repo.index.diff(None) ]
    else:
        files = args[1]

    git_add_files(repo, files)
    git_commit(repo, args[0].amend, files, diff)

    print("=-->", args[0].keep)

    if args[0].force:
        git_force_push(repo.remote().name, repo.active_branch.name)
    else:
        if not args[0].keep:
            os.remove(filename)
        exit(0)

    if args[0].pr == None:
        exit(0)

    gh_add_comment(filename, args[0].pr, args[0].repo)

    if not args[0].keep:
        os.remove(filename)
