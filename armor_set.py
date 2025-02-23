from enum import Enum, auto
from typing import Any, Self


class ArmorType(Enum):
    HELM = auto()
    CHEST = auto()
    ARM = auto()
    WAIST = auto()
    LEG = auto()
    CHARM = auto()


class ArmorRank(Enum):
    LR = "low"
    HR = "high"
    MR = "master"

    @staticmethod
    def from_str(value: str) -> Self:
        for rank in ArmorRank:
            if rank.value == value:
                return rank
        raise ValueError(f"Could not convert {value} to ArmorRank enum")


class ArmorPiece:
    def __init__(
        self,
        armor_type: ArmorType,
        rank: ArmorRank,
        name: str,
        buffs: list[dict[str, int]],
        slots: list[int],
    ) -> None:
        if len(slots) != 4:
            raise ValueError("Slots must be an array of length 4")

        self.name = name
        self.armor_type = armor_type
        self.rank = rank
        self.buffs = buffs  # NOTE: Buff as class with name/level/max level?
        self.slots = slots

    @staticmethod
    def new(
        armor_type: ArmorType, rank: str, name: str, armor_data: dict[str, Any]
    ) -> Self | None:
        if rank not in armor_data.keys():
            raise ValueError(f"rank must be one of: {list(armor_data.keys())}")

        piece_data = armor_data[rank].get(name)
        if piece_data is None:
            return None

        return ArmorPiece(
            armor_type=ArmorType.HELM,
            rank=ArmorRank.from_str(rank),
            name=name,
            slots=piece_data.get("slots", [0, 0, 0, 0]),
            buffs=piece_data.get("buffs", {}),
        )

    def __repr__(self) -> str:
        return f"ArmorPiece(rank={self.rank.name}, name={self.name}, type={self.armor_type.name})"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "type": self.armor_type,
            "rank": self.rank.value,
            "buffs": self.buffs,
            "slots": self.slots,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Self:
        try:
            return ArmorPiece(
                name=data["name"],
                armor_type=data["type"],
                rank=ArmorRank.from_str(data["rank"]),
                buffs=data["buffs"],
                slots=data["slots"],
            )
        except (KeyError, ValueError) as exc:
            raise ValueError(
                f"dict: {data} is not a valid dictionary for an armor piece. {exc}"
            )


class ArmorSet:
    def __init__(
        self,
        name: str,
        helm: ArmorPiece | None = None,
        chest: ArmorPiece | None = None,
        arm: ArmorPiece | None = None,
        waist: ArmorPiece | None = None,
        leg: ArmorPiece | None = None,
        charm: ArmorPiece | None = None,
    ) -> None:
        self.name = name
        self.helm = helm
        self.chest = chest
        self.arm = arm
        self.waist = waist
        self.leg = leg
        # NOTE: Possibly create charm as seperate class? it has name + buff
        self.charm = charm

    def get_buffs(self) -> dict[str, int]:
        pieces = [self.helm, self.chest, self.arm, self.waist, self.leg]
        buffs = {}

        for piece in pieces:
            if piece is None:
                continue

            for key, value in piece.buffs.items():
                if key not in buffs:
                    buffs[key] = 0
                buffs[key] += value

        return buffs

    def get_decoration_slots(self) -> list[int]:
        pieces = [self.helm, self.chest, self.arm, self.waist, self.leg]
        slots = [0, 0, 0, 0]

        for piece in pieces:
            if piece is None:
                continue

            for i in range(len(slots)):
                slots[i] += piece.slots[i]

        return slots

    def __repr__(self) -> str:
        return f"""ArmorSet(
            name={self.name}
            helm={self.helm}
            chest={self.chest}
            arm={self.arm}
            waist={self.waist}
            leg={self.leg}
            charm={self.charm}
        )"""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "helm": self.helm.to_dict(),
            "chest": self.chest.to_dict(),
            "arm": self.arm.to_dict(),
            "waist": self.waist.to_dict(),
            "leg": self.leg.to_dict(),
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Self:
        try:
            return ArmorSet(
                name=data["name"],
                helm=ArmorPiece.from_dict(data["helm"]),
                chest=ArmorPiece.from_dict(data["chest"]),
                arm=ArmorPiece.from_dict(data["arm"]),
                waist=ArmorPiece.from_dict(data["waist"]),
                leg=ArmorPiece.from_dict(data["leg"]),
            )

        except (KeyError, ValueError):
            raise ValueError(
                f"dict: {data} is not a valid dictionary for an armor set. {exc}"
            )
