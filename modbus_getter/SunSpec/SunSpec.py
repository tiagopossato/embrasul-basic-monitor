from . import Model

from typing import List

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