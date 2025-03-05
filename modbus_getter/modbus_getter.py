from time import sleep
import os
from logger import logger
from create_modbus_client import create_modbus_client
from SunSpec import SunSpec

from read_config import read_config
from save_data_on_pg import setup_database_engine,get_session_factory, save_data

from Embrasul_models import voltage_model, frequency_model, current_model, active_power_model, pf_model
from Enviromental_models import metereological_model

def print_data(point, session):
    print(f"point: {point.get_value()}")

if __name__ == '__main__':
    config = read_config()
    logger.info("Inicializando leitor dos sensores via Modbus...")

    # start the database session
    # As informações de configuração podem ser obtidas de qualquer fonte.
    # Aqui, estamos usando variáveis de ambiente ou valores padrão.
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "postgres")
    DB_HOST = os.getenv("DB_HOST", "192.168.3.132")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "monitor")

    # # Configura o engine usando a função setup_database_engine
    engine = setup_database_engine(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, echo=False)

    # # Obtém a fábrica de sessões
    Session = get_session_factory(engine)
    #Session = None

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

    # embrasul_controller = SunSpec(slave_id=1,
    #                 modbus_client=modbus_client,
    #                 models=[voltage_model, frequency_model, current_model, active_power_model, pf_model],
    #                 fn_save_data=print_data,
    #                 session_factory=Session)

    sensor = SunSpec(slave_id=100,
                modbus_client=modbus_client,
                models=[metereological_model],
                fn_save_data=save_data,
                session_factory=Session)
    
    while(True):
        try:
            # inserir um parametro da localização do ponto medido
            #embrasul_controller.update()
            sensor.update()

            sleep(1)
        except Exception as e:
            logger.exception(e)
            sleep(10)
            #tenta novamente
        except KeyboardInterrupt as e:
            logger.exception("Saindo...")
            exit(0)