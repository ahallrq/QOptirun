import json
import os

PATH_NOT_EXISTS = 0
PATH_IS_FILE = 1
PATH_IS_DIR = 2


def check_preset_file_exists(preset_file):
    if os.path.exists(preset_file):  # Path Exists and...
        if os.path.isfile(preset_file):  # is a file
            return PATH_IS_FILE
        elif os.path.isdir(preset_file):  # is a directory
            return PATH_IS_DIR
    else:  # Path doesn't exist..'
        return PATH_NOT_EXISTS


def verify_preset_file_integrity():
    pass


def verify_preset_integrity():
    pass


def load_presets(preset_file):
    pass


def save_presets(preset_file, preset_list):
    status = check_preset_file_exists(preset_file)

    if status == PATH_NOT_EXISTS
        try:
            os.makedirs(os.path.join(os.path.expanduser("~"), ".config/qoptirun"))
        except OSError as e:
            print("Path already exists or could not be created.") ## TODO: Do more intelligent handling later.
        
