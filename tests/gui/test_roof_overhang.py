import pytest
from PySide6.QtCore import Qt


class TestStudioOverhang:

    @pytest.mark.gui
    @pytest.mark.integration
    def test_overhang_input(self, qtbot, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that overhang is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in overhang field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_roof.overhang_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_roof.overhang_edit, '10 in.')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_roof.overhang_edit, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_a.text() == '10 in.'
        assert main_window.toolkit_state.overhang.length == 10.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_overhang_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that overhang is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in overhang field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_roof.overhang_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_roof.overhang_edit, 'abc')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_roof.overhang_edit, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_a.text() == ''
        assert main_window.toolkit_state.overhang.length == 0.0


class TestCathedralOverhang:

    @pytest.mark.gui
    @pytest.mark.integration
    def test_overhang_input(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that overhang is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in overhang field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_roof.overhang_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_roof.overhang_edit, '10 in.')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_roof.overhang_edit, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_a.text() == '10 in.'
        assert main_window.toolkit_state.overhang.length == 10.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_overhang_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that overhang is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in overhang field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_roof.overhang_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_roof.overhang_edit, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_roof.overhang_edit, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_a.text() == ''
        assert main_window.toolkit_state.overhang.length == 0.0