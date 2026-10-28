# Lab 5: Reflection

**Name:** Dhruva Myakeri  **SRN:** PES1UG24CS156  **File:** `blood_donation.py`

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

**Easiest:** the Flake8 style issues (E501, E303, E261, E225) and Pylint's naming and docstring warnings. Each one points to an exact line and has one obvious fix, such as adding a space, removing a blank line or renaming to snake_case. None of them can change how the program behaves.

**Hardest:** the Bandit **B605** shell-injection finding in `notifyDonors`. Swapping `os.system` for `subprocess` was not enough on its own. Bandit then raised B404 and B603, so I had to decide what "safe" really means here. I removed the shell, passed the arguments as a list, resolved the executable with `shutil.which`, and validated every phone number with a regex before suppressing the two leftover generic warnings. The broad `except Exception` (W0718) was also harder than it looked. Narrowing it to `KeyError` made me ask why it was there at all, and that led me to a real bug: the `COMPATIBLE` table had no entries for A-, B- and AB-, so those patients were always shown 0 available units.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Yes, partly. **Bandit B105** flagged `OFFICER_PASSWORD` only because the variable name contains "password". The value was a demo string and the variable was never used. Still, it is good practice not to commit secrets, so I moved it to an environment variable anyway.

A clearer false positive is **B603** (`subprocess` call without `shell=True`), which appeared after my fix. Bandit raises it for every subprocess call, even when the arguments are a list, no shell is used and the input is validated. I checked it and suppressed it with a targeted `# nosec B603`. **B404** (importing `subprocess`) is the same kind of blanket warning.

The opposite also happened: the tools *missed* the incomplete `COMPATIBLE` table, the mixed meaning of "universal" (O- is the universal donor, AB+ the universal recipient), and `main()` running on import. Static analysis does not replace reading the code.

## 3. How would you integrate static analysis tools into your actual software development workflow?

- **While coding:** turn on Pylint and Flake8 in the editor (for example VS Code's Python extension) so warnings show up as I type.
- **Before each commit:** add a `pre-commit` hook that runs `flake8`, `pylint` and `bandit -r .`, so style and security problems never reach the repository.
- **In CI:** run all three tools in GitHub Actions on every push and pull request. Fail the build on any Bandit Medium/High issue, any Flake8 error, or a Pylint score below a threshold (for example `pylint --fail-under=9.5`).
- **Configuration:** keep shared settings in `pyproject.toml` / `.flake8` so the whole team uses the same rules, and require a written justification for every `# nosec` or `# pylint: disable`.
- **Existing code:** start from a baseline report and fix the most severe issues first, as I did in this lab.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Measurable:** the Pylint score went from **4.81 → 10.00/10**, Bandit from **4 issues (1 High, 1 Medium) → 0**, and Flake8 from **4 → 0** errors. The demo output did not change.
- **Security:** user data can no longer be run as shell commands, temp files are created atomically and privately, no secret sits in the source, and input validation still works under `python -O`.
- **Correctness:** the shared mutable default is gone, and patients with A-, B- and AB- blood now get correct counts of compatible units instead of a silent 0.
- **Robustness:** errors that should not happen are no longer swallowed by a broad `except`, so bugs show up instead of hiding.
- **Readability and maintainability:** consistent snake_case names, docstrings on every function, PEP 8 formatting, and a `__main__` guard so the module can be imported and tested without running the demo.
