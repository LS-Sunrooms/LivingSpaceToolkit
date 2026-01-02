from pathlib import Path
from platformdirs import PlatformDirs


# Configure log and config directory. Linux logs: ~/.local/state/<APP_NAME>/logs, Windows logs: %LocalAppData%\<APP_NAME>\logs
APP_NAME = "LivingSpaceToolkit"
dirs = PlatformDirs(APP_NAME, "Livingspace Sunrooms")
log_dir = Path(dirs.user_log_dir)
# config_dir = Path(dirs.user_config_dir) # If in the future the maintainer wants to have a configuration directory.