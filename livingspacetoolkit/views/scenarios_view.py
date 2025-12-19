import logging
from typing import Dict

from PySide6.QtWidgets import QRadioButton, QHBoxLayout, QGroupBox, QButtonGroup
from PySide6.QtCore import Qt

from livingspacetoolkit.lib.toolkit_enums import Scenario
from livingspacetoolkit.utils.helpers import temporary_change

logger = logging.getLogger(name="livingspacetoolkit")


class ScenariosView(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setTitle("Scenarios")
        self.scenario_dict: Dict[QRadioButton: Scenario] = {}

        layout: QHBoxLayout = QHBoxLayout()
        self.radio_group: QButtonGroup = QButtonGroup()

        self.radio1: QRadioButton = QRadioButton()
        self.radio1.setObjectName("radio1")
        self.radio1.setChecked(False)
        self.radio1.setEnabled(True)
        self.radio1.setText("Wall Height\nand Pitch")
        self.scenario_dict.update({self.radio1: Scenario.WALL_HEIGHT_PITCH})
        self.radio_group.addButton(self.radio1)
        layout.addWidget(self.radio1)

        self.radio2: QRadioButton = QRadioButton()
        self.radio2.setObjectName("radio2")
        self.radio2.setChecked(False)
        self.radio2.setEnabled(True)
        self.radio2.setText("Wall Height and\nPeak Height")
        self.scenario_dict.update({self.radio2: Scenario.WALL_HEIGHT_PEAK_HEIGHT})
        self.radio_group.addButton(self.radio2)
        layout.addWidget(self.radio2)

        self.radio3: QRadioButton = QRadioButton()
        self.radio3.setObjectName("radio3")
        self.radio3.setChecked(False)
        self.radio3.setEnabled(True)
        self.radio3.setText("Max Height\nand Pitch")
        self.scenario_dict.update({self.radio3: Scenario.MAX_HEIGHT_PITCH})
        self.radio_group.addButton(self.radio3)
        layout.addWidget(self.radio3)

        self.radio4: QRadioButton = QRadioButton()
        self.radio4.setObjectName("radio4")
        self.radio4.setChecked(False)
        self.radio4.setEnabled(True)
        self.radio4.setText("Soffit Height and\nPeak Height")
        self.scenario_dict.update({self.radio4: Scenario.SOFFIT_HEIGHT_PEAK_HEIGHT})
        self.radio_group.addButton(self.radio4)
        layout.addWidget(self.radio4)

        self.radio5: QRadioButton = QRadioButton()
        self.radio5.setObjectName("radio5")
        self.radio5.setChecked(False)
        self.radio5.setEnabled(True)
        self.radio5.setText("Soffit Height\nand Pitch")
        self.scenario_dict.update({self.radio5: Scenario.SOFFIT_HEIGHT_PITCH})
        self.radio_group.addButton(self.radio5)
        layout.addWidget(self.radio5)

        self.radio6: QRadioButton = QRadioButton()
        self.radio6.setObjectName("radio6")
        self.radio6.setChecked(False)
        self.radio6.setEnabled(True)
        self.radio6.setText("Drip Edge\nand Peak Height")
        self.scenario_dict.update({self.radio6: Scenario.DRIP_EDGE_PEAK_HEIGHT})
        self.radio_group.addButton(self.radio6)
        layout.addWidget(self.radio6)

        self.radio7: QRadioButton = QRadioButton()
        self.radio7.setObjectName("radio7")
        self.radio7.setChecked(False)
        self.radio7.setEnabled(True)
        self.radio7.setText("Drip Edge\nand Pitch")
        self.scenario_dict.update({self.radio7: Scenario.DRIP_EDGE_PITCH})
        self.radio_group.addButton(self.radio7)
        layout.addWidget(self.radio7)

        self.setLayout(layout)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    @temporary_change('radio_group', 'setExclusive', False, True)
    def default_state(self) -> None:
        logger.debug("Setting scenarios to default state.")
        for button in self.scenario_dict.keys():
            if button.isChecked():
                button.setChecked(False)
                logger.debug(f"Setting {self.scenario_dict[button].name} to unchecked.")
