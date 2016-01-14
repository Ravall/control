class bestkarta() {
    $doc_root = '/home/web/bestkarta.ru'
    $site_name = 'bestkarta.ru'
    $bind = "localhost:8004"

    git::repo { "${site_name}":
        path   => "${doc_root}",
        source => 'ssh://jenkins@gerrit.sancta.ru:29418/bestkarta'
    }

    nginx::resource::upstream { "${site_name}":
        ensure  => present,
        members => [$bind,],
    }

    nginx::vhost { "${site_name}":
        template       => 'envs/nginx/django.erb',
        docroot        => $doc_root,
        create_docroot => false,
    }

    include supervisor

    supervisor::service {"${site_name}":
        command     => "/home/envs/sancta/bin/python ${doc_root}/manage.py run_gunicorn --bind=${bind}",
        autorestart => true,
        startsecs   => 5,
    }
}
