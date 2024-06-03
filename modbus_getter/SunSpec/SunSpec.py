from . import Model

from typing import List
import json

class SunSpec():
    def __init__(self, models: List[Model] = None) -> None:
        """
        Initializes a SunSpec object.

        Parameters:
        - models (List[Model], optional): List of Model objects associated with the SunSpec.
        """
        if models is None:
            models = []
        else:
            # Validate models
            if not isinstance(models, list) or not all(isinstance(m, Model) for m in models):
                raise TypeError("Models must be a list of Model objects.")
        
        self.__models = models
    
    def get_models(self) -> List[Model]:
        """
        Get the list of models associated with the SunSpec.

        Returns:
        - List[Model]: List of Model objects.
        """
        return self.__models
    
    def add_model(self, model: Model) -> None:
        """
        Add a Model object to the list of models associated with the SunSpec.

        Parameters:
        - model (Model): The Model object to be added.
        """
        if not isinstance(model, Model):
            raise TypeError("model must be a Model object.")
        
        self.__models.append(model)

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

