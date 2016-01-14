class aim() {
    $doc_root = '/home/web/aim'
    $site_name = 'aim.sancta.ru'
    $bind = "localhost:8005"

    git::repo { "${site_name}":
        path   => "${doc_root}",
        source => 'ssh://ravall@gerrit.sancta.ru:29418/aim_project'
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
        command     => "/home/envs/sancta/bin/python ${doc_root}/aim/manage.py run_gunicorn --bind=${bind}",
        autorestart => true,
        startsecs   => 5,
    }
}
