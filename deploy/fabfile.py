from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random
import os
REPO_URL = 'https://github.com/objectisliper/TDDPython'

'''
:argument PROJECT - folder where project will live
:argument SERVER_NAME - ip or domain of server
:argument SERVER_PORT - port server will listen to
:argument NODE_PORT - port for pm2, server will try listen to
:argument CELERY_QUEUES - QUEUES that celery will be listen to
:argument DAPHNE_PORT - port, that daphne will be listen to
:argument IS_SSL - bool that decide, is need to use ssl certificate.
:argument SSL_LOCAL_PATH - local path to ssl certificate and rsa key
'''


def deploy():
    project = os.getenv('PROJECT', env.host)

    site_folder = f'/home/{env.user}/sites/{project}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder: str):
    if exists(f'{source_folder}/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder: str, site_name: str):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = FALSE")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]')
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.6 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py migrate --noinput')
