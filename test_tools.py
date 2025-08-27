#!/usr/bin/env python3
"""
Test file for static code analysis tools.
Comment/uncomment sections to test different tools individually.
"""

# ============================================================================
# BLACK FORMATTING ISSUES (Comment out the fixed version to see Black fail)
# ============================================================================

# BLACK ISSUE: Poor formatting, long lines, inconsistent spacing
# Uncomment below to trigger Black failures:
"""
def poorly_formatted_function(x,y,z):
    if x>0 and y>0:
        result=x+y*z
        return result
    else:return None

very_long_line_that_exceeds_88_characters = "This is a very long string that will definitely exceed the 88 character limit that Black enforces by default and should trigger a formatting error"
"""

# BLACK FIXED: Properly formatted version (comment out to see failures)
def properly_formatted_function(x, y, z):
    """A properly formatted function."""
    if x > 0 and y > 0:
        result = x + y * z
        return result
    else:
        return None


# Properly formatted long line
very_long_line_formatted = (
    "This is a properly formatted long string that has been "
    "split across multiple lines to stay within the 88 character limit"
)

# ============================================================================
# ISORT IMPORT ISSUES (Comment out fixed imports to see isort fail)
# ============================================================================

# ISORT ISSUE: Poorly organized imports
# Uncomment below to trigger isort failures:
"""
import sys
import os
from collections import defaultdict
import json
from typing import Dict, List
import re
import datetime
from pathlib import Path
import requests
"""

# ISORT FIXED: Properly organized imports (comment out to see failures)
import datetime
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import requests

# ============================================================================
# FLAKE8 STYLE ISSUES (Comment out fixed code to see Flake8 fail)
# ============================================================================

# FLAKE8 ISSUE: Style violations
# Uncomment below to trigger Flake8 failures:
"""
def bad_style_function():
    unused_variable = 42  # F841: unused variable
    x=1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+16+17+18  # E501: line too long
    if x==42:  # E225: missing whitespace around operator
        pass
    import json  # E402: module level import not at top
    return x

# E302: expected 2 blank lines
class BadClass:
    pass
"""

# FLAKE8 FIXED: Style compliant code (comment out to see failures)
class GoodClass:
    """A properly styled class."""
    
    def good_style_function(self):
        """A properly styled function."""
        result = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10
        if result == 42:
            return result
        return result

# ============================================================================
# PYLINT ISSUES (Comment out fixed code to see Pylint fail)
# ============================================================================

# PYLINT ISSUE: Various code quality issues
# Uncomment below to trigger Pylint failures:
"""
def bad_function():
    # C0103: Invalid name
    x = 1
    # W0612: Unused variable
    unused = 42
    # R0911: Too many return statements (add more returns to trigger)
    if x == 1:
        return 1
    elif x == 2:
        return 2
    elif x == 3:
        return 3
    elif x == 4:
        return 4
    elif x == 5:
        return 5
    elif x == 6:
        return 6
    elif x == 7:
        return 7
    else:
        return 0

# C0115: Missing class docstring
class BadPylintClass:
    def method(self, x):  # C0116: Missing function docstring
        return x
"""

# PYLINT FIXED: Code quality compliant code (comment out to see failures)
def good_pylint_function():
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
# MYPY TYPE ISSUES (Comment out fixed code to see MyPy fail)
# ============================================================================

# MYPY ISSUE: Type annotation problems
# Uncomment below to trigger MyPy failures:
"""
def no_type_annotations(x, y):
    return x + y

def inconsistent_return_type(condition):
    if condition:
        return "string"
    else:
        return 42

def list_type_error():
    items = [1, 2, 3]
    return items.append("string")  # Wrong: append returns None
"""

# MYPY FIXED: Properly typed code (comment out to see failures)
def typed_function(x: int, y: int) -> int:
    """A properly typed function."""
    return x + y


def consistent_return_type(condition: bool) -> str:
    """A function with consistent return type."""
    if condition:
        return "condition_true"
    else:
        return "condition_false"


def proper_list_handling() -> List[int]:
    """Properly handle list operations."""
    items = [1, 2, 3]
    items.append(4)  # Correct: append modifies list in-place
    return items

# ============================================================================
# BANDIT SECURITY ISSUES (Comment out fixed code to see Bandit fail)
# ============================================================================

