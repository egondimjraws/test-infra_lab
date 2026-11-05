# Managed Node: VM Ubuntu Server que recebe as configurações do Ansible.
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.hostname = "web"

  # A VM é configurada pelo Ansible; a pasta compartilhada não é necessária.
  config.vm.synced_folder ".", "/vagrant", disabled: true

  # SSH: VM porta 22 -> host porta 2222.
  # id "ssh" substitui o encaminhamento padrão do Vagrant, que só escuta em
  # 127.0.0.1. Com 0.0.0.0 o container consegue chegar à VM através do host.
  config.vm.network "forwarded_port",
    id: "ssh",
    guest: 22,
    host: 2222,
    host_ip: "0.0.0.0"

  # HTTP: VM porta 80 -> host porta 8080 (acessível só pelo próprio host).
  config.vm.network "forwarded_port",
    guest: 80,
    host: 8080,
    host_ip: "127.0.0.1"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "test-infra-lab"
    vb.memory = 1024
    vb.cpus = 1
    # Evita o arquivo de log do console serial na pasta do projeto.
    vb.customize ["modifyvm", :id, "--uartmode1", "disconnected"]
  end
end
