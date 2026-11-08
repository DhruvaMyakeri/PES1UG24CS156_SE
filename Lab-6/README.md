# Lab 6: Code and Branch Coverage Analysis

**Name:** Dhruva Myakeri  **SRN:** PES1UG24CS156
**Assigned repo:** [SETAPESU26/L6_L7_28_airline_baggage](https://github.com/SETAPESU26/L6_L7_28_airline_baggage) (`lab6/`)

Line and branch coverage of `airline_baggage.py` were measured with `coverage` and `pytest`. New test cases were then written to cover the untested lines and branches.

| Test file | Tests | Line coverage (`airline_baggage.py`) | Branch coverage (`airline_baggage.py`) |
|-----------|-------|--------------------------------------|----------------------------------------|
| `test_airline_baggage.py` (starter) | 2 | 38% (23 of 37 lines missed) | 32% (6 of 26 branches partial) |
| `CodeCoverageTest_PES1UG24CS156_airline_baggage.py` | 11 | **100%** | 98% (branch `21->23` missed) |
| `BranchCoverageTest_PES1UG24CS156_airline_baggage.py` | 61 | **100%** | **100%** (26 of 26 branches) |

## Contents

| File | Description |
|------|-------------|
| `airline_baggage.py` | Module under test (unchanged from the assigned repo) |
| `test_airline_baggage.py` | Starter test file from the assigned repo |
| `CodeCoverageTest_PES1UG24CS156_airline_baggage.py` | Test cases written for code (line) coverage |
| `BranchCoverageTest_PES1UG24CS156_airline_baggage.py` | Test cases written for branch coverage |
| `screenshots/code_coverage.png` | Terminal output: line coverage with the code-coverage tests (100%) |
| `screenshots/code_coverage_tests_branch_report.png` | Terminal output: the same tests measured with `--branch` (98%, one missed branch) |
| `screenshots/branch_coverage.png` | Terminal output: branch coverage with the branch-coverage tests (100%) |
| `reports/` | Plain-text output of every coverage run, including the starter test baseline |
| `Lab_6_Code_and_Branch_Coverage_Student_Handout.pdf` | Lab handout |

## How to run

```bash
pip install coverage pytest
cd Lab-6

# Code (line) coverage
coverage run -m pytest CodeCoverageTest_PES1UG24CS156_airline_baggage.py
coverage report -m

# Branch coverage
coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS156_airline_baggage.py
coverage report -m
```

## Module under test

| Function | What it does |
|----------|--------------|
| `baggage_fee(cabin, weight_kg, route, is_member)` | Fee for checked baggage over the free allowance (economy 15 kg, premium 25 kg, business 40 kg; members get +10 kg except in business). Excess is charged at 20/kg domestic or 45/kg otherwise. Above 20 kg of excess the rate doubles, plus 10/kg more on international routes. |
| `carry_on_ok(weight_kg, items, is_infant)` | Infants may carry up to 2 items whatever the weight. Others may carry 1 item of up to 7 kg. |
| `check_in_status(minutes_before, has_baggage, is_international)` | The cutoff is 60 min with bags or 45 without, plus 60 for international flights. The result is `open` at or before the cutoff, `late` within 15 minutes after it, and `closed` after that. |

The module has 13 decisions, giving 26 branch outcomes:

| # | Function | Decision |
|---|----------|----------|
| D1 | `baggage_fee` | `cabin not in FREE_ALLOWANCE` |
| D2 | `baggage_fee` | `weight_kg < 0` |
| D3 | `baggage_fee` | `is_member and cabin != "business"` |
| D4 | `baggage_fee` | `excess <= 0` |
| D5 | `baggage_fee` | `route == "domestic"` |
| D6 | `baggage_fee` | `excess > 20` |
| D7 | `baggage_fee` | `route == "international"` (nested in D6) |
| D8 | `carry_on_ok` | `is_infant` |
| D9 | `carry_on_ok` | `weight_kg > 7` |
| D10 | `check_in_status` | `has_baggage` |
| D11 | `check_in_status` | `is_international` |
| D12 | `check_in_status` | `minutes_before >= cutoff` |
| D13 | `check_in_status` | `minutes_before >= cutoff - 15` |

## Step 1: Initial coverage (starter tests)

The two starter tests only cover an economy bag under the allowance and a light single carry-on item.

```
Name                      Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------------------
airline_baggage.py           37     23     26      6    32%   6, 8, 11, 15-23, 28, 30, 35-45
```

Nothing in `check_in_status` ran, and neither error path ran. No excess fee was ever calculated. See `reports/01_initial_line_coverage.txt` and `reports/02_initial_branch_coverage.txt`.

## Step 2: Code (line) coverage

`CodeCoverageTest_PES1UG24CS156_airline_baggage.py` adds one test for each group of missed lines:

| Test | Lines it covers |
|------|-----------------|
| `test_unknown_cabin_raises` | `raise ValueError("unknown cabin")` |
| `test_negative_weight_raises` | `raise ValueError("invalid weight")` |
| `test_member_domestic_small_excess` | member bonus `allowance += 10`, `rate = 20`, `return excess * rate` |
| `test_international_large_excess` | `rate = 45`, `rate = rate * 2`, `rate += 10` |
| `test_carry_on_infant` | `return items <= 2` |
| `test_carry_on_overweight` | `return False` |
| `test_check_in_open_international_with_bags` | `cutoff = 60`, `cutoff += 60`, `return "open"` |
| `test_check_in_late_domestic_no_bags` | `cutoff = 45`, `return "late"` |
| `test_check_in_closed` | `return "closed"` |

**Result: 100% line coverage** (`screenshots/code_coverage.png`).

### Why 100% line coverage is not enough

The same 11 tests were run again with `--branch` (`screenshots/code_coverage_tests_branch_report.png`):

```
airline_baggage.py      37      0     26      1    98%   21->23
```

Every line ran, but branch `21->23` was never taken. That is D7 (`if route == "international":`) evaluating to **False**: excess over 20 kg on a non-international route. The only heavy-excess test was international, so the doubled-rate path without the +10 surcharge was never checked. A bug there (for example, the surcharge also being added for domestic flights) would not be caught by these tests.

## Step 3: Branch coverage

`BranchCoverageTest_PES1UG24CS156_airline_baggage.py` makes every decision evaluate to both True and False. It also tests the boundary values on each side of every comparison. Most tests use `pytest.mark.parametrize`.

- **D7 False (the missed branch):** `test_domestic_heavy_excess` (economy, 36 kg and 40 kg, domestic: rate 20 × 2) and `test_other_route_heavy_excess` (a `"regional"` route is charged 45 × 2 with no +10).
- **D1/D2:** unknown cabins (`"first"`, `""`, `"Economy"`, since the lookup is case-sensitive), negative weights, and both invalid at once (the cabin check runs first).
- **D3:** members and non-members in every cabin. Business members get no bonus allowance, which is the right-hand side of the `and` being False.
- **D4/D6 boundaries:** weight exactly at the allowance (fee 0), 1 kg over, exactly 20 kg excess (not doubled) and 21 kg excess (doubled).
- **D8/D9:** an infant with 2 items vs 3 items, an infant's weight ignored, exactly 7 kg vs 7.1 kg, and an adult with 2 items.
- **D10 to D13:** all four cutoffs (60, 45, 120, 105), each tested at `+30`, `0`, `-1`, `-15` and `-16` minutes from the cutoff, which gives 20 combinations.

**Result: 100% branch coverage. 26 of 26 branches were taken and 61 tests passed** (`screenshots/branch_coverage.png`).

## Observations

- Line coverage only asks whether a line ran. Here 11 tests reached 100% line coverage while still missing one decision outcome. Branch coverage exposed it.
- `coverage.py` measures branches, not conditions. D3 is a compound condition (`is_member and cabin != "business"`), and the business-member case is needed to show the bonus is not applied. Branch coverage alone would not require that case, so it was added deliberately.
- Any route string other than `"domestic"` is charged the higher base rate, but only `"international"` gets the +10 surcharge. The branch tests document this behaviour (`test_other_route_heavy_excess`).
