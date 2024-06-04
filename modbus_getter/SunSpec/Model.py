"""
The model definition element includes all the definition elements. It is used as the container for
the logically related set of device data points, for a particular model.

A Model has one Point Group.
A Point Group as one or more Point

One or more Models belong to SunSpec
"""
import re
import json
from time import time

from pymodbus.exceptions import ConnectionException
import logging

from .transformers import transformer_value

logging.basicConfig(level=logging.ERROR, format='(%(threadName)-9s) %(message)s',)

from . import PointGroup

class Model():
    def __init__(self, id: int, start_address: int, update_interval: int = 1, group: PointGroup = [], label: str=None, description: str=None) -> None:
        """
        Initializes a Model object.

        Parameters:
        - id (int): The ID of the model.
        - start_address (int): Address of the first data register for this model in the modbus 
        - update_interval (int): Update interval for the points value
        - label (str): A short label associated with the model.
        - description (str): A brief description of the model.
        - group (PointGroup): The PointGroup object associated with the model.
        """
        # Validate id
        if not isinstance(id, int):
            raise TypeError("ID must be an integer.")
        
        # Validate start_address
        if not isinstance(start_address, int):
            raise TypeError("start_address must be an integer.")

        # Validate update_interval
        if not isinstance(update_interval, int):
            raise TypeError("update_interval must be an integer.")

        # Validate group
        if not isinstance(group, PointGroup):
            raise TypeError("group must be a PointGroup object.")
        
        
        self.__id = id
        self.__label = label
        self.__description = description
        self.__group = group
        # SunSpec extra
        self.__start_address = start_address
        self.__total_size = sum(p.get_size() for p in group.get_points())
        self.__update_interval = update_interval
        self.__last_update = 0
    
    def get_id(self) -> str:
        return self.__id

    def get_label(self) -> str:
        return self.__label

    def get_description(self) -> str:
        return self.__description

    def get_group(self) -> PointGroup:
        return self.__group

    def get_start_address(self) -> int:
        return self.__start_address

    def get_total_size(self) -> int:
        return self.__total_size

    def get_update_interval(self) -> int:
        return self.__update_interval

    def get_last_update(self):
        return self.__last_update

    def set_last_update(self, val):
        self.__last_update = val

    def to_dict(self):
        # Cria um dicionário apenas com chaves que têm valores diferentes de None
        return {
            key: value
            for key, value in {
                "id": self.get_id(),
                "label": self.get_label(),
                "desc": self.get_description(),
                "group": self.__group.to_dict()
            }.items()
            if value is not None
        }
    
    def to_json(self):        
        return json.dumps(self.to_dict(), indent=4)

    def points_value_to_dict(self):
        data = {
            'id':self.get_id(),
            'name':self.get_group().get_name(),
            }

        for point in self.get_group().get_points():
            data.update(point.get_value_to_dict())
        
        return data

    def update(self, modbus_client, slave_id):
        
        if time() - self.get_last_update() < self.get_update_interval():
            return
        
        with modbus_client:
            try:
                read = modbus_client.read_holding_registers(address=self.get_start_address(), count=self.get_total_size(), slave=slave_id)
                if (read.isError()):
                    logging.error(f'Slave id {slave_id}. Model: {self.get_group().get_name()}: {read.message}')
                    return
            except ConnectionException:
                logging.error(f"ConnectionException: Slave id {slave_id}. Point: {self.get_name()}")
                return
        # data read, decode and fill points
        registers = read.registers
        for point in self.get_group().get_points():
            size = point.get_size()
            value = transformer_value(point.get_type(), registers[0 : size])
            point.set_value(value)
            del registers[0 : size]

        self.set_last_update(time())
        print(self.points_value_to_dict())
