import json
import os

PROJECT_NAME = "AuthLens"
VERSION = "1.0.0"
TAGLINE = "Authentication Security Audit Suite"
MODULE_NAMES = ["PassForge", "StrengthMeter", "BruteCheck", "HashScan", "Auditor"]

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "output_directory": "output",
    "default_brute_speed": "fast",
    "show_banner": True
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            # Merge with defaults to ensure all keys exist
            config = DEFAULT_CONFIG.copy()
            config.update(data)
            return config
    except Exception:
        # Fall back to defaults without crashing
        return DEFAULT_CONFIG.copy()

def save_config(config_data):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=4)
    except Exception:
        pass
