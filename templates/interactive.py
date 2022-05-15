from dataclasses import dataclass


@dataclass
class InteractiveCase:
    n: int
    remaining_tries: int

    def is_empty(self):
        return self.remaining_tries <= 0


# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


def read_strings():
    return input().split(" ")


def _ask_base(case: InteractiveCase, query: "str", read_fn: "function"):
    case.remaining_tries -= 1
    print(query)
    return read_fn()


def ask_int(case: InteractiveCase, query: "str") -> "int":
    return _ask_base(case, query, read_int)


def ask_ints(case: InteractiveCase, query: "str") -> "list[int]":
    return _ask_base(case, query, read_ints)


def ask_string(case: InteractiveCase, query: "str") -> "str":
    return _ask_base(case, query, input)


def ask_strings(case: InteractiveCase, query: "str") -> "list[str]":
    return _ask_base(case, query, read_strings)


# endregion


def solve_problem():
    test_cases = read_int()

    for c in range(test_cases):
        case = InteractiveCase(*read_ints())
        print(f"{solve_case(case)}")


def solve_case(case: InteractiveCase):
    output = ask_ints(case, "")

    if case.is_empty():
        pass

    return ""


if __name__ == "__main__":
    solve_problem()
