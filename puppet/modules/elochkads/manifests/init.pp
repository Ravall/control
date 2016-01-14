class elochkads() {
    include git

    $doc_root = '/home/web/elochkads.ru'
    $site_name = 'ildus.sancta.ru'

    nginx::vhost { "${site_name}":
        docroot        => $doc_root,
        create_docroot => false,
    }

    git::repo { "${site_name}":
        path   => "${doc_root}",
        source => 'ssh://jenkins@gerrit.sancta.ru:29418/elochkads.ru'
    }
}
