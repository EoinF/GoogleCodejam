from itertools import permutations

# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


# endregion


def main():
    test_cases = int(input())

    for case in range(1, test_cases + 1):
        input()  # N
        nums = [int(num) for num in input().split(" ")]
        paths = [int(num) for num in input().split(" ")]
        print(f"Case #{case}: {solve_problem(nums, paths)}")


def get_fun_from(nums: "list[int]", paths: "list[int]", initiators: "list[int]", cache):
    cache_node = cache
    current_idx = 0
    visited_list = [0]
    total_fun = 0
    for i in initiators:
        if i not in cache_node:
            break
        else:
            current_idx += 1
            cache_node = cache_node[i]
            total_fun += cache_node[-1]
            visited_list.extend(cache_node[-2])

    old_visited_list = set(visited_list)

    for i in initiators[current_idx:]:
        current = i
        line = []
        new_visited_list = set()

        while current not in new_visited_list and current not in old_visited_list:
            new_visited_list.add(current)
            old_visited_list.add(current)
            line.append(nums[current])
            current = paths[current]

        cache_node[i] = {-1: max(line), -2: new_visited_list}
        cache_node = cache_node[i]
        total_fun += cache_node[-1]

    return total_fun


def solve_problem(nums: "list[int]", paths: "list[int]"):
    paths.insert(0, 0)
    nums.insert(0, 0)

    initiators = []
    referenced_paths = set()

    for i in range(1, len(paths)):
        current = len(paths) - i

        if current not in referenced_paths:
            initiators.append(current)
        referenced_paths.add(paths[current])

    perms = permutations(initiators)

    cache = {-1: 0, -2: []}
    fun_results = [get_fun_from(nums, paths, p, cache) for p in perms]
    return str(max(fun_results))


main()
