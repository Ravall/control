# -*- coding: utf-8 -*-
from time import sleep
from fabric.api import (
    run, task, roles, hide, cd, prompt, sudo,
    execute, local, lcd, prefix
)
from fab.env import env
from fab.const import (
    PATH_CONTROL, PATH_EZODATE, PATH_BESTKARTA, PATH_AIM_PROJECT
)


def reset():
    run('service nginx restart')
    # gunicorn
    run('service supervisor stop')
    sleep(10)
    run('service supervisor start')


def clear_pyc():
    local("find . -name '*.pyc' -delete")


def sancta_serv(tag):
    with cd(PATH_EZODATE):
        run("git fetch")
        run("git remote prune origin")
        run("git checkout {0}".format(tag))
        run("git submodule update --init")
        clear_pyc()
        with prefix(env.activate):
            run("python serv/manage.py compass")
            run("python serv/manage.py collectstatic --noinput")
        reset()


def bestkarta(tag):
    with cd(PATH_BESTKARTA):
        run("git fetch")
        run("git remote prune origin")
        run("git checkout {0}".format(tag))
        run("git submodule update --init")
        clear_pyc()
        with prefix(env.activate):
            run("python manage.py collectstatic --noinput")
        reset()


def control(tag):
    with cd(PATH_CONTROL):
        run("git fetch")
        run("git remote prune origin")
        run("git pull origin master")
        run("git submodule update --init")
        sudo('puppet apply --modulepath=puppet/modules puppet/sancta.pp')
        with prefix(env.activate):
            sudo("pip install -r pip.freeze")
        clear_pyc()


def aim_project(tag):
    with cd(PATH_AIM_PROJECT):
        run("git fetch")
        run("git remote prune origin")
        run("git checkout {0}".format(tag))
        run("git submodule update --init")
        clear_pyc()
        with prefix(env.activate):
            run("python aim/manage.py migrate")
            run("python aim/manage.py compass")
            run("python aim/manage.py collectstatic --noinput")
        reset()
