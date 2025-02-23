import configparser
from logger import logger

class Slave:
    """
    Representa um escravo Modbus.

    Attributes:
        node (int): Identificador do nó escravo.
        get_interval (float): Intervalo (em segundos) para realizar a leitura de dados.
        last_read (int): Timestamp da última leitura realizada (inicialmente 0).
    """
    def __init__(self, _id, _get_interval):
        self.node = int(_id)
        self.get_interval = float(_get_interval)
        self.last_read = 0

    def __str__(self):
        """
        Retorna a representação em string do objeto Slave.
        """
        return f'{{"node":{self.node}, "get_interval":{self.get_interval}, "last_read":{self.last_read}}}'

def read_config():
    """
    Lê o arquivo 'config.ini' e extrai as configurações das seções obrigatórias.
    
    Regras:
    - Deve existir exatamente **uma** das seções: `[serial]` ou `[tcp]`.
    - A seção `[database.local]` é obrigatória.

    Returns:
        dict: Dicionário contendo apenas as configurações presentes.
        None: Se houver erro na configuração (exemplo: ambas ou nenhuma das seções 'serial' e 'tcp' presentes).
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    has_serial = config.has_section('serial')
    has_tcp = config.has_section('tcp')

    # Garantir que apenas uma das seções 'serial' ou 'tcp' esteja presente
    if has_serial and has_tcp:
        logger.error("Erro: As seções [serial] e [tcp] são mutuamente exclusivas. Remova uma delas.")
        return None
    elif not has_serial and not has_tcp:
        logger.error("Erro: Nenhuma configuração de comunicação foi encontrada. Defina [serial] ou [tcp].")
        return None

    # Verificar se a seção de banco de dados está presente
    if not config.has_section('database.local'):
        logger.error("Erro: A seção [database.local] é obrigatória e não foi encontrada.")
        return None

    # Criar o dicionário apenas com as configurações presentes
    config_data = {}

    if has_serial:
        config_data['serial_port'] = dict(config.items('serial'))
    elif has_tcp:
        config_data['tcp_port'] = dict(config.items('tcp'))

    config_data['database_local'] = dict(config.items('database.local'))

    return config_data

if __name__ == '__main__':
    config_data = read_config()
    if config_data is None:
        print("Falha na leitura da configuração.")
    else:
        print(config_data)
