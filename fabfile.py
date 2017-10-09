from fabric.context_managers import cd
from fabric.operations import require, local
from fabric.api import execute, task, sudo, env
import os
import posixpath


if env.ssh_config_path and os.path.isfile(os.path.expanduser(env.ssh_config_path)):
    env.use_ssh_config = True


env.user = 'findwine'
env.project = 'findwine'
env.code_branch = 'master'
env.sudo_user = 'findwine'

ENVIRONMENTS = ('production',)

@task
def _setup_path():
    env.root = posixpath.join(env.home, 'www', env.environment)
    env.hosts = ['ec2-54-229-166-59.eu-west-1.compute.amazonaws.com']
    env.log_dir = posixpath.join(env.home, 'www', env.environment, 'log')
    env.code_root = posixpath.join(env.root, 'code_root')
    env.project_media = posixpath.join(env.code_root, 'media')
    env.virtualenv_root = posixpath.join(env.home, '.virtualenvs', 'findwine')
    env.services = posixpath.join(env.home, 'services')
    env.db = '%s_%s' % (env.project, env.environment)


@task
def update_local():
    # checkout master branch locally
    local('git checkout master')
    # pull remote code changes
    local('git pull origin master')
    # install any new requirements, if necessary
    local('pip install -r requirements/requirements.txt')
    # delete .pyc files (in case anything removed) - commented out for windows support
    # local("find . -name '*.pyc' -delete")
    # migrate database tables if necessary
    local('python manage.py migrate')


@task
def production():
    env.home = "/home/findwine"
    env.environment = 'findwine'
    env.app_port = '9090'
    _setup_path()


@task
def deploy():
    """
    Deploy code to remote host by checking out the latest via git.
    """
    require('root', provided_by=ENVIRONMENTS)
    try:
        execute(update_code)
        execute(update_virtualenv)
        execute(django_stuff)
    finally:
        # hopefully bring the server back to life if anything goes wrong
        execute(services_restart)
        pass


def update_code():
    with cd(env.code_root):
        sudo('git fetch', user=env.sudo_user)
        sudo('git checkout %(code_branch)s' % env, user=env.sudo_user)
        sudo('git reset --hard origin/%(code_branch)s' % env, user=env.sudo_user)
        # remove all .pyc files in the project
        sudo("find . -name '*.pyc' -delete", user=env.sudo_user)


def update_virtualenv():
    """
    Update external dependencies on remote host assumes you've done a code update.
    """
    require('code_root', provided_by=ENVIRONMENTS)
    files = (
        posixpath.join(env.code_root, 'requirements', 'requirements.txt'),
        posixpath.join(env.code_root, 'requirements', 'prod-requirements.txt'),
    )
    for req_file in files:
        cmd = 'source %s/bin/activate && pip install -r %s' % (
            env.virtualenv_root,
            req_file
        )
        sudo(cmd, user=env.sudo_user)


def django_stuff():
    """
    staticfiles, migrate, etc.
    """
    require('code_root', provided_by=ENVIRONMENTS)
    with cd(env.code_root):
        # todo: staticfiles
        # sudo('{}/bin/python manage.py collectstatic --noinput'.format(env.virtualenv_root), user=env.sudo_user)
        sudo('{}/bin/python manage.py migrate'.format(env.virtualenv_root), user=env.sudo_user)
        sudo('{}/bin/python manage.py collectstatic --noinput'.format(env.virtualenv_root), user=env.sudo_user)


def services_restart():
    require('environment', provided_by=ENVIRONMENTS)
    _supervisor_command('stop findwine-django')
    _supervisor_command('start findwine-django')


def _supervisor_command(command):
    require('hosts', provided_by=ENVIRONMENTS)
    sudo('supervisorctl %s' % (command), shell=False, user='root')
