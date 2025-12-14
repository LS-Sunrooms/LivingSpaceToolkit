import logging

from PySide6.QtWidgets import QWidget, QLineEdit, QComboBox, QVBoxLayout, QCheckBox, QSpacerItem, QSizePolicy, QLabel
from PySide6.QtCore import QSize

from livingspacetoolkit.views.roof_pitch_component import RoofPitch
from livingspacetoolkit.views.roofing_type_component import RoofingTypeView
from livingspacetoolkit.views.roof_end_cuts_component import RoofEndCuts
from livingspacetoolkit.lib.livingspacetoolkit_enums import SunroomType, RoofingType
from livingspacetoolkit.utils.helpers import set_strikethrough

logger = logging.getLogger(__name__)


class StudioRoofView(QWidget):
    def __init__(self):
        super().__init__()

        layout: QVBoxLayout = QVBoxLayout()
        spacer: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.pitch: RoofPitch = RoofPitch("Pitch")
        self.overhang_edit: QLineEdit = QLineEdit()
        self.roofing_type: RoofingTypeView = RoofingTypeView()
        self.thickness_combo: QComboBox = QComboBox()
        self.end_cuts: RoofEndCuts = RoofEndCuts()
        self.fascia: QCheckBox = QCheckBox()

        overhang_label: QLabel = QLabel("Overhang")
        thickness_label: QLabel = QLabel("Thickness")

        self.overhang_edit.setPlaceholderText("0' or 0\"")
        self.overhang_edit.setMinimumSize(QSize(145, 35))
        self.fascia.setText("Fascia")

        layout.addWidget(self.pitch)
        layout.addWidget(overhang_label)
        layout.addWidget(self.overhang_edit)
        layout.addWidget(self.roofing_type)
        layout.addWidget(thickness_label)
        layout.addWidget(self.thickness_combo)
        layout.addWidget(self.end_cuts)
        layout.addWidget(self.fascia)
        layout.addSpacerItem(spacer)
        self.setLayout(layout)

    def default_state(self) -> None:
        logger.debug("Setting studio roof view to default state.")
        self.pitch.default_state(SunroomType.STUDIO)
        self.overhang_edit.clear()
        self.overhang_edit.setEnabled(False)
        self.roofing_type.default_state()
        self.thickness_combo.clear()
        self.thickness_combo.setEnabled(False)
        self.end_cuts.default_state()
        set_strikethrough(self.fascia, True)
        self.fascia.setChecked(False)
        self.fascia.setEnabled(False)

    def enable_except_pitch(self) -> None:
        self.overhang_edit.clear()
        self.overhang_edit.setEnabled(True)
        self.roofing_type.enabled_state()
        self.thickness_combo.clear()
        self.thickness_combo.setEnabled(True)
        self.end_cuts.enabled_state()
        set_strikethrough(self.fascia, False)

    def populate_thickness_combo(self, roof_type: RoofingType) -> None:
        self.thickness_combo.clear()
        combo_item_list = self.roofing_type.set_thickness_combo_list(roof_type)
        for item in combo_item_list:
            self.thickness_combo.addItem(item, userData=combo_item_list[item])
        self.thickness_combo.setCurrentIndex(0)
