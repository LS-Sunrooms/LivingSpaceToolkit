import logging
from abc import ABC, abstractmethod
from math import sin, cos, tan, atan, atan2, pi
from math import floor as m_floor
from math import ceil as m_ceil

from .toolkit_enums import Scenario, EndCutType, LengthType
from livingspacetoolkit.models import ToolkitStateModel

logger = logging.getLogger(name="livingspacetoolkit")


class BaseScenarioClass(ABC):
    @abstractmethod
    def __init__(self, toolkit_state_model: ToolkitStateModel) -> None:
        self.toolkit_state_model = toolkit_state_model

    @staticmethod
    @abstractmethod
    def scenario_condition(scenario: Scenario) -> bool:
        return False


class UnknownScenario(BaseScenarioClass):
    """A scenario that cannot be identified from the list of scenarios"""
    def __init__(self):
        pass

    def scenario_condition(self, scenario: Scenario) -> bool:
        return False


class ScenarioSelector:
    def __init__(self, toolkit_state_model: ToolkitStateModel) -> None:
        self.toolkit_state_model = toolkit_state_model

    def identify_scenario(self) -> BaseScenarioClass | type[UnknownScenario]:
        for scenario_cls in BaseScenarioClass.__subclasses__():
            try:
                if scenario_cls.scenario_condition(self.toolkit_state_model.scenario):
                    return scenario_cls(self.toolkit_state_model)
            except KeyError:
                pass
        return UnknownScenario