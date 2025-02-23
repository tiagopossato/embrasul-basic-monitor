from time import sleep
from logger import logger
from create_modbus_client import create_modbus_client
from SunSpec import SunSpec
from Embrasul_models import models

from read_config import read_config
from save_data import start_db_session, save_data

if __name__ == '__main__':
    config = read_config()
    logger.info("Inicializando leitor dos sensores via Modbus...")

    # start the database session
    session = start_db_session()

    # Tenta conectar ao Modbus
    modbus_client = create_modbus_client(config)
    if modbus_client is None:
        logger.error("Encerrando execução devido à falha na conexão Modbus.")
        exit(1)

    if 'serial_port' in config and config['serial_port']:
        slave_id = int(config['serial_port'].get('slave_id'))
    elif 'tcp_port' in config and config['tcp_port']:
        slave_id = int(config['tcp_port'].get('slave_id')) 
    else:
        logger.error("Nenhuma configuração válida de Modbus encontrada (serial ou TCP)")
        slave_id = None

    suns = SunSpec(slave_id=slave_id,
                    modbus_client=modbus_client,
                    models=models)
    while(True):
        try:
            suns.update(save_data, session)
            sleep(1)
        except Exception as e:
            logger.exception(e)
            sleep(10)
            #tenta novamente
        except KeyboardInterrupt as e:
            logger.exception("Saindo...")
            exit(0)