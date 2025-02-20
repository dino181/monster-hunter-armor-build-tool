import json
import os
import shutil
from unittest.mock import patch

import pytest

from armor_data import (_parse_skills, _parse_slots, _save_armor_data,
                        load_armor_data, sync_armor_data)

TEST_FOLDER = "./test_data"
TEST_FILE = "armor_data.json"
TEST_PATH = os.path.join(TEST_FOLDER, TEST_FILE)


def cleanup():
    try:
        shutil.rmtree(TEST_FOLDER)
    except:
        pass


def make_test_file(data):
    cleanup()
    os.mkdir(TEST_FOLDER)
    with open(TEST_PATH, "w") as file:
        file.write(data)


@pytest.mark.parametrize("force", [False, True])
@patch("armor_data._get_remote_armor_data")
def test_sync_armor_data(get_remote_mock, force):
    cleanup()
    get_remote_mock.return_value = {"data": "values"}

    sync_armor_data(force, TEST_FOLDER, TEST_FILE)

    with open(TEST_PATH) as file:
        result = json.load(file)

    assert result == {"data": "values"}
    cleanup()


@pytest.mark.parametrize(
    "force, expected", [(False, {"data": "values"}), (True, {"new_data": "new_values"})]
)
@patch("armor_data._get_remote_armor_data")
def test_sync_armor_data_already_synced(get_remote_mock, force, expected):
    data = {"data": "values"}
    make_test_file(json.dumps(data))

    get_remote_mock.return_value = {"new_data": "new_values"}
    sync_armor_data(force, TEST_FOLDER, TEST_FILE)

    with open(TEST_PATH) as file:
        result = json.load(file)

    assert result == expected
    cleanup()


def test_load_armor_data():
    data = {"data": "values"}
    make_test_file(json.dumps(data))
    armor_data = load_armor_data(TEST_PATH)
    assert armor_data == {"data": "values"}
    cleanup()


def test_load_armor_data_invalid():
    data = {"data": "values"}
    make_test_file(json.dumps(data)[:-2])

    armor_data = load_armor_data(TEST_PATH)

    assert armor_data == {}
    cleanup()


@pytest.mark.parametrize(
    "slots, expected",
    [
        ([{"rank": 1}, {"rank": 1}, {"rank": 2}], [2, 1, 0, 0]),
        ([{"rank": 1}, {"rank": 2}, {"rank": 3}], [1, 1, 1, 0]),
        ([{"rank": 4}, {"rank": 4}], [0, 0, 0, 2]),
        ([], [0, 0, 0, 0]),
    ],
)
def test_parse_slots(slots, expected):
    result = _parse_slots(slots)
    assert result == expected


def test_parse_slots_invalid_key():
    slots = [{"rank": 1}, {"invalid": 1}, {"rank": 2}]
    result = _parse_slots(slots)
    assert result is None


def test_parse_slots_invalid_value():
    slots = [{"rank": "not an int"}, {"rank": 1}, {"rank": 2}]
    result = _parse_slots(slots)
    assert result is None


@pytest.mark.parametrize(
    "slots",
    [
        ([{"rank": 0}]),
        ([{"rank": 5}]),
    ],
)
def test_parse_slots_invalid_slot_size(slots):
    result = _parse_slots(slots)
    assert result is None


@pytest.mark.parametrize(
    "skills, expected",
    [
        ([{"skillName": "skill 1", "level": 3}], {"skill 1": 3}),
        (
            [
                {"skillName": "skill 1", "level": 3},
                {"skillName": "skill 2", "level": 1},
            ],
            {"skill 1": 3, "skill 2": 1},
        ),
        (
            [
                {"skillName": "skill 1", "level": 3},
                {"skillName": "skill 1", "level": 1},
            ],
            {"skill 1": 1},
        ),
        ([], {}),
    ],
)
def test_parse_skills(skills, expected):
    result = _parse_skills(skills)
    assert result == expected


@pytest.mark.parametrize(
    "skills ",
    [
        [{"invalid": "skill 1", "level": 3}],
        [{"skillName": "skill 1", "invalid": 3}],
        [{"skillName": "skill 1"}],
        [{"level": 3}],
    ],
)
def test_parse_skills_invalid_keys(skills):
    result = _parse_skills(skills)
    assert result is None


def test_save_armor_data():
    cleanup()
    data = {"save": "value"}
    _save_armor_data(data, TEST_FOLDER, TEST_FILE)

    with open(TEST_PATH) as file:
        result = json.load(file)

    assert result == data
    cleanup()


def test_save_armor_data_file_already_exists():
    data = {"save": "value"}
    make_test_file(json.dumps(data))

    data = {"new_save": "new_value"}
    _save_armor_data(data, TEST_FOLDER, TEST_FILE)

    with open(TEST_PATH) as file:
        result = json.load(file)

    assert result == data
    cleanup()
