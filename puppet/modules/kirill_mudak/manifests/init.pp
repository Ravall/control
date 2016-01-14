class kirill_mudak {
    $site_name = 'sancta.ru'
    $jenkins_port = 8080

    nginx::resource::vhost { "jenkins.${site_name}":
        proxy    => "http://localhost:${jenkins_port}/"
    }
}