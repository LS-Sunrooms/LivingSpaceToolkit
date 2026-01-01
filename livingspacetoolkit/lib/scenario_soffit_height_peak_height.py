from math import tan, atan

from livingspacetoolkit.logconf.log_config import logger
from .base_scenario_class import BaseScenarioClass
from .toolkit_enums import Scenario, LengthType, SunroomSide, SunroomType
from livingspacetoolkit.models import ToolkitStateModel, SunroomModel


class SoffitHeightPeakHeight(BaseScenarioClass):
    def __init__(self, toolkit_state_model: ToolkitStateModel, sunroom_model: SunroomModel) -> None:
        self.toolkit_state_model = toolkit_state_model
        self.sunroom_model= sunroom_model


    @staticmethod
    def scenario_condition(scenario: Scenario) -> bool:
        logger.debug(f"Selecting {scenario.name} class for calculations.")
        return scenario == Scenario.SOFFIT_HEIGHT_PEAK_HEIGHT

    def calculate_sunroom_properties(self) -> None:
        match self.toolkit_state_model.sunroom_type:
            case SunroomType.STUDIO:
                # Gather variables
                gable_wall = max(self.toolkit_state_model.floor_walls[SunroomSide.A_SIDE],
                                self.toolkit_state_model.floor_walls[SunroomSide.C_SIDE]).length
                overhang = self.toolkit_state_model.overhang.length
                thickness = self.toolkit_state_model.thickness.length
                peak_height = self.toolkit_state_model.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
                soffit_height_b_side = self.toolkit_state_model.wall_heights[(SunroomSide.B_SIDE,
                                                                            LengthType.SOFFIT_HEIGHT)].length
                # Calculate
                pitch_b_side = atan((peak_height - soffit_height_b_side) / (gable_wall + overhang))
                wall_height_b_side = soffit_height_b_side + overhang * tan(pitch_b_side)
                max_height = peak_height + self.calculate_hypotenuse(thickness, pitch_b_side)
                drip_edge_b_side = self.calculate_drip_edge(thickness, soffit_height_b_side, pitch_b_side)
                # Add calculated values to toolkit_state_model
                # Turn it back into a ratio to update state model
                self.toolkit_state_model.pitch[SunroomSide.B_SIDE].pitch_value = tan(pitch_b_side) * 12
                self.toolkit_state_model.wall_heights[(None, LengthType.MAX_HEIGHT)].length = max_height
                self.toolkit_state_model.wall_heights[
                    (SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length = drip_edge_b_side
                self.toolkit_state_model.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length = (
                    wall_height_b_side)
                self.toolkit_state_model.wall_heights[
                    (SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length = wall_height_b_side
                self.toolkit_state_model.wall_heights[
                    (SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length = wall_height_b_side
                self.sunroom_model.gable_wall[SunroomSide.B_SIDE].length = gable_wall
            case SunroomType.CATHEDRAL:
                # Gather variables
                gable_wall = self.toolkit_state_model.floor_walls[SunroomSide.B_SIDE].length
                fenevision_peak = self.toolkit_state_model.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
                overhang = self.toolkit_state_model.overhang.length
                thickness = self.toolkit_state_model.thickness.length
                soffit_height_a_side = self.toolkit_state_model.wall_heights[(SunroomSide.A_SIDE,
                                                                            LengthType.SOFFIT_HEIGHT)].length
                soffit_height_c_side = self.toolkit_state_model.wall_heights[(SunroomSide.C_SIDE,
                                                                            LengthType.SOFFIT_HEIGHT)].length
                # TODO: Should probably change this if we allow different soffit heights but its in the original code.
                soffit = max(soffit_height_a_side, soffit_height_c_side)
                # Calculate
                pitch_a_side = atan((fenevision_peak - soffit) / (gable_wall / 2 + overhang - self.post_width / 2))
                pitch_c_side = atan((fenevision_peak - soffit) / (gable_wall / 2 + overhang - self.post_width / 2))
                max_height = (fenevision_peak + max(self.calculate_hypotenuse(thickness, pitch_a_side),
                                                    self.calculate_hypotenuse(thickness, pitch_c_side)) +
                              self.calculate_triangle_height(pitch_a_side, pitch_c_side, self.post_width))
                wall_height_a_side = soffit_height_a_side + overhang * tan(pitch_a_side)
                wall_height_c_side = soffit_height_a_side + overhang * tan(pitch_c_side)
                drip_edge_a_side = self.calculate_drip_edge(thickness, soffit_height_a_side, pitch_a_side)
                drip_edge_c_side = self.calculate_drip_edge(thickness, soffit_height_c_side, pitch_c_side)
                # Add calculated values to toolkit_state_model
                # Turn it back into a ratio to update state model
                self.toolkit_state_model.pitch[SunroomSide.A_SIDE].pitch_value = tan(pitch_a_side) * 12
                self.toolkit_state_model.pitch[SunroomSide.C_SIDE].pitch_value = tan(pitch_c_side) * 12
                self.toolkit_state_model.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length = (
                    wall_height_a_side)
                self.toolkit_state_model.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length = (
                    wall_height_c_side)
                self.toolkit_state_model.wall_heights[(None, LengthType.MAX_HEIGHT)].length = max_height
                self.toolkit_state_model.wall_heights[(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length = (
                    drip_edge_a_side)
                self.toolkit_state_model.wall_heights[(SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length = (
                    drip_edge_c_side)
                self.sunroom_model.gable_wall[SunroomSide.A_SIDE].length = gable_wall / 2
                self.sunroom_model.gable_wall[SunroomSide.C_SIDE].length = gable_wall / 2