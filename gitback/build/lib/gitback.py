#!/usr/bin/env python3
# -*- coding: utf8 -*-

from __future__ import print_function
from getpass import getpass
from argparse import ArgumentParser
from os import chdir, path, makedirs, pardir, environ
from subprocess import call, Popen
from functools import partial
from platform import python_version_tuple
import tarfile
from time import gmtime, strftime
import base64

from github import Github

if python_version_tuple()[0] == u'2':
    input = lambda prompt: raw_input(prompt.encode('utf8')).decode('utf8')

__author__ = u'"anuradha.neo@gmail.com"'
__version__ = '1.0'


class GitBack():

    def __init__(self):
        print(u"""
                                                                                          
    _____  _  _ __          __           _           _                                    
  / ____|(_)| |\ \        / /          | |         | |                /\                  
 | |  __  _ | |_\ \  /\  / /___   _ __ | | __ ___  | |__   _   _     /  \    _ __   _   _ 
 | | |_ || || __|\ \/  \/ // _ \ | '__|| |/ // __| | '_ \ | | | |   / /\ \  | '_ \ | | | |
 | |__| || || |_  \  /\  /| (_) || |   |   < \__ \ | |_) || |_| |  / ____ \ | | | || |_| |
  \_____||_| \__|  \/  \/  \___/ |_|   |_|\_\|___/ |_.__/  \__, | /_/    \_\|_| |_| \__,_|
                                                            __/ |                         
                                                           |___/                          
                                                                                          
created by: {__author__}
Version: {__version__}
""".format(__author__=__author__, __version__=__version__))

    def set_args(self):
        """ Create parser for command line arguments """
        parser = ArgumentParser(
                usage=u'python -m gitback \'\nUsername and password will be prompted.',
                description='Clone all your Github repositories.')
        parser.add_argument('-u', '--user', help='Your github username')
        parser.add_argument('-p', '--password', help=u'Github password')
        parser.add_argument('-t', '--token', help=u'Github OAuth token in base64')
        parser.add_argument('-o', '--org', help=u'GitGub Organisation/team. User used by default.')
        parser.add_argument('-d', '--dest', help=u'Destination directory. Created if doesn\'t exist. [curr_dir]')
        parser.add_argument('--nopull', action='store_true', help=u'Don\'t pull if repository exists. [false]')
        parser.add_argument('--shallow', action='store_true', help=u'Perform shallow clone. [false]')
        parser.add_argument('--ssh', action='store_true', help=u'Use ssh+git urls for checkout. [false]')
        parser.add_argument('--noforks', action='store_true', help=u'Skip forked repositories. [false]')
        return parser

    def decodetoken(self, b64token):
        base64_bytes = base64.b64decode(b64token)
        return base64_bytes.decode('ascii')

    def make_github_agent(self, args):
        """ Create github agent to auth """
        if args.token:
            token = self.decodetoken(args.token)
            g = Github(token)
        else:
            user = args.user
            password = args.password
            if not user:
                user = input(u'Username: ')
            if not password:
                password = getpass('Password: ')
            if not args.dest:
                args.dest = input(u'Destination: ')
            g = Github(user, password)
        return g
    
    def make_tarfile(self,args,repopath,repository):
        backuptime = strftime("%Y%m%d", gmtime())
        backuppath = './archives/'+args.org+'/'+backuptime+'/'
        if not path.exists(backuppath):
                makedirs(backuppath)

        tarfile = backuppath+repository+'.tar.gz'

        print(u'Backup {repopath} to {tarfile}...'.format(repopath=repopath,tarfile=tarfile))

        call(['tar', '-czf', tarfile, repopath])

    def clone_main(self):
        """ Clone all repos """
        parser = self.set_args()
        args = parser.parse_args()
        g = self.make_github_agent(args)
        user = g.get_user().login
        # (BadCredentialsException, TwoFactorException, RateLimitExceededException)

        join = path.join
        if args.dest:
            if not path.exists(args.dest):
                makedirs(args.dest)
                print(u'mkdir -p "{}"'.format(args.dest))
            join = partial(path.join, args.dest)

        get_repos = g.get_organization(args.org).get_repos if args.org else g.get_user().get_repos
        for repo in get_repos():
            if args.noforks and repo.fork:
                print(u'Repo "{repo.full_name}" is a fork repo, so skipping...'.format(repo=repo))
            elif not path.exists(join(repo.full_name)):
                clone_url = repo.clone_url
                if args.ssh:
                    clone_url = repo.ssh_url
                if args.shallow:
                    print(u'\nShallow cloning of repo "{repo.full_name}"'.format(repo=repo))
                    call([u'git', u'clone', '--depth=1', clone_url, join(repo.full_name)])
                else:
                    print(u'\nCloning of repo "{repo.full_name}"'.format(repo=repo))
                    call([u'git', u'clone', clone_url, join(repo.full_name)])
                
                self.make_tarfile(args,join(repo.full_name),repo.name)
            elif not args.nopull:
                print(u'\nUpdating repo (delta pull) "{repo.name}"'.format(repo=repo))
                call([u'git', u'pull'], env=dict(environ, GIT_DIR=join(repo.full_name, '.git').encode('utf8')))
                #call([u'git --git-dir=./backup/{repo.full_name}/.git/ --work-tree=./backup/{repo.full_name} pull'.format(repo=repo)])

                self.make_tarfile(args,join(repo.full_name),repo.name)
            else:
                print(u'Already cloned, so skipping repo...\t"{repo.full_name}"'.format(repo=repo))

        print(u'\nSynchronization and backup process finished !')

    
if __name__ == '__main__':
    gitback = GitBack()
    gitback.clone_main()
