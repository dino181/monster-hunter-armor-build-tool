from armor_data import load_armor_data, sync_armor_data
from armor_set import ArmorPiece, ArmorSet, ArmorType
from parse_args import parse_args


def main():
    args = parse_args()
    sync_armor_data()
    armor_data = load_armor_data()

    match args.action:
        case "create":
            armor_set = ArmorSet(
                helm=ArmorPiece.new(ArmorType.HELM, args.rank, args.helm, armor_data),
                chest=ArmorPiece.new(
                    ArmorType.CHEST,
                    args.rank,
                    args.chest,
                    armor_data,
                ),
                arm=ArmorPiece.new(ArmorType.ARM, args.rank, args.arm, armor_data),
                waist=ArmorPiece.new(
                    ArmorType.WAIST,
                    args.rank,
                    args.waist,
                    armor_data,
                ),
                leg=ArmorPiece.new(ArmorType.LEG, args.rank, args.leg, armor_data),
            )
            print(armor_set)
        case "edit":
            return
        case "compare":
            return


if __name__ == "__main__":
    main()
