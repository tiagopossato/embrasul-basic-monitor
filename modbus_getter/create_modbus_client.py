from pymodbus.client import ModbusSerialClient, ModbusTcpClient
from logger import logger

def create_modbus_client(config):
    """
    Cria e testa a conexão com o cliente Modbus RTU ou TCP.
    Retorna o cliente se a conexão for bem-sucedida, senão retorna None.
    """

    try:
        if 'serial_port' in config and config['serial_port']:
            logger.info("Inicializando cliente Modbus RTU")
            client = ModbusSerialClient(
                method='rtu',
                port=config['serial_port']['port'],
                baudrate=int(config['serial_port']['baudrate']),
                timeout=float(config['serial_port']['timeout']),
                parity='N', 
                stopbits=2, 
                retry_on_empty=2, 
                reconnect_delay=0.5
            )

        elif 'tcp_port' in config and config['tcp_port']:
            logger.info("Inicializando cliente Modbus TCP")
            client = ModbusTcpClient(
                host=config['tcp_port']['host'],
                port=int(config['tcp_port']['port']),
                timeout=float(config['tcp_port']['timeout']),
                retry_on_empty=2, 
                reconnect_delay=0.5
            )

        else:
            logger.error("Nenhuma configuração válida de Modbus encontrada (serial ou TCP)")
            return None

        if not client.connect():
            logger.error("Falha ao conectar no Modbus")
            return None

        return client

    except Exception as e:
        logger.exception("Erro ao criar cliente Modbus: %s", e)
        return None
