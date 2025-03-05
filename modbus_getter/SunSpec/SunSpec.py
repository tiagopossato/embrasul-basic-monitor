from typing import List
import json
from time import time
from typing import List, Callable, Any
from pymodbus.exceptions import ConnectionException
import logging
from . import Model
from .transformers import transformer_value
from pymodbus.client.base import ModbusBaseSyncClient

logging.basicConfig(level=logging.ERROR, format='(%(threadName)-9s) %(message)s',)


class SunSpec():
    def __init__(
        self, 
        slave_id: int, 
        modbus_client: ModbusBaseSyncClient,  # Agora explicitamente aceitando ambos os tipos
        models: List[Model], 
        fn_save_data: Callable, 
        *args: Any, 
        **kwargs: Any
    ) -> None:
        """
        Initializes a SunSpec object.

        Parameters:
        - slave_id (int): Address of the Modbus slave.
        - modbus_client (ModbusBaseSyncClient): Modbus client (Serial or TCP).
        - models (List[Model]): List of Model objects associated with the SunSpec.
        - fn_save_data (Callable): Callback function used to save data.
        - *args (Any): Additional positional arguments passed to the callback.
        - **kwargs (Any): Additional keyword arguments passed to the callback.

        Raises:
        - TypeError: If models is not a list of Model objects.
        - ValueError: If models list is empty.
        - TypeError: If modbus_client is not an instance of ModbusSerialClient or ModbusTcpClient.
        """

        # Validate modbus_client
        if not isinstance(modbus_client, ModbusBaseSyncClient):
            raise TypeError("modbus_client must be an instance of ModbusSerialClient or ModbusTcpClient.")

        # Validate models
        if not isinstance(models, list) or not all(isinstance(m, Model) for m in models):
            raise TypeError("Models must be a list of Model objects.")
        if not models:
            raise ValueError("Models list cannot be empty.")

        self._models = models
        self._slave_id = slave_id
        self._modbus_client = modbus_client
        self._fn_save_data = fn_save_data
        self._args = args
        self._kwargs = kwargs
    
    def get_models(self) -> List[Model]:
        """
        Get the list of models associated with the SunSpec.

        Returns:
        - List[Model]: List of Model objects.
        """
        return self._models

    def models_to_dict(self):
        js_models = []
        for model in self._models: 
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

    def update(self):  
        """
        Reads data from Modbus models and saves it using the callback function.
        """
        for model in self._models:
            model.update(self._modbus_client, self._slave_id, self._fn_save_data, *self._args, **self._kwargs)
