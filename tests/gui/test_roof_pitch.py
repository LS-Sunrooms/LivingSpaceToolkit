import pytest

from livingspacetoolkit.lib.toolkit_enums import PitchType, RoofSide

class TestStudioRoofPitch:

    @pytest.mark.gui
    @pytest.mark.integration
    def test_pitch_radio_changed_to_ratio(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()
        # Act: Ratio is selected by default so select angle then ratio again
        main_window.tabs_view.studio_view.sunroom_roof.pitch.radio_angle.click()
        main_window.tabs_view.studio_view.sunroom_roof.pitch.radio_ratio.click()
        # Assert: The text should change
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input_label.text() == "/12 in."
        assert main_window.toolkit_state.pitch[RoofSide.B_SIDE].pitch_type == PitchType.RATIO

    @pytest.mark.gui
    @pytest.mark.integration
    def test_pitch_radio_changed_to_angle(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()
        # Act: Select angle
        main_window.tabs_view.studio_view.sunroom_roof.pitch.radio_angle.click()
        # Assert: The text should change
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input_label.text() == u"deg(\N{DEGREE SIGN})"
        assert main_window.toolkit_state.pitch[RoofSide.B_SIDE].pitch_type == PitchType.ANGLE

    @pytest.mark.gui
    @pytest.mark.integration
    def test_ratio_pitch_line_edit(self, main_window):
        pass

    @pytest.mark.gui
    @pytest.mark.integration
    def test_angle_pitch_line_edit(self, main_window):
        pass

    @pytest.mark.gui
    @pytest.mark.integration
    def test_pitch_line_edit_(self, main_window):
        pass


class TestCathedralRoofPitch:

    @pytest.mark.gui
    @pytest.mark.integration
    def test_a_side_pitch_radio_changed_to_ratio(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Act: Ratio is selected by default so select angle then ratio again
        main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.radio_angle.click()
        main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.radio_ratio.click()
        # Assert: The text should change
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input_label.text() == "/12 in."
        assert main_window.toolkit_state.pitch[RoofSide.A_SIDE].pitch_type == PitchType.RATIO

    @pytest.mark.gui
    @pytest.mark.integration
    def test_c_side_pitch_radio_changed_to_ratio(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Act: Ratio is selected by default so select angle then ratio again
        main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.radio_angle.click()
        main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.radio_ratio.click()
        # Assert: The text should change
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input_label.text() == "/12 in."
        assert main_window.toolkit_state.pitch[RoofSide.C_SIDE].pitch_type == PitchType.RATIO

    @pytest.mark.gui
    @pytest.mark.integration
    def test_a_side_pitch_radio_changed_to_angle(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Act: Select angle
        main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.radio_angle.click()
        # Assert: The text should change
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input_label.text() == u"deg(\N{DEGREE SIGN})"
        assert main_window.toolkit_state.pitch[RoofSide.A_SIDE].pitch_type == PitchType.ANGLE

    @pytest.mark.gui
    @pytest.mark.integration
    def test_c_side_pitch_radio_changed_to_angle(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Act: Select angle
        main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.radio_angle.click()
        # Assert: The text should change
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input_label.text() == u"deg(\N{DEGREE SIGN})"
        assert main_window.toolkit_state.pitch[RoofSide.C_SIDE].pitch_type == PitchType.ANGLE

    @pytest.mark.gui
    @pytest.mark.integration
    def test_ratio_a_side_pitch_line_edit(self, main_window):
        pass

    @pytest.mark.gui
    @pytest.mark.integration
    def test_ratio_c_side_pitch_line_edit(self, main_window):
        pass

    @pytest.mark.gui
    @pytest.mark.integration
    def test_angle_a_side_pitch_line_edit(self, main_window):
        pass

    @pytest.mark.gui
    @pytest.mark.integration
    def test_angle_c_side_pitch_line_edit(self, main_window):
        pass

    @pytest.mark.gui
    @pytest.mark.integration
    def test_a_side_pitch_line_edit_(self, main_window):
        pass

    @pytest.mark.gui
    @pytest.mark.integration
    def test_c_side_pitch_line_edit_(self, main_window):
        pass