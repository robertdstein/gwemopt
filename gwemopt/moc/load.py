import json
from pathlib import Path


def load_moc(output_path: Path):
    """
    Load MOC from file.

    :param output_path: path to MOC file
    :return: MOC
    """
    with open(output_path, "r") as f:
        moc_struct = json.load(f)

    return moc_struct
