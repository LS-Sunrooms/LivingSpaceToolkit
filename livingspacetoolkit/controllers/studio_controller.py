import logging

from livingspacetoolkit.views import StudioView
from livingspacetoolkit.models import ToolkitStateModel, RoofModel
from livingspacetoolkit.lib.livingspacetoolkit_enums import PitchType, SunroomType, RoofingType, EndCutType, Scenario
from livingspacetoolkit.utils.helpers import set_strikethrough
from .base_sunroom_controller import BaseSunroomController

logger = logging.getLogger(__name__)


class StudioController(BaseSunroomController):
    def __init__(self, view: StudioView, toolkit_state: ToolkitStateModel):
        self.toolkit_state = toolkit_state
        self.roof_model: RoofModel = RoofModel(toolkit_state)

        self.sunroom_roof = view.sunroom_roof
        self.sunroom_wall = view.sunroom_wall
        self.sunroom_floor = view.sunroom_floor

        # Connect signals
        self.sunroom_roof.pitch.radio_ratio.clicked.connect(
            lambda: self.handle_pitch_type_click(PitchType.RATIO, SunroomType.STUDIO))
        self.sunroom_roof.pitch.radio_angle.clicked.connect(
            lambda: self.handle_pitch_type_click(PitchType.ANGLE, SunroomType.STUDIO))
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
        self.sunroom_floor.wall_a.editingFinished.connect(self.handle_a_wall_finish_edit)


    def handle_a_wall_finish_edit(self) -> None:
        # TODO: A model should verify text
        self.toolkit_state.floor_walls.update({"a_wall": self.sunroom_floor.wall_a.text()})
        logger.debug(f"Studio A Wall set to: {self.sunroom_floor.wall_a.text()}.")

    def update_to_scenario(self) -> None:
        self.set_to_default()
        self.sunroom_roof.enable_except_pitch()
        match self.toolkit_state.scenario:
            case Scenario.WALL_HEIGHT_PITCH:
                self.sunroom_roof.pitch.enabled_state(self.toolkit_state.sunroom_type)
                set_strikethrough(self.sunroom_wall.b_wall_height_label, False)
                self.sunroom_wall.b_wall_height_edit.setEnabled(True)
            case Scenario.WALL_HEIGHT_PEAK_HEIGHT:
                set_strikethrough(self.sunroom_wall.peak_height_label, False)
                self.sunroom_wall.peak_height_edit.setEnabled(True)
                set_strikethrough(self.sunroom_wall.b_wall_height_label, False)
                self.sunroom_wall.b_wall_height_edit.setEnabled(True)
            case Scenario.MAX_HEIGHT_PITCH:
                self.sunroom_roof.pitch.enabled_state(self.toolkit_state.sunroom_type)
                set_strikethrough(self.sunroom_wall.max_height_label, False)
                self.sunroom_wall.max_height_edit.setEnabled(True)
            case Scenario.SOFFIT_HEIGHT_PEAK_HEIGHT:
                set_strikethrough(self.sunroom_wall.peak_height_label, False)
                self.sunroom_wall.peak_height_edit.setEnabled(True)
                set_strikethrough(self.sunroom_wall.soffit_height_label, False)
                self.sunroom_wall.soffit_height_edit.setEnabled(True)
            case Scenario.SOFFIT_HEIGHT_PITCH:
                self.sunroom_roof.pitch.enabled_state(self.toolkit_state.sunroom_type)
                set_strikethrough(self.sunroom_wall.soffit_height_label, False)
                self.sunroom_wall.soffit_height_edit.setEnabled(True)
            case Scenario.DRIP_EDGE_PEAK_HEIGHT:
                set_strikethrough(self.sunroom_wall.peak_height_label, False)
                self.sunroom_wall.peak_height_edit.setEnabled(True)
                set_strikethrough(self.sunroom_wall.drip_edge_height_label, False)
                self.sunroom_wall.drip_edge_height_edit.setEnabled(True)
            case Scenario.DRIP_EDGE_PITCH:
                self.sunroom_roof.pitch.enabled_state(self.toolkit_state.sunroom_type)
                set_strikethrough(self.sunroom_wall.drip_edge_height_label, False)
                self.sunroom_wall.drip_edge_height_edit.setEnabled(True)
