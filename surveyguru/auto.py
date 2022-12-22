import random
from typing import List

from survey import EffectType, Option, Question, Survey

__all__ = ("Guru", "forms_to_dict")


class Form:
    def __init__(self, survey: Survey):
        self.survey = survey
        self.answers = {}

    def answer(self, qs: int, answer: Option):
        self.survey.check_q_exists(qs)
        self.answers[qs] = answer

    def accumulate_effect(self, qs_id: int) -> int:
        qs: Question = self.survey.get_question(qs_id)
        total_effect = 0
        if qs is None:
            raise ValueError(f"Question {qs_id} not found")

        for qs_id, con in qs.connection.items():
            ans = self.answers.get(qs_id, None)
            if ans is None:
                continue
            for opt, prob in (
                self.survey.get_question(qs_id).opt_probabilities().items()
            ):
                if opt == ans:
                    total_effect += (con.weight * prob) * (
                        1 if con.effect == EffectType.DIRECT else -1
                    )
                    break
        return round(total_effect)

    def to_dict(self) -> dict:
        sorted_keys = sorted(self.answers.keys())
        return {q: self.answers[q].name for q in sorted_keys}


class Guru:
    def __init__(self, survey: Survey):
        self.survey = survey

    def smart_answer(self, population: int) -> List[Form]:
        forms = []
        sorted_qs = self.survey.sort_questions(reverse=True)
        for _ in range(population):
            form = Form(self.survey)
            for q in sorted_qs:
                form.answer(q.id, rand_decide(form, q.id))
            forms.append(form)
        return forms

    def rand_answer(self, population: int) -> List[Form]:
        forms = []
        for _ in range(population):
            form = Form(self.survey)
            for q in self.survey.questions:
                form.answer(q, random.choice(self.survey.questions[q].options))
            forms.append(form)
        return forms


def forms_to_dict(forms: List[Form]) -> dict:
    return {i: form.to_dict() for i, form in enumerate(forms)}


def rand_decide(form: Form, qs_id: int) -> Option:
    total_effect = form.accumulate_effect(qs_id)
    min_r = min(0 + (total_effect if total_effect > 0 else 0), 100)
    max_r = max(100 + (total_effect if total_effect < 0 else 0), 0)
    qs: Question = form.survey.get_question(qs_id)
    opts = qs.sorted_options()

    ans_prob = random.randrange(min_r, max_r)
    dist = qs.probability_left / qs.num_unprioritized
    start, end = 0, 0
    for opt in opts:
        if opt.probability is None:
            end = start + dist
        else:
            end = start + opt.probability
        if start <= ans_prob < end:
            return opt
        start = end
