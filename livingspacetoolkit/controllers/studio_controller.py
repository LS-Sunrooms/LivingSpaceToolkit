import logging

from livingspacetoolkit.views.studio_view import Studio
from livingspacetoolkit.models.toolkit_state_model import ToolkitState
from livingspacetoolkit.lib.livingspacetoolkit_enums import PitchType, SunroomType, RoofingType, EndCutType, Scenario
from livingspacetoolkit.utils.helpers import set_strikethrough

logger = logging.getLogger(__name__)


class StudioController:
    def __init__(self, view: Studio, toolkit_state: ToolkitState):
        self.toolkit_state = toolkit_state
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

    def handle_pitch_type_click(self, pitch_type: PitchType, sunroom: SunroomType) -> None:
        logger.debug(f"{sunroom.name} pitch radio button clicked for type {pitch_type.name}.")
        self.sunroom_roof.pitch.update_pitch_text(pitch_type, sunroom)

    def handle_roofing_type_click(self, roof_type: RoofingType) -> None:
        logger.debug(f"Studio roofing type set to {roof_type.name}.")
        self.toolkit_state.roofing_type = roof_type
        logger.info(f"Populating studio thickness combo box for {roof_type.name} roofing type.")
        self.sunroom_roof.populate_thickness_combo(roof_type)
        self.sunroom_roof.end_cuts.set_end_cuts_by_roof_type(roof_type)
        self.toolkit_state.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        self.set_fascia_checkbox()

    def handle_thickness_combo_index_change(self) -> None:
        thickness_index = self.sunroom_roof.thickness_combo.currentIndex()
        thickness_item = self.sunroom_roof.thickness_combo.itemData(thickness_index)
        thickness_text = self.sunroom_roof.thickness_combo.itemText(thickness_index)
        self.toolkit_state.thickness = thickness_item
        self.set_fascia_checkbox()
        if thickness_item is not None:
            logger.info(f"Setting thickness to {thickness_text}.")

    def handle_end_cuts_click(self, end_cut_type: EndCutType) -> None:
        logger.info(f"Setting Studio end cuts to {end_cut_type.name}.")
        self.toolkit_state.end_cuts = end_cut_type
        self.set_fascia_checkbox()

    def handle_fascia_click(self) -> None:
        fascia_state = self.sunroom_roof.fascia.isChecked()
        self.toolkit_state.fascia = fascia_state
        logger.info(f"Setting fascia to {fascia_state}.")

    def set_fascia_checkbox(self) -> None:
        if self.toolkit_state.roofing_type == RoofingType.ECO_GREEN and (
                self.toolkit_state.end_cuts == EndCutType.UNCUT_TOP_BOTTOM
                or self.toolkit_state.end_cuts == EndCutType.PLUMB_CUT_TOP):
            if self.toolkit_state.thickness == '6"':
                self.sunroom_roof.fascia.setEnabled(True)
                self.sunroom_roof.fascia.setChecked(True)
                set_strikethrough(self.sunroom_roof.fascia, False)
            else:
                self.sunroom_roof.fascia.setEnabled(False)
                self.sunroom_roof.fascia.setChecked(False)
                set_strikethrough(self.sunroom_roof.fascia, True)

        elif self.toolkit_state.roofing_type == RoofingType.ALUMINUM:
            self.sunroom_roof.fascia.setEnabled(True)
            self.sunroom_roof.fascia.setChecked(True)
            set_strikethrough(self.sunroom_roof.fascia, False)
        else:
            self.sunroom_roof.fascia.setEnabled(False)
            self.sunroom_roof.fascia.setChecked(False)
            set_strikethrough(self.sunroom_roof.fascia, True)
        fascia_state = self.sunroom_roof.fascia.isChecked()
        logger.info(f"Setting fascia to {fascia_state}.")

    def set_to_default(self) -> None:
        self.sunroom_roof.default_state()
        self.sunroom_wall.default_state()
        self.sunroom_floor.default_state()

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
