"""Безпечний процес-імітатор із маркером у командному рядку."""

import argparse
from time import sleep


def main() -> None:
    parser = argparse.ArgumentParser(description="Імітатор для аналізу процесів")
    parser.add_argument("--lab-keylogger-demo", action="store_true", required=True)
    parser.parse_args()
    sleep(10)


if __name__ == "__main__":
    main()
