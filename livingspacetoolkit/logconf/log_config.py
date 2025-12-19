import logging.config
import os
import json
from pathlib import Path

with open(Path.joinpath(Path(os.path.dirname(__file__)).parent,
                        "logconf/log_config.json"), "rt") as f:
    log_config: dict = json.loads(f.read())
    # Logs Directory
    logs_dir: Path = Path.joinpath(Path(__file__).parent.parent.parent, "Logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Update file handler
    log_config['handlers']['file']['filename'] = logs_dir / log_config['handlers']['file']['filename']
    logging.config.dictConfig(log_config)
    
logger = logging.getLogger(name="livingspacetoolkit")