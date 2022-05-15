from cmath import sqrt
from dataclasses import dataclass
from math import ceil


@dataclass
class InteractiveCase:
    n: int
    remaining_tries: int = 1000

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
        solve_case(case)


def hash_x_y(x, y, n):
    return y * n + x


def move_right_if_needed(
    current_square_buffer,
    top_edge_hits,
    left_edge_x,
    right_edge_x,
    top_edge_y,
    bottom_edge_y,
    n,
):
    while left_edge_x in top_edge_hits and left_edge_x + 3 < right_edge_x:
        top_edge_hits.remove(left_edge_x)
        left_edge_x += 1

    if top_edge_y + 3 < bottom_edge_y and left_edge_x + 3 == right_edge_x:
        if len(top_edge_hits) == 3:
            left_edge_x = 0
            top_edge_y += 1
            top_edge_hits = set(
                [
                    p
                    for p in range(3)
                    if hash_x_y(p, top_edge_y, n) in current_square_buffer
                ]
            )
            if top_edge_y + 3 < bottom_edge_y:
                return move_right_if_needed(
                    current_square_buffer,
                    top_edge_hits,
                    left_edge_x,
                    right_edge_x,
                    top_edge_y,
                    bottom_edge_y,
                    n,
                )

    return left_edge_x, top_edge_y


def solve_case(case: InteractiveCase):
    area = case.n

    width, height = (67, 3) if area == 200 else (7, 3)
    right_edge_x = width
    bottom_edge_y = height
    left_edge_x = 0
    top_edge_y = 0

    left_edge_hits = set()
    top_edge_hits = set()

    current_square_buffer = set()

    while not case.is_empty():
        [prepped_y, prepped_x] = ask_ints(case, f"{top_edge_y + 2} {left_edge_x + 2}")

        if prepped_x == -1 and prepped_y == -1:
            exit()
        if prepped_y == 0 and prepped_x == 0:
            return  # Solved
        else:
            prepped_x -= 1
            prepped_y -= 1

        current_square_buffer.add(hash_x_y(prepped_x, prepped_y, width))

        if top_edge_y + 3 < bottom_edge_y and prepped_y == top_edge_y:
            top_edge_hits.add(prepped_x)
            left_edge_x, top_edge_y = move_right_if_needed(
                current_square_buffer,
                top_edge_hits,
                left_edge_x,
                right_edge_x,
                top_edge_y,
                bottom_edge_y,
                width,
            )

        if top_edge_y + 3 == bottom_edge_y and prepped_x == left_edge_x:
            left_edge_hits.add(prepped_y)
            while left_edge_x + 3 < right_edge_x and len(left_edge_hits) == 3:
                left_edge_x += 1
                left_edge_hits = set(
                    [
                        p
                        for p in range(3)
                        if hash_x_y(left_edge_x, top_edge_y + p, width)
                        in current_square_buffer
                    ]
                )

    if case.is_empty():
        exit()

    return ""


if __name__ == "__main__":
    solve_problem()
