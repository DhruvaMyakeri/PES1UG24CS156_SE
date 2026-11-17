# Lab 7: Fuzzing for Input Validation Bugs

**Name:** Dhruva Myakeri  **SRN:** PES1UG24CS156
**Assigned repo:** [SETAPESU26/L6_L7_28_airline_baggage](https://github.com/SETAPESU26/L6_L7_28_airline_baggage) (`lab7/`)

The three functions in `airline_baggage.py` were fuzzed with Hypothesis. Each one crashed or returned wrong results, so the functions were then hardened against invalid input.

| Run | Command | Result |
|-----|---------|--------|
| Buggy program | `python airline_baggage.py` | Crashes on `AI203`, `12.5,,7` and `Dhruva`; returns `nan` for `nan,-40,inf`; `Rahul Kumar Sharma` gives `R. KUMAR` |
| Fuzz tests vs buggy code | `pytest test_airline_baggage.py` | **9 failed**, 2 passed |
| Fixed program | `python airline_baggage.py` | Same inputs: clear "Invalid input" messages, no crashes, `R. SHARMA` |
| Fuzz tests vs fixed code | `pytest test_airline_baggage.py` | **11 passed** (and 6 more runs with new random inputs) |

## Contents

| File | Description |
|------|-------------|
| `PES1UG24CS156_LAB7.pdf` | Lab report with all screenshots, bug table and fixes |
| `airline_baggage.py` | Fixed (hardened) application |
| `airline_baggage_original.py` | Original buggy application from the assigned repo |
| `test_airline_baggage.py` | Completed Hypothesis test file (11 tests) |
| `screenshots/buggy_run.png` | Step 2: buggy program output |
| `screenshots/fuzz_fail_top.png`, `fuzz_fail_summary.png` | Step 4: tests failing on the buggy code (start and end of the output) |
| `screenshots/fixed_run.png` | Step 5: fixed program output |
| `screenshots/fuzz_pass.png` | Step 6: tests passing on the fixed code |
| `reports/` | Full text output of each run (the failing run is 434 lines) |
| `Lab_7_FuzzTesting_handout.pdf` | Lab handout |

## How to run

```bash
pip install hypothesis pytest
cd Lab-7
python airline_baggage.py
pytest test_airline_baggage.py
```

## Tests

Each function has a no-crash test on `st.text() | st.none()` (the three starter tests, completed), a no-crash test on any type, and property tests:

- `parse_booking`: near-valid codes give either `None` or a well-formed `(AIRLINE, flight, LETTER)`; generated valid codes parse correctly.
- `total_weight`: CSVs built from `st.floats()` (nan, inf, negatives) and junk give either `None` or a finite positive total; valid weights sum correctly.
- `tag_label`: names of 2 to 4 words give `F. LASTWORD`.

## Bugs found by Hypothesis

| # | Function | Falsifying input | Failure | Fix |
|---|----------|------------------|---------|-----|
| 1 | `parse_booking` | `''`, `'--'` | `ValueError` (unpack / `int()`), `IndexError` | Exactly 3 parts, each checked with a regex |
| 2 | `parse_booking` | `None` | `AttributeError` | Return `None` for non-strings |
| 3 | `total_weight` | `''` | `ValueError: could not convert string to float` | Each item must be a plain decimal number |
| 4 | `total_weight` | `None` | `AttributeError` | Return `None` for non-strings |
| 5 | `total_weight` | `'0.0'` | No crash, but a 0 total (also `nan`, `inf`, negative) | Each weight must be 0 < w ≤ 100 kg; total must be finite |
| 6 | `tag_label` | `''` | `IndexError` | At least two words required |
| 7 | `tag_label` | `None` | `AttributeError` | Return `None` for non-strings |
| 8 | `tag_label` | `['A', 'A', 'AA']` | `'A. A'` instead of `'A. AA'`: uses the middle name | Use `parts[-1]` as the surname |

Invalid input now returns `None` instead of raising, and `main()` prints a helpful message for it. Flight numbers and weights accept only ASCII digits, because `int()` and `float()` would otherwise accept Unicode digits, `1_000`, `1e400`, `nan` and `inf`. Seat letters must be ASCII, since `'ß'.upper()` is `'SS'`.
