#!/usr/bin/env python

import argparse
import os
import sys


def parseRepos(repofile):
    with open(repofile, 'r') as fd:
        return [x.strip() for x in fd.readlines()]
    return None


def ensure_outdir(dirname):
    if not dirname:
        return os.path.curdir
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    if not os.path.exists(dirname):
        return None
    if os.path.isfile(dirname):
        return None
    return dirname



def do_fetch_all_branches(opath):
    os.system('cd "%s" && git branch -r | grep -v \'\->\' | while read remote; do git branch --track "${remote#origin/}" "$remote"; done' % opath)


def do_fetch(opath):
    os.system('cd "%s" && git fetch --all' % (opath))

def do_pull(opath):
    os.system('cd "%s" && git pull --all' % (opath))

def do_fetch_repo(repo, outdir):
    bname = os.path.basename(repo)
    if not bname:
        return False

    opath = os.path.join(outdir, bname)
    if not os.path.exists(opath):
        os.system('git clone "%s" "%s"' % (repo, opath))

    do_fetch_all_branches(opath)
    do_fetch(opath)
    do_pull(opath)

    #else:
    #    os.system('cd "%s" && git pull --all' % (opath))
    #os.path.makedirs(opath)


def do_sync(repofile, outdir):
    if repofile is None:
        return False

    repos = parseRepos(repofile)
    if not repos:
        return False

    odir = ensure_outdir(outdir)
    if odir is None:
        return False

    for repo in repos:
        do_fetch_repo(repo, odir)

    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repos',  help='Repositories list file')
    parser.add_argument('-o', '--output',  help='Output folder')
    parser.add_argument('operation', help='Operation, "sync" or "test"')

    args = parser.parse_args()
    flags = vars(args)
    res = False

    if flags['operation'] == 'sync':
        res = do_sync(flags['repos'], flags['output'])
    elif flags['operation'] == 'test':
        res = do_test(flags['repos'])
    elif flags['operation'] == 'help':
        res = False
    else:
        print('ERROR: Invalid operation: %s' % flags['operation'])
        parser.print_help()
        sys.exit(1)

    if not res:
        parser.print_help()
