# -*- coding: utf-8 -*-
from fabric.api import *

env.activate = 'source /home/envs/admin_sancta/bin/activate'
env.hosts = ['root@78.47.157.221']

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
            run("pip install -r files/pip.freeze")
            run("find . -name '*.pyc' -delete")
            run("python sancta/manage.py syncdb  --settings=config.admin")
            run("python sancta/manage.py syncdb  --settings=config.admin --database=sancta_db")
            run("python sancta/manage.py migrate --settings=config.admin --merge")
            run("python sancta/manage.py collectstatic  --settings=config.admin --noinput")
            run("python sancta/manage.py collectstatic  --settings=config.api --noinput")
            restart()


def restart():
    run('service nginx restart')
    # django_graceful
    run('python sancta/manage.py update --settings=config.admin')
    run('python sancta/manage.py update --settings=config.api')
    #celery
    run('service celeryd stop')
    run('service celeryd start')
