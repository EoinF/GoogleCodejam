from copy import deepcopy
from dataclasses import dataclass, field
from types import prepare_class

# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


def read_strings():
    return input().split(" ")


# endregion


@dataclass
class SearchState:
    n: int
    board_state: "list[list[int]]"
    preplaced: "list[list[bool]]"
    columns_used: "list[list[int]]"
    rows_used: "list[list[int]]"
    diagonals_down_right_used: "list[list[int]]"
    diagonals_down_left_used: "list[list[int]]"

    columns_with_rook: "list[int]" = field(default_factory=list)
    rows_with_rook: "list[int]" = field(default_factory=list)
    diagonals_down_right_with_bishop: "list[int]" = field(default_factory=list)
    diagonals_down_left_with_bishop: "list[int]" = field(default_factory=list)

    def place_rook(
        self, r, c, diagonal_down_left, diagonal_down_right, is_preplaced=False
    ):
        print(f"place + {r} {c}")
        self.board_state[r][c] = "+"
        self.preplaced[r][c] = is_preplaced
        self.rows_with_rook.append(r)
        self.columns_with_rook.append(c)
        self.rows_used[r] += 1
        self.columns_used[c] += 1
        self.diagonals_down_left_used[diagonal_down_left] += 1
        self.diagonals_down_right_used[diagonal_down_right] += 1

    def place_bishop(
        self, r, c, diagonal_down_left, diagonal_down_right, is_preplaced=False
    ):
        print(f"place x {r} {c}")
        self.preplaced[r][c] = is_preplaced
        self.board_state[r][c] = "x"
        self.rows_used[r] += 1
        self.columns_used[c] += 1
        self.diagonals_down_left_used[diagonal_down_left] += 1
        self.diagonals_down_right_used[diagonal_down_right] += 1
        self.diagonals_down_left_with_bishop.append(diagonal_down_left)
        self.diagonals_down_right_with_bishop.append(diagonal_down_right)

    def remove_rook(self, r, c, diagonal_down_left, diagonal_down_right):
        print(f"remove + {r} {c}")
        self.board_state[r][c] = ""
        self.rows_used[r] -= 1
        self.columns_used[c] -= 1
        self.diagonals_down_left_used[diagonal_down_left] -= 1
        self.diagonals_down_right_used[diagonal_down_right] -= 1
        self.rows_with_rook.remove(r)
        self.columns_with_rook.remove(c)

    def remove_bishop(self, r, c, diagonal_down_left, diagonal_down_right):
        print(f"remove x {r} {c}")
        self.board_state[r][c] = ""
        self.rows_used[r] -= 1
        self.columns_used[c] -= 1
        self.diagonals_down_left_used[diagonal_down_left] -= 1
        self.diagonals_down_right_used[diagonal_down_right] -= 1
        self.diagonals_down_left_with_bishop.remove(diagonal_down_left)
        self.diagonals_down_right_with_bishop.remove(diagonal_down_right)

    def place_queen(
        self, r, c, diagonal_down_left, diagonal_down_right, is_preplaced=False
    ):
        print(f"place o {r} {c}")
        self.preplaced[r][c] = is_preplaced
        self.board_state[r][c] = "o"
        self.rows_used[r] += 1
        self.columns_used[c] += 1
        self.diagonals_down_left_used[diagonal_down_left] += 1
        self.diagonals_down_right_used[diagonal_down_right] += 1

    def remove_queen(self, r, c, diagonal_down_left, diagonal_down_right):
        print(f"remove o {r} {c}")
        self.board_state[r][c] = ""
        self.rows_used[r] -= 1
        self.columns_used[c] -= 1
        self.diagonals_down_left_used[diagonal_down_left] -= 1
        self.diagonals_down_right_used[diagonal_down_right] -= 1


@dataclass
class CaseParams:
    n: int
    m: int


def get_diagonals(r, c, n):
    diagonal_down_right = r + c
    diagonal_down_left = (n - r) + c
    return diagonal_down_left, diagonal_down_right


def solve_problem():
    test_cases = read_int()

    for c in range(1, test_cases + 1):
        case = CaseParams(*read_ints())
        total, lines = solve_case(case)
        print(f"Case #{c}: {total} {len(lines)}")
        for line in lines:
            print(line)


