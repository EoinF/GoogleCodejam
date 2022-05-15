from dataclasses import dataclass
from math import ceil, floor

# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


def read_strings():
    return input().split(" ")


# endregion


@dataclass
class CaseParams:
    n: int
    l: int


def solve_problem():
    test_cases = read_int()

    for c in range(1, test_cases + 1):
        case = CaseParams(*read_ints())
        print(f"Case #{c}: {solve_case(case)}")


@dataclass
class Answer:
    c: int
    pct: int
    pop_needed: int
    add_1: int

    def __init__(self, c, n) -> None:
        self.c = c
        pct = (100 * c) / n
        self.pct = round(pct)
        self.add_1 = self.pct - floor(pct)

    def calc_pop_needed(self, n, unused):
        n_div_100 = 100 / n

        if self.add_1 == 0:
            a = 0
            add_1 = 0

            # search for needed
            while a < unused:
                a += 1
                pct = (self.c + a) * n_div_100
                rounded_pct = round(pct)
                add_1 = rounded_pct - floor(pct)

                if add_1 == 1:
                    self.pop_needed = a
                    self.new_pct = rounded_pct
                    return

            self.pop_needed = n
        else:
            self.pop_needed = n + 1
            self.new_pct = self.pct


def solve_case(case: CaseParams):
    counts = read_ints()
    answers = []
    total_used = 0
    for c in counts:
        answers.append(Answer(c, case.n))
        total_used += c

    unused = case.n - total_used

    for a in answers:
        a.calc_pop_needed(case.n, unused)

    new_answer = Answer(1, case.n)
    new_answer.calc_pop_needed(case.n, unused)
    if new_answer.pop_needed == case.n + 1:
        new_answer.pop_needed = 0

    sorted(answers, key=lambda a: a.pop_needed)

    total_pct = 0

    while unused > 0:
        next_pop = answers[0].pop_needed if len(answers) > 0 else case.n
        new_pop = new_answer.pop_needed + 1

        if new_pop > unused and next_pop > unused:
            unused_answer = Answer(unused, case.n)
            total_pct += unused_answer.pct
            break

        if next_pop < new_pop:
            old = answers.pop(0)
            total_pct += old.new_pct
            unused -= next_pop
        else:
            total_pct += new_answer.new_pct
            unused -= new_pop

    total_pct += sum([answer.pct for answer in answers])

    return total_pct


if __name__ == "__main__":
    solve_problem()
