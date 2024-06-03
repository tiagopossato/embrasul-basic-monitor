"""
The model definition element includes all the definition elements. It is used as the container for
the logically related set of device data points, for a particular model.

A Model has one Point Group.
A Point Group as one or more Point

One or more Models belong to SunSpec
"""
import re
import json
from . import PointGroup

class Model():
    def __init__(self, id: int, group: PointGroup, label: str=None, description: str=None) -> None:
        """
        Initializes a Model object.

        Parameters:
        - id (int): The ID of the model.
        - label (str): A short label associated with the model.
        - description (str): A brief description of the model.
        - group (PointGroup): The PointGroup object associated with the model.
        """
        # Validate id
        if not isinstance(id, int):
            raise TypeError("ID must be an integer.")
          
        # # Validate label
        # if not isinstance(label, str):
        #     raise TypeError("Label must be a string.")
        
        # # Validate description
        # if not isinstance(description, str):
        #     raise TypeError("Description must be a string.")
        
        # Validate group
        if not isinstance(group, PointGroup):
            raise TypeError("group must be a PointGroup object.")
        
        self.__id = id
        self.__label = label
        self.__description = description
        self.__group = group
    
    def get_id(self) -> str:
        return self.__id

    def get_label(self) -> str:
        return self.__label

    def get_description(self) -> str:
        return self.__description

    def get_group(self) -> PointGroup:
        return self.__group
    
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

