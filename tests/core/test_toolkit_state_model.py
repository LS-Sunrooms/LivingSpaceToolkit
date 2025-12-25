import pytest
from contextlib import nullcontext as does_not_raise

from livingspacetoolkit.models import ToolkitStateModel
from livingspacetoolkit.lib.toolkit_enums import Scenario, RoofSide, RoofingType, SunroomType, EndCutType
from livingspacetoolkit.lib.toolkit_length import LengthType


class TestToolkitStateModel:

    @pytest.mark.unit
    def test_default_state(self):
        # Arrange
        toolkit_1 = ToolkitStateModel()
        toolkit_2 = ToolkitStateModel()
        # Act
        toolkit_2.sunroom_type = SunroomType.CATHEDRAL
        toolkit_2.scenario = Scenario.DRIP_EDGE_PITCH
        toolkit_2.pitch[RoofSide.A_SIDE].pitch_value = '5'
        toolkit_2.pitch[RoofSide.B_SIDE].pitch_value = '5'
        toolkit_2.overhang.length = '10'
        toolkit_2.roofing_type = RoofingType.ECO_GREEN
        toolkit_2.thickness.length = '3'
        toolkit_2.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit_2.wall_heights[LengthType.DRIP_EDGE_HEIGHT].length = "10'"
        toolkit_2.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit_2.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit_2.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        assert toolkit_1 != toolkit_2
        toolkit_2.default_state()
        assert toolkit_1 == toolkit_2

    @pytest.mark.unit
    def test_check_calculation_ready_exception(self):
        # Arrange
        toolkit = ToolkitStateModel()
        # Act: All inputs for selected scenario EXCEPT overhang. Comment it out to visually see that it was skipped.
        toolkit.sunroom_type = SunroomType.CATHEDRAL
        toolkit.scenario = Scenario.DRIP_EDGE_PITCH
        toolkit.pitch[RoofSide.A_SIDE].pitch_value = '5'
        toolkit.pitch[RoofSide.C_SIDE].pitch_value = '5'
        # toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.DRIP_EDGE_HEIGHT].length = "10'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with pytest.raises(TypeError):
            toolkit.check_calculation_ready()


class TestStudioToolkitStateModel:
    def test_wall_height_pitch_check_calculation_ready(self):
        # Arrange
        toolkit = ToolkitStateModel()
        toolkit.sunroom_type = SunroomType.STUDIO
        toolkit.scenario = Scenario.WALL_HEIGHT_PITCH
        toolkit.pitch[RoofSide.B_SIDE].pitch_value = '5'
        toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.B_WALL_HEIGHT].length = "10'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with does_not_raise():
            assert toolkit.check_calculation_ready() is None

    def test_wall_height_peak_height_check_calculation_ready(self):
        # Arrange
        toolkit = ToolkitStateModel()
        toolkit.sunroom_type = SunroomType.STUDIO
        toolkit.scenario = Scenario.WALL_HEIGHT_PEAK_HEIGHT
        toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.B_WALL_HEIGHT].length = "10'"
        toolkit.wall_heights[LengthType.PEAK_HEIGHT].length = "12'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with does_not_raise():
            assert toolkit.check_calculation_ready() is None

    def test_max_height_pitch_check_calculation_ready(self):
        # Arrange
        toolkit = ToolkitStateModel()
        toolkit.sunroom_type = SunroomType.STUDIO
        toolkit.scenario = Scenario.MAX_HEIGHT_PITCH
        toolkit.pitch[RoofSide.B_SIDE].pitch_value = '5'
        toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.MAX_HEIGHT].length = "13'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with does_not_raise():
            assert toolkit.check_calculation_ready() is None

    def test_soffit_height_peak_height_check_calculation_ready(self):
        # Arrange
        toolkit = ToolkitStateModel()
        toolkit.sunroom_type = SunroomType.STUDIO
        toolkit.scenario = Scenario.SOFFIT_HEIGHT_PEAK_HEIGHT
        toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.B_SIDE_SOFFIT_HEIGHT].length = "10'"
        toolkit.wall_heights[LengthType.PEAK_HEIGHT].length = "13'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with does_not_raise():
            assert toolkit.check_calculation_ready() is None

    def test_soffit_height_pitch_check_calculation_ready(self):
        # Arrange
        toolkit = ToolkitStateModel()
        toolkit.sunroom_type = SunroomType.STUDIO
        toolkit.scenario = Scenario.SOFFIT_HEIGHT_PITCH
        toolkit.pitch[RoofSide.B_SIDE].pitch_value = '5'
        toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.B_SIDE_SOFFIT_HEIGHT].length = "10'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with does_not_raise():
            assert toolkit.check_calculation_ready() is None

    def test_drip_edge_peak_height_check_calculation_ready(self):
        # Arrange
        toolkit = ToolkitStateModel()
        toolkit.sunroom_type = SunroomType.STUDIO
        toolkit.scenario = Scenario.DRIP_EDGE_PEAK_HEIGHT
        toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.DRIP_EDGE_HEIGHT].length = "10'"
        toolkit.wall_heights[LengthType.PEAK_HEIGHT].length = "13'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with does_not_raise():
            assert toolkit.check_calculation_ready() is None

    def test_drip_edge_pitch_check_calculation_ready(self):
        # Arrange
        toolkit = ToolkitStateModel()
        toolkit.sunroom_type = SunroomType.STUDIO
        toolkit.scenario = Scenario.DRIP_EDGE_PITCH
        toolkit.pitch[RoofSide.B_SIDE].pitch_value = '5'
        toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.DRIP_EDGE_HEIGHT].length = "10'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with does_not_raise():
            assert toolkit.check_calculation_ready() is None


