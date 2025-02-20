import json
import os
from typing import Any

import requests

ARMOR_DATA_URL = "https://mhw-db.com/armor"

DATA_FOLDER = "./data"
ARMOR_DATA_FILE = "armor_data.json"
ARMOR_DATA = os.path.join(DATA_FOLDER, ARMOR_DATA_FILE)


def sync_armor_data(
    force: bool = False, path: str = DATA_FOLDER, filename: str = ARMOR_DATA_FILE
) -> None:
    """
    Syncs the armor data with a remote database if no local file exists.
    The force flag can be used to sync even if a local file exists.
    """
    if os.path.exists(os.path.join(path, filename)) and not force:
        print("Armor data already exists. Not syncing with remote armor data.")
        return

    armor_data = _get_remote_armor_data()
    _save_armor_data(armor_data, path, filename)


def load_armor_data(file_path: str = ARMOR_DATA) -> dict[str, Any]:
    """
    Loads the json data from the given path.
    """
    if not os.path.exists(file_path):
        print(f"Could not find path {file_path}")
        return {}

    with open(file_path) as file:
        try:
            armor_data = json.load(file)
        except json.JSONDecodeError as exc:
            print(f"Failed to load armor data: {exc}")
            return {}

    print("Loaded armor data.")
    return armor_data


def _get_remote_armor_data(url: str = ARMOR_DATA_URL) -> dict[str, Any]:
    """
    Requests armor data from a remote database.
    If the response is succesfull it formats the data as follows and returns it:
    {
        <rank> : {
            <armor_set> :{
                <armor_piece_type> : {
                    "slots": list[int],
                    "skills": {
                        <skill_name>:<level>
                    }
                }
            }
        }
    }

    """
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to collect data")
        return {}

    armor_data = {"low": {}, "high": {}, "master": {}}
    armor_pieces = response.json()
    for armor_piece in armor_pieces:
        try:
            name = armor_piece["armorSet"]["name"]
            rank = armor_piece["rank"]
            armor_type = armor_piece["type"]
            skills = armor_piece["skills"]
            slots = armor_piece["slots"]
        except KeyError as exc:
            print(f"Failed to get required data for armor piece {armor_piece}. {exc}")
            continue

        armor_slots = _parse_slots(slots)
        if slots is None:
            print(f"Failed to parse slots: {slots}.")
            continue

        armor_skills = _parse_skills(skills)
        if skills is None:
            print(f"Failed to parse skills {skills}.")
            continue

        if name not in armor_data:
            armor_data[rank][name] = {}
        armor_data[rank][name][armor_type] = {
            "slots": armor_slots,
            "skills": armor_skills,
        }

    return armor_data


def _parse_slots(slots: list[dict[str, Any]]) -> list[int] | None:
    """
    Converts a list of dicts that contain slot information to
    a list where each index hold the amount of slots for that size.
    """
    armor_slots = [0, 0, 0, 0]
    for slot in slots:
        try:
            rank = slot["rank"]
            if not 1 <= rank <= 4:
                return None

            armor_slots[rank - 1] += 1
        except (KeyError, TypeError):
            return None

    return armor_slots


def _parse_skills(skills: list[dict[str, Any]]) -> dict[str, int] | None:
    """
    Converts a list of dicts that contain skill information to a dict
    where they keys are the skill names and the values the corresponding level.
    """
    armor_skills = {}
    for skill in skills:
        try:
            armor_skills[skill["skillName"]] = skill["level"]
        except KeyError:
            return None

    return armor_skills


def _save_armor_data(
    armor_data: dict[str, Any], path: str = DATA_FOLDER, filename: str = ARMOR_DATA_FILE
) -> None:
    """
    Saves the given data as json at the give path and filename.
    If the file/folder does not exist yet, it gets created automatically.
    """
    if not os.path.exists(path):
        os.mkdir(path)

    with open(os.path.join(path, filename), "w") as file:
        json.dump(armor_data, file)

    print("Saved armor data.")
