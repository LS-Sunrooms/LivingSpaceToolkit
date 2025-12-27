import pytest
from PySide6.QtCore import Qt

from livingspacetoolkit.lib.toolkit_enums import SunroomSide


class TestStudioFloorPlan:

    @pytest.mark.gui
    @pytest.mark.integration
    def test_a_wall_width_input(self, qtbot, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that floor plan input is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in A wall width field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_floor.wall_a.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_floor.wall_a, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_floor.wall_a, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_a.text() == '10 ft.'
        assert main_window.toolkit_state.floor_walls[SunroomSide.A_SIDE].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_a_wall_width_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that floor plan input is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in A wall width field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_floor.wall_a.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_floor.wall_a, 'abc')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_floor.wall_a, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_a.text() == ''
        assert main_window.toolkit_state.floor_walls[SunroomSide.A_SIDE].length == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_b_wall_width_input(self, qtbot, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that floor plan input is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in B wall width field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_floor.wall_b.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_floor.wall_b, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_floor.wall_b, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_b.text() == '10 ft.'
        assert main_window.toolkit_state.floor_walls[SunroomSide.B_SIDE].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_b_wall_width_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that floor plan input is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in B wall width field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_floor.wall_b.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_floor.wall_b, 'abc')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_floor.wall_b, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_b.text() == ''
        assert main_window.toolkit_state.floor_walls[SunroomSide.B_SIDE].length == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_c_wall_width_input(self, qtbot, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that floor plan input is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in C wall width field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_floor.wall_c.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_floor.wall_c, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_floor.wall_c, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_c.text() == '10 ft.'
        assert main_window.toolkit_state.floor_walls[SunroomSide.C_SIDE].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_c_wall_width_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that floor plan input is enabled
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in C wall width field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_floor.wall_c.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_floor.wall_c, 'abc')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_floor.wall_c, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_c.text() == ''
        assert main_window.toolkit_state.floor_walls[SunroomSide.C_SIDE].length == 0.0


class TestCathedralFloorPlan:

    @pytest.mark.gui
    @pytest.mark.integration
    def test_a_wall_width_input(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that floor plan input is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in A wall width field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_floor.wall_a.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_floor.wall_a, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_floor.wall_a, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_a.text() == '10 ft.'
        assert main_window.toolkit_state.floor_walls[SunroomSide.A_SIDE].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_a_wall_width_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that floor plan input is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in A wall width field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_floor.wall_a.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_floor.wall_a, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_floor.wall_a, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_a.text() == ''
        assert main_window.toolkit_state.floor_walls[SunroomSide.A_SIDE].length == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_b_wall_width_input(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that floor plan input is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in B wall width field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_floor.wall_b.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_floor.wall_b, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_floor.wall_b, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_b.text() == '10 ft.'
        assert main_window.toolkit_state.floor_walls[SunroomSide.B_SIDE].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_b_wall_width_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that floor plan input is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in B wall width field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_floor.wall_b.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_floor.wall_b, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_floor.wall_b, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_b.text() == ''
        assert main_window.toolkit_state.floor_walls[SunroomSide.B_SIDE].length == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_c_wall_width_input(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that floor plan input is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in C wall width field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_floor.wall_c.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_floor.wall_c, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_floor.wall_c, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_c.text() == '10 ft.'
        assert main_window.toolkit_state.floor_walls[SunroomSide.C_SIDE].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_c_wall_width_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH so that floor plan input is enabled
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()

        # Act: Enter text in C wall width field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_floor.wall_c.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_floor.wall_c, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_floor.wall_c, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_c.text() == ''
        assert main_window.toolkit_state.floor_walls[SunroomSide.C_SIDE].length == 0.0
