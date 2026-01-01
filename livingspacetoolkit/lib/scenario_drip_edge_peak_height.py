from math import tan, atan2

from livingspacetoolkit.logconf.log_config import logger
from models import SunroomModel
from .base_scenario_class import BaseScenarioClass
from .toolkit_enums import Scenario, LengthType, SunroomSide, SunroomType
from livingspacetoolkit.models import ToolkitStateModel


class DripEdgePeakHeight(BaseScenarioClass):
    def __init__(self, toolkit_state_model: ToolkitStateModel, sunroom_model: SunroomModel) -> None:
        self.toolkit_state_model = toolkit_state_model
        self.sunroom_model = sunroom_model


    @staticmethod
    def scenario_condition(scenario: Scenario) -> bool:
        logger.debug(f"Selecting {scenario.name} class for calculations.")
        return scenario == Scenario.DRIP_EDGE_PEAK_HEIGHT

    def calculate_sunroom_properties(self) -> None:
        # TODO: I didn't have the patience to figure out an analytical solution so I made up a numerical one. This
        #  should be replaced with the Bisection Method.
        tolerance = 0.01
        difference = 100
        increment = 0.1
        ratio_pitch = 0.0
        old_ratio_pitch = 0.0
        match self.toolkit_state_model.sunroom_type:
            case SunroomType.STUDIO:
                pitch_b_side = 0
                # Gather variables
                gable_wall = max(self.toolkit_state_model.floor_walls[SunroomSide.A_SIDE],
                                self.toolkit_state_model.floor_walls[SunroomSide.C_SIDE]).length
                overhang = self.toolkit_state_model.overhang.length
                thickness = self.toolkit_state_model.thickness.length
                peak_height = self.toolkit_state_model.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
                drip_edge_b_side = self.toolkit_state_model.wall_heights[(SunroomSide.B_SIDE,
                                                                          LengthType.DRIP_EDGE_HEIGHT)].length
                # Calculate
                while difference > tolerance:
                    old_ratio_pitch = ratio_pitch
                    ratio_pitch += increment
                    pitch_b_side = atan2(ratio_pitch, 12)
                    drip_estimate_b_side = self.estimate_drip_from_peak(peak_height, overhang, thickness, pitch_b_side,
                                                                        gable_wall)
                    difference = abs(drip_edge_b_side - drip_estimate_b_side)
                    if ratio_pitch > 12:
                        logger.error("Failed to estimate the drip edge!")
                        break
                    if drip_estimate_b_side < drip_edge_b_side:
                        ratio_pitch = old_ratio_pitch
                        increment /= 2
                wall_height_b_side = peak_height - gable_wall * tan(pitch_b_side)
                soffit_height_b_side = wall_height_b_side - overhang * tan(pitch_b_side)
                max_height = peak_height + self.calculate_hypotenuse(thickness, pitch_b_side)
                # TODO: Do I really need to recalculate the drip edge? It's what is in the original so it's here.
                drip_edge_b_side = self.calculate_drip_edge(thickness, soffit_height_b_side, pitch_b_side)
                # Add calculated values to toolkit_state_model
                # Turn it back into a ratio to update state model
                self.toolkit_state_model.pitch[SunroomSide.B_SIDE].pitch_value = tan(pitch_b_side) * 12
                self.toolkit_state_model.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length = (
                    soffit_height_b_side)
                self.toolkit_state_model.wall_heights[(None, LengthType.MAX_HEIGHT)].length = max_height
                self.toolkit_state_model.wall_heights[
                    (SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length = drip_edge_b_side
                self.toolkit_state_model.wall_heights[
                    (SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length = wall_height_b_side
                self.toolkit_state_model.wall_heights[
                    (SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length = wall_height_b_side
                self.toolkit_state_model.wall_heights[
                    (SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length = wall_height_b_side
                self.sunroom_model.gable_wall[SunroomSide.B_SIDE].length = gable_wall
            case SunroomType.CATHEDRAL:
                pitch = 0
                # Gather variables
                gable_wall = self.toolkit_state_model.floor_walls[SunroomSide.B_SIDE].length
                fenevision_peak = self.toolkit_state_model.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
                overhang = self.toolkit_state_model.overhang.length
                thickness = self.toolkit_state_model.thickness.length
                drip_edge_a_side = self.toolkit_state_model.wall_heights[(SunroomSide.A_SIDE,
                                                                            LengthType.DRIP_EDGE_HEIGHT)].length
                drip_edge_c_side = self.toolkit_state_model.wall_heights[(SunroomSide.C_SIDE,
                                                                            LengthType.DRIP_EDGE_HEIGHT)].length
                # Calculate
                while difference > tolerance:
                    old_ratio_pitch = ratio_pitch
                    ratio_pitch += increment
                    pitch = atan2(ratio_pitch, 12)
                    drip_estimate = self.estimate_drip_from_peak(fenevision_peak, overhang, thickness, pitch,
                                                                 gable_wall / 2 - self.post_width / 2)
                    difference = abs(drip_estimate - drip_edge_a_side) # There's only one input for drip edge.
                    if ratio_pitch > 12:
                        logger.error("Failed to estimate the drip edge!")
                        break
                    if drip_estimate < drip_edge_a_side:
                        ratio_pitch = old_ratio_pitch
                        increment /= 2
                    # Now take the estimated pitch and set it as a ratio then convert back to radians. It's more
                    # accurate for some reason.
                wall_height_a_c_side = fenevision_peak - (gable_wall / 2 - self.post_width / 2) * tan(pitch)
                soffit_height_a_c_side = wall_height_a_c_side - overhang * tan(pitch)
                max_height = (fenevision_peak + self.calculate_hypotenuse(thickness, pitch) +
                              self.calculate_triangle_height(pitch, pitch, self.post_width))
                # Add calculated values to toolkit_state_model
                # Turn it back into a ratio to update state model
                self.toolkit_state_model.pitch[SunroomSide.A_SIDE].pitch_value = tan(pitch) * 12
                self.toolkit_state_model.pitch[SunroomSide.C_SIDE].pitch_value = tan(pitch) * 12
                self.toolkit_state_model.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length = (
                    soffit_height_a_c_side)
                self.toolkit_state_model.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length = (
                    soffit_height_a_c_side)
                self.toolkit_state_model.wall_heights[(None, LengthType.MAX_HEIGHT)].length = max_height
                self.toolkit_state_model.wall_heights[(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length = (
                    drip_edge_a_side)
                self.toolkit_state_model.wall_heights[(SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length = (
                    drip_edge_c_side)
                self.toolkit_state_model.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length = (
                    wall_height_a_c_side)
                self.toolkit_state_model.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length = (
                    wall_height_a_c_side)
                self.sunroom_model.gable_wall[SunroomSide.A_SIDE].length = gable_wall / 2
                self.sunroom_model.gable_wall[SunroomSide.C_SIDE].length = gable_wall / 2