def ensure_board_valid(state: SearchState, r: int, c: int):
    diagonal_down_left, diagonal_down_right = get_diagonals(r, c, state.n)
    print(f"ensure valid {r} {c}")
    print(state.rows_used[r], state.rows_with_rook)
    # Ensure row is valid
    if state.rows_used[r] > 1 and r not in state.rows_with_rook:
        print("checking row", c + 1, state.n + 2)
        for c2 in range(c + 1, state.n + 2):
            if c2 >= state.n:
                print(f"row not valid {r} {c}")
                return None
            elif state.board_state[r][c2] == "":
                state.place_rook(r, c2, diagonal_down_left, diagonal_down_right)
                result = ensure_board_valid(state, r, c2)
                if result is None:
                    state.remove_rook(r, c2, diagonal_down_left, diagonal_down_right)
                else:
                    break
    print(f"row valid {r} {c}")

    # Ensure column is valid
    if state.columns_used[c] > 1 and c not in state.columns_with_rook:
        print("checking column", r + 1, state.n + 2)
        for r2 in range(r + 1, state.n + 2):
            if r2 >= state.n:
                print(f"column not valid {r} {c}")
                return None
            elif state.board_state[r2][c] == "":
                state.place_rook(r2, c, diagonal_down_left, diagonal_down_right)
                result = ensure_board_valid(state, r2, c)
                if result is None:
                    state.remove_rook(r2, c, diagonal_down_left, diagonal_down_right)
                else:
                    break
    print(f"column valid {r} {c}")

    print(state.diagonals_down_right_used[diagonal_down_right])
    # Ensure diagonal down right is valid
    if (
        state.diagonals_down_right_used[diagonal_down_right] > 1
        and diagonal_down_right not in state.diagonals_down_right_with_bishop
    ):
        upper_bound = state.n - max(r, c) - 1
        i = 1
        while True:
            if i >= upper_bound:
                print(f"down_right not valid {r} {c}")
                return None
            elif state.board_state[r + i][c + i] == "":
                state.place_bishop(
                    r + i, c + i, diagonal_down_left, diagonal_down_right
                )
                result = ensure_board_valid(state, r + i, c + i)
                if result is None:
                    state.remove_bishop(
                        r + i, c + i, diagonal_down_left, diagonal_down_right
                    )
                else:
                    break
        i += 1

    print(f"----------down_right valid {r} {c}")

    print(state.diagonals_down_left_used[diagonal_down_left])
    # Ensure diagonal down left is valid
    if (
        state.diagonals_down_left_used[diagonal_down_left] > 1
        and diagonal_down_left not in state.diagonals_down_left_with_bishop
    ):
        print("checking", state.n, r - 1, state.n - c)
        upper_bound = state.n - max(r - 1, state.n - c)
        i = 1
        while True:
            if i >= upper_bound:
                print(f"down_left not valid {r} {c}")
                return None
            elif state.board_state[r + i][c - i] == "":
                state.place_bishop(
                    r + i, c - i, diagonal_down_left, diagonal_down_right
                )
                result = ensure_board_valid(state, r + i, c - i)
                if result is None:
                    state.remove_bishop(
                        r + i, c - i, diagonal_down_left, diagonal_down_right
                    )
                else:
                    break
            i += 1

    print(f"down_left valid {r} {c}")
    return True


def try_place_queen(state: SearchState, r, c):
    diagonal_down_left, diagonal_down_right = get_diagonals(r, c, state.n)
    state.place_queen(r, c, diagonal_down_left, diagonal_down_right)
    result = ensure_board_valid(state, r, c)
    if result is None:
        state.remove_queen(r, c, diagonal_down_left, diagonal_down_right)


def try_place_bishop(state: SearchState, r, c):
    diagonal_down_left, diagonal_down_right = get_diagonals(r, c, state.n)
    state.place_bishop(r, c, diagonal_down_left, diagonal_down_right)
    result = ensure_board_valid(state, r, c)
    if result is None:
        state.remove_bishop(r, c, diagonal_down_left, diagonal_down_right)


def try_place_rook(state: SearchState, r, c):
    diagonal_down_left, diagonal_down_right = get_diagonals(r, c, state.n)
    state.place_rook(r, c, diagonal_down_left, diagonal_down_right)
    result = ensure_board_valid(state, r, c)
    if result is None:
        state.remove_rook(r, c, diagonal_down_left, diagonal_down_right)


def search_next(state: SearchState):
    r = 0
    c = 0

    for r in range(state.n):
        for c in range(state.n):
            print("============")
            print(f"trying {r} {c}")
            print("============")
            print(state.board_state[r][c])

            preplaced_type = ""
            diagonal_down_left, diagonal_down_right = get_diagonals(r, c, state.n)

            if state.preplaced[r][c]:
                preplaced_type = state.board_state[r][c]
                if preplaced_type == "+":
                    state.remove_rook(r, c, diagonal_down_left, diagonal_down_right)
                if preplaced_type == "x":
                    state.remove_bishop(r, c, diagonal_down_left, diagonal_down_right)

            if state.board_state[r][c] == "":
                try_place_queen(state, r, c)
            if state.board_state[r][c] == "":
                try_place_rook(state, r, c)
            if state.board_state[r][c] == "":
                try_place_bishop(state, r, c)

            if state.board_state[r][c] == "":
                if preplaced_type == "+":
                    state.place_rook(r, c, diagonal_down_left, diagonal_down_right)
                if preplaced_type == "x":
                    state.remove_bishop(r, c, diagonal_down_left, diagonal_down_right)


style_map = {"+": 1, "x": 1, "o": 2, "": 0}


def solve_case(case: CaseParams):
    n = case.n

    # print(f"case {case.n} {case.m}")

    state = SearchState(
        n,
        [[""] * n for _ in range(n)],
        [[False] * n for _ in range(n)],
        [0] * n,
        [0] * n,
        [0] * (n * 2),
        [0] * (n * 2),
    )
    for m in range(case.m):
        [t, y, x] = read_strings()
        c = int(x) - 1
        r = int(y) - 1
        diagonal_down_left, diagonal_down_right = get_diagonals(r, c, n)
        if t == "x":
            state.place_bishop(r, c, diagonal_down_left, diagonal_down_right, True)
        elif t == "+":
            state.place_rook(r, c, diagonal_down_left, diagonal_down_right, True)
        else:
            state.place_queen(r, c, diagonal_down_left, diagonal_down_right, True)

    print(state)
    search_next(state)

    total = 0
    lines = []
    for r in range(n):
        for c in range(n):
            if state.board_state[r][c] != "" and not state.preplaced[r][c]:
                lines.append(f"{state.board_state[r][c]} {r + 1} {c + 1}")
            total += style_map[state.board_state[r][c]]

    return total, lines


if __name__ == "__main__":
    solve_problem()
