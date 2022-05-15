from dataclasses import dataclass, field
from time import perf_counter_ns


@dataclass
class SearchState:
    n: int
    board_state: "list[list[int]]"
    columns_used: "list[int]" = field(default_factory=list)
    rows_used: "list[int]" = field(default_factory=list)
    diagonals_down_right_used: "list[int]" = field(default_factory=list)
    diagonals_down_left_used: "list[int]" = field(default_factory=list)

    def place_queen(self, r, c, diagonal_down_left, diagonal_down_right):
        self.rows_used.append(r)
        self.columns_used.append(c)
        self.diagonals_down_left_used.append(diagonal_down_left)
        self.diagonals_down_right_used.append(diagonal_down_right)

    def remove_queen(self, r, c, diagonal_down_left, diagonal_down_right):
        self.rows_used.remove(r)
        self.columns_used.remove(c)
        self.diagonals_down_left_used.remove(diagonal_down_left)
        self.diagonals_down_right_used.remove(diagonal_down_right)


def main():
    start_ns = perf_counter_ns()
    state = solve_n_queens(8)
    print(f"elapsed: {(perf_counter_ns() - start_ns) // 1000} microseconds")
    print()
    print_chessboard(state)


def print_chessboard(state: SearchState):
    for r in range(state.n):
        row_cells = []
        for c in range(state.n):
            cell_state = " Q " if c in state.board_state[r] else "   "
            row_cells.append(f"{cell_state}")

        print(f"|{'|'.join(row_cells)}|")
        print(f"|{'--' * (2 * state.n - 1)}-|")


def get_diagonals(r, c, n):
    diagonal_down_right = r + c
    diagonal_down_left = (n - r) + c
    return diagonal_down_left, diagonal_down_right


def search_next(state: SearchState, queens_left: int):
    if queens_left <= 0:
        return state
    else:
        columns = [c for c in range(state.n) if c not in state.columns_used]
        rows = [r for r in range(state.n) if r not in state.rows_used]
        # choose next column
        for c in columns:
            # choose row within column
            for r in rows:
                diagonal_down_left, diagonal_down_right = get_diagonals(r, c, state.n)
                if (
                    diagonal_down_left not in state.diagonals_down_left_used
                    and diagonal_down_right not in state.diagonals_down_right_used
                ):
                    state.place_queen(r, c, diagonal_down_left, diagonal_down_right)
                    result = search_next(state, queens_left - 1)
                    if result is None:
                        state.remove_queen(
                            r, c, diagonal_down_left, diagonal_down_right
                        )
                    else:
                        state.board_state[r].append(c)
                        return state

        return None


def solve_n_queens(n):
    state = SearchState(n, [[] for _ in range(n)])
    search_next(state, n)
    return state


if __name__ == "__main__":
    main()
