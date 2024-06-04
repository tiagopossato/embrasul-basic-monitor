from .voltage_model import voltage_model
from .frequency_model import frequency_model
from .current_model import current_model
from .active_power_model import active_power_model

models = [
    voltage_model,
    frequency_model,
    current_model,
    active_power_model
]