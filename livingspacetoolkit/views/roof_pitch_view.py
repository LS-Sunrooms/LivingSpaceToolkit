from PySide6.QtWidgets import QGroupBox, QRadioButton, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QButtonGroup
from PySide6.QtCore import Qt, QSize

from livingspacetoolkit.logconf.log_config import logger
from livingspacetoolkit.lib.toolkit_enums import PitchType, SunroomType
from livingspacetoolkit.utils.helpers import temporary_change, set_strikethrough


class RoofPitchView(QGroupBox):
    def __init__(self, name: str = ""):
        super().__init__()

        self.name = name
        self.radio_group: QButtonGroup = QButtonGroup()

        self.radio_ratio: QRadioButton = QRadioButton()
        self.radio_ratio.setObjectName("radio_ratio")
        self.radio_ratio.setChecked(False)
        self.radio_ratio.setEnabled(True)
        self.radio_ratio.setText("Ratio")
        self.radio_group.addButton(self.radio_ratio)

        self.radio_angle: QRadioButton = QRadioButton()
        self.radio_angle.setObjectName("radio_angle")
        self.radio_angle.setChecked(False)
        self.radio_angle.setEnabled(True)
        self.radio_angle.setText("Angle")
        self.radio_group.addButton(self.radio_angle)

        self.pitch_input: QLineEdit = QLineEdit()
        self.pitch_input.setMinimumSize(QSize(145, 35))
        self.pitch_input.setObjectName("pitch_input")
        self.pitch_input.setEnabled(True)
        self.pitch_input.setPlaceholderText("0 in. or 0deg.")

        self.pitch_input_label: QLabel = QLabel("/12 in.")
        self.pitch_input_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout_ratio: QHBoxLayout = QHBoxLayout()
        layout_ratio.addWidget(self.radio_ratio)
        layout_ratio.addWidget(self.radio_angle)

        layout_main: QGridLayout = QGridLayout()
        layout_main.addLayout(layout_ratio, 0, 0)
        layout_main.addWidget(self.pitch_input, 1, 0)
        layout_main.addWidget(self.pitch_input_label, 1, 1)

        self.setLayout(layout_main)

    @temporary_change('radio_group', 'setExclusive', False, True)
    def default_state(self, sunroom: SunroomType) -> None:
        logger.debug(f"Setting {sunroom.name} {self.name} to default state.")
        self.radio_angle.setChecked(False)
        self.radio_ratio.setChecked(False)
        self.pitch_input.clear()
        self.update_pitch_text(PitchType.RATIO, sunroom)
        self.setEnabled(False)
        set_strikethrough(self, True)

    @temporary_change('radio_group', 'setExclusive', False, True)
    def enabled_state(self, sunroom: SunroomType) -> None:
        logger.debug(f"Setting {sunroom.name} {self.name} to enabled state.")
        self.radio_angle.setChecked(False)
        self.radio_ratio.setChecked(True)
        self.pitch_input.clear()
        self.update_pitch_text(PitchType.RATIO, sunroom)
        self.setEnabled(True)
        set_strikethrough(self, False)

    def update_pitch_text(self, pitch_type: PitchType, sunroom: SunroomType) -> None:
        match pitch_type:
            case pitch_type.ANGLE:
                self.pitch_input_label.setText(u"deg(\N{DEGREE SIGN})")
                logger.info(f"{sunroom.name} {self.name} unit type set to angle.")
            case pitch_type.RATIO:
                self.pitch_input_label.setText("/12 in.")
                logger.info(f"{sunroom.name} {self.name} unit type set to ratio.")
