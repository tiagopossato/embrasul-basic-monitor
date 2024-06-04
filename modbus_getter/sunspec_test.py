from time import sleep
from time import time
from pymodbus.client import ModbusSerialClient as ModbusClient
import logging
import struct

from read_config import read_config
from save_data import start_db_session, save_data
from SunSpec import *

voltage_model = Model(id=1, start_address=68, update_interval=2,
    group = PointGroup(id="1", name="Tensão", label="Valores de tensão", 
    points = [
        Point(id='UrmsA', size=2, label='Tensão A', description='Tensão RMS na fase A',  pt_type=point_type.float32, units="V"),
        Point(id='UrmsB', size=2, label='Tensão B', description='Tensão RMS na fase B',  pt_type=point_type.float32, units="V"),
        Point(id='UrmsC', size=2, label='Tensão C', description='Tensão RMS na fase C',  pt_type=point_type.float32, units="V"),
    ]))

frequency_model = Model(id=2, start_address=66, update_interval=10,
    group = PointGroup(id="2", name="Frequência", label="Frequência da rede", 
    points = [
        Point(id='FreqA', size=2, label='Frequência A', description='Frequência na fase A',  pt_type=point_type.float32, units="Hz"),
    ]))

current_model = Model(id=3, start_address=74, update_interval=10,
    group = PointGroup(id="1", name="Corrente", label="Valores de corrente", 
    points = [
        Point(id='IrmsA', size=2, label='Corrente A', description='Corrente na fase A',  pt_type=point_type.float32, units="A"),
        Point(id='IrmsB', size=2, label='Corrente B', description='Corrente na fase B',  pt_type=point_type.float32, units="A"),
        Point(id='IrmsC', size=2, label='Corrente C', description='Corrente na fase C',  pt_type=point_type.float32, units="A"),
    ]))

active_power_model = Model(id=4, start_address=80, update_interval=10,
    group = PointGroup(id="1", name="Potência ativa", label="Potência ativa", 
    points = [
        Point(id='PotAtivA', size=2, label='Potência ativa A', description='Potência ativa na fase A',  pt_type=point_type.float32, units="W"),
        Point(id='PotAtivB', size=2, label='Potência ativa B', description='Potência ativa na fase B',  pt_type=point_type.float32, units="W"),
        Point(id='PotAtivC', size=2, label='Potência ativa C', description='Potência ativa na fase C',  pt_type=point_type.float32, units="W"),
        Point(id='PotAtivT', size=2, label='Potência ativa Total', description='Potência ativa Total',  pt_type=point_type.float32, units="W"),
    ]))

if __name__ == '__main__':
    config = read_config()
    logging.info("Inicializando leitor dos sensores via Modbus")

    # start the database session
    session = start_db_session()

    modbus_client = ModbusClient(method='rtu', port=config['serial_port']['port'], 
                          baudrate=int(config['serial_port']['baudrate']), 
                          timeout=float(config['serial_port']['timeout']),
                          parity='N', stopbits=2, retry_on_empty=2, reconnect_delay=0.1)
    
    suns = SunSpec(slave_id=int(config['serial_port']['slave_id']),
                    modbus_client=modbus_client,
                    models=[voltage_model, frequency_model, current_model, active_power_model])
    while(True):
        try:
            suns.update()
            sleep(1)
        except Exception as e:
            logging.exception(e)
            sleep(10)
            #tenta novamente
        except KeyboardInterrupt as e:
            logging.exception("Saindo...")
            exit(0)