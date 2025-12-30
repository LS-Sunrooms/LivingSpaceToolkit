import pytest
from math import tan

from livingspacetoolkit.lib import *
from livingspacetoolkit.models import ToolkitStateModel
from livingspacetoolkit.utils.helpers import to_nice_number
from livingspacetoolkit.lib.toolkit_enums import Scenario, SunroomSide, RoofingType, SunroomType, EndCutType
from livingspacetoolkit.lib.toolkit_length import LengthType


class TestScenarioSelection:

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected", [
        (Scenario.WALL_HEIGHT_PITCH, "WallHeightPitch"),
        (Scenario.WALL_HEIGHT_PEAK_HEIGHT, "WallHeightPeakHeight"),
        (Scenario.MAX_HEIGHT_PITCH, "MaxHeightPitch"),
        (Scenario.SOFFIT_HEIGHT_PEAK_HEIGHT, "SoffitHeightPeakHeight"),
        (Scenario.SOFFIT_HEIGHT_PITCH, "SoffitHeightPitch"),
        (Scenario.DRIP_EDGE_PEAK_HEIGHT, "DripEdgePeakHeight"),
        (Scenario.DRIP_EDGE_PITCH, "DripEdgePitch"),
    ])
    def test_scenario_selection(self, actual, expected):
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.STUDIO
        toolkit_state.scenario = actual
        # Act
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Assert
        assert scenario.__class__.__name__ == expected


