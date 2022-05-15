from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


def read_strings():
    return input().split(" ")


# endregion

counter = 0


@dataclass
class Horse:
    type: str


class HorseNode:
    current: Horse
    next: Optional[HorseNode] = None
    prev: Optional[HorseNode] = None

    def __init__(self, current, next=None, prev=None):
        self.current = current
        self.next = next
        self.prev = prev


def create_combined_node(type, other_type):
    prev = HorseNode(Horse(other_type))
    next = HorseNode(Horse(other_type))
    middle = HorseNode(Horse(type), next, prev)
    prev.next = middle
    next.prev = middle
    return prev, next


def get_horse_nodes():
    [n, r, o, y, g, b, v] = read_ints()

    if o > b or g > r or v > y:
        return None

    reds = []
    blues = []
    yellows = []

    for _ in range(o):
        blues.extend(create_combined_node("O", "B"))
    for _ in range(g):
        reds.extend(create_combined_node("G", "R"))
    for _ in range(v):
        yellows.extend(create_combined_node("V", "Y"))

    reds.extend([HorseNode(Horse("R")) for _ in range(r - g)])
    blues.extend([HorseNode(Horse("B")) for _ in range(b - o)])
    yellows.extend([HorseNode(Horse("Y")) for _ in range(y - v)])

    return [reds, blues, yellows]


def solve_problem():
    test_cases = int(input())

    for c in range(1, test_cases + 1):
        horses = get_horse_nodes()
        if horses is None:
            print(f"Case #{c}: IMPOSSIBLE")
        else:
            print(f"Case #{c}: {solve_case(*horses)}")


def pair_next(state):
    groups_to_pair = []
    if len(state["B"]) > len(state["Y"]):
        groups_to_pair.append([state["R"], [*state["B"], *state["Y"]]])
    else:
        groups_to_pair.append([state["R"], [*state["Y"], *state["B"]]])
    groups_to_pair.append([state["B"], state["Y"]])
    for group in groups_to_pair:
        [mains, others] = group
        if len(mains) > 0:
            next_red = mains[0]
            if next_red.prev is None:
                for b in others:
                    if b.next is not None or (
                        b.prev is not None and b.prev is next_red
                    ):
                        continue
                    next_red.prev = b
                    b.next = next_red

                    red_has_next = next_red.next is not None
                    if red_has_next:
                        state[next_red.current.type].remove(next_red)
                    other_has_prev = b.prev is not None
                    if other_has_prev:
                        state[b.current.type].remove(b)
                    result = pair_next(state)
                    if result:
                        return True
                    else:
                        b.next = None
                        next_red.prev = None
                        if red_has_next:
                            state[next_red.current.type].insert(0, next_red)
                        if other_has_prev:
                            state[b.current.type].insert(0, b)
            else:  # next is None
                for b in others:
                    if b.prev is not None or (
                        b.next is not None and b.next is next_red
                    ):
                        continue
                    next_red.next = b
                    b.prev = next_red
                    state[next_red.current.type].remove(next_red)
                    other_has_next = b.next is not None
                    if other_has_next:
                        state[b.current.type].remove(b)
                    result = pair_next(state)
                    if result:
                        return True
                    else:
                        b.prev = None
                        next_red.next = None
                        state[next_red.current.type].insert(0, next_red)
                        if other_has_next:
                            state[b.current.type].insert(0, b)

    return len(state["R"]) == 0 and len(state["B"]) == 0 and len(state["Y"]) == 0


def solve_case(
    reds: "list[HorseNode]", blues: "list[HorseNode]", yellows: "list[HorseNode]"
):
    if len(reds) > 0:
        start = reds[0]
    elif len(blues) > 0:
        start = blues[0]
    elif len(yellows) > 0:
        start = yellows[0]
    else:
        return "IMPOSSIBLE"

    # pair all reds with yellow/blue
    result = pair_next({"R": reds, "B": blues, "Y": yellows})

    if not result:
        return "IMPOSSIBLE"

    node = start.next
    output = start.current.type
    while node != start:
        output += node.current.type
        node = node.next

    return output


if __name__ == "__main__":
    solve_problem()
