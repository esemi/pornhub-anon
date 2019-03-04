#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from shutil import copy, rmtree, copytree

from fabric import task

SERVICE_NAME = 'pornanon'

BUILD_FILENAME = 'build.tar.gz'
BUILD_FOLDERS = ['app', 'data']
BUILD_FILES = ['requirements.txt']
LOCAL_APP_PATH = os.path.dirname(__file__)
LOCAL_BUILD_PATH = os.path.join(LOCAL_APP_PATH, 'build')
LOCAL_BUILD_BUNDLE = os.path.join(LOCAL_APP_PATH, BUILD_FILENAME)

REMOTE_HOME_PATH = os.path.join('/home', SERVICE_NAME)
APP_PATH = os.path.join(REMOTE_HOME_PATH, SERVICE_NAME)
DEPLOY_PATH = os.path.join(REMOTE_HOME_PATH, '%s-deploy' % SERVICE_NAME)
BACKUP_PATH = os.path.join(REMOTE_HOME_PATH, '%s-backup' % SERVICE_NAME)
VENV_PATH = os.path.join(REMOTE_HOME_PATH, 'venv')
LOG_PATH = os.path.join(REMOTE_HOME_PATH, 'logs')


@task()
def deploy(c):
    # init remote host
    if not c.run("test -d {}".format(APP_PATH), warn=True):
        c.run('mkdir -p {}'.format(APP_PATH))

    if not c.run("test -d {}".format(VENV_PATH), warn=True):
        c.run("cd {} && python3.7 -m venv {}".format(REMOTE_HOME_PATH, VENV_PATH))
        c.run("cd {} && {}/bin/pip install --upgrade pip".format(REMOTE_HOME_PATH, VENV_PATH))

    if not c.run("test -d {}".format(LOG_PATH), warn=True):
        c.run('mkdir -p {}'.format(LOG_PATH))

    # make local build
    if os.path.exists(LOCAL_BUILD_PATH):
        rmtree(LOCAL_BUILD_PATH)
    os.mkdir(LOCAL_BUILD_PATH)
    for folder in BUILD_FOLDERS:
        copytree(os.path.join(LOCAL_APP_PATH, folder), os.path.join(LOCAL_BUILD_PATH, folder))
    for filename in BUILD_FILES:
        copy(os.path.join(LOCAL_APP_PATH, filename), os.path.join(LOCAL_BUILD_PATH, filename))

    c.local("cd {} && tar -czf {} .".format(LOCAL_BUILD_PATH, LOCAL_BUILD_BUNDLE))
    rmtree(LOCAL_BUILD_PATH)

    # load build
    if not c.run("test -d {}".format(DEPLOY_PATH), warn=True):
        c.run('rm -rf {}'.format(DEPLOY_PATH))
    c.run('mkdir -p {}'.format(DEPLOY_PATH))
    c.put(LOCAL_BUILD_BUNDLE, DEPLOY_PATH)

    c.run('cd {} && tar -xzf {}'.format(DEPLOY_PATH, BUILD_FILENAME))
    c.run('cd {} && {}/bin/pip install -r requirements.txt'.format(DEPLOY_PATH, VENV_PATH))

    # deploy (move build to production)
    if not c.run("test -d {}".format(BACKUP_PATH), warn=True):
        c.run('rm -rf {}'.format(BACKUP_PATH))
    c.run('mv %s %s' % (APP_PATH, BACKUP_PATH))
    c.run('mv %s %s' % (DEPLOY_PATH, APP_PATH))
    c.run('supervisorctl restart %s' % SERVICE_NAME)
