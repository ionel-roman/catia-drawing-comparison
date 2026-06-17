# CATIA Drawing Comparison Tool

A Python automation tool for validating engineering drawing revisions in automotive product development. Automatically detects missing dimensions, tolerance inconsistencies, and specification deviations between two CATIA V5 drawing versions — replacing a manual, error-prone review process.

Built and used in a production automotive engineering environment at Aumovio (formerly Continental Automotive).


## Problem it solves

During product development, engineering drawings go through multiple revisions. Manually comparing two versions of a complex technical drawing to find changed or missing dimensions and tolerances is time-consuming and unreliable. A missed deviation can propagate through manufacturing and quality validation.

This tool automates that comparison, producing a structured Excel report that flags every discrepancy between a reference drawing and a compared revision.


## How it works

1. The tool connects to an active CATIA V5 session via the COM API (`win32com`)
2. It extracts all dimension parameters (values, types, tolerances) from both drawings, organised by sheet and view
3. It compares dimensions between the two documents using value-based matching with a configurable tolerance threshold
4. Each dimension is classified as:
- **OK** — matched with consistent tolerances
- **NOT FOUND in Compared Drawing** — present in reference, missing in revision
- **EXTRA in Compared Drawing** — new dimension not present in reference
5. Results are exported to a structured Excel report


## Output example

| Sheet | View | Dimension (Ref) | Value (Ref) | Upper Tol | Lower Tol | Status |
|---|---|---|---|---|---|---|
| Sheet.1 | Front View | Dimension.1 | 45.000 | +0.1 | -0.1 | OK |
| Sheet.1 | Front View | Dimension.3 | 12.500 | +0.05 | -0.05 | NOT FOUND in Compared Drawing |
| Sheet.2 | Section A | — | — | — | — | EXTRA in Compared Drawing |


## Requirements

- Windows (CATIA V5 COM API is Windows-only)
- CATIA V5 installed and running with the target drawings open
- Python 3.8+

Install dependencies:

```bash
pip install -r requirements.txt
