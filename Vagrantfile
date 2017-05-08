required_plugins = %w( vagrant-vbguest )
required_plugins.each do |plugin|
  system "vagrant plugin install #{plugin}" unless Vagrant.has_plugin? plugin
end

Vagrant.configure(2) do |config|
  #16.10
  config.vm.box = "ubuntu/yakkety64"
  config.vm.box_url = "https://cloud-images.ubuntu.com/yakkety/current/yakkety-server-cloudimg-amd64-vagrant.box"

  #16.04
  config.vm.box = "ubuntu/xenial64"
  config.vm.box_url = "https://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-vagrant.box"

  #config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"

  config.vm.provider "virtualbox" do |v|
    v.memory = 4096
    v.cpus = 2

    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  config.vm.define "reefsource" do |web|
    web.vm.network :forwarded_port, guest: 22, host: 2233, id: 'ssh'

    #app via nginx
    web.vm.network :forwarded_port, guest:80, host:80, auto_correct: true
    #app via nginx for https testing
    web.vm.network :forwarded_port, guest:443, host:443, auto_correct: true

    #app directly to django
    web.vm.network :forwarded_port, guest:8000, host:7000, auto_correct: true

    #postgress
    web.vm.network :forwarded_port, guest:5432, host:5432, auto_correct: true

    #rabbitmq
    web.vm.network :forwarded_port, guest:15672, host:15672, auto_correct: true

    #celery flower
    web.vm.network :forwarded_port, guest:5555, host:5555, auto_correct: true

    web.vm.synced_folder ".", "/home/ubuntu/reefsource"

    web.vm.provision :shell, :path => ".vagrant-setup/install.sh", :args => "reefsource"
  end
end
