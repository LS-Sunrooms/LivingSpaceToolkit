import logging

from typing import Dict
from PySide6.QtWidgets import QGroupBox, QRadioButton, QVBoxLayout, QButtonGroup
from livingspacetoolkit.utils.helpers import temporary_change, set_strikethrough
from livingspacetoolkit.lib.livingspacetoolkit_enums import RoofingType

logger = logging.getLogger(__name__)


class RoofingTypeView(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setTitle("Roofing Type")
        self.radio_group: QButtonGroup = QButtonGroup()

        self.radio_eco: QRadioButton = QRadioButton()
        self.radio_eco.setObjectName("radio_eco")
        self.radio_eco.setChecked(False)
        self.radio_eco.setEnabled(True)
        self.radio_eco.setText("EcoGreen")
        self.radio_group.addButton(self.radio_eco)

        self.radio_al: QRadioButton = QRadioButton()
        self.radio_al.setObjectName("radio_al")
        self.radio_al.setChecked(False)
        self.radio_al.setEnabled(True)
        self.radio_al.setText("Aluminum")
        self.radio_group.addButton(self.radio_al)

        layout: QVBoxLayout = QVBoxLayout()
        layout.addWidget(self.radio_eco)
        layout.addWidget(self.radio_al)

        self.setLayout(layout)

    @temporary_change('radio_group', 'setExclusive', False, True)
    def default_state(self) -> None:
        logger.debug("Setting roofing type to default state.")
        self.radio_eco.setChecked(False)
        set_strikethrough(self.radio_eco, True)
        self.radio_al.setChecked(False)
        set_strikethrough(self.radio_al, True)
        self.setEnabled(False)

    @temporary_change('radio_group', 'setExclusive', False, True)
    def enabled_state(self) -> None:
        logger.debug("Setting roofing type to enabled state.")
        self.radio_eco.setChecked(False)
        set_strikethrough(self.radio_eco, False)
        self.radio_al.setChecked(False)
        set_strikethrough(self.radio_al, False)
        self.setEnabled(True)

    @staticmethod
    def set_thickness_combo_list(roof_type: RoofingType) -> Dict[str, str]:
        combo_item_list: Dict = {}
        match roof_type:
            case RoofingType.ALUMINUM:
                combo_item_list.update(
                    {
                        '3"': '3"',
                        '6"': '6"'
                    }
                )
            case RoofingType.ECO_GREEN:
                combo_item_list.update(
                    {
                        '6"': '6"',
                        '8"': '8.25"',
                        '10"': '10.25"',
                        '12"': '12.25"'
                    }
                )
        return combo_item_list
