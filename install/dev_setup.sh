#!/usr/bin/env bash

# Instala a dependência
sudo apt install python3 python3-pip python3-venv

# vai para a pasta do app
cd ../

# Cria o ambiente virtual
python3 -m venv env

#ativa o venv env|
source env/bin/activate

#install as dependencias
pip install -r install/requirements.txt