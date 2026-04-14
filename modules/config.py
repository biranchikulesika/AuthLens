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
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            config = DEFAULT_CONFIG.copy()
            config.update(data)
            return config
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(config_data):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)
    except Exception:
        pass


# Load once globally
CONFIG = load_config()