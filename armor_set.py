from enum import Enum, auto


class ArmorType(Enum):
    HELM = auto()
    CHEST = auto()
    ARM = auto()
    WAIST = auto()
    LEG = auto()
    CHARM = auto()


class ArmorRank(Enum):
    LR = auto()
    HR = auto()
    MR = auto()


class ArmorPiece:
    def __init__(self, armor_type: ArmorType, rank: ArmorRank, name: str) -> None:
        self.name = name
        self.armor_type = armor_type
        self.rank = rank

    def get_buffs(self) -> dict[str, int]:
        raise NotImplementedError

    def get_decoration_slots(self) -> list[int]:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"ArmorPiece(rank={self.rank.name}, name={self.name}, type={self.armor_type.name})"


class ArmorSet:
    def __init__(
        self,
        helm: ArmorPiece | None = None,
        chest: ArmorPiece | None = None,
        arm: ArmorPiece | None = None,
        waist: ArmorPiece | None = None,
        leg: ArmorPiece | None = None,
        charm: ArmorPiece | None = None,
    ) -> None:
        self.helm = helm
        self.chest = chest
        self.arm = arm
        self.waist = waist
        self.leg = leg
        self.charm = charm

    def get_set_buffs(self) -> dict[str, int]:
        raise NotImplementedError

    def get_set_decoration_slots(self) -> list[int]:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"""ArmorSet(
            helm={self.helm}
            chest={self.chest}
            arm={self.arm}
            waist={self.waist}
            leg={self.leg}
            charm={self.charm}
        )"""
