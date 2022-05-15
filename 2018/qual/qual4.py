from dataclasses import dataclass, field
from decimal import Decimal
from math import pi, cos, sin
import heapq
from typing import Any

# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


def read_strings():
    return input().split(" ")


# endregion


dec2 = Decimal(2)


@dataclass(order=True)
class PrioritizedItem:
    priority: Decimal
    item: Any = field(compare=False)


@dataclass
class Rotation:
    min: Decimal = Decimal(0)
    max: Decimal = Decimal(pi) / Decimal(4)
    current: Decimal = Decimal(0)

    def raise_rotation(self):
        self.min = current
        current = self.max + self.min / dec2

    def lower_rotation(self):
        self.max = current
        current = self.max + self.min / dec2


def solve_problem():
    test_cases = int(input())

    for c in range(1, test_cases + 1):
        area = Decimal(input())
        print(f"Case #{c}: {solve_case(area)}")


# points of the bottom square
p1 = (Decimal(-0.5), Decimal(-0.5), Decimal(-0.5))
q1 = (Decimal(-0.5), Decimal(-0.5), Decimal(+0.5))
r1 = (Decimal(+0.5), Decimal(-0.5), Decimal(-0.5))
s1 = (Decimal(+0.5), Decimal(-0.5), Decimal(+0.5))
# points of the top square
p2 = (Decimal(-0.5), Decimal(0.5), Decimal(-0.5))
q2 = (Decimal(-0.5), Decimal(0.5), Decimal(+0.5))
r2 = (Decimal(+0.5), Decimal(0.5), Decimal(-0.5))
s2 = (Decimal(+0.5), Decimal(0.5), Decimal(+0.5))


def rotate_xy(v, angle):
    cosA = Decimal(cos(angle))
    sinA = Decimal(sin(angle))
    x = v[0] * cosA - v[1] * sinA
    y = v[0] * sinA + v[1] * cosA
    return (x, y, v[2])


def rotate_yz(v, angle):
    cosA = Decimal(cos(angle))
    sinA = Decimal(sin(angle))
    y = v[1] * cosA - v[2] * sinA
    z = v[1] * sinA + v[2] * cosA
    return (v[0], y, z)


def rotate_xz(v, angle):
    cosA = Decimal(cos(angle))
    sinA = Decimal(sin(angle))
    x = v[0] * cosA + v[2] * sinA
    z = -v[0] * sinA + v[2] * cosA
    return (x, v[1], z)


def max_abs_x(p1, p2):
    return p1 if abs(p1[0]) > abs(p2[0]) else p2


def calculate_area_triangle(p1, p2, p3):
    p2_normalized = (p2[0] - p1[0], p2[2] - p1[2])
    p3_normalized = (p3[0] - p1[0], p3[2] - p1[2])

    return (
        abs(p2_normalized[0] * p3_normalized[1] - p2_normalized[1] * p3_normalized[0])
        / dec2
    )


def calculate_area(rxy, ryz, rxz):
    vertice_groups = [p1, p2, q1, q2, r1, r2, s1, s2]
    rotated_along_xy = [rotate_xy(v, rxy.current) for v in vertice_groups]
    rotated_along_yz = [rotate_yz(v, ryz.current) for v in rotated_along_xy]
    rotated_along_xz = [rotate_xz(v, rxz.current) for v in rotated_along_yz]

    points_to_use = [
        max_abs_x(rotated_along_xz[i], rotated_along_yz[i + 1]) for i in range(0, 8, 2)
    ]

    return calculate_area_triangle(
        points_to_use[0], points_to_use[1], points_to_use[2]
    ) + calculate_area_triangle(points_to_use[1], points_to_use[2], points_to_use[3])


def search_by_rotating(frontier: "list", target_area: Decimal):
    current = heapq.heappop(frontier)
    distance_to_target = current.priority
    [rxy, ryz, rxz] = current.item
    while abs(distance_to_target) > Decimal(0.000001):
        # try rotate xy
        new_rxy = Rotation(rxy.min, rxy.max, (rxy.max + rxy.min) / dec2)
        new_area = calculate_area(new_rxy, ryz, rxz)

        new_rxy2 = Rotation(new_rxy.current, new_rxy.max, new_rxy.current)
        new_rxy.max = new_rxy.current
        new_item1 = PrioritizedItem(abs(target_area - new_area), [new_rxy, ryz, rxz])
        new_item2 = PrioritizedItem(abs(target_area - new_area), [new_rxy2, ryz, rxz])

        heapq.heappush(frontier, new_item1)
        heapq.heappush(frontier, new_item2)

        # try rotate yz
        # new_ryz = Rotation(ryz.min, ryz.max, (ryz.max + ryz.min) / dec2)
        # new_area = calculate_area(rxy, new_ryz, rxz)

        # new_ryz2 = Rotation(new_ryz.current, ryz.max, new_ryz.current)
        # new_ryz.max = new_ryz.current
        # new_item1 = PrioritizedItem(abs(target_area - new_area), [rxy, new_ryz, rxz])
        # new_item2 = PrioritizedItem(abs(target_area - new_area), [rxy, new_ryz2, rxz])

        # heapq.heappush(frontier, new_item1)
        # heapq.heappush(frontier, new_item2)

        # # try rotate xz
        # new_rxz = Rotation(rxz.min, rxz.max, (rxz.max + rxz.min) / dec2)
        # new_area = calculate_area(rxy, ryz, new_rxz)

        # new_rxz2 = Rotation(new_rxz.current, rxz.max, new_rxz.current)
        # new_rxz.max = new_rxz.current
        # new_item1 = PrioritizedItem(abs(target_area - new_area), [rxy, ryz, new_rxz])
        # new_item2 = PrioritizedItem(abs(target_area - new_area), [rxy, ryz, new_rxz2])

        # heapq.heappush(frontier, new_item1)
        # heapq.heappush(frontier, new_item2)

        current = heapq.heappop(frontier)
        distance_to_target = current.priority
        [rxy, ryz, rxz] = current.item
    return rxy, ryz, rxz


def solve_case(target_area: Decimal):
    area = Decimal(1)

    frontier = []
    item = PrioritizedItem(
        abs(target_area - area), [Rotation(), Rotation(), Rotation()]
    )
    heapq.heappush(frontier, item)
    rxy, ryz, rxz = search_by_rotating(frontier, target_area)

    face_locations = [
        (Decimal(0.5), Decimal(0), Decimal(0)),
        (Decimal(0), Decimal(0.5), Decimal(0)),
        (Decimal(0), Decimal(0), Decimal(0.5)),
    ]
    rotated_along_xy = [rotate_xy(v, rxy.current) for v in face_locations]
    rotated_along_yz = [rotate_yz(v, ryz.current) for v in rotated_along_xy]
    rotated_along_xz = [rotate_xz(v, rxz.current) for v in rotated_along_yz]

    points = [
        " ".join(["{0:f}".format(d) for d in point]) for point in rotated_along_xz
    ]
    return "\n" + "\n".join(points)


if __name__ == "__main__":
    solve_problem()
