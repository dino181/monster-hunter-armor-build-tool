import argparse
import sys


def add_create_args(parser: argparse.ArgumentParser):
    group_create = parser.add_argument_group("create")
    group_create.add_argument(
        "-r",
        "--rank",
        required=True,
        choices=["low", "high", "master"],
        help="The rank of the armor ",
    )
    group_create.add_argument(
        "-n",
        "--name",
        required=True,
        type=str,
        help="The name for the armor set",
    )
    group_create.add_argument(
        "--head",
        type=str,
        default="",
        help="The armor set name of the helm piece.",
    )

    group_create.add_argument(
        "--chest",
        type=str,
        default="",
        help="The armor set name of the helm piece.",
    )

    group_create.add_argument(
        "--gloves",
        type=str,
        default="",
        help="The armor set name of the arm piece.",
    )

    group_create.add_argument(
        "--waist",
        type=str,
        default="",
        help="The armor set name of the waist piece.",
    )

    group_create.add_argument(
        "--legs",
        type=str,
        default="",
        help="The armor set name of the leg piece.",
    )


def add_list_args(parser: argparse.ArgumentParser):
    group = parser.add_argument_group("list")
    group.add_argument(
        "type",
        choices=["set", "piece", "all-pieces", "all-sets"],
        help="The item(s) to see the details of",
    )
    group.add_argument(
        "-n",
        "--name",
        required="set" in sys.argv or "piece" in sys.argv,
        type=str,
        help="the name of the item you want to list",
    )

    group.add_argument(
        "-r",
        "--rank",
        required="piece" in sys.argv,
        choices=["low", "high", "master"],
        help="The rank of the armor ",
    )

    group.add_argument(
        "-p",
        "--piece",
        required="piece" in sys.argv,
        choices=["head", "chest", "gloves", "waist", "legs", "all"],
        help="The piece of armor you want to see",
    )


def add_edit_args(parser: argparse.ArgumentParser):
    group = parser.add_argument_group("edit")
    group.add_argument(
        "-n",
        "--name",
        required=True,
        type=str,
        help="the name of the set you want to edit",
    )

    group.add_argument(
        "-r",
        "--rank",
        required=True,
        choices=["master", "high", "low"],
        help="the rank of the piece you want to edit",
    )

    group.add_argument(
        "-p",
        "--piece",
        required=True,
        choices=["head", "chest", "gloves", "waist", "legs"],
        help="the piece you want to edit",
    )

    group.add_argument(
        "--new-piece",
        required=True,
        type=str,
        help="the name of the piece you want to replace it with",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="armor-build-tool")
    parser.add_argument(
        "action",
        choices=["create", "edit", "compare", "list"],
        help="The action to perform.",
    )

    if "create" in sys.argv:
        add_create_args(parser)
    elif "edit" in sys.argv:
        add_edit_args(parser)
    elif "compare" in sys.argv:
        pass
    elif "list" in sys.argv:
        add_list_args(parser)
    else:
        print("Missing an action")

    return parser.parse_args()
