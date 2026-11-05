"""Verifica por SSH a VM configurada pelo playbook.

Execute a partir da raiz do projeto: pytest -v
"""

testinfra_hosts = ["ansible://web?ansible_inventory=inventory.ini"]

TITULO = "Test Infra Lab"
PAGINA = "/var/www/html/index.html"


def test_apache_instalado(host):
    assert host.package("apache2").is_installed


def test_apache_ativo(host):
    assert host.service("apache2").is_running


def test_apache_habilitado(host):
    assert host.service("apache2").is_enabled


def test_porta_http(host):
    assert host.socket("tcp://80").is_listening


def test_pagina_inicial(host):
    pagina = host.file(PAGINA)
    assert pagina.exists
    assert pagina.user == "root"
    assert pagina.mode == 0o644


def test_conteudo_html(host):
    resposta = host.check_output("curl -fsS http://localhost/")
    assert TITULO in resposta
