import argparse
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="armor-build-tool")
    group_create = parser.add_argument_group("create")
    # group_edit = parser.add_argument_group("edit")
    # group_compare = parser.add_argument_group("compare")
    parser.add_argument(
        "action",
        choices=["create", "edit", "compare"],
        help="The action to perform.",
    )
    group_create.add_argument(
        "-r",
        "--rank",
        required="create" in sys.argv,
        choices=["low", "high", "master"],
        help="The rank of the armor ",
    )

    group_create.add_argument(
        "--helm",
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
        "--arm",
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
        "--leg",
        type=str,
        default="",
        help="The armor set name of the leg piece.",
    )

    return parser.parse_args()
