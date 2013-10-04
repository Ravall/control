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
        creates => "${gerrit_war_file}",
        require => [
            Package["wget"],
            File[$gerrit_tmp]
        ],
    }

    #exec {"install_gerrit":
    #    command => "java -jar ${gerrit_war_file} init --batch -d ${gerrit_home}",
    #    require => [
    #        Package["java"],
    #        File[$gerrit_home]
    #    ],
    #}
}
