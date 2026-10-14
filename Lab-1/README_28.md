# SE Lab 1 — Requirements Engineering & UML Use-Case Modelling

**Problem Statement #28 — Inter-City Freight Load Matching Marketplace**
Domain: Smart Cities, Transport & Logistics
Course: Software Engineering, Dept. of CSE, PES University

A B2B freight brokerage exchange where commercial shippers post cargo loads and trucking
carriers bid on them, with milestone payments released automatically from escrow once
electronic proof-of-delivery is verified.

## Repository contents

| File | Deliverable |
|---|---|
| `Requirements_Table.docx` / `.pdf` | 5 functional + 2 non-functional requirements with ID, Type, Description, Priority, Acceptance Criteria and Rationale |
| `UseCase_Diagram.pdf` | UML use-case diagram (actors, system boundary, associations, «include» and «extend») |
| `UseCase_Diagram.svg` | Editable source of the diagram — open/import in draw.io if you want to redraw or tweak it |
| `UseCase_Flow.docx` / `.pdf` | One-page flow specification for UC-05 with preconditions, postconditions, main success scenario and two alternate flows |

## Actors

| Actor | Role |
|---|---|
| Shipper | Posts loads, reviews bids, awards the load, tracks the shipment, can dispute a delivery |
| Freight Carrier | Bids on loads, moves the cargo, submits electronic proof of delivery |
| Carrier Verification Service (external) | Validates permits, insurance and KYC before a bid is accepted |
| Escrow Payment Gateway (external) | Holds the shipper's funds and disburses the milestone payment |

## Use cases

| ID | Use case | Notes |
|---|---|---|
| UC-01 | Post Freight Load | Shipper |
| UC-02 | Submit Bid on Load | «include» UC-06 |
| UC-03 | Award Load to Carrier | Locks bid, generates contract, funds escrow |
| UC-04 | Track Shipment Status | Shipper + Carrier |
| UC-05 | Submit Electronic Proof of Delivery | «include» UC-07 |
| UC-06 | Verify Carrier Credentials | Included use case |
| UC-07 | Release Escrow Milestone Payment | Included use case |
| UC-08 | Auto-Extend Auction Window | «extend» UC-02 (only if a bid lands in the final 2 minutes) |
| UC-09 | Raise Delivery Dispute | «extend» UC-05 (only if the shipper contests the delivery) |

**«include»** — always executed as part of the base use case (a bid always triggers credential
verification; a verified POD always triggers the escrow release).
**«extend»** — conditional behaviour (the auction window is extended only for a last-minute bid;
a dispute is raised only when the shipper contests the POD).

## Traceability

FR-001 → UC-02, UC-06 · FR-002 → UC-01 · FR-003 → UC-03 · FR-004 → UC-05 ·
FR-005 → UC-04 · NFR-001 → UC-07 · NFR-002 → platform-wide

## How to submit

```bash
git init
git add .
git commit -m "SE Lab 1: requirements table, use-case diagram and use-case flow (PS #28)"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-lab1-repo>.git
git push -u origin main
```
