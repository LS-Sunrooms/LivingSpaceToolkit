from math import sin, cos, tan, pi
from abc import ABC, abstractmethod

from livingspacetoolkit.config.log_config import logger
from .toolkit_enums import Scenario, EndCutType
from livingspacetoolkit.models import ToolkitStateModel, SunroomModel



class BaseScenarioClass(ABC):
    """This is the base class for all scenario calculations. All scenarios must inherit this class."""
    post_width = 3.25  # Business logic. The width of the center post. Used in cathedral calculations.

    @abstractmethod
    def __init__(self, toolkit_state_model: ToolkitStateModel, sunroom_model: SunroomModel) -> None:
        self.toolkit_state_model = toolkit_state_model
        self.sunroom_model = sunroom_model

    @staticmethod
    @abstractmethod
    def scenario_condition(scenario: Scenario) -> bool:
        return False

    @abstractmethod
    def calculate_sunroom_properties(self) -> None:
        pass

    @staticmethod
    def calculate_hypotenuse(opposite: float, pitch: float) -> float:
        """
        Calculates the hypotenuse given pitch and the opposite (panel thickness). Pitch has to be in radians.
        :param opposite: float
        :param pitch: float
        :return: float
        """
        if pitch == pi/2:
            raise ZeroDivisionError("The pitch is 90 degrees?")
        return opposite * (sin(pi / 2) / sin(pi / 2 - pitch))

    def calculate_drip_edge(self, thickness: float, soffit: float, pitch: float) -> float:
        """
        Returns the drip edge height given the soffit and angled thickness. Returns in units of inches.

        :param thickness: float: Panel thickness in inches
        :param soffit: float: Soffit height in inches
        :param pitch: float: Pitch in radians
        :return:
        """
        angled_thickness = self.calculate_hypotenuse(opposite=thickness, pitch=pitch)
        if self.toolkit_state_model.end_cuts == EndCutType.PLUMB_CUT_TOP_BOTTOM:
            drip_edge = soffit + angled_thickness
        else:
            drip_edge = soffit + thickness * cos(pitch)
        return drip_edge

    def estimate_drip_from_peak(self, peak: float, overhang: float, thickness: float, estimate_pitch: float,
                                pitched_wall_length: float) -> float:
        """
        This method is used to help estimate the pitch. Since I forgot how to do numerical methods this will have to do.
        All lengths must be in inches, the estimated pitch in radians, and this assumes you are cycling through a list
        of pitches.
        :param thickness: float: Panel thickness in inches
        :param overhang: float: Overhang in inches
        :param peak: float: Sunroom peak in inches
        :param estimate_pitch: float: The estimated pitch of the room in radians
        :param pitched_wall_length: float: The length of the pitched-side wall in inches
        :return: float: Returns the drip edge height in inches
        """
        wall_height = peak - pitched_wall_length * tan(estimate_pitch)
        soffit = wall_height - overhang * tan(estimate_pitch)

        return self.calculate_drip_edge(thickness, soffit, estimate_pitch)

    @staticmethod
    def calculate_triangle_height(angle_1: float, angle_2: float, base_length: float) -> float:
        """
        This is business logic used to figure out the height of a triangle when only given the two base angles and base
        width. Use the Sine Rule to figure out the missing angle, that same rule to get the hypotenuse of one side, and
        finally the right angle rule to figure out the height of the triangle. This is used primarily to find the
        difference between the calculated peak height and the peak height used in Fenevision which is at the base of the
        post sitting at the center of a cathedral sunroom.
        :param angle_1:
        :param angle_2:
        :param base_length:
        :return: float: Returns the height of the triangle.
        """
        return base_length * sin(angle_1) * sin(angle_2) / sin(pi - angle_1 - angle_2)


class UnknownScenario(BaseScenarioClass):
    """A scenario that cannot be identified from the list of scenarios"""
    def __init__(self):
        pass

    @staticmethod
    def scenario_condition(scenario: Scenario) -> bool:
        return False

    def calculate_sunroom_properties(self) -> None:
        raise NotImplementedError


class ScenarioSelector:
    def __init__(self, toolkit_state_model: ToolkitStateModel) -> None:
        self.toolkit_state_model = toolkit_state_model

    def identify_scenario(self, sunroom_model: SunroomModel):
        for scenario_cls in BaseScenarioClass.__subclasses__():
            try:
                if scenario_cls.scenario_condition(self.toolkit_state_model.scenario):
                    return scenario_cls(self.toolkit_state_model, sunroom_model)
            except KeyError:
                pass
        return UnknownScenario