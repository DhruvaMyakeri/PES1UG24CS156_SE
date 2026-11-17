"""
Lab 7 - Fuzz testing airline_baggage.py with Hypothesis
Name: Dhruva Myakeri    SRN: PES1UG24CS156

Two kinds of property are checked for each function:
  1. "no crash"  - for ANY input (random text, None, numbers, ...) the
                   function must not raise an exception.
  2. "correct"   - for well-formed input the result is right, and for any
                   input the result is either None (rejected) or valid.

Run:
    pytest test_airline_baggage.py
"""
import math
import string

from hypothesis import given, settings, strategies as st

from airline_baggage import parse_booking, total_weight, tag_label

# Any kind of junk a caller might pass in, not just strings.
ANY_INPUT = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.booleans(),
    st.lists(st.text(), max_size=3),
)

LETTERS = string.ascii_letters


# ================================================================ parse_booking

@settings(max_examples=500)
@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        parse_booking(s)
    except Exception as e:
        assert False, f"parse_booking crashed with: {e!r}"


@given(ANY_INPUT)
def test_parse_booking_no_crash_any_type(x):
    try:
        parse_booking(x)
    except Exception as e:
        assert False, f"parse_booking crashed with: {e!r}"


# Inputs that look almost like booking codes: three '-'-separated pieces
# made of letters, digits, spaces and other characters.
NEAR_CODE = st.lists(
    st.text(alphabet=LETTERS + string.digits + " -_+.ßİ٣", max_size=5),
    min_size=1, max_size=4,
).map("-".join)


@settings(max_examples=500)
@given(NEAR_CODE)
def test_parse_booking_result_is_valid_or_none(code):
    try:
        result = parse_booking(code)
    except Exception as e:
        assert False, f"parse_booking crashed with: {e!r}"
    if result is not None:
        airline, flight, seat = result
        assert airline.isascii() and airline.isalnum() and airline == airline.upper()
        assert isinstance(flight, int) and flight >= 0
        assert len(seat) == 1 and seat in string.ascii_uppercase


@given(
    airline=st.text(alphabet=LETTERS, min_size=2, max_size=2),
    flight=st.integers(min_value=1, max_value=9999),
    row=st.integers(min_value=1, max_value=99),
    letter=st.sampled_from("abcdefABCDEF"),
)
def test_parse_booking_valid_codes(airline, flight, row, letter):
    code = f"{airline}-{flight}-{row}{letter}"
    assert parse_booking(code) == (airline.upper(), flight, letter.upper())


# ================================================================ total_weight

@settings(max_examples=500)
@given(st.text() | st.none())
def test_total_weight_no_crash(s):
    try:
        total_weight(s)
    except Exception as e:
        assert False, f"total_weight crashed with: {e!r}"


@given(ANY_INPUT)
def test_total_weight_no_crash_any_type(x):
    try:
        total_weight(x)
    except Exception as e:
        assert False, f"total_weight crashed with: {e!r}"


# CSV built from arbitrary floats (including nan, inf, negatives, huge
# values) mixed with blanks and junk words.
WEIGHT_CSV = st.lists(
    st.one_of(
        st.floats().map(str),
        st.sampled_from(["", " ", "kg", "1e400", "-0", "1_000"]),
    ),
    min_size=1, max_size=6,
).map(",".join)


@settings(max_examples=500)
@given(WEIGHT_CSV)
def test_total_weight_result_is_valid_or_none(csv):
    try:
        result = total_weight(csv)
    except Exception as e:
        assert False, f"total_weight crashed with: {e!r}"
    if result is not None:
        assert math.isfinite(result), f"total_weight({csv!r}) = {result}"
        assert result > 0, f"total_weight({csv!r}) = {result}"


@given(st.lists(st.floats(min_value=0.1, max_value=100), min_size=1, max_size=10))
def test_total_weight_valid_csv(weights):
    csv = ",".join(repr(w) for w in weights)
    assert math.isclose(total_weight(csv), sum(weights))


# ================================================================ tag_label

@settings(max_examples=500)
@given(st.text() | st.none())
def test_tag_label_no_crash(s):
    try:
        tag_label(s)
    except Exception as e:
        assert False, f"tag_label crashed with: {e!r}"


@given(ANY_INPUT)
def test_tag_label_no_crash_any_type(x):
    try:
        tag_label(x)
    except Exception as e:
        assert False, f"tag_label crashed with: {e!r}"


WORD = st.text(alphabet=LETTERS, min_size=1, max_size=10)


@given(st.lists(WORD, min_size=2, max_size=4), st.sampled_from([" ", "  ", "\t"]))
def test_tag_label_uses_first_initial_and_last_name(words, sep):
    # "first [middle ...] last" -> "F. LAST"
    label = tag_label(sep.join(words))
    assert label == words[0][0].upper() + ". " + words[-1].upper()
