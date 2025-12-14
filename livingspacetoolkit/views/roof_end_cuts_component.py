import logging

from PySide6.QtWidgets import QGroupBox, QRadioButton, QVBoxLayout, QButtonGroup

from livingspacetoolkit.lib.livingspacetoolkit_enums import RoofingType, EndCutType
from livingspacetoolkit.utils.helpers import temporary_change, set_strikethrough

logger = logging.getLogger(__name__)


class RoofEndCuts(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setTitle("End Cuts")
        self.radio_group: QButtonGroup = QButtonGroup()

        self.radio_endcut1: QRadioButton = QRadioButton()
        self.radio_endcut1.setObjectName("radio_endcut1")
        self.radio_endcut1.setChecked(False)
        self.radio_endcut1.setEnabled(True)
        self.radio_endcut1.setText("Uncut Top && Bottom")
        self.radio_group.addButton(self.radio_endcut1)

        self.radio_endcut2: QRadioButton = QRadioButton()
        self.radio_endcut2.setObjectName("radio_endcut2")
        self.radio_endcut2.setChecked(False)
        self.radio_endcut2.setEnabled(True)
        self.radio_endcut2.setText("Plumb Cut Top && Bottom")
        self.radio_group.addButton(self.radio_endcut2)

        self.radio_endcut3: QRadioButton = QRadioButton()
        self.radio_endcut3.setObjectName("radio_endcut3")
        self.radio_endcut3.setChecked(False)
        self.radio_endcut3.setEnabled(True)
        self.radio_endcut3.setText("Plumb Cut Top Only")
        self.radio_group.addButton(self.radio_endcut3)

        layout: QVBoxLayout = QVBoxLayout()
        layout.addWidget(self.radio_endcut1)
        layout.addWidget(self.radio_endcut2)
        layout.addWidget(self.radio_endcut3)

        self.setLayout(layout)

    @temporary_change('radio_group', 'setExclusive', False, True)
    def default_state(self) -> None:
        logger.debug("Setting end cuts to default state.")
        self.radio_endcut1.setChecked(False)
        set_strikethrough(self.radio_endcut1, True)
        self.radio_endcut2.setChecked(False)
        set_strikethrough(self.radio_endcut2, True)
        self.radio_endcut3.setChecked(False)
        set_strikethrough(self.radio_endcut3, True)
        self.setEnabled(False)

    @temporary_change('radio_group', 'setExclusive', False, True)
    def enabled_state(self) -> None:
        logger.debug("Setting end cuts to enabled state.")
        self.radio_endcut1.setChecked(False)
        set_strikethrough(self.radio_endcut1, False)
        self.radio_endcut2.setChecked(False)
        set_strikethrough(self.radio_endcut2, False)
        self.radio_endcut3.setChecked(False)
        set_strikethrough(self.radio_endcut3, False)
        self.setEnabled(True)

    def set_end_cuts_by_roof_type(self, roof_type: RoofingType) -> None:
        logger.debug(f"Enabling/Disabling end cuts for roofing type {roof_type.name}")
        match roof_type:
            case RoofingType.ECO_GREEN:
                self.radio_endcut1.setEnabled(True)
                set_strikethrough(self.radio_endcut1, False)
                self.radio_endcut2.setEnabled(True)
                set_strikethrough(self.radio_endcut2, False)
                self.radio_endcut3.setEnabled(True)
                set_strikethrough(self.radio_endcut3, False)
            case RoofingType.ALUMINUM:
                self.radio_endcut1.setEnabled(True)
                set_strikethrough(self.radio_endcut1, False)
                self.radio_endcut2.setEnabled(False)
                set_strikethrough(self.radio_endcut2, True)
                self.radio_endcut3.setEnabled(False)
                set_strikethrough(self.radio_endcut3, True)
        self.radio_endcut1.setChecked(True)