"""Module demonstrating compliance with multiple static analysis tools.

This module contains well-formatted, type-safe, and secure example code.
"""

from __future__ import annotations

from typing import List

import requests  # noqa: F401  (kept for demonstration of typing/mypy stubs)


# ============================================================================
# BLACK + FLAKE8 + PYLINT FIXED
# ============================================================================


class ExampleClass:
    """A simple class with proper style."""

    def __init__(self, value: int) -> None:
        """Initialize with a value."""
        self.value: int = value

    def get_value(self) -> int:
        """Return the stored value."""
        return self.value


def add_numbers(x: int, y: int, z: int = 1) -> int:
    """Add numbers in a safe and formatted way."""
    return x + y * z


def properly_typed_function(x: int, y: int) -> int:
    """Return the sum of two integers."""
    return x + y


def safe_list_operations() -> List[int]:
    """Return a list with appended values."""
    items: List[int] = [1, 2, 3]
    items.append(4)
    return items


# ============================================================================
# SECURITY (BANDIT FIXED)
# ============================================================================


def run_safe_subprocess() -> str:
    """Safely run a subprocess using full path and without untrusted input."""
    import shutil
    import subprocess

    echo_path = shutil.which("echo")
    if not echo_path:
        raise FileNotFoundError("echo command not found")

    result = subprocess.run(
        [echo_path, "safe"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def handle_password(password: str | None = None) -> str:
    """Handle password securely without hardcoding."""
    if password is None:
        raise ValueError("Password must be provided securely")
    return f"Received password of length {len(password)}"


# ============================================================================
# MAIN (for demonstration only, not for production)
# ============================================================================


if __name__ == "__main__":
    obj = ExampleClass(42)
    print("Value:", obj.get_value())
    print("Addition:", add_numbers(2, 3))
    print("Typed sum:", properly_typed_function(5, 6))
    print("List:", safe_list_operations())
    print("Subprocess:", run_safe_subprocess())
    print("Password:", handle_password("supersecret"))
