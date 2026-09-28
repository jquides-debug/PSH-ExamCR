# Application input templates

The **Templates** window shows these three supplied files with usage instructions and lets users save their own copies. Keep the filenames unchanged when packaging the application.

- **[examinee-list.xlsx](examinee-list.xlsx)**: enter one examinee per row on the first worksheet. Keep `Examinee-ID`, `NAME` and `EMAIL ADDRESS:` on row 1. Use the IDs marked on the answer sheets, stored as text to preserve leading zeroes. Import the completed copy with **Add examinee list**.
- **[answer-key.csv](answer-key.csv)**: this file has headings only. Add exactly one answer row under `Q1` through `Q150`; the first `Answer Key` column can be blank. For a shorter exam, remove unused trailing question columns and their answers. Save as CSV and import with **Answer key CSV**.
- **[examination-sheet.png](examination-sheet.png)**: print the 150-question sheet for examinees. Scan completed sheets as individual images into a folder, then choose that folder with **Select Input Folder**.

Saving a template does not load it into the checker. Complete the saved copy before importing. The Windows build includes this directory as `assets/templates` alongside the runtime branding assets.
