# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


# endregion


def solve_problem():
    [test_cases, n, q] = read_ints()

    for case in range(1, test_cases + 1):
        print(f"{solve_case(n, q)}")
        answer = input()
        if answer != "1" or q <= 0:
            return


def search_for_next(q, test_list, new_num, result_list, left_index, right_index):
    print(" ".join([str(item) for item in test_list]))
    q -= 1
    median = read_int()
    if median == new_num:
        print("new_num = median")
        result_list.insert(left_index, new_num)
    elif median == result_list[-1]:
        result_list.append(new_num)
    else:
        non_medians = [num for num in test_list if num != median]
        left_index = get_smaller_index(result_list, non_medians)
        test_list = [test_list[left_index - 1], test_list[left_index], new_num]
        return search_for_next(q, test_list, new_num, result_list)
    return q


def get_smaller_index(result_list, a, b):
    return min(result_list.index(a), result_list.index(b))


def solve_case(n, q):
    test_list = [1, 2, 3]
    q -= 1
    print(" ".join([str(item) for item in test_list]))
    median = read_int()
    non_medians = [num for num in test_list if num != median]
    result_list = [non_medians[0], median, non_medians[1]]

    for i in range(2, n - 1):
        test_list = [i, i + 1, i + 2]

        new_num = i + 2

        (q,) = search_for_next(
            q, test_list, new_num, result_list, 0, len(result_list) - 1
        )
        print("result", result_list)

    return result_list


if __name__ == "__main__":
    solve_problem()
