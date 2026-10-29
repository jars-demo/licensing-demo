"""Command-line scaffolding, from kestrel-template: argument parsing, colours and exit codes."""

import sys

GREEN, RED, RESET = "\033[32m", "\033[31m", "\033[0m"


def ok(message: str) -> None:
    print(f"{GREEN}{message}{RESET}")


def fail(message: str, code: int = 1) -> None:
    print(f"{RED}{message}{RESET}", file=sys.stderr)
    sys.exit(code)
