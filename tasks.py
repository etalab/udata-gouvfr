# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from os.path import join, abspath, dirname

from invoke import run, task

ROOT = abspath(join(dirname(__file__)))
I18N_DOMAIN = 'udata-gouvfr'


def green(text):
    return '\033[1;32m{0}\033[0;m'.format(text)


def red(text):
    return '\033[1;31m{0}\033[0;m'.format(text)


def cyan(text):
    return '\033[1;36m{0}\033[0;m'.format(text)


def lrun(command, *args, **kwargs):
    run('cd {0} && {1}'.format(ROOT, command), *args, **kwargs)


@task
def clean(ctx, bower=False, node=False):
    '''Cleanup all build artifacts'''
    patterns = [
        'build', 'dist', 'cover', 'docs/_build',
        '**/*.pyc', '*.egg-info', '.tox'
    ]
    for pattern in patterns:
        print('Removing {0}'.format(pattern))
        lrun('rm -rf {0}'.format(pattern))


@task
def test(ctx):
    '''Run tests suite'''
    lrun('nosetests --rednose --force-color udata_gouvfr', pty=True)


@task
def cover(ctx):
    '''Run tests suite with coverage'''
    lrun('nosetests --rednose --force-color --with-coverage '
         '--cover-html --cover-package=udata_gouvfr', pty=True)


@task
def qa(ctx):
    '''Run a quality report'''
    lrun('flake8 udata_gouvfr')


@task
def i18n(ctx):
    '''Extract translatable strings'''
    lrun('python setup.py extract_messages')
    lrun('python setup.py update_catalog')


@task
def i18nc(ctx):
    '''Compile translations'''
    print(cyan('Compiling translations'))
    lrun('python setup.py compile_catalog')


@task
def watch(ctx):
    print(red('[deprecated] Please use `inv assets_watch` instead.'))
    assets_watch(ctx)


@task
def assets_watch(ctx):
    '''Build assets on change'''
    lrun('npm run dev', pty=True)


@task
def assets(ctx):
    print(red('[deprecated] Please use `inv assets_build` instead.'))
    assets_build(ctx)


@task
def assets_build(ctx):
    '''Install and compile assets'''
    print(cyan('Building static assets'))
    lrun('npm run build', pty=True)


@task(clean, i18nc, assets_build, default=True)
def dist(ctx, buildno=None):
    '''Package for distribution'''
    perform_dist(buildno)


@task(i18nc)
def pydist(ctx, buildno=None):
    '''Perform python packaging (without compiling assets)'''
    perform_dist(buildno)


def perform_dist(buildno=None):
    print(cyan('Building a distribuable package'))
    cmd = ['python setup.py']
    if buildno:
        cmd.append('egg_info -b {0}'.format(buildno))
    cmd.append('bdist_wheel')
    lrun(' '.join(cmd), pty=True)
