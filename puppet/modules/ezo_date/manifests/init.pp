class ezo_date() {
    $doc_root = '/home/web/ezo-date.ru'
    $site_name = 'ezo-date.ru'
    $bind = "localhost:8003"

    git::repo { "${site_name}":
        path   => "${doc_root}",
        source => 'ssh://jenkins@gerrit.sancta.ru:29418/sancta_serv'
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
        command     => "/home/envs/sancta/bin/python ${doc_root}/serv/manage.py run_gunicorn --bind=${bind}",
        autorestart => true,
        startsecs   => 5,
    }
}
