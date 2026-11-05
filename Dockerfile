# Control Node: container com Ansible, cliente SSH, Pytest e Testinfra.
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Versões fixas deixam o build reproduzível.
RUN pip install --no-cache-dir \
    ansible-core==2.18.6 \
    pytest==8.4.1 \
    pytest-testinfra==10.2.2

# Roda sem root: o container só precisa de SSH para fora.
RUN useradd --create-home --uid 1000 ansible
USER ansible

WORKDIR /workspace
CMD ["bash"]
