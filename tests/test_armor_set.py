import pytest

from armor_set import ArmorPiece, ArmorRank, ArmorSet, ArmorType


@pytest.fixture
def armor_set():
    return ArmorSet(
        name="test-set",
        helm=ArmorPiece(
            armor_type=ArmorType.HELM,
            name="Piece 1",
            rank=ArmorRank.MR,
            slots=[0, 0, 0, 0],
            buffs={"buff 1": 2},
        ),
        chest=ArmorPiece(
            armor_type=ArmorType.CHEST,
            name="Piece 2",
            rank=ArmorRank.MR,
            slots=[1, 0, 0, 0],
            buffs={"buff 1": 2},
        ),
        arm=ArmorPiece(
            armor_type=ArmorType.ARM,
            name="Piece 3",
            rank=ArmorRank.MR,
            slots=[1, 1, 1, 1],
            buffs={"buff 2": 1},
        ),
        waist=ArmorPiece(
            armor_type=ArmorType.WAIST,
            name="Piece 4",
            rank=ArmorRank.MR,
            slots=[0, 0, 2, 0],
            buffs={"buff 3": 3},
        ),
        leg=ArmorPiece(
            armor_type=ArmorType.LEG,
            name="Piece 5",
            rank=ArmorRank.MR,
            slots=[2, 0, 0, 0],
            buffs={},
        ),
        charm=None,
    )


def test_armor_piece_new():
    armor_data = {"master": {"test-armor": {"slots": [0, 0, 0, 0], "buffs": {}}}}
    armor_piece = ArmorPiece.new(ArmorType.HELM, "master", "test-armor", armor_data)
    assert armor_piece.armor_type == ArmorType.HELM
    assert armor_piece.rank == ArmorRank.MR
    assert armor_piece.name == "test-armor"
    assert armor_piece.buffs == {}
    assert armor_piece.slots == [0, 0, 0, 0]


def test_create_armor_piece_name_not_in_armor_data():
    result = ArmorPiece.new(ArmorType.HELM, "master", "test-armor", {"master": {}})
    assert result is None


@pytest.mark.parametrize("slots", [[0, 0, 0], [0, 0, 0, 0, 0]])
def test_create_armor_piece_invalid_slots(slots):
    armor_data = {"master": {"test-armor": {"slots": slots, "buffs": {}}}}
    with pytest.raises(ValueError):
        ArmorPiece.new(ArmorType.HELM, "master", "test-armor", armor_data)


def test_create_armor_piece_rank_not_in_armor_data():
    with pytest.raises(ValueError):
        ArmorPiece.new(ArmorType.HELM, "master", "test-armor", {})


def test_create_armor_piece_rank_not_convertable():
    with pytest.raises(ValueError):
        ArmorPiece.new(ArmorType.HELM, "something", "test-armor", {})


def test_get_buffs(armor_set: ArmorSet):
    result = armor_set.get_buffs()
    assert result == {
        "buff 1": 4,
        "buff 2": 1,
        "buff 3": 3,
    }


def test_get_buffs_missing_pieces(armor_set: ArmorSet):
    armor_set.helm = None
    armor_set.waist = None

    result = armor_set.get_buffs()
    assert result == {
        "buff 1": 2,
        "buff 2": 1,
    }


def test_get_buffs_no_armor():
    armor_set = ArmorSet(name="test-set")
    result = armor_set.get_buffs()
    assert result == {}


def test_get_decoration_slots(armor_set: ArmorSet):
    result = armor_set.get_decoration_slots()
    assert result == [4, 1, 3, 1]


def test_get_decoration_missing_pieces(armor_set: ArmorSet):
    armor_set.leg = None
    armor_set.arm = None

    result = armor_set.get_decoration_slots()
    assert result == [1, 0, 2, 0]


def test_get_decoration_no_pieces():
    armor_set = ArmorSet(name="test-set")
    result = armor_set.get_decoration_slots()
    assert result == [0, 0, 0, 0]


@pytest.mark.parametrize(
    "rank, expected",
    [("low", ArmorRank.LR), ("high", ArmorRank.HR), ("master", ArmorRank.MR)],
)
def test_armor_rank_from_str(rank, expected):
    result = ArmorRank.from_str(rank)
    assert result == expected


def test_armor_rank_from_str_invalid():
    with pytest.raises(ValueError):
        ArmorRank.from_str("this is not a rank")


@pytest.mark.parametrize(
    "armor_type, expected",
    [
        ("helm", ArmorType.HELM),
        ("chest", ArmorType.CHEST),
        ("arm", ArmorType.ARM),
        ("waist", ArmorType.WAIST),
        ("leg", ArmorType.LEG),
        ("charm", ArmorType.CHARM),
    ],
)
def test_armor_type_from_str(armor_type, expected):
    result = ArmorType.from_str(armor_type)
    assert result == expected


def test_armor_type_from_str_invalid():
    with pytest.raises(ValueError):
        ArmorType.from_str("this is not a type")


def test_armor_piece_from_dict():
    data = {
        "name": "test",
        "type": "helm",
        "rank": "master",
        "buffs": {},
        "slots": [0, 0, 0, 0],
    }
    result = ArmorPiece.from_dict(data)
    assert result.name == "test"
    assert result.armor_type == ArmorType.HELM
    assert result.rank == ArmorRank.MR
    assert result.buffs == {}
    assert result.slots == [0, 0, 0, 0]


