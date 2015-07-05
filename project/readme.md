
#Using Vagrant to setup your MongoDB instances

The vagrant subdirectory under the project directory is set up to make it really easy to spin up a MongoDB instance on a virtual machine either in AWS EC2 or locally on VMWare Fusion or VirtualBox. The Linux instances are nearly the same which means that there's no real configuration difference between the two - if you get something setup and working for one, you'll have it for the other as long as your putting in the settings and modules in the Puppet manifest. But let's start from the beginning...

##Cloning the Project Repository

This will clone the entire project into your local directory. Make sure to specify the recursive option in order to get all the git submodules used for Vagrant.

    git clone --recursive https://github.com/rocket-ron/MIDS-W205.git
(that’s 2 dashes in front of recursive)

and then from the top directory of the project

    git checkout branch project

That’s about it. All local commits will be accumulated, well, locally, until you do a push. To push your local commits to the branch, just do

    git push origin project

##Vagrant and AWS EC2

What I’ve done is to use [Vagrant](https://www.vagrantup.com) to make it trivial to spin up a MongoDB machine from scratch by invoking the command:

    vagrant up

To make this work with your AWS EC2 you need:
- Create an EC2 key pair if you don't already have one
- Modify the Vagrantfile in your local ec2 directory
    + Change the name of the referenced key pair
    + Change the path to the location of the .pem file used for the key pair
    + Change the AWS keys to use your keys

### EC2 Key Pair

From the AWS console navigate to the EC2 section and click on Key Pairs on the left navigation pane. You will see either a list of key pairs that you already have or an empty page. You can use an existing key pair or create a new one as you prefer. When you create a new one you will download the .pem file. I recommend that you place this in your `~/.ssh` directory. If you don't have that directory, create it.

### Get Vagrant

To use Vagrant, [first download it](https://www.vagrantup.com/downloads.html). If you are on Windows you may need to install Ruby, or Iron Ruby - check the VagrantUp.com site for how to install.

### Install the AWS Plugin

Once Vagrant is installed, install the [AWS plugin](https://github.com/mitchellh/vagrant-aws). See the Quick Start instructions on that Github page, but basically you type

    vagrant plugin install vagrant-aws

and it will download the plugin and install it for you. Again, follow the Quick Start instructions to add a “dummy box” for AWS like so:

    vagrant box add dummy https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box

### Edit the Vagrantfile

Now move to the `project/vagrant/ec2` folder and edit the Vagrantfile there. You will see the following:

    Vagrant.configure(2) do |config|

        config.vm.box = "mongo"

        config.vm.provider :aws do |aws, override|
            override.nfs.functional = false
            aws.access_key_id = ""
            aws.secret_access_key = ""
            aws.keypair_name = ""

            #aws.ami = "ami-a7fdfee2"
            aws.ami = "ami-777f9b33"
            aws.region = "us-west-1"
            aws.instance_type = "m4.xlarge"
            override.ssh.username = "ec2-user"
            override.ssh.private_key_path = "/Users/rcordell/ssh/AWS_EC2_VAGRANT.pem"
            aws.security_groups = ['vagrant']

            config.vm.provision :shell, :path => "../puppet/bootstrap/centos_6_x.sh"

            config.vm.provision :puppet do |puppet|
                puppet.manifests_path = "../puppet/manifests"
                puppet.module_path = "../puppet/modules"
                puppet.options = ['--verbose']
            end
        end


Change the lines for `aws.access_key_id`, `aws.secret_access_key`, `aws.keypair_name` to match your AWS information and EC2 key pair.

Change the line `config.vm.box = “mongo”` to `config.vm.box = "dummy.box"`

Change the line `override.ssh.private_key_path` to use the path where you placed the EC2 key pair .pem file (the private key).

You may need to comment out the line for `aws.security_groups` so that a security group is created on the fly. Otherwise, use a security group of your choice.

Save the Vagrantfile.

### vagrant up

From the `project/vagrant/ec2` directory (you should already be there), issue the command

    vagrant up

It will spin up an EC2 machine, set it up with the Python modules, install MongoDB and initialize it with a database called `twitter_db`. Authenticate is not enabled on MongoDB so you don't need a user and password to access it.

To log into the new machine, just

    vagrant ssh

and you’ll log into the machine as the ec2-user. 
- Type `mongo` to start the mongo shell. 
- Type `quit()` to exit the mongo shell. 
- Type `exit` to log out from the EC2 instance

- To shut down the machine type:   `vagrant halt`
- To destroy the machine type:     `vagrant destroy`
- To start it or recreate it       `vagrant up`

## Vagrant and Local Virtual Machine for MongoDB

This is all set up to make it easy to move from a local MongoDB instance to one running in EC2. They will be configured the same and work the same so there are no surprises or forgotten installations or settings. If you want to make this work on a local virtual machine, you need VMWare, Parallels, or VirtualBox. I have VMWare Fusion because that's what I use at work, but the Vagrant plugin costs $$. VirtualBox is free all around but I can't install VirtualBox and VMWare at the same time, so if you want to set up VirtualBox you'll have to create some stuff - but it's pretty easy, really.

### The Local VM

There’s a `project/vagrant/vmware` directory that will create a local Linux VM and fire it up and turn it into a MongoDB machine. What local Linux VM you may ask? That’s one of the many cool things about Vagrant - there are directories of machines for you to use just by copying them. They are called “boxes”, as in “Windows box” or “Linux box”. You pulled down a “dummy” EC2 box so Vagrant had what it needed to create an EC2 instance. [PuppetLabs](https://atlas.hashicorp.com/puppetlabs). Specifically, I recommend the [CentOS 6.6 box](https://atlas.hashicorp.com/puppetlabs/puppetlabs/centos-6.6-64-puppet-enterprise). You will see choices - two for VMware (Mac or Windows), and one for VirtualBox. Assuming Vagrant is installed, just issue the command as shown and vagrant will download the box (3-4GB). Then you can do `vagrant up` and it will start up. 

### VirtualBox

If you have VMWare and you decide to fork out the $$ for the Vagrant plugin, you're all set. Otherwise install [VirtualBox](https://www.virtualbox.org/wiki/Downloads). 

Create a `virtualbox` directory at the same level as `project/vagrant/ec2` and `project/vagrant/vmware`. From there, execute
    
    vagrant init --provider=virtualbox

Copy the following sections from the WMWare Vagrantfile to your new VirtualBox vagrantfile. 

        config.vm.box = "puppetlabs/centos-6.6-64-puppet"

        config.vm.provision :puppet do |puppet|
            puppet.manifests_path = "../puppet/manifests"
            puppet.module_path = "../puppet/modules"
            puppet.options = ['--verbose']
        end

You should be able to `vagrant up` and see a local Linux VM spin up and be provisioned with MongoDB.

## Twitter Code

My [Twitter search code](https://github.com/rocket-ron/Twitter) is in a public repository to make it easy to dowload. Once a MongoDB machine is created, either on EC2 or locally, you can `vagrant ssh` to the machine to login, enter

    git clone https://github.com/rocket-ron/Twitter.git
    cd Twitter/search
    python search.py "#hashtag" "since date" "until date"

And it will by default pull data from Twitter and store it in the local MongoDB `twitter_db` under the `tweets` collection. To change the collection, say for a different search, edit `tweetFetcher.py`.

