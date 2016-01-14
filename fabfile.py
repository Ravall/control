# -*- coding: utf-8 -*-
from fabric.api import (
    run, task, roles, hide, env, cd, prompt, sudo,
    execute, local, lcd, hosts
)
from time import sleep
from fabric.contrib.files import exists
from fabric.context_managers import settings
from string import Template
from deploy import PROJECTS
from fab.env import env
try:
    import jenkins
except ImportError:
    # не переживаем если jenkins не импортировался
    pass


git_repo = {
    'control': 'ssh://jenkins@gerrit.sancta.ru:29418/control'
}

JENKINS_DEFAULTS = {
    'git_base_url': 'ssh://jenkins@gerrit.sancta.ru:29418',

    'recipients': 'kirillaborin@gmail.com',

    'server_url': 'http://jenkins.sancta.ru/',

    # Отдельный пользователь, создающий задачи
    'job_creator_name': 'control',
    'job_creator_pass': 'control12345',

    # Должен ли создаваться tag как первый шаг процесса автоматической
    # выкладки. Возможные значения: tag, dont_tag
    'tag_policy': 'tag',

    'validate_command': 'make integrate',

    'disable_jenkins_submodules': 'false',

    # Ветка, коммиты в которую считаются релиз-кандидатами и запускают
    # весь deployment pipeline.
    'branch': 'master',

    # Путь относительно рабочей папки задачи в Jenkins, куда нужно
    # извлекать код. Должен совпадать с путем относительно домашней
    # папки того пользователя, где это будет выкладываться на бою.
    'repo_dir': 'repo',

    'dont_deploy': False,
}


JENKINS_PROJECTS_METADATA = {
    'control': {
        'repo_dir': 'control',
    },
    'aim_project': {
        'repo_dir': 'aim_project',
    },
}

def jenkins_job_from_template(job_name, template_name, template_data):

    def get_contents(filename):
        with open(filename, 'r') as filehandle:
            return filehandle.read()

    template = Template(get_contents('jenkins-jobs/{0}.xml'.format(template_name)))
    config_xml = template.substitute(template_data)
    j = jenkins.Jenkins(
        JENKINS_DEFAULTS['server_url'],
        JENKINS_DEFAULTS['job_creator_name'],
        JENKINS_DEFAULTS['job_creator_pass']
    )
    if not j.job_exists(job_name):
        j.create_job(job_name, config_xml)


def jenkins_jobs():
    for project_name, options in JENKINS_PROJECTS_METADATA.items():
        template_data = JENKINS_DEFAULTS.copy()

        template_data['project_name'] = project_name
        template_data['gerrit_project'] = project_name

        template_data.update(options)

        jenkins_job_from_template(
            'gerrit-{0}'.format(project_name),
            'gerrit',
            template_data
        )


@roles('digitalocean')
def puppet_init():
    '''
    Установка puppet. Выполнять один раз на чистом сервере
    '''
    run("apt-get -y install puppet puppetmaster")
    run("apt-get -y install git")
    run('rm -rf /home/control')
    if not exists('/home/control'):
        '''
        в каталоге /home/control храним control
        '''
        run('mkdir /home/control')
        with cd('/home/control'):
            run('git clone {0} .'.format(git_repo['control']))




@roles('digitalocean')
def deploy(project, version, **kwargs):
    '''
    выкладка проекта.
    '''
    with settings(deployed_project=project):
        try:
            execute(PROJECTS[project], version, **kwargs)
        except KeyError:
            print 'ERROR: Unknown project. Projects:{0}'.format(
                PROJECTS.keys()
            )


def deploy_old(project=None, tag=None):
    if not tag or not project:
        print "требуются параметры"
    print "выкладываем тег {0}".format(tag)
    with cd('/home/web/django_admin'):
        with prefix(env.activate):
            run("git fetch")
            run("git remote prune origin")
            run("git checkout {0}".format(tag))
            run("git submodule update --init")
            run("cat release")
            run("pip install -r control/pip.freeze")
            run("find . -name '*.pyc' -delete")
            run("python sancta/manage.py syncdb  --settings=config.admin")
            run("python sancta/manage.py syncdb  --settings=config.admin --database=sancta_db")
            run("python sancta/manage.py migrate --settings=config.admin --merge --database='sancta_db'")
            run("python sancta/manage.py collectstatic  --settings=config.admin --noinput")
            run("python sancta/manage.py collectstatic  --settings=config.api --noinput")
            restart()


def deploy_engdel(tag=None):
    if not tag:
        print "для выкладки нужен тег"
    print "выкладываем тег {0}".format(tag)
    with cd('/home/web/engdel.ru'):
        with prefix(env.activate):
            run("git fetch")
            run("git remote prune origin")
            run("git checkout {0}".format(tag))
            run("git submodule update --init")
            run("pip install -r control/pip.freeze")
            run("find . -name '*.pyc' -delete")
            run("python frgn/manage.py syncdb")
            run("python frgn/manage.py migrate --merge")
            run("python frgn/manage.py compass")
            run("python frgn/manage.py collectstatic --noinput")
            restart()


def deploy_engdel(tag=None):
    if not tag:
        print "для выкладки нужен тег"
    print "выкладываем тег {0}".format(tag)
    with cd('/home/web/sancta.ru'):
        with prefix(env.activate):
            run("git fetch")
            run("git remote prune origin")
            run("git checkout {0}".format(tag))
            run("git submodule update --init")
            run("pip install -r control/pip.freeze")
            run("find . -name '*.pyc' -delete")
            run("python frgn/manage.py syncdb")
            run("python frgn/manage.py migrate --merge")
            run("python frgn/manage.py compass")
            run("python frgn/manage.py collectstatic --noinput")


def restart():
    run('service nginx restart')
    # gunicorn
    run('service supervisor stop')
    sleep(10)
    run('service supervisor start')
    #celery
    run('service celeryd stop')
    sleep(1)
    run('service celeryd start')
