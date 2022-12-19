from __future__ import annotations
from typing import Dict, List, Union
from enum import IntEnum

__all__ = (
    "Survey",
    "Question",
    "Option",
    "Connection",
    "EffectType",
)


class EffectType(IntEnum):
    NONE = 0
    POSITIVE = 1
    NEGATIVE = 2


class Connection:
    def __init__(
        self, q1: int, qs: Union(List[int], int), effect: EffectType, weight: float
    ) -> None:
        self.affector = q1
        self.affected = type(qs) == list and qs or [qs]
        self.effect = effect
        self.weight = weight


class Option:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"{self.name} - ({self.value})"

    def __str__(self) -> str:
        return f"{self.name} - ({self.value})"


class Question:
    def __init__(self, question: str, options: List[Option]):
        self.question = question
        self.options = options

    def __repr__(self) -> str:
        return f"Question: {self.question}"

    def __str__(self) -> str:
        return f"Question: {self.question}"

    def add_option(self, option: Option):
        self.options.append(option)


class Survey:
    def __init__(
        self,
        title: str = "",
        description: str = "",
        questions: Dict[int, Question] = {},
        connections: List[Connection] = [],
    ):
        self.title = title
        self.description = description
        self.questions = questions
        self.connections = connections

    def __repr__(self) -> str:
        return f"Survey: {self.title}"

    def __str__(self) -> str:
        return f"Survey: {self.title}"

    def check_q_exists(self, q: int):
        if q not in self.questions:
            raise ValueError(f"Question {q} does not exist")

    @staticmethod
    def from_dict(dict: dict) -> Survey:
        survey = Survey()
        for key, value in dict.items():
            if key == "title":
                survey.title = value
            elif key == "description":
                survey.description = value
            elif key == "questions":
                for question in value:
                    id = question["id"]
                    options = [
                        Option(o["name"], o["value"]) for o in question["options"]
                    ]
                    survey.questions[id] = Question(question["question"], options)
            elif key == "connections":
                for connection in value:
                    if survey.check_q_exists(connection["affector"]):
                        survey.connections.append(
                            Connection(
                                connection["affector"],
                                connection["affected"],
                                connection["effect"],
                                connection["weight"],
                            )
                        )
        return survey
