# test-infra_lab

Laboratório de infraestrutura como código. Um container Docker com Ansible (Control Node) configura por SSH uma VM Ubuntu criada pelo Vagrant (Managed Node). O Testinfra verifica o resultado.

```
Host (Vagrant + VirtualBox + Docker)
├── Container: Ansible, Pytest, Testinfra
│     └── SSH -> host.docker.internal:2222
└── VM Ubuntu: Apache
      ├── porta 22 -> host 2222
      └── porta 80 -> host 8080
```

## Pré-requisitos

VirtualBox, Vagrant e Docker. As portas 2222 e 8080 do host precisam estar livres.

## Execução

Os comandos do host funcionam em Bash e PowerShell.

### 1. Criar a VM (host)

```bash
vagrant up
```

### 2. Construir e entrar no container (host)

```bash
docker build -t test-infra-control .
docker run --rm -it --add-host=host.docker.internal:host-gateway -v "${PWD}:/workspace" test-infra-control
```

`--add-host` é necessário no Linux, onde `host.docker.internal` não existe por padrão. No Docker Desktop ele não atrapalha.

### 3. Validar as ferramentas (container)

```bash
python --version
pytest --version
ansible --version
```

### 4. Preparar a conexão SSH (container)

```bash
cp .vagrant/machines/default/virtualbox/private_key /tmp/vagrant_key
chmod 600 /tmp/vagrant_key
getent hosts host.docker.internal
```

### 5. Testar a conexão (container)

```bash
ansible web -i inventory.ini -m ping
```

Deve retornar `"ping": "pong"`.

### 6. Executar o playbook (container)

```bash
ansible-playbook -i inventory.ini playbook.yaml
```

Depois abra <http://localhost:8080> no navegador do host.

### 7. Executar os testes (container)

```bash
pytest -v
```

Os 6 testes devem aparecer como `PASSED`.

## Recriar a VM

```bash
vagrant destroy -f
vagrant up
```

O container não precisa ser reconstruído. Mas a VM nova tem outra chave SSH, então saia do container, entre de novo (passo 2) e repita o passo 4. Sem isso o SSH recusa a conexão, porque a chave da VM mudou.

## Arquivos

| Arquivo | Função |
|---|---|
| `Dockerfile` | Imagem do Control Node, com versões fixas e usuário sem root |
| `Vagrantfile` | VM Ubuntu 22.04 e encaminhamento de portas |
| `inventory.ini` | Como o Ansible chega à VM |
| `playbook.yaml` | Atualiza pacotes, instala e habilita o Apache, cria a página |
| `tests/test_web.py` | Verifica pacote, serviço, porta, arquivo e conteúdo da página |

## Segurança

- A chave privada fica em `.vagrant/`, fora do Git (`.gitignore`) e fora da imagem (`.dockerignore`).
- O container roda sem root.
- A porta 8080 escuta só em `127.0.0.1`.
- A porta 2222 escuta em `0.0.0.0` para o container alcançar a VM, então fica visível na rede local. O acesso exige a chave gerada pelo Vagrant. Rode `vagrant halt` ao terminar.
