from copy import deepcopy
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


def p_hit(rooms, room):
    return rooms[room]["unknown"] / (rooms[room]["unknown"] + len(rooms[room]["known"]))


def get_next_to_walk_from(rooms, current_room):
    # Find the room which has the most unexplored paths
    # Default to the current room
    least_explored_room = current_room
    p_hit_least_explored = p_hit(rooms, current_room)

    for room in range(1, len(rooms) + 1):
        p_hit_next = p_hit(rooms, room)
        if p_hit_next > p_hit_least_explored:
            p_hit_least_explored = p_hit_next
            least_explored_room = room

    return least_explored_room


def walk_from(case, previous_room, rooms):
    [room, num_passages] = ask_ints(case, "W")

    if previous_room not in rooms[room]["known"]:
        rooms[room]["unknown"] = num_passages - 1
    rooms[room]["known"].add(previous_room)

    if room not in rooms[previous_room]["known"]:
        rooms[previous_room]["unknown"] -= 1
    rooms[previous_room]["known"].add(room)
    return [room, num_passages]


def get_first_unvisited(rooms):
    return next(
        (room for room in range(1, len(rooms) + 1) if rooms[room]["unknown"] is None),
        None,
    )


def teleport_to(case, next_room, rooms):
    [room, num_passages] = ask_ints(case, f"T {next_room}")
    rooms[room]["unknown"] = num_passages
    return [room, num_passages]


def get_min_passages(rooms_ref):
    rooms = deepcopy(rooms_ref)
    j = 1
    i = 2
    total = 0

    if rooms[1]["unknown"] is None:
        rooms[1]["unknown"] = 0 if len(rooms[1]["known"]) > 0 else 1
    while i < len(rooms) + 1:
        if rooms[i]["unknown"] is None:
            rooms[i]["unknown"] = 0 if len(rooms[i]["known"]) > 0 else 1

        if rooms[i]["unknown"] > rooms[j]["unknown"]:
            total += rooms[j]["unknown"]
            rooms[i]["unknown"] -= rooms[j]["unknown"]
            j = i
        elif rooms[i]["unknown"] < rooms[j]["unknown"]:
            total += rooms[i]["unknown"]
            rooms[j]["unknown"] -= rooms[i]["unknown"]
        else:
            total += rooms[i]["unknown"]
            rooms[i]["unknown"] = 0
            rooms[j]["unknown"] = 0
            j = i + 1
            if j in rooms and rooms[j]["unknown"] is None:
                rooms[j]["unknown"] = 0 if len(rooms[j]["known"]) > 0 else 1
            i = i + 1
        i += 1

    # add any leftovers in case we underestimated
    if i - 1 < len(rooms) + 1:
        total += rooms[i - 1]["unknown"]
    if j < len(rooms) + 1:
        total += rooms[j]["unknown"]

    return total


def get_max_passages(rooms_ref):
    rooms = deepcopy(rooms_ref)
    j = 1
    i = 2
    total = 0
    total_missing_values = len([r for r in rooms if rooms[r]["unknown"] is None])

    if rooms[1]["unknown"] is None:
        total_missing_values = (
            0 if total_missing_values <= 0 else total_missing_values - 1
        )
        rooms[1]["unknown"] = total_missing_values
    while i < len(rooms) + 1:
        if rooms[i]["unknown"] is None:
            total_missing_values = (
                0 if total_missing_values <= 0 else total_missing_values - 1
            )
            rooms[i]["unknown"] = total_missing_values

        if rooms[i]["unknown"] > rooms[j]["unknown"]:
            total += rooms[j]["unknown"]
            rooms[i]["unknown"] -= rooms[j]["unknown"]
            j = i
        elif rooms[i]["unknown"] < rooms[j]["unknown"]:
            total += rooms[i]["unknown"]
            rooms[j]["unknown"] -= rooms[i]["unknown"]
        else:
            total += rooms[i]["unknown"]
            rooms[i]["unknown"] = 0
            rooms[j]["unknown"] = 0
            j = i + 1
            if j in rooms and rooms[j]["unknown"] is None:
                total_missing_values = (
                    0 if total_missing_values <= 0 else total_missing_values - 1
                )
                rooms[j]["unknown"] = total_missing_values
            i = i + 1
        i += 1

    # remove any leftovers in case we overestimated
    if i - 1 < len(rooms) + 1:
        total -= rooms[i - 1]["unknown"]
    if j < len(rooms) + 1:
        total -= rooms[j]["unknown"]

    return total


def estimate_passages(rooms):
    known_passages = sum([len(rooms[room]["known"]) for room in rooms]) / 2
    max_passages = get_max_passages(rooms)
    min_passages = get_min_passages(rooms)
    print(f"E {int(max_passages)}")
    print(f"E {int(min_passages)}")

    return int(known_passages + ((max_passages + min_passages) / 2))


def solve_case(case: "InteractiveCase"):
    rooms = {r: {"known": set(), "unknown": None} for r in range(1, case.n + 1)}

    [room, num_passages] = read_ints()
    if rooms[room]["unknown"] is None:
        rooms[room]["unknown"] = num_passages
    while not case.is_empty():
        if num_passages == 1:
            [room, num_passages] = walk_from(case, room, rooms)
        else:
            next_room = get_first_unvisited(rooms)
            if next_room is not None:
                [room, num_passages] = teleport_to(case, next_room, rooms)
            else:
                next_room = get_next_to_walk_from(rooms, room)
                if room != next_room:
                    if case.remaining_tries > 1:
                        [room, num_passages] = teleport_to(case, next_room, rooms)
                    else:
                        walk_from(case, room, rooms)
                        break

                [room, num_passages] = walk_from(case, room, rooms)

    return f"E {estimate_passages(rooms)}"


if __name__ == "__main__":
    solve_problem()
