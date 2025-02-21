import pytest

from armor_set import ArmorPiece, ArmorRank, ArmorSet, ArmorType


@pytest.fixture
def armor_set():
    return ArmorSet(
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


def test_create_armor_piece():
    armor_piece = ArmorPiece(
        ArmorType.HELM, ArmorRank.MR, "piece", buffs={}, slots=[0, 0, 0, 0]
    )
    assert armor_piece.armor_type == ArmorType.HELM
    assert armor_piece.rank == ArmorRank.MR
    assert armor_piece.name == "piece"
    assert armor_piece.buffs == {}
    assert armor_piece.slots == [0, 0, 0, 0]


@pytest.mark.parametrize("slots", [[0, 0, 0], [0, 0, 0, 0, 0]])
def test_create_armor_piece_invalid_slots(slots):
    with pytest.raises(ValueError):
        ArmorPiece(ArmorType.HELM, ArmorRank.MR, "piece", buffs={}, slots=slots)


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
    armor_set = ArmorSet()
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
    armor_set = ArmorSet()
    result = armor_set.get_decoration_slots()
    assert result == [0, 0, 0, 0]
