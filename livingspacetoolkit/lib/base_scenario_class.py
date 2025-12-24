from abc import ABC, abstractmethod

from .toolkit_enums import Scenario
from livingspacetoolkit.models import ToolkitStateModel


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