import pytest

from PySide6.QtCore import Qt

from livingspacetoolkit.lib.toolkit_enums import LengthType, SunroomSide


class TestStudioWallHeights:

    @pytest.mark.gui
    @pytest.mark.integration
    def test_peak_height_input(self, qtbot, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio2.click()

        # Act: Enter text in peak height field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit.text() == '10 ft.'
        assert main_window.toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_peak_height_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio2.click()

        # Act: Enter text in peak height field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit, 'abc')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit.text() == ''
        assert main_window.toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_b_wall_height_input(self, qtbot, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio2.click()

        # Act: Enter text in b wall height field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit.text() == '10 ft.'
        assert main_window.toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_b_wall_height_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio2.click()

        # Act: Enter text in b wall height field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit, 'abc')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit.text() == ''
        assert main_window.toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_max_height_input(self, qtbot, main_window):
        # Arrange: Set tab to studio and scenario to MAX_HEIGHT_PITCH
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio3.click()

        # Act: Enter text in max height field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_wall.max_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_wall.max_height_edit, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_wall.max_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_edit.text() == '10 ft.'
        assert main_window.toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_max_height_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to studio and scenario to MAX_HEIGHT_PITCH
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio3.click()

        # Act: Enter text in max height field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_wall.max_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_wall.max_height_edit, 'abc')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_wall.max_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_edit.text() == ''
        assert main_window.toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_soffit_height_input(self, qtbot, main_window):
        # Arrange: Set tab to studio and scenario to SOFFIT_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio4.click()

        # Act: Enter text in soffit height field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit.text() == '10 ft.'
        assert main_window.toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_soffit_height_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to studio and scenario to SOFFIT_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio4.click()

        # Act: Enter text in soffit height field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit, 'abc')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit.text() == ''
        assert main_window.toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_drip_edge_height_input(self, qtbot, main_window):
        # Arrange: Set tab to studio and scenario to DRIP_EDGE_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio6.click()

        # Act: Enter text in drip edge height field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit.text() == '10 ft.'
        assert main_window.toolkit_state.wall_heights[(None, LengthType.DRIP_EDGE_HEIGHT)].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_drip_edge_height_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to studio and scenario to DRIP_EDGE_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio6.click()

        # Act: Enter text in drip edge height field
        with qtbot.waitSignal(main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit, 'abc')
            qtbot.keyClick(main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit.text() == ''
        assert main_window.toolkit_state.wall_heights[(None, LengthType.DRIP_EDGE_HEIGHT)].length == 0.0


class TestCathedralWallHeights:

    @pytest.mark.gui
    @pytest.mark.integration
    def test_peak_height_input(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio2.click()

        # Act: Enter text in peak height field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit.text() == '10 ft.'
        assert main_window.toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_peak_height_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio2.click()

        # Act: Enter text in peak height field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit.text() == ''
        assert main_window.toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_a_wall_height_input(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio2.click()

        # Act: Enter text in a wall height field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit.text() == '10 ft.'
        assert main_window.toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_a_wall_height_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio2.click()

        # Act: Enter text in a wall height field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit.text() == ''
        assert main_window.toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_c_wall_height_input(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio2.click()

        # Act: Enter text in c wall height field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit.text() == '10 ft.'
        assert main_window.toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_c_wall_height_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio2.click()

        # Act: Enter text in c wall height field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit.text() == ''
        assert main_window.toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_max_height_input(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to MAX_HEIGHT_PITCH
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio3.click()

        # Act: Enter text in max height field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit.text() == '10 ft.'
        assert main_window.toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_max_height_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to MAX_HEIGHT_PITCH
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio3.click()

        # Act: Enter text in max height field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit.text() == ''
        assert main_window.toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_a_side_soffit_height_input(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to SOFFIT_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio4.click()

        # Act: Enter text in a side soffit height field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit.text() == '10 ft.'
        assert main_window.toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_a_side_soffit_height_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to SOFFIT_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio4.click()

        # Act: Enter text in a side soffit height field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit.text() == ''
        assert main_window.toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_c_side_soffit_height_input(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to SOFFIT_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio4.click()

        # Act: Enter text in c side soffit height field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit.text() == '10 ft.'
        assert main_window.toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_c_side_soffit_height_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to SOFFIT_HEIGHT_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio4.click()

        # Act: Enter text in c side soffit height field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit.text() == ''
        assert main_window.toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length == 0.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_drip_edge_height_input(self, qtbot, main_window):
        # Arrange: Set tab to cathedral and scenario to DRIP_EDGE_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio6.click()

        # Act: Enter text in drip edge height field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit, '10 ft.')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit.text() == '10 ft.'
        assert main_window.toolkit_state.wall_heights[(None, LengthType.DRIP_EDGE_HEIGHT)].length == 120.0

    @pytest.mark.gui
    @pytest.mark.integration
    def test_drip_edge_height_input_error(self, qtbot, main_window, mock_warning):
        # Arrange: Set tab to cathedral and scenario to DRIP_EDGE_PEAK_HEIGHT
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio6.click()

        # Act: Enter text in drip edge height field
        with qtbot.waitSignal(main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit.editingFinished):
            qtbot.keyClicks(main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit, 'abc')
            qtbot.keyClick(main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit, Qt.Key.Key_Return)

        # Assert changes
        assert mock_warning["title"] == "WARNING"
        assert mock_warning["text"] == 'Invalid imperial format: abc'
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit.text() == ''
        assert main_window.toolkit_state.wall_heights[(None, LengthType.DRIP_EDGE_HEIGHT)].length == 0.0