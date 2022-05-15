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


def sum_paths(initiators, generated_paths, selected_paths):
    total = 0
    for i in initiators:
        current = i
        longest = generated_paths[current]["value"]
        next = generated_paths[current]["next"]

        while next != 0 and not (
            next in selected_paths and selected_paths[next] != current
        ):
            if generated_paths[next]["value"] > longest:
                longest = generated_paths[next]["value"]
            current = next
            next = generated_paths[current]["next"]

        total += longest
    return total


def find_longest(
    duplicate_paths,
    generated_paths,
    selected_paths,
    initiators,
):
    if len(duplicate_paths) == 0:
        return sum_paths(initiators, generated_paths, selected_paths)
    else:
        longest = 0
        for i in range(len(duplicate_paths)):
            for reference in generated_paths[duplicate_paths[i]]["references"]:
                copied_selected_paths = selected_paths.copy()
                copied_selected_paths[duplicate_paths[i]] = reference

                result = find_longest(
                    duplicate_paths[0:i] + duplicate_paths[i + 1 :],
                    generated_paths,
                    copied_selected_paths,
                    initiators,
                )
                if result > longest:
                    longest = result
        return longest


def solve_problem(nums: "list[int]", paths: "list[int]"):
    paths.insert(0, 0)
    nums.insert(0, 0)
    initiators = set()
    duplicate_paths = []
    traversed_paths = set()

    generated_paths = {
        (i): {"value": nums[i], "next": paths[i], "references": []}
        for i in range(len(nums))
    }
    for i in range(1, len(nums)):
        i = len(nums) - i

        if i not in traversed_paths:
            traversed_paths.add(i)
            initiators.add(i)

        if len(generated_paths[i]["references"]) > 1:
            duplicate_paths.append(i)

        traversed_paths.add(paths[i])
        generated_paths[paths[i]]["references"].append(i)

    # try every combination of duplicate paths
    duplicate_paths.sort()
    return str(find_longest(duplicate_paths, generated_paths, {}, initiators))


main()
