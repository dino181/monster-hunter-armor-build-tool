from enum import Enum
from typing import Any, Self

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

LEVEL_FILLED = "▰"
LEVEL_NOT_FILLED = "▱"


class ArmorType(Enum):
    HELM = "head"
    CHEST = "chest"
    ARM = "gloves"
    WAIST = "waist"
    LEG = "legs"
    CHARM = "charm"

    @staticmethod
    def from_str(value: str) -> Self:
        for rank in ArmorType:
            if rank.value == value:
                return rank
        raise ValueError(f"Could not convert {value} to ArmorType enum")


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
        armor_type: str, rank: str, name: str, armor_data: dict[str, Any]
    ) -> Self | None:
        if rank not in armor_data.keys():
            raise ValueError(f"rank must be one of: {list(armor_data.keys())}")

        try:
            piece_data = armor_data[rank][name][armor_type]
        except KeyError:
            print("Could not find piece.")
            return None

        return ArmorPiece(
            armor_type=ArmorType.from_str(armor_type),
            rank=ArmorRank.from_str(rank),
            name=name,
            slots=piece_data.get("slots", [0, 0, 0, 0]),
            buffs=piece_data.get("skills", {}),
        )

    def __repr__(self) -> str:
        return f"ArmorPiece(rank={self.rank.name}, name={self.name}, type={self.armor_type.name})"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "type": self.armor_type.value,
            "rank": self.rank.value,
            "buffs": self.buffs,
            "slots": self.slots,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Self | None:
        if not data:
            return None
        try:
            return ArmorPiece(
                name=data["name"],
                armor_type=ArmorType.from_str(data["type"]),
                rank=ArmorRank.from_str(data["rank"]),
                buffs=data["buffs"],
                slots=data["slots"],
            )
        except (KeyError, ValueError) as exc:
            raise ValueError(
                f"dict: {data} is not a valid dictionary for an armor piece. {exc}"
            )

    def print_to_console(self):
        max_level = 5
        console = Console()

        skill_table = Table(show_edge=False, show_header=False)
        skill_table.add_column("Skill name")
        skill_table.add_column("Skill level")
        for name, level in self.buffs.items():
            skill_name = f"{name}"
            skill_level = f"[bold cyan]{LEVEL_FILLED * level}[/bold cyan][cyan]{LEVEL_NOT_FILLED * (max_level - level)}"
            skill_table.add_row(skill_name, skill_level)
        skill_panel = Panel.fit(skill_table, title="Skills", padding=1)

        slot_table = Table(show_edge=False, show_header=False)
        slot_table.add_column("slot size")
        slot_table.add_column("amount")
        for slot_size, amount in enumerate(self.slots):
            if amount != 0:
                slot_table.add_row(f"{slot_size + 1} Slot", f"[cyan]{amount}[/cyan]")
        slot_panel = Panel.fit(slot_table, title=f"Decoration slots", padding=1)

        console.print(Columns([skill_panel, slot_panel]))


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

    def get_piece_names(self) -> dict[str, str]:
        return {
            "head": self.helm.name if self.helm else "-",
            "chest": self.chest.name if self.chest else "-",
            "gloves": self.arm.name if self.arm else "-",
            "waist": self.waist.name if self.waist else "-",
            "legs": self.leg.name if self.leg else "-",
        }

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

    def replace_piece(self, armor_type: ArmorType, piece: ArmorPiece):
        match armor_type:
            case ArmorType.HELM:
                self.helm = piece
            case ArmorType.CHEST:
                self.chest = piece
            case ArmorType.ARM:
                self.arm = piece
            case ArmorType.WAIST:
                self.waist = piece
            case ArmorType.LEG:
                self.leg = piece

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
            "helm": self.helm.to_dict() if self.helm else None,
            "chest": self.chest.to_dict() if self.chest else None,
            "arm": self.arm.to_dict() if self.arm else None,
            "waist": self.waist.to_dict() if self.waist else None,
            "leg": self.leg.to_dict() if self.leg else None,
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

        except (KeyError, ValueError) as exc:
            raise ValueError(
                f"dict: {data} is not a valid dictionary for an armor set. \n{exc}"
            )

    def print_to_console(self):
        max_level = 5
        console = Console()

        piece_table = Table(show_edge=False, show_header=False)
        piece_table.add_column("piece")
        piece_table.add_column("name")
        for piece, name in self.get_piece_names().items():
            piece_table.add_row(f"{piece}", f"[cyan]{name}[/cyan]")
        piece_panel = Panel.fit(piece_table, title=f"Decoration slots", padding=1)

        skill_table = Table(show_edge=False, show_header=False)
        skill_table.add_column("Skill name")
        skill_table.add_column("Skill level")
        buffs = self.get_buffs()
        if not buffs:
            skill_table.add_row("No skills", "[cyan]-[/cyan]")

        for name, level in buffs.items():
            skill_name = f"{name}"
            skill_level = f"[bold cyan]{LEVEL_FILLED * level}[/bold cyan][cyan]{LEVEL_NOT_FILLED * (max_level - level)}"
            skill_table.add_row(skill_name, skill_level)
        skill_panel = Panel.fit(skill_table, title="Skills", padding=1)

        slot_table = Table(show_edge=False, show_header=False)
        slot_table.add_column("slot size")
        slot_table.add_column("amount")
        decoration_slots = self.get_decoration_slots()
        if sum(decoration_slots) == 0:
            slot_table.add_row("No slots", "[cyan]-[/cyan]")

        for slot_size, amount in enumerate(decoration_slots):
            if amount != 0:
                slot_table.add_row(f"{slot_size + 1} Slot", f"[cyan]{amount}[/cyan]")
        slot_panel = Panel.fit(slot_table, title=f"Decoration slots", padding=1)

        console.print(Columns([piece_panel, skill_panel, slot_panel]))
