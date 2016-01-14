class quqs() {
    $doc_root = '/home/web/quqs'
    $site_name = 'quqs.ru'
    $bind = "localhost:8006"

    git::repo { "${site_name}":
        path   => "${doc_root}",
        source => 'ssh://ravall@gerrit.sancta.ru:29418/quqs'
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
        command     => "/home/envs/sancta/bin/python ${doc_root}/quqs/manage.py run_gunicorn --bind=${bind}",
        autorestart => true,
        startsecs   => 5,
    }
}
