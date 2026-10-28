# Lab 5: Identified Issues — Blood Donation Management System

**Name:** Dhruva Myakeri  **SRN:** PES1UG24CS156  **File:** `blood_donation.py`

Baseline: Pylint **4.81/10**, Bandit **4 issues** (1 High, 1 Medium, 2 Low), Flake8 **4 issues**.
Final: Pylint **10.00/10**, Bandit **0 issues**, Flake8 **0 issues**. Line numbers refer to the original file.

## High and medium severity

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | Shell injection — Bandit **B605** (High) | Security | 65 | `os.system("send-sms " + " ".join(phoneList))` builds a shell command from caller data, so a value like `"123; rm -rf /"` runs extra commands. | Validate each number against `PHONE_PATTERN`, resolve the tool with `shutil.which`, and call `subprocess.run([tool, *phone_list], check=True)` with an argument list (no shell). |
| 2 | Insecure temp file — Bandit **B306** (Medium) | Security | 60 | `tempfile.mktemp()` only returns a name, so another process can create that file first (a race condition, CWE-377). | Use `tempfile.mkstemp()`, which creates the file atomically with private permissions, then close the descriptor and return the path. |
| 3 | Mutable default argument — Pylint **W0102** | Bug | 17 | `notes=[]` is created once and shared by every call, so age-rejection notes pile up between unrelated calls. | Default to `notes=None` and create a new list inside the function. |
| 4 | Broad exception — Pylint **W0718** | Bug | 45–46 | `except Exception` hides every error. It hid the real bug in issue 5 and would hide typos as well. | Catch only `KeyError`, the expected error for an unknown blood group. |
| 5 | Incomplete compatibility table (found by reviewing the code, not reported by any tool) | Bug | 8–14 | `COMPATIBLE` had no entries for `A-`, `B-` or `AB-`, so `unitsFor("A-")` returned 0 even when compatible stock existed. The broad `except` hid this. | Add `A-: [A-, O-]`, `B-: [B-, O-]` and `AB-: [AB-, A-, B-, O-]`. |

## Low severity, convention and style

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 6 | Hardcoded password — Bandit **B105** | Security | 5 | `OFFICER_PASSWORD = "bloodbank-demo"` puts a secret in source control. | Read it from the environment: `os.environ.get("OFFICER_PASSWORD", "")`. |
| 7 | Assert used for validation — Bandit **B101** | Security / Bug | 18 | `assert` is removed when Python runs with `-O`, so the blood-group check would silently disappear. | Replace it with `if blood_group not in stock: raise ValueError(...)`. |
| 8 | Naming convention — Pylint **C0103** (×19) | Convention | 17–63 | Functions and arguments use camelCase (`registerDonor`, `donorName`, …). | Rename to snake_case (`register_donor`, `donor_name`, …) and update all call sites. |
| 9 | Missing docstrings — Pylint **C0114 / C0116** (×9) | Convention | 1, 17–68 | The module and its functions have no docstrings. | Add a module docstring and a one-line docstring to each function. |
| 10 | Chained comparison — Pylint **R1714** | Refactor | 50 | `bloodGroup == "O-" or bloodGroup == "AB+"` | Use `blood_group in ("O-", "AB+")`. |
| 11 | Line too long — Flake8 **E501** | Style | 7 | The `stock` dict line is 82 characters (limit 79). | Split the dict across several lines. |
| 12 | Too many blank lines — Flake8 **E303** | Style | 56–58 | Three blank lines before `donorSheetPath`. | Reduce to the two blank lines PEP 8 expects. |
| 13 | Inline comment spacing — Flake8 **E261** | Style | 80 | Only one space before `# below 2 units`. | Use two spaces before the inline comment. |
| 14 | Missing operator whitespace — Flake8 **E225** | Style | 81 | `eligible=[...]` | Change to `eligible = [...]`. |
| 15 | Code runs on import (found by review) | Maintainability | 85 | `main()` was called at module level, so importing the module ran the demo. | Wrap it in `if __name__ == "__main__":`. |

## Notes on Bandit suppressions

After the fix for issue 1, Bandit raises two generic Low-severity reminders: **B404** (importing `subprocess`) and **B603** (subprocess call without a shell). I reviewed both. The call uses no shell, takes its arguments as a list, resolves the executable path, and validates every number first, so there is no injection path left. I marked both lines with targeted `# nosec B404` and `# nosec B603` comments. The final Bandit report shows these as 2 deliberately skipped findings, with 0 open issues.

## Commits

| Commit | Tool | Summary |
|--------|------|---------|
| `Add baseline Pylint, Bandit and Flake8 reports` | — | `reports/before/` |
| `Fix security issues reported by Bandit` | Bandit | Issues 1, 2, 6, 7 |
| `Fix code quality issues reported by Pylint` | Pylint | Issues 3, 4, 5, 8, 9, 10, 15 (4.81 → 10.00) |
| `Fix PEP 8 style issues reported by Flake8` | Flake8 | Issues 11–14 |

The demo output is the same before and after all fixes.
