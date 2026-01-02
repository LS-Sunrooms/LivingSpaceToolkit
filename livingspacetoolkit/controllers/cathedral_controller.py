from livingspacetoolkit.config.log_config import logger
from livingspacetoolkit.views import CathedralView
from livingspacetoolkit.models import ToolkitStateModel, RoofModel
from livingspacetoolkit.lib.toolkit_enums import (PitchType, SunroomType, RoofingType, EndCutType, Scenario,
                                                  SunroomSide, LengthType)
from livingspacetoolkit.utils.helpers import set_strikethrough
from .base_sunroom_controller import BaseSunroomController



class CathedralController(BaseSunroomController):
    """Controller for the cathedral view. Handles signals from the view and updates the toolkit_state_model."""
    def __init__(self, view: CathedralView, toolkit_state: ToolkitStateModel):
        self.toolkit_state = toolkit_state
        self.roof_model: RoofModel = RoofModel(toolkit_state)

        self.view = view
        self.sunroom_roof = view.sunroom_roof
        self.sunroom_wall = view.sunroom_wall
        self.sunroom_floor = view.sunroom_floor

        # Connect signals
        # Roof view signals
        self.sunroom_roof.pitch_a.radio_ratio.clicked.connect(
            lambda: self.handle_pitch_type_click(PitchType.RATIO, SunroomType.CATHEDRAL, SunroomSide.A_SIDE))
        self.sunroom_roof.pitch_a.radio_angle.clicked.connect(
            lambda: self.handle_pitch_type_click(PitchType.ANGLE, SunroomType.CATHEDRAL, SunroomSide.A_SIDE))
        self.sunroom_roof.pitch_a.pitch_input.editingFinished.connect(
            lambda: self.handle_line_edit_finish_edit(SunroomSide.A_SIDE))
        self.sunroom_roof.pitch_c.radio_ratio.clicked.connect(
            lambda: self.handle_pitch_type_click(PitchType.RATIO, SunroomType.CATHEDRAL, SunroomSide.C_SIDE))
        self.sunroom_roof.pitch_c.radio_angle.clicked.connect(
            lambda: self.handle_pitch_type_click(PitchType.ANGLE, SunroomType.CATHEDRAL, SunroomSide.C_SIDE))
        self.sunroom_roof.pitch_c.pitch_input.editingFinished.connect(
            lambda: self.handle_line_edit_finish_edit(SunroomSide.C_SIDE))
        self.sunroom_roof.overhang_edit.editingFinished.connect(
            lambda: self.handle_line_edit_finish_edit(None, LengthType.OVERHANG))
        self.sunroom_roof.roofing_type.radio_al.clicked.connect(
            lambda: self.handle_roofing_type_click(RoofingType.ALUMINUM))
        self.sunroom_roof.roofing_type.radio_eco.clicked.connect(
            lambda: self.handle_roofing_type_click(RoofingType.ECO_GREEN))
        self.sunroom_roof.thickness_combo.currentIndexChanged.connect(self.handle_thickness_combo_index_change)
        self.sunroom_roof.end_cuts.radio_endcut1.clicked.connect(
            lambda: self.handle_end_cuts_click(EndCutType.UNCUT_TOP_BOTTOM))
        self.sunroom_roof.end_cuts.radio_endcut2.clicked.connect(
            lambda: self.handle_end_cuts_click(EndCutType.PLUMB_CUT_TOP_BOTTOM))
        self.sunroom_roof.end_cuts.radio_endcut3.clicked.connect(
            lambda: self.handle_end_cuts_click(EndCutType.PLUMB_CUT_TOP))
        self.sunroom_roof.fascia.clicked.connect(self.handle_fascia_click)
        # Floor view signals
        self.sunroom_floor.wall_a.editingFinished.connect(
            lambda: self.handle_line_edit_finish_edit(SunroomSide.A_SIDE, LengthType.WALL_WIDTH))
        self.sunroom_floor.wall_b.editingFinished.connect(
            lambda: self.handle_line_edit_finish_edit(SunroomSide.B_SIDE, LengthType.WALL_WIDTH))
        self.sunroom_floor.wall_c.editingFinished.connect(
            lambda: self.handle_line_edit_finish_edit(SunroomSide.C_SIDE, LengthType.WALL_WIDTH))
        # Wall view signals
        self.sunroom_wall.peak_height_edit.editingFinished.connect(
            lambda: self.handle_line_edit_finish_edit(None, LengthType.PEAK_HEIGHT))
        self.sunroom_wall.max_height_edit.editingFinished.connect(
            lambda: self.handle_line_edit_finish_edit(None, LengthType.MAX_HEIGHT))
        self.sunroom_wall.a_wall_height_edit.editingFinished.connect(
            lambda: self.handle_line_edit_finish_edit(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT))
        self.sunroom_wall.c_wall_height_edit.editingFinished.connect(
            lambda: self.handle_line_edit_finish_edit(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT))
        self.sunroom_wall.soffit_height_a_edit.editingFinished.connect(
            lambda: self.handle_line_edit_finish_edit(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT))
        self.sunroom_wall.soffit_height_c_edit.editingFinished.connect(
            lambda: self.handle_line_edit_finish_edit(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT))
        self.sunroom_wall.drip_edge_height_edit.editingFinished.connect(
            lambda: self.handle_line_edit_finish_edit(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT))

    def update_to_scenario(self):
        self.set_to_default()
        self.sunroom_roof.enable_except_pitch()
        self.sunroom_floor.enable_floor_input()
        match self.toolkit_state.scenario:
            case Scenario.WALL_HEIGHT_PITCH:
                self.sunroom_roof.pitch_a.enabled_state(self.toolkit_state.sunroom_type)
                self.sunroom_roof.pitch_c.enabled_state(self.toolkit_state.sunroom_type)
                set_strikethrough(self.sunroom_wall.a_wall_height_label, False)
                self.sunroom_wall.a_wall_height_edit.setEnabled(True)
                set_strikethrough(self.sunroom_wall.c_wall_height_label, False)
                self.sunroom_wall.c_wall_height_edit.setEnabled(True)
            case Scenario.WALL_HEIGHT_PEAK_HEIGHT:
                set_strikethrough(self.sunroom_wall.peak_height_label, False)
                self.sunroom_wall.peak_height_edit.setEnabled(True)
                set_strikethrough(self.sunroom_wall.a_wall_height_label, False)
                self.sunroom_wall.a_wall_height_edit.setEnabled(True)
                set_strikethrough(self.sunroom_wall.c_wall_height_label, False)
                self.sunroom_wall.c_wall_height_edit.setEnabled(True)
            case Scenario.MAX_HEIGHT_PITCH:
                self.sunroom_roof.pitch_a.enabled_state(self.toolkit_state.sunroom_type)
                self.sunroom_roof.pitch_c.enabled_state(self.toolkit_state.sunroom_type)
                set_strikethrough(self.sunroom_wall.max_height_label, False)
                self.sunroom_wall.max_height_edit.setEnabled(True)
            case Scenario.SOFFIT_HEIGHT_PEAK_HEIGHT:
                set_strikethrough(self.sunroom_wall.peak_height_label, False)
                self.sunroom_wall.peak_height_edit.setEnabled(True)
                set_strikethrough(self.sunroom_wall.soffit_height_a_label, False)
                self.sunroom_wall.soffit_height_a_edit.setEnabled(True)
                set_strikethrough(self.sunroom_wall.soffit_height_c_label, False)
                self.sunroom_wall.soffit_height_c_edit.setEnabled(True)
            case Scenario.SOFFIT_HEIGHT_PITCH:
                self.sunroom_roof.pitch_a.enabled_state(self.toolkit_state.sunroom_type)
                self.sunroom_roof.pitch_c.enabled_state(self.toolkit_state.sunroom_type)
                set_strikethrough(self.sunroom_wall.soffit_height_a_label, False)
                self.sunroom_wall.soffit_height_a_edit.setEnabled(True)
                set_strikethrough(self.sunroom_wall.soffit_height_c_label, False)
                self.sunroom_wall.soffit_height_c_edit.setEnabled(True)
            case Scenario.DRIP_EDGE_PEAK_HEIGHT:
                set_strikethrough(self.sunroom_wall.peak_height_label, False)
                self.sunroom_wall.peak_height_edit.setEnabled(True)
                set_strikethrough(self.sunroom_wall.drip_edge_height_label, False)
                self.sunroom_wall.drip_edge_height_edit.setEnabled(True)
            case Scenario.DRIP_EDGE_PITCH:
                self.sunroom_roof.pitch_a.enabled_state(self.toolkit_state.sunroom_type)
                self.sunroom_roof.pitch_c.enabled_state(self.toolkit_state.sunroom_type)
                set_strikethrough(self.sunroom_wall.drip_edge_height_label, False)
                self.sunroom_wall.drip_edge_height_edit.setEnabled(True)
        self.toolkit_state.default_state(sunroom= SunroomType.CATHEDRAL, scenario=self.toolkit_state.scenario)