@pytest.mark.parametrize(
    "data",
    [
        {
            "type": "helm",
            "rank": "master",
            "buffs": {},
            "slots": [0, 0, 0, 0],
        },
        {
            "name": "test",
            "rank": "master",
            "buffs": {},
            "slots": [0, 0, 0, 0],
        },
        {
            "name": "test",
            "type": "helm",
            "buffs": {},
            "slots": [0, 0, 0, 0],
        },
        {
            "name": "test",
            "type": "helm",
            "rank": "master",
            "slots": [0, 0, 0, 0],
        },
        {
            "name": "test",
            "type": "helm",
            "rank": "master",
            "buffs": {},
        },
        {
            "name": "test",
            "type": "helm",
            "rank": "not a rank",
            "buffs": {},
            "slots": [0, 0, 0, 0],
        },
        {
            "name": "test",
            "type": "not a type",
            "rank": "master",
            "buffs": {},
            "slots": [0, 0, 0, 0],
        },
        {
            "name": "test",
            "type": "not a type",
            "rank": "master",
            "buffs": {},
            "slots": [0, 0, 0, 0, 0],
        },
        {
            "name": "test",
            "type": "not a type",
            "rank": "master",
            "buffs": {},
            "slots": [0, 0, 0],
        },
    ],
)
def test_armor_piece_from_dict_invalid_dict(data):
    with pytest.raises(ValueError):
        ArmorPiece.from_dict(data)


@pytest.mark.parametrize("data", [{}, None])
def test_armor_piece_from_dict_no_data(data):
    assert ArmorPiece.from_dict(data) is None


def test_armor_piece_to_dict():
    armor_piece = ArmorPiece(
        armor_type=ArmorType.HELM,
        name="test",
        rank=ArmorRank.MR,
        buffs={"some buff": 3},
        slots=[1, 0, 0, 2],
    )
    assert armor_piece.to_dict() == {
        "type": "helm",
        "name": "test",
        "rank": "master",
        "buffs": {"some buff": 3},
        "slots": [1, 0, 0, 2],
    }


def test_armor_set_to_dict(armor_set: ArmorSet):
    expected = {
        "name": "test-set",
        "helm": {
            "type": "helm",
            "name": "Piece 1",
            "rank": "master",
            "slots": [0, 0, 0, 0],
            "buffs": {"buff 1": 2},
        },
        "chest": {
            "type": "chest",
            "name": "Piece 2",
            "rank": "master",
            "slots": [1, 0, 0, 0],
            "buffs": {"buff 1": 2},
        },
        "arm": {
            "type": "arm",
            "name": "Piece 3",
            "rank": "master",
            "slots": [1, 1, 1, 1],
            "buffs": {"buff 2": 1},
        },
        "waist": {
            "type": "waist",
            "name": "Piece 4",
            "rank": "master",
            "slots": [0, 0, 2, 0],
            "buffs": {"buff 3": 3},
        },
        "leg": {
            "type": "leg",
            "name": "Piece 5",
            "rank": "master",
            "slots": [2, 0, 0, 0],
            "buffs": {},
        },
    }

    assert armor_set.to_dict() == expected


def test_armor_set_to_dict_no_pieces():
    armor_set = ArmorSet("test")
    assert armor_set.to_dict() == {
        "name": "test",
        "helm": None,
        "chest": None,
        "arm": None,
        "waist": None,
        "leg": None,
    }


def test_armor_set_from_dict():
    data = {
        "name": "test-set",
        "helm": {
            "type": "helm",
            "name": "Piece 1",
            "rank": "master",
            "slots": [0, 0, 0, 0],
            "buffs": {"buff 1": 2},
        },
        "chest": {
            "type": "chest",
            "name": "Piece 2",
            "rank": "master",
            "slots": [1, 0, 0, 0],
            "buffs": {"buff 1": 2},
        },
        "arm": {
            "type": "arm",
            "name": "Piece 3",
            "rank": "master",
            "slots": [1, 1, 1, 1],
            "buffs": {"buff 2": 1},
        },
        "waist": {
            "type": "waist",
            "name": "Piece 4",
            "rank": "master",
            "slots": [0, 0, 2, 0],
            "buffs": {"buff 3": 3},
        },
        "leg": None,
    }
    result = ArmorSet.from_dict(data)
    assert result.name == "test-set"
    assert result.helm.name == "Piece 1"
    assert result.chest.name == "Piece 2"
    assert result.arm.name == "Piece 3"
    assert result.waist.name == "Piece 4"
    assert result.leg is None


@pytest.mark.parametrize(
    "data",
    [
        {
            "helm": None,
            "chest": None,
            "arm": None,
            "waist": None,
            "leg": None,
        },
        {
            "name": "test-set",
            "chest": None,
            "arm": None,
            "waist": None,
            "leg": None,
        },
        {
            "name": "test-set",
            "helm": None,
            "arm": None,
            "waist": None,
            "leg": None,
        },
        {
            "name": "test-set",
            "helm": None,
            "chest": None,
            "waist": None,
            "leg": None,
        },
        {
            "name": "test-set",
            "helm": None,
            "chest": None,
            "arm": None,
            "leg": None,
        },
        {
            "name": "test-set",
            "helm": None,
            "chest": None,
            "arm": None,
            "waist": None,
        },
        {},
    ],
)
def test_armor_set_from_dict_invalid_dict(data):
    with pytest.raises(ValueError):
        ArmorSet.from_dict(data)
