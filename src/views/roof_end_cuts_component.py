import logging

from PySide6.QtWidgets import QGroupBox, QRadioButton, QVBoxLayout

logger = logging.getLogger(__name__)

class RoofEndCuts(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setTitle("End Cuts")

        self.radio_endcut1: QRadioButton = QRadioButton()
        self.radio_endcut1.setObjectName("radio_endcut1")
        self.radio_endcut1.setChecked(False)
        self.radio_endcut1.setEnabled(True)
        self.radio_endcut1.setText("Uncut Top && Bottom")

        self.radio_endcut2: QRadioButton = QRadioButton()
        self.radio_endcut2.setObjectName("radio_endcut2")
        self.radio_endcut2.setChecked(False)
        self.radio_endcut2.setEnabled(True)
        self.radio_endcut2.setText("Plumb Cut Top && Bottom")

        self.radio_endcut3: QRadioButton = QRadioButton()
        self.radio_endcut3.setObjectName("Plum Cut Top Only")
        self.radio_endcut3.setChecked(False)
        self.radio_endcut3.setEnabled(True)
        self.radio_endcut3.setText("EcoGreen")

        layout: QVBoxLayout = QVBoxLayout()
        layout.addWidget(self.radio_endcut1)
        layout.addWidget(self.radio_endcut2)
        layout.addWidget(self.radio_endcut3)

        self.setLayout(layout)

    def uncheck_all(self) -> None:
        logger.debug("Unchecking all radio buttons.")
        self.radio_endcut1.setChecked(False)
        self.radio_endcut2.setChecked(False)
        self.radio_endcut3.setChecked(False)