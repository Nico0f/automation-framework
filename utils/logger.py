import logging
import yaml
from pathlib import Path

def setup_logger():
    """Configure logging based on config file"""
    config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    logging.basicConfig(
        level=config['logging']['level'],
        format=config['logging']['format'],
        filename=config['logging']['file']
    )
    
    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(config['logging']['format']))
    logging.getLogger().addHandler(console_handler)
    
    return logging.getLogger(__name__)