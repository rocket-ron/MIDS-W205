Exec { path => [ "/bin/", "/sbin", "/usr/bin", "/usr/sbin" ] }

class system-update {
  exec { 'yum update':
    command => 'yum update -y',
  }
}

class {'::mongodb::globals':
  manage_package_repo => true,
}->
class {'::mongodb::server':
  verbose => true,
  require => Class["system-update"]
}->
class {'::mongodb::client':}

mongodb::db { 'twitter_db':}

include system-update
include mongodb
include stdlib
