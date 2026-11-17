"""Airline baggage helpers, hardened against invalid input (Lab 7).

Name: Dhruva Myakeri    SRN: PES1UG24CS156

Every function validates its input and returns None for anything it cannot
handle, instead of raising an exception. See airline_baggage_original.py for
the original (buggy) version.
"""
import math
import re

# Airline code: 2-3 ASCII letters/digits with at least one letter (AI, 6E, UK).
_AIRLINE_RE = re.compile(r"(?=[0-9]*[A-Za-z])[A-Za-z0-9]{2,3}")
# Flight number: 1-4 ASCII digits.
_FLIGHT_RE = re.compile(r"[0-9]{1,4}")
# Seat: row number 1-3 digits followed by one seat letter (12A).
_SEAT_RE = re.compile(r"[0-9]{1,3}[A-Za-z]")
# Weight: plain decimal number such as 7, 12.5 or .5 (no signs, exponents,
# underscores, nan or inf).
_WEIGHT_RE = re.compile(r"[0-9]+(\.[0-9]+)?|\.[0-9]+")
# Name word: letters (any alphabet), allowing inner ' and - (O'Brien, Jean-Luc).
_NAME_WORD_RE = re.compile(r"[^\W\d_]+(?:['-][^\W\d_]+)*")

MAX_BAG_KG = 100.0


def parse_booking(code):
    """Return (airline, flight_number, seat_letter) or None if code is invalid.

    Expected format: AIRLINE-FLIGHT-SEAT, e.g. "AI-203-12A".
    """
    if not isinstance(code, str):
        return None
    parts = [p.strip() for p in code.strip().split("-")]
    if len(parts) != 3:
        return None
    airline, flight, seat = parts
    if not (_AIRLINE_RE.fullmatch(airline)
            and _FLIGHT_RE.fullmatch(flight)
            and _SEAT_RE.fullmatch(seat)):
        return None
    return airline.upper(), int(flight), seat[-1].upper()


def total_weight(weights_csv):
    """Return the total of comma-separated bag weights in kg, or None if invalid.

    Each weight must be a plain positive number no larger than MAX_BAG_KG.
    """
    if not isinstance(weights_csv, str):
        return None
    total = 0.0
    for item in weights_csv.split(","):
        item = item.strip()
        if not _WEIGHT_RE.fullmatch(item):
            return None
        weight = float(item)
        if not 0 < weight <= MAX_BAG_KG:
            return None
        total += weight
    if not math.isfinite(total):
        return None
    return total


def tag_label(name):
    """Return a tag label "F. LASTNAME" for a full name, or None if invalid.

    Uses the first letter of the first name and the LAST word as the surname,
    so middle names are skipped ("Rahul Kumar Sharma" -> "R. SHARMA").
    """
    if not isinstance(name, str):
        return None
    parts = name.split()
    if len(parts) < 2 or not all(_NAME_WORD_RE.fullmatch(p) for p in parts):
        return None
    return parts[0][0].upper() + ". " + parts[-1].upper()


def _show(label, result, hint):
    if result is None:
        print(f"Invalid input. {hint}")
    else:
        print(label, result)


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter a booking code (e.g. AI-203-12A): ")
    _show("Airline, Flight and Seat Letter:", parse_booking(user_input),
          "Use AIRLINE-FLIGHT-SEAT, e.g. AI-203-12A.")

    print("\n==== Running total_weight ====")
    user_input = input("Enter bag weights in kg as CSV (e.g. 12.5,7,23): ")
    _show("Total Weight:", total_weight(user_input),
          f"Use positive numbers up to {MAX_BAG_KG:g} kg separated by commas.")

    print("\n==== Running tag_label ====")
    user_input = input("Enter a passenger name (first and last): ")
    _show("Tag Label:", tag_label(user_input),
          "Enter at least a first and a last name using letters only.")


if __name__ == "__main__":
    main()
