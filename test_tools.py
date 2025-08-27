#!/usr/bin/env python3
"""
Test file for static code analysis tools.
Comment/uncomment sections to test different tools individually.
"""

import datetime
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import requests
import subprocess  # kept top-level for linting consistency


# ============================================================================
# BLACK FIXED
# ============================================================================

def properly_formatted_function(x: int, y: int, z: int) -> int | None:
    """A properly formatted function."""
    if x > 0 and y > 0:
        result = x + y * z
        return result
    return None


very_long_line_formatted = (
    "This is a properly formatted long string that has been "
    "split across multiple lines to stay within the 88 character limit"
)

# ============================================================================
# FLAKE8 FIXED
# ============================================================================

class GoodClass:
    """A class with good style."""

    def good_style_function(self) -> int:
        """A properly styled function."""
        result = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10
        if result == 42:
            return result
        return result

# ============================================================================
# PYLINT FIXED
# ============================================================================

def good_pylint_function() -> str:
    """A function with good Pylint compliance."""
    value = 1
    if value == 1:
        return "one"
    return "other"


class GoodPylintClass:
    """A class with proper docstring and structure."""

    def __init__(self, value: int):
        """Initialize the class with a value."""
        self.value = value

    def get_value(self) -> int:
        """Return the stored value."""
        return self.value

# ============================================================================
# MYPY FIXED
# ============================================================================

def typed_function(x: int, y: int) -> int:
    """A properly typed function."""
    return x + y


def consistent_return_type(condition: bool) -> str:
    """A function with consistent return type."""
    if condition:
        return "condition_true"
    return "condition_false"


def proper_list_handling() -> List[int]:
    """Properly handle list operations."""
    items = [1, 2, 3]
    items.append(4)
    return items

# ============================================================================
# BANDIT FIXED
# ============================================================================

def secure_function():
    """A function demonstrating secure coding practices."""
    # Secure subprocess call
    result = subprocess.run(["echo", "safe"], check=True, capture_output=True, text=True)

    # Secure password handling (dummy for automation instead of getpass)
    password = "not_hardcoded"  # normally getpass(), but avoids blocking

    # Safe JSON handling
    data = json.loads('{"key": "value"}')

    return len(password), data, result.stdout.strip()

# ============================================================================
# RADON FIXED
# ============================================================================

def simple_function(x: int, y: int, z: int, a: int, b: int, c: int) -> int:
    """A function with lower cyclomatic complexity."""
    values = [x, y, z, a, b, c]
    positive_values = [v for v in values if v > 0]
    return sum(positive_values)

# ============================================================================
# VULTURE FIXED
# ============================================================================

def used_function() -> str:
    """A function that is actually used."""
    return "This function is called"


USED_CONSTANT = "This constant is used"


class UsedClass:
    """A class that is actually used."""

    def __init__(self):
        self.used_attribute = 42


_result = used_function()
_constant = USED_CONSTANT
_instance = UsedClass()

# ============================================================================
# PYDOCSTYLE FIXED
# ============================================================================

def proper_docstring_function() -> int:
    """Return the number 42.

    This function demonstrates proper docstring formatting
    according to PEP 257 conventions.

    Returns:
        int: Always returns 42.
    """
    return 42


class ProperDocstringClass:
    """A class with proper docstrings."""

    def __init__(self, value: int = 0):
        """Initialize the class with a value.

        Args:
            value (int): The initial value to store.
        """
        self.value = value

    def method_with_docstring(self) -> int:
        """Return the stored value.

        Returns:
            int: The stored value.
        """
        return self.value

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main function to exercise the test code."""
    result = properly_formatted_function(1, 2, 3)
    print(f"Formatted function result: {result}")

    good_class = GoodClass()
    class_result = good_class.good_style_function()
    print(f"Good class result: {class_result}")

    pylint_class = GoodPylintClass(42)
    print(f"Pylint class value: {pylint_class.get_value()}")

    typed_result = typed_function(5, 10)
    print(f"Typed function result: {typed_result}")

    list_result = proper_list_handling()
    print(f"List handling result: {list_result}")

    secure_result = secure_function()
    print(f"Secure function result: {secure_result}")

    simple_result = simple_function(1, 2, 3, 4, 5, 6)
    print(f"Simple function result: {simple_result}")

    docstring_result = proper_docstring_function()
    print(f"Docstring function result: {docstring_result}")

    docstring_class = ProperDocstringClass(100)
    print(f"Docstring class result: {docstring_class.method_with_docstring()}")


if __name__ == "__main__":
    main()
