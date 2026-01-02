from abc import ABC, abstractmethod
from typing import Protocol, Any

from livingspacetoolkit.config.log_config import logger
from livingspacetoolkit.models import ToolkitStateModel, RoofModel
from livingspacetoolkit.lib.toolkit_enums import (PitchType, SunroomType, RoofingType, EndCutType,
                                                  LengthType, SunroomSide)
from livingspacetoolkit.utils.helpers import set_strikethrough


class BaseSunroomProtocol(Protocol):
    view: Any
    sunroom_roof: Any
    sunroom_wall: Any
    sunroom_floor: Any
    toolkit_state: ToolkitStateModel
    roof_model: RoofModel


class BaseSunroomController(ABC, BaseSunroomProtocol):
    """Base controller for each sunroom type in the Tabs view (studio and cathedral for now). This class is inherited."""
    @abstractmethod
    def update_to_scenario(self) -> None:
        pass

    def set_to_default(self) -> None:
        logger.debug(f"Setting {self.toolkit_state.sunroom_type.name} roof tab to default state.")
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
            if self.toolkit_state.thickness.length == 6:
                self.sunroom_roof.fascia.setEnabled(True)
                self.sunroom_roof.fascia.setChecked(True)
                self.toolkit_state.fascia = True
                set_strikethrough(self.sunroom_roof.fascia, False)
            else:
                self.sunroom_roof.fascia.setEnabled(False)
                self.sunroom_roof.fascia.setChecked(False)
                self.toolkit_state.fascia = False
                set_strikethrough(self.sunroom_roof.fascia, True)

        elif self.toolkit_state.roofing_type == RoofingType.ALUMINUM:
            self.sunroom_roof.fascia.setEnabled(True)
            self.sunroom_roof.fascia.setChecked(True)
            self.toolkit_state.fascia = True
            set_strikethrough(self.sunroom_roof.fascia, False)
        else:
            self.sunroom_roof.fascia.setEnabled(False)
            self.sunroom_roof.fascia.setChecked(False)
            self.toolkit_state.fascia = False
            set_strikethrough(self.sunroom_roof.fascia, True)
        fascia_state = self.sunroom_roof.fascia.isChecked()
        logger.info(f"Setting fascia to {fascia_state}.")

    def handle_pitch_type_click(self, pitch_type: PitchType, sunroom: SunroomType, pitch_side: SunroomSide) -> None:
        logger.debug(f"{sunroom.name} pitch radio button clicked for type {pitch_type.name}.")
        match pitch_side:
            case SunroomSide.A_SIDE:
                self.sunroom_roof.pitch_a.update_pitch_text(pitch_type, sunroom)
            case SunroomSide.B_SIDE:
                self.sunroom_roof.pitch.update_pitch_text(pitch_type, sunroom)
            case SunroomSide.C_SIDE:
                self.sunroom_roof.pitch_c.update_pitch_text(pitch_type, sunroom)
        self.toolkit_state.pitch[pitch_side].pitch_type = pitch_type

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
        if self.sunroom_roof.thickness_combo.currentIndex() != -1: # Index of -1 happens when combo box is cleared
            thickness_index = self.sunroom_roof.thickness_combo.currentIndex()
            thickness_item = self.sunroom_roof.thickness_combo.itemData(thickness_index)
            thickness_text = self.sunroom_roof.thickness_combo.itemText(thickness_index)
            try:
                self.toolkit_state.thickness.length = thickness_item
            except ValueError:
                logger.warning('Roofing Type changed')
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

    def handle_line_edit_finish_edit(self, sunroom_side: SunroomSide | None, length_type: LengthType = None) -> None:
        match length_type:
            case None:
                widget_text = self.sunroom_roof.pitch_dict[sunroom_side].text()
                try:
                    self.toolkit_state.pitch[sunroom_side].pitch_value = widget_text
                    logger.info(
                        f"{self.toolkit_state.sunroom_type.name} {sunroom_side.name} pitch input saved as: {widget_text}.")
                except ValueError as err:
                    self.view.show_warning(str(err))
                    logger.warning(f"Invalid {sunroom_side.name} pitch input: {widget_text}")
                    self.sunroom_roof.pitch_dict[sunroom_side].clear()
            case LengthType.WALL_WIDTH:
                widget_text = self.sunroom_floor.wall_dict[sunroom_side].text()
                try:
                    self.toolkit_state.floor_walls[sunroom_side].length = widget_text
                    logger.info(f"{self.toolkit_state.sunroom_type.name} {sunroom_side.name} wall width set to: {widget_text}.")
                except ValueError as err:
                    self.view.show_warning(str(err))
                    logger.warning(f"Invalid {sunroom_side.name} wall width input: {widget_text}")
                    self.sunroom_floor.wall_dict[sunroom_side].clear()
            case LengthType.OVERHANG:
                widget_text = self.sunroom_roof.overhang_edit.text()
                try:
                    self.toolkit_state.overhang.length = widget_text
                    logger.info(f"{self.toolkit_state.sunroom_type.name} overhang set to: {widget_text}.")
                except ValueError as err:
                    self.view.show_warning(str(err))
                    logger.warning(f"Invalid {length_type.name} input: {widget_text}")
                    self.sunroom_roof.overhang_edit.clear()
            case LengthType.THICKNESS | LengthType.PANEL | LengthType.HANG_RAIL | LengthType.FASCIA:
                pass
            case _:
                widget_text = self.sunroom_wall.wall_height_dict[(sunroom_side, length_type)].text()
                try:
                    if sunroom_side == SunroomSide.A_SIDE and length_type == LengthType.DRIP_EDGE_HEIGHT:
                        # There's only 1 input for cathedral drip edge but two sides so add the other side here for now
                        self.toolkit_state.wall_heights[(SunroomSide.C_SIDE, length_type)].length = widget_text
                    self.toolkit_state.wall_heights[(sunroom_side, length_type)].length = widget_text
                    if sunroom_side is None:
                        logger.info(f"{self.toolkit_state.sunroom_type.name} {length_type.name} "
                                    f"set to: {widget_text}.")
                    else:
                        logger.info(f"{self.toolkit_state.sunroom_type.name} {sunroom_side.name} {length_type.name} set"
                                    f" to: {widget_text}.")
                except ValueError as err:
                    self.view.show_warning(str(err))
                    if sunroom_side is None:
                        logger.warning(f"Invalid {length_type.name} input: {widget_text}")
                    else:
                        logger.warning(f"Invalid {sunroom_side.name} {length_type.name} input: {widget_text}")
                    self.sunroom_wall.wall_height_dict[(sunroom_side, length_type)].clear()
