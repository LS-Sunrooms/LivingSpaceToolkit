import logging

from PySide6.QtWidgets import QRadioButton, QHBoxLayout, QGroupBox
from PySide6.QtCore import Qt

logger = logging.getLogger(__name__)


class ScenariosView(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setTitle("Scenarios")

        layout: QHBoxLayout = QHBoxLayout()

        self.radio1: QRadioButton = QRadioButton()
        self.radio1.setObjectName("radio1")
        self.radio1.setChecked(False)
        self.radio1.setEnabled(True)
        self.radio1.setText("Wall Height\nand Pitch")
        layout.addWidget(self.radio1)

        self.radio2: QRadioButton = QRadioButton()
        self.radio2.setObjectName("radio2")
        self.radio2.setChecked(False)
        self.radio2.setEnabled(True)
        self.radio2.setText("Wall Height and\nPeak Height")
        layout.addWidget(self.radio2)

        self.radio3: QRadioButton = QRadioButton()
        self.radio3.setObjectName("radio3")
        self.radio3.setChecked(False)
        self.radio3.setEnabled(True)
        self.radio3.setText("Max Height\nand Pitch")
        layout.addWidget(self.radio3)

        self.radio4: QRadioButton = QRadioButton()
        self.radio4.setObjectName("radio4")
        self.radio4.setChecked(False)
        self.radio4.setEnabled(True)
        self.radio4.setText("Soffit Height and\nPeak Height")
        layout.addWidget(self.radio4)

        self.radio5: QRadioButton = QRadioButton()
        self.radio5.setObjectName("radio5")
        self.radio5.setChecked(False)
        self.radio5.setEnabled(True)
        self.radio5.setText("Soffit Height\nand Pitch")
        layout.addWidget(self.radio5)

        self.radio6: QRadioButton = QRadioButton()
        self.radio6.setObjectName("radio6")
        self.radio6.setChecked(False)
        self.radio6.setEnabled(True)
        self.radio6.setText("Drip Edge\nand Peak Height")
        layout.addWidget(self.radio6)

        self.radio7: QRadioButton = QRadioButton()
        self.radio7.setObjectName("radio7")
        self.radio7.setChecked(False)
        self.radio7.setEnabled(True)
        self.radio7.setText("Drip Edge\nand Pitch")
        layout.addWidget(self.radio7)

        self.setLayout(layout)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def uncheck_all(self) -> None:
        logger.debug("Unchecking scenario radio buttons.")
        self.radio1.setChecked(False)
        self.radio2.setChecked(False)
        self.radio3.setChecked(False)
        self.radio4.setChecked(False)
        self.radio5.setChecked(False)
        self.radio6.setChecked(False)
        self.radio7.setChecked(False)
