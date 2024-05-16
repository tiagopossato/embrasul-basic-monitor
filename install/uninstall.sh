#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

echo "Parando serviço"

systemctl stop modbus_getter.service
systemctl disable modbus_getter.service
rm /etc/systemd/system/modbus_getter.service


echo "removendo pasta"
rm -rf /opt/monitor/app

echo "Concluído"