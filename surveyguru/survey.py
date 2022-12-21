from __future__ import annotations
from enum import IntEnum
from functools import cmp_to_key
from math import ceil, floor
from typing import Dict, List, Union

__all__ = (
    "Survey",
    "Question",
    "Option",
    "Connection",
    "EffectType",
)


class EffectType(IntEnum):
    NONE = 0
    DIRECT = 1
    INVERSE = 2


class QuestionPriority(IntEnum):
    LOW = 0
    NORMAL = 1
    MEDIUM = 2
    HIGH = 3


class Connection:
    def __init__(self, weight: float, effect: EffectType) -> None:
        self.weight = weight
        self.effect = effect


class Option:
    def __init__(self, name: str, value, probability: int = None):
        self.name = name
        self.value = value
        self.probability = probability

    def __repr__(self) -> str:
        return f"{self.name} - ({self.value})"

    def __str__(self) -> str:
        return f"{self.name} - ({self.value})"


class Question:
    def __init__(
        self,
        id: int,
        qs: str,
        opts: List[Option],
        priority: QuestionPriority = QuestionPriority.NORMAL,
    ):
        self.id = id
        self.question = qs
        self.options = opts
        self.prority = priority
        self.connection = {}

        self._probability_left = 100
        self._unprioritized = len(opts)
        for opt in opts:
            if opt.probability is not None:
                self.probability_left -= opt.probability
                self._unprioritized -= 1

    def __repr__(self) -> str:
        return f"Question: {self.question}"

    def __str__(self) -> str:
        return f"Question: {self.question}"

    @property
    def probability_left(self) -> int:
        return self._probability_left

    @probability_left.setter
    def probability_left(self, a: int):
        if a < 0:
            raise ValueError("Allocatable probability is below zero")
        self._probability_left = a

    @property
    def num_unprioritized(self) -> int:
        return self._unprioritized

    @num_unprioritized.setter
    def num_unprioritized(self, a: int):
        if a < 0:
            raise ValueError("Unprioritized options can't be less than zero")
        self._unprioritized = a

    def add_connection(self, qs_id: int, con: Connection):
        self.connection[qs_id] = con

    def add_option(self, opt: Option):
        if opt.probability is not None:
            self.probability_left -= opt.probability
        else:
            self.num_unprioritized += 1
        self.options.append(opt)

    def sorted_options(self, reverse: bool = False):
        return sorted(self.options, key=lambda a: a.value, reverse=reverse)

    def get_opt_values(self, sort=False, reverse=False) -> List:
        return [
            opt.value
            for opt in (self.sorted_options(reverse=reverse) if sort else self.options)
        ]

    def get_max_opt(self) -> Option:
        return max(self.options, key=lambda a: a.value)

    def num_opts(self) -> int:
        return len(self.options)

    def opt_probabilities(self) -> Dict[Option, int]:
        sorted_opt = self.sorted_options()
        opt_probs = {}
        mid = len(sorted_opt) / 2
        if mid % 1 != 0:
            opt_probs[sorted_opt[floor(mid)]] = 0

        # left side
        left = sorted_opt[0 : floor(mid)]
        for i, opt in enumerate(left):
            opt_probs[opt] = -100 + 100 * i / len(left)

        # right side
        right = sorted_opt[ceil(mid) : :]
        for i, opt in enumerate(right):
            opt_probs[opt] = 100 - 100 * (len(right) - i - 1) / len(right)
        return opt_probs


class Survey:
    def __init__(
        self,
        title: str = "",
        description: str = "",
        qs: Dict[int, Question] = {},
        no_qs: int = 0,
    ):
        self.title = title
        self.description = description
        self.questions = qs
        self.num_questions = no_qs

    def __repr__(self) -> str:
        return f"Survey: {self.title}"

    def __str__(self) -> str:
        return f"Survey: {self.title}"

    def check_q_exists(self, q: int):
        if q not in self.questions:
            raise ValueError(f"Question {q} does not exist")

    def add_question(self, qs: Question):
        if qs.id in self.questions:
            raise ValueError(f"Question {qs.id} already in survey")
        self.num_questions += 1
        self.questions[qs.id] = qs

    def get_question(self, id: int) -> Union(Question, None):
        return self.questions.get(id)

    def add_connection(self, frm: int, to: int, con: Connection):
        frm_qs = self.questions.get(frm, None)
        to_qs = self.questions.get(to, None)

        if frm_qs is None:
            raise ValueError(f"Question {frm} not found")
        if to_qs is None:
            raise ValueError(f"Question {to} not found")

        frm_qs.add_connection(to, con)
        to_qs.add_connection(frm, con)

    def sort_questions(self, reverse: bool = False) -> List[Question]:
        return sorted(
            self.questions.values(),
            key=lambda qs: (qs.prority, len(qs.connection)),
            reverse=reverse,
        )

    @staticmethod
    def from_dict(data: dict) -> Survey:
        survey = Survey()
        for key, value in data.items():
            if key == "title":
                survey.title = value
            elif key == "description":
                survey.description = value
            elif key == "questions":
                for qs_data in value:
                    qs = Question(
                        qs_data["id"],
                        qs_data["question"],
                        [
                            Option(
                                opt["name"],
                                opt["value"],
                                probability=opt.get("probability"),
                            )
                            for opt in qs_data["options"]
                        ],
                        priority=qs_data.get("priority", 1),
                    )
                    survey.add_question(qs)
            elif key == "connections":
                for con_data in value:
                    con = Connection(con_data["weight"], con_data["effect"])
                    survey.add_connection(
                        con_data["affector"], con_data["affected"], con
                    )
        return survey
