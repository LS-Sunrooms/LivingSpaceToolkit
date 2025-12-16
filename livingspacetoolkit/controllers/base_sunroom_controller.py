import logging

from interfaces.base_tab_view import BaseTabView
from livingspacetoolkit.models import ToolkitStateModel, RoofModel
from livingspacetoolkit.lib.livingspacetoolkit_enums import PitchType, SunroomType, RoofingType, EndCutType, Scenario
from livingspacetoolkit.utils.helpers import set_strikethrough

logger = logging.getLogger(__name__)


class BaseSunroomController:
    def __init__(self, view, toolkit_state: ToolkitStateModel):
        self.toolkit_state = toolkit_state
        self.roof_model: RoofModel = RoofModel(toolkit_state)

        self.sunroom_roof = view.sunroom_roof
        self.sunroom_wall = view.sunroom_wall
        self.sunroom_floor = view.sunroom_floor

    def set_to_default(self) -> None:
        self.sunroom_roof.default_state()
        self.sunroom_wall.default_state()
        self.sunroom_floor.default_state()

    def set_end_cuts_by_roof_type(self, roof_type: RoofingType) -> None:
        logger.debug(f"Enabling/Disabling end cuts for roofing type {roof_type.name}")
        match roof_type:
            case RoofingType.ECO_GREEN:
                self.sunroom_roof.end_cuts.radio_endcut1.setEnabled(True)
                set_strikethrough(self.sunroom_roof.end_cuts.radio_endcut1, False)
                self.sunroom_roof.end_cuts.radio_endcut2.setEnabled(True)
                set_strikethrough(self.sunroom_roof.end_cuts.radio_endcut2, False)
                self.sunroom_roof.end_cuts.radio_endcut3.setEnabled(True)
                set_strikethrough(self.sunroom_roof.end_cuts.radio_endcut3, False)
            case RoofingType.ALUMINUM:
                self.sunroom_roof.end_cuts.radio_endcut1.setEnabled(True)
                set_strikethrough(self.sunroom_roof.end_cuts.radio_endcut1, False)
                self.sunroom_roof.end_cuts.radio_endcut2.setEnabled(False)
                set_strikethrough(self.sunroom_roof.end_cuts.radio_endcut2, True)
                self.sunroom_roof.end_cuts.radio_endcut3.setEnabled(False)
                set_strikethrough(self.sunroom_roof.end_cuts.radio_endcut3, True)
        self.sunroom_roof.end_cuts.radio_endcut1.setChecked(True)

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

    def handle_pitch_type_click(self, pitch_type: PitchType, sunroom: SunroomType) -> None:
        logger.debug(f"{sunroom.name} pitch radio button clicked for type {pitch_type.name}.")
        self.sunroom_roof.pitch.update_pitch_text(pitch_type, sunroom)

    def handle_roofing_type_click(self, roof_type: RoofingType) -> None:
        logger.debug(f"{self.toolkit_state.sunroom_type.name} roofing type set to {roof_type.name}.")
        self.toolkit_state.roofing_type = roof_type
        combo_item_dict = self.roof_model.set_thickness_combo_dict(roof_type)
        logger.info(f"Populating {self.toolkit_state.sunroom_type.name} thickness combo box for {roof_type.name} "
                    f"roofing type.")
        self.sunroom_roof.thickness_combo.clear()
        for item in combo_item_dict:
            self.sunroom_roof.thickness_combo.addItem(item, userData=combo_item_dict[item])
        self.sunroom_roof.thickness_combo.setCurrentIndex(0)
        self.set_end_cuts_by_roof_type(roof_type)
        self.toolkit_state.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        self.set_fascia_checkbox()

    def handle_thickness_combo_index_change(self) -> None:
        thickness_index = self.sunroom_roof.thickness_combo.currentIndex()
        thickness_item = self.sunroom_roof.thickness_combo.itemData(thickness_index)
        thickness_text = self.sunroom_roof.thickness_combo.itemText(thickness_index)
        self.toolkit_state.thickness = thickness_item
        self.set_fascia_checkbox()
        if thickness_item is not None:
            logger.info(f"Setting {self.toolkit_state.sunroom_type.name} thickness to {thickness_text}.")

    def handle_end_cuts_click(self, end_cut_type: EndCutType) -> None:
        logger.info(f"Setting {self.toolkit_state.sunroom_type.name} end cuts to {end_cut_type.name}.")
        self.toolkit_state.end_cuts = end_cut_type
        self.set_fascia_checkbox()

    def handle_fascia_click(self) -> None:
        fascia_state = self.sunroom_roof.fascia.isChecked()
        self.toolkit_state.fascia = fascia_state
        logger.info(f"Setting {self.toolkit_state.sunroom_type.name} fascia to {fascia_state}.")