# Note the parametrized tests changes the End Cuts type because the function, calculate_drip_edge in base_scenario_class
# calculates the drip edge differently for EndCutType.PLUMB_CUT_TOP_BOTTOM. This also means that scenario
# DRIP_EDGE_PEAK_HEIGHT will calculate soffit, max_height, wall_heights differently. These are tests to match the output
# of the previous version of this software.
class TestStudioScenarios:

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected",
                             [
                                 (EndCutType.UNCUT_TOP_BOTTOM, 116.25),
                                 (EndCutType.PLUMB_CUT_TOP_BOTTOM, 119.5),
                             ])
    def test_wall_height_pitch(self, actual, expected):
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.STUDIO
        toolkit_state.scenario = Scenario.WALL_HEIGHT_PITCH
        toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = 10
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = actual
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        pitch = 12 * tan(toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value)
        peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
        max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
        soffit = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length
        drip_edge = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        b_wall_height = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length
        a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
        c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
        assert to_nice_number(pitch, 2) == 10
        assert to_nice_number(peak, 16) == 220
        assert to_nice_number(soffit, 16) == 111.6875
        assert to_nice_number(drip_edge, 16) == expected
        assert to_nice_number(max_height, 16) == 227.8125
        assert to_nice_number(a_wall_height, 16) == 120
        assert to_nice_number(b_wall_height, 16) == 120
        assert to_nice_number(c_wall_height, 16) == 120

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected",
                             [
                                 (EndCutType.UNCUT_TOP_BOTTOM, 116.25),
                                 (EndCutType.PLUMB_CUT_TOP_BOTTOM, 119.5),
                             ])
    def test_wall_height_peak_height(self, actual, expected):
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.STUDIO
        toolkit_state.scenario = Scenario.WALL_HEIGHT_PEAK_HEIGHT
        toolkit_state.overhang.length = 10
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = actual
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length = 220
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        pitch = 12 * tan(toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value)
        peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
        max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
        soffit = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length
        drip_edge = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        b_wall_height = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length
        a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
        c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
        assert to_nice_number(pitch, 2) == 10
        assert to_nice_number(peak, 16) == 220
        assert to_nice_number(soffit, 16) == 111.6875
        assert to_nice_number(drip_edge, 16) == expected
        assert to_nice_number(max_height, 16) == 227.8125
        assert to_nice_number(a_wall_height, 16) == 120
        assert to_nice_number(b_wall_height, 16) == 120
        assert to_nice_number(c_wall_height, 16) == 120

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected",
                             [
                                 (EndCutType.UNCUT_TOP_BOTTOM, 116.25),
                                 (EndCutType.PLUMB_CUT_TOP_BOTTOM, 119.5),
                             ])
    def test_max_height_pitch(self, actual, expected):
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.STUDIO
        toolkit_state.scenario = Scenario.MAX_HEIGHT_PITCH
        toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = 10
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = actual
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length = 227.8125
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        pitch = 12 * tan(toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value)
        peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
        max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
        soffit = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length
        drip_edge = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        b_wall_height = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length
        a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
        c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
        assert to_nice_number(pitch, 2) == 10
        assert to_nice_number(peak, 16) == 220
        assert to_nice_number(soffit, 16) == 111.6875
        assert to_nice_number(drip_edge, 16) == expected
        assert to_nice_number(max_height, 16) == 227.8125
        assert to_nice_number(a_wall_height, 16) == 120
        assert to_nice_number(b_wall_height, 16) == 120
        assert to_nice_number(c_wall_height, 16) == 120

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected",
                             [
                                 (EndCutType.UNCUT_TOP_BOTTOM, 116.3125),
                                 (EndCutType.PLUMB_CUT_TOP_BOTTOM, 119.5),
                             ])
    def test_soffit_height_peak_height(self, actual, expected):
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.STUDIO
        toolkit_state.scenario = Scenario.SOFFIT_HEIGHT_PEAK_HEIGHT
        toolkit_state.overhang.length = 10
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = actual
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length = 111.6875
        toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length = 220
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        pitch = 12 * tan(toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value)
        peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
        max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
        soffit = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length
        drip_edge = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        b_wall_height = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length
        a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
        c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
        assert to_nice_number(pitch, 2) == 10
        assert to_nice_number(peak, 16) == 220
        assert to_nice_number(soffit, 16) == 111.6875
        assert to_nice_number(drip_edge, 16) == expected
        assert to_nice_number(max_height, 16) == 227.8125
        assert to_nice_number(a_wall_height, 16) == 120
        assert to_nice_number(b_wall_height, 16) == 120
        assert to_nice_number(c_wall_height, 16) == 120

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected",
                             [
                                 (EndCutType.UNCUT_TOP_BOTTOM, 116.3125),
                                 (EndCutType.PLUMB_CUT_TOP_BOTTOM, 119.5),
                             ])
    def test_soffit_height_pitch(self, actual, expected):
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.STUDIO
        toolkit_state.scenario = Scenario.SOFFIT_HEIGHT_PITCH
        toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = 10
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = actual
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length = 111.6875
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        pitch = 12 * tan(toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value)
        peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
        max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
        soffit = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length
        drip_edge = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        b_wall_height = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length
        a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
        c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
        assert to_nice_number(pitch, 2) == 10
        assert to_nice_number(peak, 16) == 220
        assert to_nice_number(soffit, 16) == 111.6875
        assert to_nice_number(drip_edge, 16) == 116.3125
        assert to_nice_number(max_height, 16) == 227.8125
        assert to_nice_number(a_wall_height, 16) == 120
        assert to_nice_number(b_wall_height, 16) == 120
        assert to_nice_number(c_wall_height, 16) == 120

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected",
                             [
                                 (EndCutType.UNCUT_TOP_BOTTOM, [111.625, 227.8125, 120]),
                                 (EndCutType.PLUMB_CUT_TOP_BOTTOM, [108.375, 227.9375, 116.9375]),
                             ])
    def test_drip_edge_peak_height(self, actual, expected):
        # Arrange
        # expected = [soffit, max_height, wall_heights (a,b,c)]
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.STUDIO
        toolkit_state.scenario = Scenario.DRIP_EDGE_PEAK_HEIGHT
        toolkit_state.overhang.length = 10
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = actual
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length = 116.25
        toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length = 220
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        pitch = 12 * tan(toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value)
        peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
        max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
        soffit = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length
        drip_edge = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        b_wall_height = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length
        a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
        c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
        assert to_nice_number(pitch, 2) == 10
        assert to_nice_number(peak, 16) == 220
        assert to_nice_number(soffit, 16) == expected[0]
        assert to_nice_number(drip_edge, 16) == 116.25
        assert to_nice_number(max_height, 16) == expected[1]
        assert to_nice_number(a_wall_height, 16) == expected[2]
        assert to_nice_number(b_wall_height, 16) == expected[2]
        assert to_nice_number(c_wall_height, 16) == expected[2]

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected",
                             [
                                 (EndCutType.UNCUT_TOP_BOTTOM, 113.0625),
                                 (EndCutType.PLUMB_CUT_TOP_BOTTOM, 116.25),
                             ])
    def test_drip_edge_pitch(self, actual, expected):
        # This test is special because the drip edge is calculated using a janky numerical method. Estimates need to be
        # close instead of exact.
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.STUDIO
        toolkit_state.scenario = Scenario.DRIP_EDGE_PITCH
        toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = 10
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = actual
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length = 116.25
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        pitch = 12 * tan(toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value)
        peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
        max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
        soffit = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length
        drip_edge = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        b_wall_height = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length
        a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
        c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
        assert to_nice_number(pitch, 2) == 10
        assert to_nice_number(peak, 16) == 216.75
        assert to_nice_number(soffit, 16) == 108.4375
        assert to_nice_number(drip_edge, 16) == expected
        assert to_nice_number(max_height, 16) == 224.5625
        assert to_nice_number(a_wall_height, 16) == 116.75
        assert to_nice_number(b_wall_height, 16) == 116.75
        assert to_nice_number(c_wall_height, 16) == 116.75


