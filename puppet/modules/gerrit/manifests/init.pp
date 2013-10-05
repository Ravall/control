class gerrit (
    $download     = 'https://gerrit.googlecode.com/files',
    $warfile      = 'gerrit-2.7-rc1.war',
    $gerrit_tmp   = '/tmp',
    $gerrit_home  = '/home/web/gerrit/'
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
        onlyif  => "test -f ${gerrit_war_file}",
        require => [
            Package["java"],
        ],
    }

    file { 'foldergerrit':
        ensure => "directory",
        path   => "${gerrit_home}",
    }

    exec { "configgerrit":
        path    => "/usr/bin:/usr/sbin:/bin",
        command => "git config -f ${gerrit_home}etc/gerrit.config gerrit.canonicalWebUrl",
        require => [
            File['foldergerrit']
        ],
    }
}
