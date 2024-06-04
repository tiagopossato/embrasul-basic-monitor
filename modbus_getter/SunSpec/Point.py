"""
The point definition element defines a Device Information Model data point. Point elements hold
data values that correspond to a device property. There are typically multiple point definitions in
the model definition.
"""
import re
import json

from . import static_type, access_type, mandatory_type, point_type

class Point():
    def __init__(self, id: str, size: int, label: str, description: str, pt_type: point_type, units: str, sf: int = 1, 
                 access: access_type = access_type.R, mandatory: mandatory_type = mandatory_type.M, static: static_type = static_type.D) -> None:   
        """
        Initializes a Point object.

        Parameters:
        - id (str): The ID of the point, must be unique and consist of alphanumeric characters and underscores only.
        - size (int): Data size in modbus equipment
        - label (str): A short label associated with the point.
        - description (str): A brief description of the point.
        - pt_type: The type of the point.
        - sf (int): The scale factor applied to the point values.
        - units (str): The units associated with the point.
        - access: The accessibility of the point, can be 'R' for read-only or 'RW' for read/write.
        - mandatory: The mandatory status of the point, can be 'M' for mandatory or 'O' for optional.
        - static: Whether the point is static or dynamic.
        """
        # Validate id using regular expression
        if not re.match(r'^[a-zA-Z0-9_]+$', id):
            raise ValueError("Invalid id format. ID must consist of only alphanumeric characters and underscores.")
               
        # Validate label
        if not isinstance(label, str):
            raise TypeError("Label must be a string.")
        
        # Validate description
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        
        # Validate pt_type
        if not isinstance(pt_type, point_type):
            raise TypeError("pt_type must be of type point_type.")
        
        # Validate sf
        if not isinstance(sf, int):
            raise TypeError("Scale factor must be an integer.")
        
        # Validate units
        if not isinstance(units, str):
            raise TypeError("Units must be a string.")
        
        # Validate access
        if not isinstance(access, access_type):
            raise TypeError("Access must be of type access_type.")
        
        # Validate mandatory
        if not isinstance(mandatory, mandatory_type):
            raise TypeError("Mandatory must be of type mandatory_type.")
        
        # Validate static
        if not isinstance(static, static_type):
            raise TypeError("Static must be of type static_type.")

        # The ID attribute is the element name and MUST be unique in the immediate group in which it is
        # defined. An ID MUST consist of only alphanumeric characters and the underscore character.
        # The ID attribute for a model element MUST be the numeric SunSpec model id.
        self.__id = id
  
        self.__value = None
    
        # The type attribute is the element type.
        self.__type = pt_type

        # The count attribute specifies the number of occurrences of the element in the model.
        self.count = 1 

        # The size attribute specifies the maximum element length in 16-bit words. The size attribute
        # MUST be provided for the string point type and MAY be provided for the pad type. 
        # The size attribute MUST not be provided for any other type.
        self.__size = size

        # As an alternative to floating-point format, values are represented by integer values with a signed
        # scale factor applied. A negative scale factor explicitly shifts the decimal point to the left, and a
        # positive scale factor shifts the decimal point to the right by the number of places specified in the
        # scale factor value.
        self.__sf = sf

        # The units attribute is a string that specifies the units associated with the element.
        # Units are defined as needed by specific models. Where units are shared across models, care is
        # taken to ensure a common definition of those units.
        self.__units = units
        
        # The access attribute specifies if the element is writable or read-only. If specified, the value
        # MUST be read-only (R) or read/write (RW). If not specified, the default access is read-only.
        self.__access = access

        #The mandatory attribute specifies whether the element is required to be implemented. If
        # specified, the value MUST be either mandatory (M) or optional (O). If not specified, the default
        # value is optional. Points specified as mandatory MUST always have a valid value. Points
        # specified as optional may have the unimplemented value for the corresponding point type.
        self.__mandatory = mandatory

        # if the point is static or dynamic
        self.__static = static

        # The label attribute specifies a short label associated with the element.
        self.__label = label

        # The description attribute provides a brief description of the element.
        self.__description = description
    
    def get_id(self):
        return self.__id
      
    def get_type(self):
        return self.__type

    def get_size(self):
        return self.__size

    def get_sf(self):
        return self.__sf

    def get_units(self):
        return self.__units

    def get_access(self):
        return self.__access

    def get_mandatory(self):
        return self.__mandatory

    def get_static(self):
        return self.__static

    def get_label(self):
        return self.__label

    def get_description(self):
        return self.__description
    
    def get_value(self):
      return self.__value
    
    def set_value(self, value):
        self.__value = value
    
    def to_dict(self):
        return {
            key: value
            for key, value in {
                "id": self.get_id(),
                "value": self.get_value(),
                "label": self.get_label(),
                "desc": self.get_description(),
                "type": self.get_type().name,
                "size": self.get_size(),
                "sf": self.get_sf(),
                "units": self.get_units(),
                "access": self.get_access().name,
                "mandatory": self.get_mandatory().name,
                "static": self.get_static().name
                # Add other attributes as needed
            }.items()
            if value is not None
        }

    def get_value_to_dict(self):
        return {self.get_id(): self.get_value()}
    
    def to_json(self):
        """
        Convert Point object to JSON format.

        Returns:
        - str: JSON representation of the Point object.
        """
        return json.dumps(self.to_dict(), indent=4)