import json
import os
from typing import Any

import requests


def sync_armor_data():
    armor_data = get_armor_data()
    save_armor_data(armor_data)


def get_armor_data():
    response = requests.get("https://mhw-db.com/armor")
    if response.status_code != 200:
        print("Failed to collect data")
        return

    armor_data = {"low": {}, "high": {}, "master": {}}
    armor_pieces = response.json()
    for armor_piece in armor_pieces:
        name = armor_piece["armorSet"]["name"]
        rank = armor_piece["rank"]
        armor_type = armor_piece["type"]
        if name not in armor_data[rank]:
            armor_data[rank][name] = {}

        slots = [0, 0, 0, 0]
        for slot in armor_piece["slots"]:
            slots[slot["rank"] - 1] += 1

        skills = {}
        for skill in armor_piece["skills"]:
            skills[skill["skillName"]] = skill["level"]

        armor_data[rank][name][armor_type] = {"slots": slots, "skills": skills}

    return armor_data


def load_armor_data() -> dict[str, Any]:
    if not os.path.exists("./data/armor_data.json"):
        print("Could not find path ./data/armor_data.json")
        return

    with open("./data/armor_data.json") as file:
        armor_data = json.load(file)

    return armor_data


def save_armor_data(armor_data: dict[str, Any]):
    if not os.path.exists("./data"):
        os.mkdir("data")

    with open("./data/armor_data.json", "w") as file:
        json.dump(armor_data, file)
