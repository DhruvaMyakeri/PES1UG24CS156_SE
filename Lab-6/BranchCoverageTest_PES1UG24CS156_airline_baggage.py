"""
Lab 6 - Branch coverage tests for airline_baggage.py
Name: Dhruva Myakeri    SRN: PES1UG24CS156

Goal: make every decision in airline_baggage.py evaluate to BOTH True and
False, and also check the boundary values on each side of every comparison.

Decisions in the module (13 decisions -> 26 branch outcomes):
  baggage_fee      D1  cabin not in FREE_ALLOWANCE
                   D2  weight_kg < 0
                   D3  is_member and cabin != "business"
                   D4  excess <= 0
                   D5  route == "domestic"
                   D6  excess > 20
                   D7  route == "international"   (nested inside D6)
  carry_on_ok      D8  is_infant
                   D9  weight_kg > 7
  check_in_status  D10 has_baggage
                   D11 is_international
                   D12 minutes_before >= cutoff
                   D13 minutes_before >= cutoff - 15

The code-coverage test file reached 100% line coverage but never took
D7 -> False (excess > 20 on a NON-international route). The cases marked
"D7 False" below cover that missing branch.

Run:
    coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS156_airline_baggage.py
    coverage report -m
"""
import pytest
from airline_baggage import FREE_ALLOWANCE, baggage_fee, carry_on_ok, check_in_status


# ================================================================ baggage_fee

# D1 True: cabin is not a known cabin
@pytest.mark.parametrize("cabin", ["first", "", "Economy"])
def test_unknown_cabin_raises(cabin):
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee(cabin, 10, "domestic", False)


# D2 True: negative weight
@pytest.mark.parametrize("weight", [-1, -0.5])
def test_negative_weight_raises(weight):
    with pytest.raises(ValueError, match="invalid weight"):
        baggage_fee("economy", weight, "domestic", False)


def test_cabin_checked_before_weight():
    # both inputs invalid -> D1 is evaluated first
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee("first", -5, "domestic", False)


# D2 False with the smallest valid weight, D4 True
def test_zero_weight_is_free():
    assert baggage_fee("economy", 0, "domestic", False) == 0


# D4 True: weight at or under the allowance for every cabin (non-member)
@pytest.mark.parametrize("cabin", ["economy", "premium", "business"])
def test_exactly_at_allowance_is_free(cabin):
    assert baggage_fee(cabin, FREE_ALLOWANCE[cabin], "domestic", False) == 0


# D3 True / False, D4 True / False
@pytest.mark.parametrize(
    "cabin, weight, is_member, expected",
    [
        ("economy", 16, False, 20),    # D3 False (not member): 1 kg excess
        ("economy", 25, True, 0),      # D3 True: 15 + 10 = 25, no excess
        ("economy", 26, True, 20),     # D3 True: 1 kg excess
        ("premium", 35, True, 0),      # D3 True: 25 + 10 = 35, no excess
        ("premium", 36, True, 20),     # D3 True: 1 kg excess
        ("premium", 26, False, 20),    # D3 False: 1 kg excess
        ("business", 40, True, 0),     # D3 False (business member, no bonus)
        ("business", 41, True, 20),    # D3 False: bonus NOT added for business
        ("business", 41, False, 20),   # D3 False (not member)
    ],
)
def test_member_allowance(cabin, weight, is_member, expected):
    assert baggage_fee(cabin, weight, "domestic", is_member) == expected


# D5 True / False with D6 False (excess up to 20 kg -> base rate)
@pytest.mark.parametrize(
    "route, weight, expected",
    [
        ("domestic", 20, 5 * 20),        # D5 True, small excess
        ("domestic", 35, 20 * 20),       # D6 False at the boundary (excess = 20)
        ("international", 20, 5 * 45),   # D5 False, small excess
        ("international", 35, 20 * 45),  # D6 False at the boundary (excess = 20)
    ],
)
def test_base_rate_up_to_20kg_excess(route, weight, expected):
    assert baggage_fee("economy", weight, route, False) == expected


# D6 True, D7 True: international and over 20 kg excess -> rate * 2 + 10
@pytest.mark.parametrize(
    "weight, expected",
    [
        (36, 21 * (45 * 2 + 10)),   # just over the boundary: 21 kg excess
        (50, 35 * (45 * 2 + 10)),
    ],
)
def test_international_heavy_excess(weight, expected):
    assert baggage_fee("economy", weight, "international", False) == expected


# D6 True, D7 False: domestic and over 20 kg excess -> rate * 2 only
# (this is the branch that line coverage alone never forced us to test)
@pytest.mark.parametrize(
    "weight, expected",
    [
        (36, 21 * (20 * 2)),   # just over the boundary: 21 kg excess
        (40, 25 * (20 * 2)),
    ],
)
def test_domestic_heavy_excess(weight, expected):
    assert baggage_fee("economy", weight, "domestic", False) == expected


def test_other_route_heavy_excess():
    # D5 False and D7 False: a route that is neither "domestic" nor
    # "international" is charged the international base rate (45),
    # doubled, but without the +10 international surcharge.
    assert baggage_fee("economy", 40, "regional", False) == 25 * (45 * 2)


def test_member_heavy_international():
    # all of D3, D6 and D7 True: premium member 35 kg allowance, 60 kg bag
    assert baggage_fee("premium", 60, "international", True) == 25 * 100


# ================================================================ carry_on_ok

# D8 True: an infant may carry up to 2 items, whatever the weight
@pytest.mark.parametrize(
    "weight, items, expected",
    [
        (5, 0, True),
        (10, 2, True),     # boundary: exactly 2 items
        (20, 1, True),     # weight is ignored for infants
        (5, 3, False),     # boundary: one item too many
    ],
)
def test_carry_on_infant(weight, items, expected):
    assert carry_on_ok(weight, items, True) is expected


# D8 False, D9 True: adult bag over 7 kg
@pytest.mark.parametrize("weight", [7.1, 8, 15])
def test_carry_on_overweight(weight):
    assert carry_on_ok(weight, 1, False) is False


# D8 False, D9 False: adult bag within 7 kg -> at most 1 item
@pytest.mark.parametrize(
    "weight, items, expected",
    [
        (5, 1, True),
        (7, 1, True),      # boundary: exactly 7 kg is allowed
        (0, 0, True),
        (5, 2, False),     # adults only get 1 item
    ],
)
def test_carry_on_adult_within_weight(weight, items, expected):
    assert carry_on_ok(weight, items, False) is expected


# ================================================================ check_in_status

# D10 / D11 give four cutoffs; for each, test D12 True, D13 True and D13 False
# at the exact boundaries:
#   bags, domestic       -> cutoff 60
#   no bags, domestic    -> cutoff 45
#   bags, international  -> cutoff 120
#   no bags, intl.       -> cutoff 105
@pytest.mark.parametrize(
    "has_baggage, is_international, cutoff",
    [
        (True, False, 60),
        (False, False, 45),
        (True, True, 120),
        (False, True, 105),
    ],
)
@pytest.mark.parametrize(
    "offset, expected",
    [
        (30, "open"),      # well before the cutoff
        (0, "open"),       # D12 True at the boundary
        (-1, "late"),      # D12 False, D13 True
        (-15, "late"),     # D13 True at the boundary
        (-16, "closed"),   # D13 False
    ],
)
def test_check_in_status(has_baggage, is_international, cutoff, offset, expected):
    minutes = cutoff + offset
    assert check_in_status(minutes, has_baggage, is_international) == expected


def test_check_in_after_departure_is_closed():
    assert check_in_status(0, False, False) == "closed"
