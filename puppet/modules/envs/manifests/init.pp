class envs() {
    # тут служебные примочки - все нужное окружение (программы, скрипты)
    $env_root = '/home/envs/sancta'

    #mysql
    class { "mysql":
        root_password => 'prana',
    }
    include mysql::client

    package { 'libmysqlclient':
        ensure => installed,
        name   => "libmysqlclient-dev",
    }

    #postgresql
    class { 'postgresql':
        puppi    => true,
        debug    => true,
    }
    package { 'postgresql-server-dev':
        ensure => installed,
        name   => "postgresql-server-dev-${postgresql::real_version}",
    }

    # установим питон в системуу
    class { 'python':
        pip        => true,
        dev        => true,
        virtualenv => true,
        gunicorn   => true,
    }

    # вирутальное окружение
    python::virtualenv { "${env_root}":
        ensure       => present,
        systempkgs   => false,
    }

    # фапать, фапать и еще раз фапать
    package { "fabric":
        name   => "fabric",
        ensure => installed,
    }

    # требуется для компаса
    package { "sass":
        name   => "ruby-sass",
        ensure => installed,
    }
    # требуется для компаса
    package { "compass":
        name   => "ruby-compass",
        ensure => installed,
    }


    # nginx - основа!
    class { 'nginx':
        config_file_default_purge => true,
    }
}