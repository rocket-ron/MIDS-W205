Exec { path => [ "/bin/", "/sbin", "/usr/bin", "/usr/sbin" ] }

class system-update {
  exec { 'yum update':
    command => 'yum update -y',
  }
}

class dev-tools {
  exec { 'dev tools':
    command => 'yum groupinstall \"Development Tools\" -y',
    require => Class["system-update"],
  }
}

class install-git {
  exec { 'install git':
    command => 'yum install -y git',
    require => Class['dev-tools'],
  }
}

class epel-release {
  exec { 'epel release':
    command => "yum install -y epel-release",
  }
}

class python-pip {
  exec { 'install pip':
    command => 'yum install -y python-pip',
    require => Class["dev-tools", "epel-release"],
  }
}

class upgrade-pip {
  exec{ 'upgrade pip':
    command => "pip install 'pip>1.5' --upgrade",
    require => Class["python-pip"],
    }
}

class python-modules {
  exec { 'tweepy':
    command => 'pip install tweepy',
    require => Class["upgrade-pip"],
    }
  exec { 'pymongo':
    command => 'pip install pymongo',
    require => Class["upgrade-pip"],
  }
}

class {'::mongodb::globals':
  manage_package_repo => true,
}->
class {'::mongodb::server':
  verbose => true,
  bind_ip => ['0.0.0.0'],
  require => Class["system-update"],
}->
class {'::mongodb::client':}

mongodb_database { twitter_db:
  ensure => present,
  tries => 10,
  require => Class['mongodb::server'],
}

class user-creation {
  user { "rcordell":
    name 	=> 'rcordell',
    ensure 	=> 'present',
    shell	=> '/bin/bash',
    password	=> '685addb7fc7d06ec07b91a611ff351e5',
    managehome => true,
  }
}

mongodb_user { testuser:
  username	=> 'testuser',
  ensure	=> present,
  password_hash	=> mongodb_password('testuser','p@ssw0rd'),
  database	=> twitter_db,
  roles		=> ['readWrite','dbAdmin'],
  tries		=> 10,
  require	=> Class['mongodb::server'],
}

include install-git
include epel-release
include dev-tools
include python-pip
include system-update
include python-modules
include upgrade-pip
include stdlib
include user-creation
