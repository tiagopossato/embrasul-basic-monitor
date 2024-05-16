#!/usr/bin/env bash
source install_common_functions.sh

user=""

# Verifica se está executando com root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

verifyUser $1


# Instala a dependência
sudo apt install python3 python3-pip python3-venv

# Verifica se já existe uma instalação
if [ -d /opt/monitor ]; then
    if [ -d /opt/monitor/modbus_getter ]; then
        # Remove a instalação anterior
        rm -rf /opt/monitor/modbus_getter
    fi
else
    mkdir /opt/monitor
fi

cp requirements.txt /opt/monitor/requirements.txt

# Copia a pasta do app
cp -r ../modbus_getter /opt/monitor/modbus_getter

cp uninstall.sh /opt/monitor/uninstall.sh


# Verifica se não existe o banco de dados
if [ ! -d /opt/monitor/db ]; then
    # cria pasta do banco de dados
    mkdir /opt/monitor/db
else
    echo ""
    echo "WARNING"
    echo "------The database already exists. Please verify if the migration is necessary------"
    echo ""
fi

# Altera as permissões de acesso à pasta do app
chown -R ${user}:${user} /opt/monitor

# Cria o ambiente virtual
python3 -m venv /opt/monitor/env

#ativa o venv dashEnv
source /opt/monitor/env/bin/activate

#instala as dependencias
pip install -r requirements.txt 

# Copia o arquivo do serviço
cp modbus_getter.service /etc/systemd/system/modbus_getter.service
sed -i 's/#user#/'$user'/g' /etc/systemd/system/modbus_getter.service

printMessage "Atualizando script de inicialização"
chmod 644 /etc/systemd/system/modbus_getter.service

systemctl enable modbus_getter

systemctl restart modbus_getter