# BANDIT ISSUE: Security vulnerabilities
# Uncomment below to trigger Bandit failures:
"""
import subprocess

def security_issues():
    # B602: subprocess call with shell=True
    subprocess.call("ls -la", shell=True)
    
    # B105: Hardcoded password
    password = "hardcoded_password123"
    
    # B301: Pickle usage (potential security risk)
    import pickle
    data = pickle.loads(b"some_data")
    
    # B608: SQL injection possibility
    sql_query = "SELECT * FROM users WHERE id = '%s'" % user_id
    
    return password, data, sql_query
"""

# BANDIT FIXED: Secure code practices (comment out to see failures)
def secure_function():
    """A function demonstrating secure coding practices."""
    import subprocess
    from getpass import getpass
    
    # Secure subprocess call
    subprocess.run(["ls", "-la"], check=True)
    
    # Secure password handling
    password = getpass("Enter password: ")
    
    # Use JSON instead of pickle for data serialization
    import json
    data = json.loads('{"key": "value"}')
    
    # Parameterized query (conceptual)
    # sql_query = "SELECT * FROM users WHERE id = %s"  # Use with parameters
    
    return len(password), data

# ============================================================================
# SAFETY DEPENDENCY ISSUES
# ============================================================================

# Note: Safety checks dependencies, not code directly
# To test Safety failures, you would need to add vulnerable dependencies
# to your requirements.txt file. For example:
# requests==2.6.0  # (old version with known vulnerabilities)
# django==1.8.0    # (old version with known vulnerabilities)

# ============================================================================
# RADON COMPLEXITY ISSUES (Comment out simple version to see high complexity)
# ============================================================================

# RADON ISSUE: High cyclomatic complexity
# Uncomment below to trigger Radon complexity warnings:
"""
def complex_function(x, y, z, a, b, c):
    if x > 0:
        if y > 0:
            if z > 0:
                if a > 0:
                    if b > 0:
                        if c > 0:
                            return x + y + z + a + b + c
                        else:
                            return x + y + z + a + b
                    else:
                        return x + y + z + a
                else:
                    return x + y + z
            else:
                return x + y
        else:
            return x
    else:
        return 0
"""

# RADON FIXED: Lower complexity version (comment out to see high complexity)
def simple_function(x: int, y: int, z: int, a: int, b: int, c: int) -> int:
    """A function with lower cyclomatic complexity."""
    values = [x, y, z, a, b, c]
    positive_values = [v for v in values if v > 0]
    return sum(positive_values)

# ============================================================================
# VULTURE DEAD CODE ISSUES (Comment out usage to see dead code detection)
# ============================================================================

# VULTURE ISSUE: Dead code (unused functions/variables)
# Uncomment below to trigger Vulture dead code detection:
"""
def unused_function():
    return "This function is never called"

UNUSED_CONSTANT = "This constant is never used"

class UnusedClass:
    def __init__(self):
        self.unused_attribute = 42
"""

# VULTURE FIXED: Used code (comment out usage to see dead code warnings)
def used_function() -> str:
    """A function that is actually used."""
    return "This function is called"

USED_CONSTANT = "This constant is used"

class UsedClass:
    """A class that is actually used."""
    def __init__(self):
        self.used_attribute = 42

# Usage to prevent Vulture from flagging as dead code
_result = used_function()
_constant = USED_CONSTANT
_instance = UsedClass()

# ============================================================================
# PYDOCSTYLE DOCSTRING ISSUES (Comment out proper docstrings to see failures)
# ============================================================================

# PYDOCSTYLE ISSUE: Missing or improperly formatted docstrings
# Uncomment below to trigger pydocstyle failures:
"""
def no_docstring_function():
    return 42

def bad_docstring_function():
    '''Bad docstring format (single quotes, no period)'''
    return 42

class NoDocstringClass:
    def method_without_docstring(self):
        pass
"""

# PYDOCSTYLE FIXED: Properly formatted docstrings (comment out to see failures)
def proper_docstring_function() -> int:
    """Return the number 42.
    
    This function demonstrates proper docstring formatting
    according to PEP 257 conventions.
    
    Returns:
        int: Always returns 42.
    """
    return 42


class ProperDocstringClass:
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
# MAIN FUNCTION TO TEST EVERYTHING
# ============================================================================

def main():
    """Main function to exercise the test code."""
    # Test the functions to ensure they work
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
