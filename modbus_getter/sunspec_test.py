from time import sleep
from pymodbus.client import ModbusSerialClient as ModbusClient
import logging

from SunSpec import SunSpec
from Embrasul_models import models

from read_config import read_config
from save_data import start_db_session, save_data

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
                    models=models)
    while(True):
        try:
            suns.update(save_data, session)
            sleep(1)
        except Exception as e:
            logging.exception(e)
            sleep(10)
            #tenta novamente
        except KeyboardInterrupt as e:
            logging.exception("Saindo...")
            exit(0)