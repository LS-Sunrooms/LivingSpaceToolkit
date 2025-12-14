from livingspacetoolkit.logconf import log_config
import logging

from PySide6.QtWidgets import QApplication

from livingspacetoolkit.main_window import MainWindow
from livingspacetoolkit.theme_manager import apply_theme

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting LivingSpace Toolkit…")
    app = QApplication([])
    apply_theme(app)
    window = MainWindow()
    window.show()
    window.tabs_controller.set_to_default_state()
    app.exec()

if __name__ == "__main__":
    main()