class TestCathedralToolkitStateModel:
    def test_wall_height_pitch_check_calculation_ready(self):
        # Arrange
        toolkit = ToolkitStateModel()
        toolkit.sunroom_type = SunroomType.CATHEDRAL
        toolkit.scenario = Scenario.WALL_HEIGHT_PITCH
        toolkit.pitch[RoofSide.A_SIDE].pitch_value = '5'
        toolkit.pitch[RoofSide.C_SIDE].pitch_value = '5'
        toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.A_WALL_HEIGHT].length = "10'"
        toolkit.wall_heights[LengthType.C_WALL_HEIGHT].length = "10'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with does_not_raise():
            assert toolkit.check_calculation_ready() is None

    def test_wall_height_peak_height_check_calculation_ready(self):
        # Arrange
        toolkit = ToolkitStateModel()
        toolkit.sunroom_type = SunroomType.CATHEDRAL
        toolkit.scenario = Scenario.WALL_HEIGHT_PEAK_HEIGHT
        toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.A_WALL_HEIGHT].length = "10'"
        toolkit.wall_heights[LengthType.C_WALL_HEIGHT].length = "10'"
        toolkit.wall_heights[LengthType.PEAK_HEIGHT].length = "12'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with does_not_raise():
            assert toolkit.check_calculation_ready() is None

    def test_max_height_pitch_check_calculation_ready(self):
        # Arrange
        toolkit = ToolkitStateModel()
        toolkit.sunroom_type = SunroomType.CATHEDRAL
        toolkit.scenario = Scenario.MAX_HEIGHT_PITCH
        toolkit.pitch[RoofSide.A_SIDE].pitch_value = '5'
        toolkit.pitch[RoofSide.C_SIDE].pitch_value = '5'
        toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.MAX_HEIGHT].length = "13'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with does_not_raise():
            assert toolkit.check_calculation_ready() is None

    def test_soffit_height_peak_height_check_calculation_ready(self):
        # Arrange
        toolkit = ToolkitStateModel()
        toolkit.sunroom_type = SunroomType.CATHEDRAL
        toolkit.scenario = Scenario.SOFFIT_HEIGHT_PEAK_HEIGHT
        toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.A_SIDE_SOFFIT_HEIGHT].length = "10'"
        toolkit.wall_heights[LengthType.C_SIDE_SOFFIT_HEIGHT].length = "10'"
        toolkit.wall_heights[LengthType.PEAK_HEIGHT].length = "13'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with does_not_raise():
            assert toolkit.check_calculation_ready() is None

    def test_soffit_height_pitch_check_calculation_ready(self):
        # Arrange
        toolkit = ToolkitStateModel()
        toolkit.sunroom_type = SunroomType.CATHEDRAL
        toolkit.scenario = Scenario.SOFFIT_HEIGHT_PITCH
        toolkit.pitch[RoofSide.A_SIDE].pitch_value = '5'
        toolkit.pitch[RoofSide.C_SIDE].pitch_value = '5'
        toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.A_SIDE_SOFFIT_HEIGHT].length = "10'"
        toolkit.wall_heights[LengthType.C_SIDE_SOFFIT_HEIGHT].length = "10'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with does_not_raise():
            assert toolkit.check_calculation_ready() is None

    def test_drip_edge_peak_height_check_calculation_ready(self):
        # Arrange
        toolkit = ToolkitStateModel()
        toolkit.sunroom_type = SunroomType.CATHEDRAL
        toolkit.scenario = Scenario.DRIP_EDGE_PEAK_HEIGHT
        toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.DRIP_EDGE_HEIGHT].length = "10'"
        toolkit.wall_heights[LengthType.PEAK_HEIGHT].length = "13'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with does_not_raise():
            assert toolkit.check_calculation_ready() is None

    def test_drip_edge_pitch_check_calculation_ready(self):
        # Arrange
        toolkit = ToolkitStateModel()
        toolkit.sunroom_type = SunroomType.CATHEDRAL
        toolkit.scenario = Scenario.DRIP_EDGE_PITCH
        toolkit.pitch[RoofSide.A_SIDE].pitch_value = '5'
        toolkit.pitch[RoofSide.C_SIDE].pitch_value = '5'
        toolkit.overhang.length = '10'
        toolkit.roofing_type = RoofingType.ECO_GREEN
        toolkit.thickness.length = '3'
        toolkit.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit.wall_heights[LengthType.DRIP_EDGE_HEIGHT].length = "10'"
        toolkit.floor_walls[LengthType.A_WALL_WIDTH].length = "8'"
        toolkit.floor_walls[LengthType.B_WALL_WIDTH].length = "10'"
        toolkit.floor_walls[LengthType.C_WALL_WIDTH].length = "8'"
        # Assert
        with does_not_raise():
            assert toolkit.check_calculation_ready() is None
