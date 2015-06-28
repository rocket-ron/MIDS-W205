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
  auth	  => true,
  bind_ip => ['0.0.0.0'],
  require => Class["system-update"],
}->
class {'::mongodb::client':}

mongodb::db { 'twitter_db':
  user		=> 'user1',
  password 	=> 'user1',
}

include system-update
include stdlib
