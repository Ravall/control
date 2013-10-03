class gerrit::params {
    $gerrit_java = $::operatingsystem ? {
        /(?i:Debian|Ubuntu|Mint)/ => 'openjdk-6-jdk',
        default                   => 'java-1.6.0-openjdk',
    }
}

class gerrit (
    $gerrit_java = params_lookup('default-jdk'),
) {
    package {
        [ "wget",]:
        ensure => installed;
        "gerrit_java":
            ensure => installed,
            name   => "${gerrit_java}",
    }
}