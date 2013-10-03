# -*- coding: utf-8 -*-
from fabric.api import *
from time import sleep
from fabric.contrib.files import exists

env.activate = 'source /home/envs/admin_sancta/bin/activate'
env.roledefs = {
    'hetzner': ['root@78.47.157.221'],
    'digitalocean': ['root@162.243.23.252']
}

git_repo = {
    'control': 'https://github.com/Ravall/control.git'
}


@roles('digitalocean')
def puppet_init():
    '''
    Установка puppet
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
def puppet_update():
    with cd('/home/control'):
        run('git pull origin master')
        with cd('/home/control/puppet'):
            run('puppet apply *')



def deploy(tag=None):
    if not tag:
        print "для выкладки нужен тег"
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
