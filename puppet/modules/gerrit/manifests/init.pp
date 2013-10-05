class gerrit (
    $download     = 'https://gerrit.googlecode.com/files',
    $warfile      = 'gerrit-2.7-rc1.war',
    $gerrit_tmp   = '/tmp',
    $gerrit_home  = '/home/web/gerrit/',
    $gerrit_url   = 'gerrit.sancta.ru'
) {

    $gerrit_war_file = "${gerrit_tmp}/${warfile}"

    package { "java":
        name   => "default-jdk",
        ensure => installed,
    }

    exec { "downloadgerrit":
        path    => "/usr/bin:/usr/sbin:/bin",
        command => "wget -q '${download}/${warfile}' -O ${gerrit_war_file}",
        onlyif  => "test ! -f ${gerrit_war_file}",
        creates => "${gerrit_war_file}",
    }

    exec { "installgerrit":
        path    => "/usr/bin:/usr/sbin:/bin",
        command => "java -jar ${gerrit_war_file} init --batch -d ${gerrit_home}",
        onlyif  => ["test -f ${gerrit_war_file} && ", "test ! -f ${gerrit_home}"],
        require => [
            Package["java"],
        ],
    }

    file { 'foldergerrit':
        ensure => "directory",
        onlyif  => "test ! -f ${gerrit_home}",
        path   => "${gerrit_home}",
    }

    exec { "configgerrit_weburl":
        path    => "/usr/bin:/usr/sbin:/bin",
        command => "git config -f ${gerrit_home}etc/gerrit.config gerrit.canonicalWebUrl http://${gerrit_url}",
        require => [
            File['foldergerrit']
        ],
    }

    exec { "configgerrit_listenUrl":
        path    => "/usr/bin:/usr/sbin:/bin",
        command => "git config -f ${gerrit_home}etc/gerrit.config httpd.listenUrl http://${gerrit_url}",
        require => [
            File['foldergerrit']
        ],
    }

    file {'/etc/init.d/gerrit':
        ensure  => symlink,
        target  => "${gerrit_home}/bin/gerrit.sh",
        onlyif  => "test ! -f /etc/init.d/gerrit",
        require => Exec['installgerrit']
    }

    service { 'gerrit':
        ensure    => running,
        hasstatus => false,
        pattern   => 'GerritCodeReview',
        require   => File['/etc/init.d/gerrit']
    }

}
