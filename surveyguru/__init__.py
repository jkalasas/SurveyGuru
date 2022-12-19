"""
SurveyGuru
----------

SurveyGuru is an application for survey data generation.
"""

from argparse import Namespace
from survey import Survey


def get_data(filename: str) -> dict:
    import json
    import yaml

    with open(filename, "r") as f:
        if filename.endswith(".json"):
            return json.load(f)
        elif filename.endswith(".yaml") or filename.endswith(".yml"):
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unknown file type: {filename}")


def generate_filename(ext: str) -> str:
    import datetime

    now = datetime.datetime.now()
    return f"{now:%Y%m%d%H%M%S}.{ext}"


def get_args() -> Namespace:
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("input_file", type=str, help="Source of data")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=lambda: generate_filename("csv"),
        help="Destination of data",
    )

    return parser.parse_args()


def main():
    args = get_args()
    survey = Survey.from_dict(get_data(args.input_file))


if __name__ == "__main__":
    main()
