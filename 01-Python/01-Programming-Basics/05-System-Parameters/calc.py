# pylint: disable=missing-module-docstring, missing-function-docstring, eval-used
import sys

def main():
    """Implement the calculator"""
    if sys.argv[2] == "+":
        result = int(sys.argv[1]) + int(sys.argv[3])
    elif sys.argv[2] == "-":
        result = int(sys.argv[1]) - int(sys.argv[3])
    elif sys.argv[2] == "*":
        result = int(sys.argv[1]) * int(sys.argv[3])
    return result



if __name__ == "__main__":
    print(main())
