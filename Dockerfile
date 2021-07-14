# Container base: python 3.6 Alpine Linux
FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y python-dev libpq-dev libssl-dev build-essential git-core libldap2-dev libsasl2-dev libfontconfig1 libxrender1 libfreetype6-dev
# Cria diretório onde vão ficar os fontes
RUN mkdir /code

# Define o diretório de trabalho
WORKDIR /code

# "Copia" arquivo requirements.txt para o diretorio code
ADD requirements.txt /code/

# Executa o pip
RUN pip install -r requirements.txt

# "Copia" os arquivos locais para o diretorio code no container 
ADD . /code/        
