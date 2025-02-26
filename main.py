from rich import print

from armor_data import (load_armor_data, load_armor_sets, save_armor_sets,
                        sync_armor_data)
from armor_set import ArmorPiece, ArmorSet
from parse_args import parse_args


def list_armor_pieces(args, armor_data) -> None:
    for piece_type in ["head", "chest", "gloves", "waist", "legs"]:
        print(f"\n[{piece_type}]")
        piece = ArmorPiece.new(
            piece_type,
            args.rank,
            args.name,
            armor_data,
        )
        piece.print_to_console()


def create_armor_set(args, armor_data) -> ArmorSet:
    return ArmorSet(
        name=args.name,
        helm=ArmorPiece.new("head", args.rank, args.head, armor_data),
        chest=ArmorPiece.new(
            "chest",
            args.rank,
            args.chest,
            armor_data,
        ),
        arm=ArmorPiece.new("gloves", args.rank, args.gloves, armor_data),
        waist=ArmorPiece.new(
            "waist",
            args.rank,
            args.waist,
            armor_data,
        ),
        leg=ArmorPiece.new("legs", args.rank, args.legs, armor_data),
    )


def get_armor_set(armor_sets: list[ArmorSet], name) -> ArmorSet | None:
    armor_set = list(
        filter(
            lambda armor_set: armor_set.name == name,
            armor_sets,
        )
    )
    if armor_set == []:
        print(f"Could not find set with the name: {name}")
        return None
    else:
        return armor_set[0]


def main():
    args = parse_args()
    sync_armor_data()
    armor_data = load_armor_data()
    armor_sets: list[ArmorSet] = load_armor_sets()

    match args.action:
        case "create":
            armor_set = create_armor_set(args, armor_data)
            armor_sets.append(armor_set)
            save_armor_sets(armor_sets)
        case "edit":
            armor_set = get_armor_set(armor_sets, args.name)
            if armor_set is None:
                return

            new_piece = ArmorPiece.new(
                args.piece, args.rank, args.new_piece, armor_data
            )
            armor_set.replace_piece(new_piece.armor_type, new_piece)
            save_armor_sets(armor_sets)

        case "compare":
            return
        case "list":
            match args.type:
                case "piece":
                    armor_set = armor_data[args.rank].get(args.name)
                    if armor_set is None:
                        print(f"Could not find armor set: {args.name}")
                    elif args.piece == "all":
                        list_armor_pieces()
                    else:
                        piece = ArmorPiece.new(
                            args.piece,
                            args.rank,
                            args.name,
                            armor_data,
                        )
                        piece.print_to_console()

                case "set":
                    armor_set = get_armor_set(armor_sets, args.name)
                    armor_set.print_to_console()

                case "all-pieces":
                    for rank, armor_sets in armor_data.items():
                        print(f"===== {rank} =====")
                        for armor_set in armor_sets:
                            print(f"- {armor_set}")

                case "all-sets":
                    print("===== Armor Set names =====")
                    for armor_set in armor_sets:
                        print(f"- {armor_set.name}")


if __name__ == "__main__":
    main()
