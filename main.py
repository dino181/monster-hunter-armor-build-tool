from armor_data import load_armor_data, sync_armor_data
from armor_set import ArmorPiece, ArmorRank, ArmorSet, ArmorType


def main():
    sync_armor_data()
    armor_data = load_armor_data()


if __name__ == "__main__":
    main()
