from copy import copy
from dataclasses import dataclass
import string

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


def solve_problem():
    test_cases = read_int()

    for c in range(1, test_cases + 1):
        case = CaseParams(*read_ints())
        if c == 10:
            print(f"Case #{c}: {solve_case(case)}")
        else:
            blocks = read_strings()


def find_next(bleft, bright, i):
    print(bleft, i)
    if len(bleft) == 1:
        return bleft[0]
    if i >= len(bleft):
        return None

    j = 0

    while j < len(bright) and (bleft[i] == bright[j] or bright[j][-1] != bleft[i][0]):
        j += 1

    while j < len(bright) and bright[j][-1] == bleft[i][0] and bleft[i] != bright[j]:
        next_pair = bright[j] + bleft[i]

        new_left = copy(bleft)
        new_left[i] = next_pair
        new_left.remove(bright[j])
        new_right = copy(bright)
        new_right[j] = next_pair
        new_right.remove(bleft[i])

        result = find_next(new_left, new_right, 0)
        if result is not None:
            return result
        j += 1

    # try next left
    return find_next(bleft, bright, i + 1)


def same_letters(text: str):
    for i in text:
        if i != text[0]:
            return False


def solve_case(case: CaseParams):
    blocks = read_strings()

    trapped_letters = set()
    trapped_letters = set()
    seen_letters_combined = set()
    blocks_to_sort = []
    others = {c: "" for c in string.ascii_uppercase}

    for b in blocks:
        all_same_letter = True
        c = 0
        while c < len(b):
            ch = b[c]
            if ch in trapped_letters:
                return "IMPOSSIBLE"
            if ch != b[0]:
                all_same_letter = False
            if ch != b[0] and ch != b[-1]:
                trapped_letters.add(ch)
                while b[c] == ch:
                    c += 1
            c += 1

        if all_same_letter:
            others[b[0]] += b
        else:
            for ch in b:
                seen_letters_combined.add(ch)
            blocks_to_sort.append(b)

    print(blocks_to_sort)
    print([(k, v) for k, v in others.items() if v != ""])

    blocks_left_sorted = sorted(blocks_to_sort)
    blocks_right_sorted = sorted(blocks_to_sort, key=lambda b: b[-1])

    for i in range(len(blocks_left_sorted) - 1):
        if blocks_left_sorted[i][0] == blocks_left_sorted[i + 1][0]:
            return "IMPOSSIBLE"

    for i in range(len(blocks_right_sorted) - 1):
        if blocks_right_sorted[i][-1] == blocks_right_sorted[i + 1][-1]:
            return "IMPOSSIBLE"

    remainder = ""
    for (ch, other) in others.items():
        if ch in seen_letters_combined and len(other) > 0:
            blocks_to_sort.append(other)
        else:
            remainder += other

    if len(blocks_to_sort) == 0:
        return remainder

    blocks_left_sorted = sorted(blocks_to_sort)
    blocks_right_sorted = sorted(blocks_to_sort, key=lambda b: b[-1])

    print(blocks_left_sorted, blocks_right_sorted)
    result = find_next(blocks_left_sorted, blocks_right_sorted, 0)

    if result is None or (result[0] == result[-1] and not same_letters(result)):
        return "IMPOSSIBLE"

    return result + remainder


if __name__ == "__main__":
    solve_problem()
