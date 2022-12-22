"""
SurveyGuru
----------

SurveyGuru is an application for survey data generation.
"""

from argparse import Namespace
from survey import Survey
from auto import Guru, forms_to_dict


def get_data(filename: str) -> dict:
    import json
    import yaml

    data = None

    with open(filename, "r") as f:
        if filename.endswith(".json"):
            data = json.load(f)
        elif filename.endswith(".yaml") or filename.endswith(".yml"):
            data = yaml.safe_load(f)
    if data is None:
        raise ValueError(f"Unknown file type: {filename}")
    return data


def export_data(filename: str, data: dict) -> None:
    from csv import writer

    if not data:
        raise ValueError("Data is empty!")

    with open(filename, "w") as f:
        writer = writer(f)
        writer.writerow([f"Question {q}" for q in tuple(data.values())[0].keys()])
        for row in data.values():
            writer.writerow([ans for ans in row.values()])


def generate_filename(ext: str) -> str:
    import datetime

    now = datetime.datetime.now()
    return f"{now:%Y%m%d%H%M%S}.{ext}"


def get_args() -> Namespace:
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Source of data")
    parser.add_argument("-p", "--population", type=int, help="Population of the survey")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=generate_filename("csv"),
        help="Destination of data",
    )

    return parser.parse_args()


def main():
    args = get_args()
    survey = Survey.from_dict(get_data(args.input))
    guru = Guru(survey)
    data = forms_to_dict(guru.smart_answer(args.population))
    export_data(args.output, data)


if __name__ == "__main__":
    main()
