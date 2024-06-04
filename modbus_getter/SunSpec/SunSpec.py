from typing import List
import json
from time import time

from pymodbus.exceptions import ConnectionException
import logging

from . import Model
from .transformers import transformer_value

logging.basicConfig(level=logging.ERROR, format='(%(threadName)-9s) %(message)s',)


class SunSpec():
    def __init__(self, slave_id:int, modbus_client, models: List[Model] = None) -> None:
        """
        Initializes a SunSpec object.

        Parameters:
        - slave_id (int): Address of modbus slave
        - modbus_client (ModbusClient): Modbus Client
        - models (List[Model], optional): List of Model objects associated with the SunSpec.
        """
        # Validate models
        if not isinstance(models, list) or not all(isinstance(m, Model) for m in models):
            raise TypeError("Models must be a list of Model objects.")
        
        self.__models = models
        self.__slave_id = slave_id
        self.__modbus_client = modbus_client
    

    def get_models(self) -> List[Model]:
        """
        Get the list of models associated with the SunSpec.

        Returns:
        - List[Model]: List of Model objects.
        """
        return self.__models

    def models_to_dict(self):
        js_models = []
        for model in self.__models: 
            js_models.append(model.to_dict())
        return js_models
    

    def to_dict(self):
        # Cria um dicionário apenas com chaves que têm valores diferentes de None
        return {
            key: value
            for key, value in {
                "models": self.models_to_dict()
            }.items()
            if value is not None
        }
    
    def to_json(self):        
        return json.dumps(self.to_dict(), indent=4)

    def update(self, fn_save_data, db_session):  
        for model in self.get_models():
            model.update(self.__modbus_client, self.__slave_id, fn_save_data, db_session)
            
