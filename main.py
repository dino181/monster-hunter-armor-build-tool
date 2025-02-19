from armor_set import ArmorPiece, ArmorRank, ArmorSet, ArmorType


def main():
    piece = ArmorPiece(ArmorType.HELM, ArmorRank.MR, "kulu")
    print(piece)
    armor_set = ArmorSet(helm=piece)
    print(armor_set)


if __name__ == "__main__":
    main()
