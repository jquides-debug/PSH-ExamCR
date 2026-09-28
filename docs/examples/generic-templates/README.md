# Input templates

These are the earlier generic examples. The application's **Templates** button uses the three supplied files in [src/assets/templates](../../../src/assets/templates), with usage instructions. The examples here remain available for reference; replace all example rows with your own data before importing.

- `examinee_list_template.xlsx`: Excel list with `Examinee ID`, `Name` and `Email Address` columns. Use the first worksheet and keep headings on row 1. IDs are stored as text to preserve leading zeroes.
- `examinee_list_template.csv`: the same example list in UTF-8 CSV format. Import ID cells as text if editing in a spreadsheet.
- `answer_key_template.csv`: `Q1` through `Q150` with one row of example answers. Replace every example answer. For shorter exams, delete unused trailing question columns and their answers. Keep exactly one answer row.

Examinee lists require an `Examinee ID` heading; capitalization, spaces, underscores and hyphens are ignored. You may add other detail columns. Each ID must be nonblank and unique. The IDs must match those marked on the answer sheets; numeric leading zeroes are ignored for matching.

The printable sheet offered by the **Templates** window is `examination-sheet.png` in `src/assets/templates`. Scans must be individual supported image files, not PDFs or spreadsheets.
