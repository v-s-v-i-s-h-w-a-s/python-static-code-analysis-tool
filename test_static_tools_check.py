#!/usr/bin/env python3
"""
Unit tests for static_tools_check.py
Ensures test coverage across all functions and classes.
"""

import io
import sys

import static_tools_check as analysis  # ✅ FIXED import


def capture_output(func, *args, **kwargs):
    """Helper to capture stdout from functions that print."""
    captured_output = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = captured_output
    try:
        func(*args, **kwargs)
    finally:
        sys.stdout = sys_stdout
    return captured_output.getvalue()


def test_properly_formatted_function():
    assert analysis.properly_formatted_function(1, 2, 3) == 7
    assert analysis.properly_formatted_function(-1, 2, 3) == 0


def test_good_class_methods():
    obj = analysis.GoodClass(55)
    assert obj.good_style_function() in (55, 27)
    assert obj.calculate_sum([1, 2, 3]) == 6


def test_good_pylint_function():
    assert analysis.good_pylint_function() in ("one", "other")


def test_good_pylint_class():
    obj = analysis.GoodPylintClass(42)
    assert obj.get_value() == 42
    obj.set_value(100)
    assert obj.get_value() == 100


def test_typed_function():
    assert analysis.typed_function(5, 10) == 15


def test_consistent_return_type():
    assert analysis.consistent_return_type(True) == "condition_true"
    assert analysis.consistent_return_type(False) == "condition_false"


def test_proper_list_handling():
    assert analysis.proper_list_handling() == [1, 2, 3, 4]


def test_secure_function():
    password_length, data = analysis.secure_function()
    assert password_length == 12
    assert data == {"key": "value"}


def test_simple_function():
    assert analysis.simple_function(-1, -2, 3, 4) == 7
    assert analysis.simple_function() == 0


def test_used_function_and_constant():
    assert analysis.used_function() == "This function is called"
    assert analysis.USED_CONSTANT == "This constant is used"


def test_used_class():
    obj = analysis.UsedClass()
    assert obj.get_attribute() == 42
    obj.set_attribute(99)
    assert obj.get_attribute() == 99


def test_proper_docstring_function():
    assert analysis.proper_docstring_function() == 42


def test_proper_docstring_class():
    obj = analysis.ProperDocstringClass(10)
    assert obj.method_with_docstring() == 10
    obj.update_value(20)
    assert obj.method_with_docstring() == 20


def test_main_runs_without_error():
    output = capture_output(analysis.main)
    assert "Formatted function result" in output
    assert "Good class result" in output
    assert "Used class attribute" in output
