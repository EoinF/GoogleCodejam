import os
from re import search
from subprocess import Popen, PIPE, STDOUT
import sys

# edit this path
SOLUTION_PATH = "2022/round1C/p2.py"


CPP_COMPILER_PATH = "C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.28.29910/bin/Hostx64/x64/cl.exe"
CPP_ENV_VARS = "C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Auxiliary/Build/vcvars64.bat"

CPP_COMPILER_OPTIONS = [
    "/Fe:",
    "build/solution.exe",
    "/Fo:",
    "build/solution.obj",
    "/EHsc",
    "/W3",
]

ERROR_MAP = {3221225620: "division by zero"}


class Colour:
    Green = "\033[32m"
    Red = "\033[31m"
    Blue = "\033[34m"
    Purple = "\033[35m"
    ENDC = "\033[0m"
    Bold = "\033[1m"
    Underline = "\033[4m"


def print2(
    text: "str",
    colour: "Colour",
):
    print(colour + text + Colour.ENDC)


def extract_cases(test_string: "str"):
    search_results = search(r"Case #\d+:", test_string)

    start_index = 0
    previous_start = 0
    while search_results is not None:
        previous_start = start_index + search_results.start()
        start_index += search_results.end()
        search_results = search(r"Case #\d+:", test_string[start_index:])
        if search_results is not None:
            yield test_string[
                previous_start : start_index + search_results.start()
            ].rstrip()

    yield test_string[previous_start:].rstrip()


def start_python():
    return Popen(
        ["python", os.path.join("C:/Users/Eoin/codejam/", SOLUTION_PATH)],
        stdout=PIPE,
        stdin=PIPE,
        stderr=STDOUT,
    )


def start_cpp(show_warnings):
    solution_path = f"C:/Users/Eoin/codejam/{SOLUTION_PATH}"
    args = [CPP_ENV_VARS, "&&", CPP_COMPILER_PATH, solution_path]
    args.extend(CPP_COMPILER_OPTIONS)
    p = Popen(args, stdout=PIPE, stderr=open(os.devnull, "wb"))

    out, err = p.communicate()
    lines = out.decode().split("\r\n")
    error_lines = []

    is_past_init = False
    for line in lines:
        if is_past_init:
            error_lines.append(line)
        else:
            if "Environment initialized for: 'x64'" in line:
                is_past_init = True

    if p.returncode != 0:
        print2("\n".join(error_lines), Colour.Red)
        exit(1)
    if show_warnings:
        print2("\n".join(error_lines), Colour.Purple)

    return Popen(
        ["build/solution.exe"],
        stdout=PIPE,
        stdin=PIPE,
        stderr=PIPE,
    )


def main(debug=False, show_warnings=False):
    if SOLUTION_PATH.endswith(".cpp"):
        p = start_cpp(show_warnings)
    else:
        p = start_python()

    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        f_input = f.read()
    with open(os.path.join(os.path.dirname(__file__), "output.txt")) as f:
        f_output = f.read()

    p_output_bytes = p.communicate(f_input.encode())[0]
    p_output = p_output_bytes.decode().replace("\r", "")

    if p.returncode != 0:
        error_message = (
            ERROR_MAP[p.returncode] if p.returncode in ERROR_MAP else str(p.returncode)
        )
        print2(f"Error: {error_message}", Colour.Red)
        print2(p_output, Colour.Blue)
        exit(1)

    if debug:
        print2(p_output, Colour.Blue)
        exit(0)

    actual_cases = extract_cases(p_output)
    expected_cases = extract_cases(f_output)

    case = 1
    for expected in expected_cases:
        actual = next(actual_cases)
        if expected == actual:
            print(f"Case #{case}: ✔️")
        else:
            print("--------------")
            print(f"Case #{case}: ❌")
            print("--------------")
            print("expected: ")
            print2(expected.rstrip(), Colour.Green)
            print("actual: ")
            print2(actual, Colour.Red)
            print()
        case += 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        main(
            debug="debug" in args or "-d" in args,
            show_warnings="warn" in args or "-w" in args,
        )
    else:
        main()
