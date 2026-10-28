# Software Engineering Lab Submissions

**Name:** Dhruva Myakeri  **SRN:** PES1UG24CS156
**Course:** Software Engineering, Dept. of CSE, PES University
**Problem Statement #28:** Inter-City Freight Load Matching Marketplace (Labs 1–3)

---

## Labs

| Lab | Topic | Folder | Main deliverables |
|-----|-------|--------|-------------------|
| 1 | Requirements Engineering & UML Use-Case Modelling | [`Lab-1/`](Lab-1/) | Requirements table, use-case diagram, use-case flow for UC-05 |
| 2 | Agile Backlog Creation & Sprint Simulation in Jira | [`Lab-2/`](Lab-2/) | Epics, prioritized backlog with story points, sprint summary, reflection |
| 3 | Component Modelling & Architectural Pattern Selection | [`Lab-3/`](Lab-3/) | UML component diagram, justification for a microservices architecture |
| 4 | Vibe Coding: Defender Repair | [`Lab-4/`](Lab-4/) | Fixed game, before/after gameplay videos, LLM chat history |
| 5 | Static Code Analysis | [`Lab-5/`](Lab-5/) | Fixed `blood_donation.py`, before/after reports, issue table, reflection, lab report PDF |

---

## Lab 1: Requirements Engineering & UML Use-Case Modelling

Requirements and use-case model for a B2B freight marketplace. Shippers post cargo loads, carriers bid on them, and milestone payments are released from escrow once electronic proof of delivery is verified.

- `Requirements_Table_28.pdf`: 5 functional and 2 non-functional requirements
- `UseCase_Diagram_28.pdf`: actors, system boundary, «include» and «extend» relationships
- `UseCase_Flow_28.pdf`: flow specification for UC-05 (Submit Electronic Proof of Delivery)
- `README_28.md`: actors, use cases and traceability

## Lab 2: Agile Backlog & Sprint Simulation in Jira

`PES1UG24CS156_LAB2.pdf` has the Jira space *Freight Load Marketplace (FLM)*. It contains six Epics derived from the Lab 1 use cases, a prioritized backlog with Fibonacci story points, a sprint summary, screenshots and reflection answers.

## Lab 3: Component Modelling & Architecture

- `UseCase_Component_Diagram_28_PES1UG24CS156.pdf`: UML component diagram with provided and required interfaces and external services
- `Architecture_Justification_28_PES1UG24CS156.pdf`: why a microservices architecture was chosen over Layered or Client-Server

## Lab 4: Vibe Coding — Defender Repair

A single-file Defender-lite game in Pygame, fixed and extended with an LLM as a pair programmer.

| Task | Change |
|------|--------|
| Radar bug | Blips are now plotted at their absolute world position, not relative to the player |
| `sky_color(wave)` | The sky brightens and shifts hue as waves progress |
| `on_humanoid_rescued(humanoid)` | Shows a "+500" popup when a falling humanoid is caught |
| `bonus_life_threshold()` | Awards a bonus life every 10,000 points |

- `game.py`: the fixed game (the same file is also at the repo root)
- `before.mp4` / `after.mp4`: 10-second gameplay recordings before and after the changes
- `lab4_chat.pdf` / `lab4_chat.txt`: full LLM chat history
- `Lab_4_VibeCoding_handout.pdf`: lab handout

To run it:

```bash
pip install pygame
python game.py
```

**Controls:** Left/Right to thrust, Up/Down to change altitude, Space to fire, `R` to reset.

## Lab 5: Static Code Analysis

Pylint, Bandit and Flake8 were run on `blood_donation.py` from the assigned repo [SETAPESU26/L5_28_blood_donation](https://github.com/SETAPESU26/L5_28_blood_donation). The issues they found were then fixed. The demo output is unchanged after the fixes.

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.81/10 | **10.00/10** |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | **0 issues** |
| Flake8 | 4 errors | **0 errors** |

Main fixes:

- shell injection (`os.system`) replaced with a validated `subprocess.run` call that uses no shell
- insecure `tempfile.mktemp` replaced with `mkstemp`
- hardcoded password removed
- `assert` used for validation replaced with `ValueError`
- mutable default argument removed
- broad `except` narrowed to `KeyError`
- a hidden bug fixed: the blood-group compatibility table had no entries for A-, B- and AB-
- names changed to snake_case, docstrings added, PEP 8 formatting applied

See [`Lab-5/README.md`](Lab-5/README.md) for the full list of files.

---

## Repository Structure

```
28_defender/
├── README.md
├── game.py                  # Lab 4 game (fixed)
├── Lab-1/                   # Requirements & use-case modelling
├── Lab-2/                   # Jira backlog & sprint simulation
├── Lab-3/                   # Component diagram & architecture
├── Lab-4/                   # Vibe coding: Defender repair
└── Lab-5/                   # Static code analysis
    ├── PES1UG24CS156_LAB5.pdf
    ├── blood_donation.py
    ├── blood_donation_original.py
    ├── issues.md
    ├── reflection.md
    └── reports/{before,after}/
```
