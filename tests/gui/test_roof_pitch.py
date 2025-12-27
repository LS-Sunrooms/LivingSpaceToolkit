import pytest
from math import atan, radians
from PySide6.QtCore import Qt

from livingspacetoolkit.lib.toolkit_enums import PitchType, SunroomSide

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
        assert main_window.toolkit_state.pitch[SunroomSide.B_SIDE].pitch_type == PitchType.RATIO

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
        assert main_window.toolkit_state.pitch[SunroomSide.B_SIDE].pitch_type == PitchType.ANGLE

    @pytest.mark.gui
    @pytest.mark.integration
    def test_ratio_pitch_line_edit(self, qtbot, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()
        # Act: Select ratio and enter text
        main_window.tabs_view.studio_view.sunroom_roof.pitch.radio_ratio.click()
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input, '5')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input, Qt.Key.Key_Return)
        # Assert changes
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input.text() == '5'
        assert main_window.toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value == atan(5 / 12)

    @pytest.mark.gui
    @pytest.mark.integration
    def test_angle_pitch_line_edit(self, qtbot, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()
        # Act: Select angle and enter text
        main_window.tabs_view.studio_view.sunroom_roof.pitch.radio_angle.click()
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input, '15 deg')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input, Qt.Key.Key_Return)
        # Assert changes
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input.text() == '15 deg'
        assert main_window.toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value == radians(15)

    @pytest.mark.gui
    @pytest.mark.integration
    def test_ratio_pitch_line_edit_warning(self, qtbot,  main_window, mock_warning):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()
        # Act: Select ratio and enter text
        main_window.tabs_view.studio_view.sunroom_roof.pitch.radio_ratio.click()
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input, 'abc')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input, Qt.Key.Key_Return)
        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid number format: abc'
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input.text() == ''
        assert main_window.toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_angle_pitch_line_edit_warning(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()
        # Act: Select angle and enter text
        main_window.tabs_view.studio_view.sunroom_roof.pitch.radio_angle.click()
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input, 'abc')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input, Qt.Key.Key_Return)
        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid angle format: abc'
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.pitch_input.text() == ''
        assert main_window.toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value == 0.0


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
        assert main_window.toolkit_state.pitch[SunroomSide.A_SIDE].pitch_type == PitchType.RATIO

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
        assert main_window.toolkit_state.pitch[SunroomSide.C_SIDE].pitch_type == PitchType.RATIO

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
        assert main_window.toolkit_state.pitch[SunroomSide.A_SIDE].pitch_type == PitchType.ANGLE

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
        assert main_window.toolkit_state.pitch[SunroomSide.C_SIDE].pitch_type == PitchType.ANGLE

    @pytest.mark.gui
    @pytest.mark.integration
    def test_ratio_a_side_pitch_line_edit(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Act: Select ratio and enter text
        main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.radio_ratio.click()
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input, '5')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input, Qt.Key.Key_Return)
        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input.text() == '5'
        assert main_window.toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value == atan(5 / 12)

    @pytest.mark.gui
    @pytest.mark.integration
    def test_ratio_c_side_pitch_line_edit(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Act: Select ratio and enter text
        main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.radio_ratio.click()
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input, '5')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input, Qt.Key.Key_Return)
        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input.text() == '5'
        assert main_window.toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value == atan(5 / 12)

    @pytest.mark.gui
    @pytest.mark.integration
    def test_angle_a_side_pitch_line_edit(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Act: Select angle and enter text
        main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.radio_angle.click()
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input, '15 deg')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input, Qt.Key.Key_Return)
        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input.text() == '15 deg'
        assert main_window.toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value == radians(15)

    @pytest.mark.gui
    @pytest.mark.integration
    def test_angle_c_side_pitch_line_edit(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Act: Select angle and enter text
        main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.radio_angle.click()
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input, '15 deg')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input, Qt.Key.Key_Return)
        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input.text() == '15 deg'
        assert main_window.toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value == radians(15)

    @pytest.mark.gui
    @pytest.mark.integration
    def test_ratio_a_side_pitch_line_edit_warning(self, qtbot,  main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Act: Select ratio and enter text
        main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.radio_ratio.click()
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input, Qt.Key.Key_Return)
        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid number format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input.text() == ''
        assert main_window.toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_ratio_c_side_pitch_line_edit_warning(self, qtbot,  main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Act: Select ratio and enter text
        main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.radio_ratio.click()
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input, Qt.Key.Key_Return)
        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid number format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input.text() == ''
        assert main_window.toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_angle_a_side_pitch_line_edit_warning(self, qtbot,  main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Act: Select angle and enter text
        main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.radio_angle.click()
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input, Qt.Key.Key_Return)
        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid angle format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.pitch_input.text() == ''
        assert main_window.toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_angle_c_side_pitch_line_edit_warning(self, qtbot,  main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that pitch is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Act: Select angle and enter text
        main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.radio_angle.click()
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input, Qt.Key.Key_Return)
        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid angle format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.pitch_input.text() == ''
        assert main_window.toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value == 0.0
