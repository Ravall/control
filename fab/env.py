# -*- coding: utf-8 -*-
from fab import const
from fabric.api import (
    run, task, roles, hide, env, cd, prompt, sudo,
    execute, local, lcd
)


env.activate = 'source {0}bin/activate'.format(const.PATH_VIRTUALENV)
env.roledefs = {
    'hetzner': ['root@78.47.157.221'],
    'digitalocean': ['root@162.243.23.252'],
}
