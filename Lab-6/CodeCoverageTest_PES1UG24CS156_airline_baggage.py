"""
Lab 6 - Code (line) coverage tests for airline_baggage.py
Name: Dhruva Myakeri    SRN: PES1UG24CS156

Goal: make every line (statement) of airline_baggage.py execute at least once.

Run:
    coverage run -m pytest CodeCoverageTest_PES1UG24CS156_airline_baggage.py
    coverage report -m
"""
import pytest
from airline_baggage import baggage_fee, carry_on_ok, check_in_status


# ---------------------------------------------------------------- baggage_fee

def test_within_allowance():
    # economy allowance is 15 kg, 10 kg -> no excess -> "return 0"
    assert baggage_fee("economy", 10, "domestic", False) == 0


def test_unknown_cabin_raises():
    # executes: raise ValueError("unknown cabin")
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee("first", 10, "domestic", False)


def test_negative_weight_raises():
    # executes: raise ValueError("invalid weight")
    with pytest.raises(ValueError, match="invalid weight"):
        baggage_fee("economy", -1, "domestic", False)


def test_member_domestic_small_excess():
    # executes: allowance += 10 and rate = 20
    # economy 15 + 10 (member) = 25 kg, 30 kg -> excess 5 * 20 = 100
    assert baggage_fee("economy", 30, "domestic", True) == 100


def test_international_large_excess():
    # executes: rate = 45, rate = rate * 2 and rate += 10
    # economy 15 kg, 50 kg -> excess 35 (> 20) -> rate 45*2+10 = 100 -> 3500
    assert baggage_fee("economy", 50, "international", False) == 3500


# ---------------------------------------------------------------- carry_on_ok

def test_carry_on_ok():
    # 5 kg, 1 item, not infant -> "return items <= 1"
    assert carry_on_ok(5, 1, False) is True


def test_carry_on_infant():
    # executes: return items <= 2 (infant branch)
    assert carry_on_ok(10, 2, True) is True


def test_carry_on_overweight():
    # executes: return False (weight > 7 kg)
    assert carry_on_ok(8, 1, False) is False


# ---------------------------------------------------------------- check_in_status

def test_check_in_open_international_with_bags():
    # executes: cutoff = 60, cutoff += 60 and return "open"
    # cutoff = 60 + 60 = 120, 120 >= 120 -> open
    assert check_in_status(120, True, True) == "open"


def test_check_in_late_domestic_no_bags():
    # executes: cutoff = 45 and return "late"
    # cutoff = 45, 30 >= 45 - 15 -> late
    assert check_in_status(30, False, False) == "late"


def test_check_in_closed():
    # executes: return "closed"
    # cutoff = 60, 10 < 45 -> closed
    assert check_in_status(10, True, False) == "closed"
