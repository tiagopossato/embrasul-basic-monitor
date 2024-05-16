import configparser

class Slave:
    def __init__(self,_id, _get_interval):
        self.node = int(_id)
        self.get_interval = float(_get_interval)
        self.last_read = 0
    def __str__(self):
        return f'{{"node":{self.node}, "get_interval":{self.get_interval}, "last_read":{self.last_read}}}'


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    serial_port = dict(config.items('serial'))
    database_local = dict(config.items('database.local'))
    return {'serial_port': serial_port, 'database_local': database_local}

if __name__ == '__main__':
    print(read_config())