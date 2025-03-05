import logging
import pytz
from datetime import datetime
from time import time
from pymodbus.exceptions import ConnectionException

tz = pytz.timezone('America/Sao_Paulo')

# List off all create points
PointList = []

class Point:
    def __init__(self, name, base_address, count, update_interval, transformer):
        self._base_address = base_address
        self._count = count
        self._value = None
        self._name = name
        self._transformer = None
        self._datetime = None
        self._update_interval = update_interval
        self._last_update = 0

        if(hasattr(transformer, '__call__')):
            self._transformer = transformer
        else:
            raise Exception("The transformer must be a function.")
        
        PointList.append(self)

    def get_name(self):
        return self._name
        
    def get_value(self):
        return self._value     

    def update_value(self, slave_id, modbus_client):
        if time() - self._last_update < self._update_interval:
            return False
        
        with modbus_client:
            try:
                read = modbus_client.read_holding_registers(address=self._base_address, count=self._count, slave=slave_id)
                if (read.isError()):
                    logging.error(f'Slave id {slave_id}. Point: {self.get_name()}: {read.message}')
                    return False
            except ConnectionException:
                logging.error(f"ConnectionException: Slave id {slave_id}. Point: {self.get_name()}")
                return False
        # return [(read.registers[0] if read.registers[0] < 32769 else read.registers[0]-65535)/100,
        # (read.registers[1] if read.registers[1] < 32769 else read.registers[1]-65535)/100]
        if(hasattr(self._transformer, '__call__')):
            self._value = self._transformer(read.registers)
        else:
            self._value = read.registers
        
        self._datetime = datetime.fromtimestamp(time(), tz)
        self._last_update = time()
        return True
        
    def get_json_value(self):
        if(self.get_value() is None):
            return None
        return f"'datetime':{self._datetime}, 'point':'{self.get_name()}', 'value':{self.get_value():.2f}"