# Note the parametrized tests changes the End Cuts type because the function, calculate_drip_edge in base_scenario_class
# calculates the drip edge differently for EndCutType.PLUMB_CUT_TOP_BOTTOM. This also means that scenario
# DRIP_EDGE_PEAK_HEIGHT will calculate soffit, max_height, wall_heights differently.These are tests to match the output
# of the previous version of this software.
class TestCathedralScenarios:

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected",
                             [
                                 (EndCutType.UNCUT_TOP_BOTTOM, 116.25),
                                 (EndCutType.PLUMB_CUT_TOP_BOTTOM, 119.5),
                             ])
    def test_wall_height_pitch(self, actual, expected):
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.CATHEDRAL
        toolkit_state.scenario = Scenario.WALL_HEIGHT_PITCH
        toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value = '10'
        toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = 10
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = actual
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        pitch_a_side = 12 * tan(toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value)
        pitch_c_side = 12 * tan(toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value)
        peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
        max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
        soffit_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length
        soffit_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length
        drip_edge_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        drip_edge_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
        c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
        assert to_nice_number(pitch_a_side, 2) == 10
        assert to_nice_number(pitch_c_side, 2) == 10
        assert to_nice_number(peak, 16) == 168.625
        assert to_nice_number(soffit_a_side, 16) == 111.6875
        assert to_nice_number(soffit_c_side, 16) == 111.6875
        assert to_nice_number(drip_edge_a_side, 16) == expected
        assert to_nice_number(drip_edge_c_side, 16) == expected
        assert to_nice_number(max_height, 16) == 177.8125
        assert to_nice_number(a_wall_height, 16) == 120
        assert to_nice_number(c_wall_height, 16) == 120

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected",
                             [
                                 (EndCutType.UNCUT_TOP_BOTTOM, 116.4375),
                                 (EndCutType.PLUMB_CUT_TOP_BOTTOM, 119.5625),
                             ])
    def test_wall_height_peak_height(self, actual, expected):
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.CATHEDRAL
        toolkit_state.scenario = Scenario.WALL_HEIGHT_PEAK_HEIGHT
        toolkit_state.overhang.length = 10
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = actual
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length = 168
        toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        pitch_a_side = 12 * tan(toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value)
        pitch_c_side = 12 * tan(toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value)
        peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
        max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
        soffit_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length
        soffit_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length
        drip_edge_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        drip_edge_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
        c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
        assert to_nice_number(pitch_a_side, 2) == 10
        assert to_nice_number(pitch_c_side, 2) == 10
        assert to_nice_number(peak, 16) == 168
        assert to_nice_number(soffit_a_side, 16) == 111.75
        assert to_nice_number(soffit_c_side, 16) == 111.75
        assert to_nice_number(drip_edge_a_side, 16) == expected
        assert to_nice_number(drip_edge_c_side, 16) == expected
        assert to_nice_number(max_height, 16) == 177.125
        assert to_nice_number(a_wall_height, 16) == 120
        assert to_nice_number(c_wall_height, 16) == 120

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected",
                             [
                                 (EndCutType.UNCUT_TOP_BOTTOM, 158.4375),
                                 (EndCutType.PLUMB_CUT_TOP_BOTTOM, 161.6875),
                             ])
    def test_max_height_pitch(self, actual, expected):
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.CATHEDRAL
        toolkit_state.scenario = Scenario.MAX_HEIGHT_PITCH
        toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value = '10'
        toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = 10
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = actual
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length = 220
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        pitch_a_side = 12 * tan(toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value)
        pitch_c_side = 12 * tan(toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value)
        peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
        max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
        soffit_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length
        soffit_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length
        drip_edge_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        drip_edge_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
        c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
        assert to_nice_number(pitch_a_side, 2) == 10
        assert to_nice_number(pitch_c_side, 2) == 10
        assert to_nice_number(peak, 16) == 210.8125
        assert to_nice_number(soffit_a_side, 16) == 153.875
        assert to_nice_number(soffit_c_side, 16) == 153.875
        assert to_nice_number(drip_edge_a_side, 16) == expected
        assert to_nice_number(drip_edge_c_side, 16) == expected
        assert to_nice_number(max_height, 16) == 220
        assert to_nice_number(a_wall_height, 16) == 162.1875
        assert to_nice_number(c_wall_height, 16) == 162.1875

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected",
                             [
                                 (EndCutType.UNCUT_TOP_BOTTOM, 116.625),
                                 (EndCutType.PLUMB_CUT_TOP_BOTTOM, 119.75),
                             ])
    def test_soffit_height_peak_height(self, actual, expected):
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.CATHEDRAL
        toolkit_state.scenario = Scenario.SOFFIT_HEIGHT_PEAK_HEIGHT
        toolkit_state.overhang.length = 10
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = actual
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length = 168
        toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length = 112
        toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length = 112
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        pitch_a_side = 12 * tan(toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value)
        pitch_c_side = 12 * tan(toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value)
        peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
        max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
        soffit_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length
        soffit_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length
        drip_edge_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        drip_edge_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
        c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
        assert to_nice_number(pitch_a_side, 2) == 10
        assert to_nice_number(pitch_c_side, 2) == 10
        assert to_nice_number(peak, 16) == 168
        assert to_nice_number(soffit_a_side, 16) == 112
        assert to_nice_number(soffit_c_side, 16) == 112
        assert to_nice_number(drip_edge_a_side, 16) == expected
        assert to_nice_number(drip_edge_c_side, 16) == expected
        assert to_nice_number(max_height, 16) == 177.0625
        assert to_nice_number(a_wall_height, 16) == 120.1875
        assert to_nice_number(c_wall_height, 16) == 120.1875

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected",
                             [
                                 (EndCutType.UNCUT_TOP_BOTTOM, 116.625),
                                 (EndCutType.PLUMB_CUT_TOP_BOTTOM, 119.8125),
                             ])
    def test_soffit_height_pitch(self, actual, expected):
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.CATHEDRAL
        toolkit_state.scenario = Scenario.SOFFIT_HEIGHT_PITCH
        toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value = '10'
        toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = 10
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = actual
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length = 112
        toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length = 112
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        pitch_a_side = 12 * tan(toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value)
        pitch_c_side = 12 * tan(toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value)
        peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
        max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
        soffit_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length
        soffit_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length
        drip_edge_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        drip_edge_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
        c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
        assert to_nice_number(pitch_a_side, 2) == 10
        assert to_nice_number(pitch_c_side, 2) == 10
        assert to_nice_number(peak, 16) == 169
        assert to_nice_number(soffit_a_side, 16) == 112
        assert to_nice_number(soffit_c_side, 16) == 112
        assert to_nice_number(drip_edge_a_side, 16) == expected
        assert to_nice_number(drip_edge_c_side, 16) == expected
        assert to_nice_number(max_height, 16) == 178.125
        assert to_nice_number(a_wall_height, 16) == 120.3125
        assert to_nice_number(c_wall_height, 16) == 120.3125

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected",
                             [
                                 (EndCutType.UNCUT_TOP_BOTTOM, [111.375, 177.125, 119.6875]),
                                 (EndCutType.PLUMB_CUT_TOP_BOTTOM, [108, 177.4375, 116.8125]),
                             ])
    def test_drip_edge_peak_height(self, actual, expected):
        # Arrange
        # expected = [soffit (a,c), max_height, wall_heights (a,c)]
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.CATHEDRAL
        toolkit_state.scenario = Scenario.DRIP_EDGE_PEAK_HEIGHT
        toolkit_state.overhang.length = 10
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = actual
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length = 168
        toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length = 116
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        pitch_a_side = 12 * tan(toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value)
        pitch_c_side = 12 * tan(toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value)
        peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
        max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
        soffit_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length
        soffit_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length
        drip_edge_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        drip_edge_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
        c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
        assert to_nice_number(pitch_a_side, 2) == 10
        assert to_nice_number(pitch_c_side, 2) == 10
        assert to_nice_number(peak, 16) == 168
        assert to_nice_number(soffit_a_side, 16) == expected[0]
        assert to_nice_number(soffit_c_side, 16) == expected[0]
        assert to_nice_number(drip_edge_a_side, 16) == 116
        assert to_nice_number(drip_edge_c_side, 16) == 116
        assert to_nice_number(max_height, 16) == expected[1]
        assert to_nice_number(a_wall_height, 16) == expected[2]
        assert to_nice_number(c_wall_height, 16) == expected[2]

    @pytest.mark.integration
    @pytest.mark.parametrize("actual, expected",
                             [
                                 (EndCutType.UNCUT_TOP_BOTTOM, 112.8125),
                                 (EndCutType.PLUMB_CUT_TOP_BOTTOM, 116),
                             ])
    def test_drip_edge_pitch(self, actual, expected):
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.CATHEDRAL
        toolkit_state.scenario = Scenario.DRIP_EDGE_PITCH
        toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value = '10'
        toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = 10
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = actual
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length = 116
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        pitch_a_side = 12 * tan(toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value)
        pitch_c_side = 12 * tan(toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value)
        peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
        max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
        soffit_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length
        soffit_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length
        drip_edge_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        drip_edge_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
        a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
        c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
        assert to_nice_number(pitch_a_side, 2) == 10
        assert to_nice_number(pitch_c_side, 2) == 10
        assert to_nice_number(peak, 16) == 165.1875
        assert to_nice_number(soffit_a_side, 16) == 108.1875
        assert to_nice_number(soffit_c_side, 16) == 108.1875
        assert to_nice_number(drip_edge_a_side, 16) == expected
        assert to_nice_number(drip_edge_c_side, 16) == expected
        assert to_nice_number(max_height, 16) == 174.3125
        assert to_nice_number(a_wall_height, 16) == 116.5
        assert to_nice_number(c_wall_height, 16) == 116.5