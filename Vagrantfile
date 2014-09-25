# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"


# -w /cip test:latest

Vagrant.configure("2") do |config|
  IMAGE_NAME = "cip"
  IMAGE_DIR = "/cip"
  RUN_ARGS = "-p 5000:5000 -e CIP_REQ_URL=http://localhost:5000/dummy"
  TEST_CMD = "CIP_FT_CFG=/cip/config/vagrant_config.yaml python /cip/cip/func_tests.py"

  AWS_KEY = ENV.has_key?('AWS_KEY') ? ENV['AWS_KEY'] : 'UNDEFINED'
  AWS_SECRET = ENV.has_key?('AWS_SECRET') ? ENV['AWS_SECRET'] : 'UNDEFINED'
  AWS_KEYPAIR = ENV.has_key?('AWS_KEYPAIR') ? ENV['AWS_KEYPAIR'] : 'UNDEFINED'
  AWS_AMI = ENV.has_key?('AWS_AMI') ? ENV['AWS_AMI'] : 'ami-706acc07'
  AWS_REGION = ENV.has_key?('AWS_REGION') ? ENV['AWS_REGION'] : 'eu-west-1'
  AWS_SG = ENV.has_key?('AWS_SG') ? ENV['AWS_SG'].split(',') : ["ssh"]
  SSH_KEY = ENV.has_key?('SSH_KEY') ? ENV['SSH_KEY'] : "#{ENV['HOME']}/.ssh/id_rsa"

  config.vm.provider :aws do |aws, override|
    aws.access_key_id = AWS_KEY
    aws.secret_access_key = AWS_SECRET
    aws.keypair_name = AWS_KEYPAIR
    aws.region = AWS_REGION
    aws.ami = AWS_AMI
    aws.security_groups = AWS_SG
    aws.tags = {'Name' => 'CIP Docker test'}
    aws.instance_type = 't2.small'
    override.ssh.username = "ubuntu"
    override.ssh.private_key_path = SSH_KEY
    config.vm.box = "aws"
  end

  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
    config.vm.provision "shell", inline: "echo 'DOCKEROPTS=\"--dns 172.22.2.2\"'>>/etc/default/docker"
  end

  config.vm.box = 'ubuntu/trusty64'
  config.vm.synced_folder ".", IMAGE_DIR
  config.vm.provision "docker" do |d|
    d.build_image IMAGE_DIR, args: "-t #{IMAGE_NAME}"
    d.run IMAGE_NAME, args: RUN_ARGS
  end

  config.vm.provision "shell", inline: TEST_CMD
  config.vm.provision "shell", inline: "apt-get install -y s3cmd"
  config.vm.provision "shell", inline: "echo -e \"[default]\\naccess_key=#{AWS_KEY}\\nsecret_key=#{AWS_SECRET}\\n\">~/.s3cfg"
  config.vm.provision "shell", inline: "s3cmd ls|grep -q pvb_docker || s3cmd mb s3://pvb_docker"
  config.vm.provision "shell", inline: "docker export cip > cip.tar"
  config.vm.provision "shell", inline: "s3cmd -q put --multipart-chunk-size-mb=1024 cip.tar s3://pvb_docker"
end