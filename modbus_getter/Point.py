import logging
import pytz
from datetime import datetime
from time import time

tz = pytz.timezone('America/Sao_Paulo')

# List off all create points
PointList = []

class Point:
    def __init__(self, name, base_address, count):
        self.__base_address = base_address
        self.__count = count
        self.__value = None
        self.__name = name
        self.__transformer = None
        self.__datetime = None
        PointList.append(self)

    def get_name(self):
        return self.__name
        
    def get_value(self):
        return self.__value

    def set_transformer(self, transformer):
        if(hasattr(transformer, '__call__')):
            self.__transformer = transformer

    def update_value(self, slave_id, modbus_client):

        with modbus_client:
            read = modbus_client.read_holding_registers(address=self.__base_address, count=self.__count, slave=slave_id)
            if (read.isError()):
                logging.error(f'Slave id {slave_id}. {read.message}')
                return

        # return [(read.registers[0] if read.registers[0] < 32769 else read.registers[0]-65535)/100,
        # (read.registers[1] if read.registers[1] < 32769 else read.registers[1]-65535)/100]
        if(hasattr(self.__transformer, '__call__')):
            self.__value = self.__transformer(read.registers)
        else:
            self.__value = read.registers
        
        self.__datetime = datetime.fromtimestamp(time(), tz)

    def get_json_value(self):
        if(self.get_value() is None):
            return None
        return f"'datetime':{self.__datetime}, 'point':'{self.get_name()}', 'value':{self.get_value():.2f}"