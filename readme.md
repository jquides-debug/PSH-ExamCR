# PSH-ExamCR

### Examination Checker for the Philippine Society of Hypertension

PSH-ExamCR adapts OpenMCR for the Philippine Society of Hypertension's multiple-choice examination workflow. It reads scanned answer sheets, captures Examinee IDs and responses, and exports results for review, with optional scoring against an answer key.

> **Built on OpenMCR — full credit to Ian Sanders and the original contributors.**
> This repository is a fork of [OpenMCR by Ian Sanders](https://github.com/iansan5653/open-mcr). The original project provides the foundation for the answer-sheet recognition and processing used here. PSH's work builds on that foundation through organization-specific branding and examination workflows.

## Original project and acknowledgments

**Ian Sanders** developed OpenMCR and its corresponding multiple-choice sheet as an independent study project at the **University of South Florida**, under the direction of **Dr. Autar Kaw**. We gratefully acknowledge their work and the contributions of the OpenMCR community in making accessible, open-source examination processing possible.

- **Original project and reference:** [iansan5653/open-mcr](https://github.com/iansan5653/open-mcr)
- **Original author:** [Ian Sanders](https://github.com/iansan5653)
- **Original technical report:** [OpenMCR independent study report](https://github.com/iansan5653/open-mcr-report/releases/tag/1.0.0)
- **PSH fork:** [jquides-debug/PSH-ExamCR](https://github.com/jquides-debug/PSH-ExamCR)

The PSH name identifies this adaptation. Credit for the original OpenMCR software, recognition approach, and answer-sheet design remains with their original authors.

## What the PSH application does

- Processes the supported 150-question answer-sheet layout.
- Reads Examinee ID bubbles and answers from scanned images, retaining each source filename.
- Optionally scores a batch using a CSV answer key.
- Provides a results window for reviewing examinees, responses, and available scores.
- Exports an Excel review workbook with multiple responses highlighted in red, alongside CSV results.
- Lists rejected scans for follow-up and supports optional Multiple Choice Test Analysis (MCTA) exports.
- Supports successive batches without restarting the application.

Written names are not transcribed. Recognition depends on the configured bubble positions and corner markers, so a redesigned form must preserve the supported layout.

## Installation for PSH staff

This application is intended for internal use by the Philippine Society of Hypertension on 64-bit Windows computers.

1. Obtain `PSH-ExamCR-Setup.exe` from your PSH application administrator.
2. Run the installer and follow the on-screen instructions. It installs for your Windows account without requiring administrator privileges.
3. Open **PSH Examination Checker** from the Start menu.
4. Use **Help** inside the application for the operating guide and **Print Form** for the bundled answer sheet.

Python and developer tools are bundled or unnecessary; staff do not need to install them separately. An application that supports Excel workbooks is needed to open the exported workbook externally.

Close the application before installing an update. To remove it, open Windows **Settings > Apps > Installed apps**, select **PSH Examination Checker**, and choose **Uninstall**. Keep examination scans and exported results in your own folders outside the application installation directory.

## Examination workflow

1. **Prepare the forms.** Use the bundled [150-question answer sheet](src/assets/multiple_choice_sheet_150q.pdf), after confirming that it is the layout approved for your examination.
2. **Scan the completed sheets.** Save each sheet as an individual PNG, JPG, JPEG, BMP, TIFF, or TIF image in one input folder. Keep corner markers and bubble areas visible. PDF and Excel files are not scan inputs; subfolders are ignored.
3. **Select the folders.** In the application, choose the input folder and an output folder for the batch.
4. **Add an answer key if scoring is required.** Select a CSV containing exactly one answer row, with question headers starting at `Q1` and continuing through the last question to score, up to `Q150`.
5. **Process and review.** Click **Process sheets**, review the results window, and compare questionable responses and rejected scans against the originals.
6. **Open the exports.** Use **Open Excel** for the review workbook or **Open output folder** to access all generated files.

A three-question answer-key example:

```csv
Q1,Q2,Q3
A,C,B
```

Use a separate batch for each examination with a different answer key. Review the selected key before starting another batch.

For complete operating instructions, output options, and troubleshooting, see the [PSH user guide](src/assets/manual.md), also available through **Help** in the application.

> **Review before finalizing results:** Audit detected answers and scores, particularly for low-quality scans, multiple responses, and rejected sheets. The software is provided without warranty.

## Output files

Each batch normally produces timestamped files.

| File | Purpose |
| --- | --- |
| `results.xlsx` | Excel review workbook with detected responses and red highlighting for multiple answers. Examinee IDs are stored as text to preserve leading zeroes. |
| `results.csv` | Detected responses in CSV format. Import Examinee IDs as text when opening in a spreadsheet. |
| `scores.csv` | Scores and per-question results when scoring is available. |
| `keys.csv` | Answer key used for the batch, when available. |
| `rejected_files.csv` | Scans whose corner markers could not be located. |
| `mcta_*.csv` | Optional exports for Multiple Choice Test Analysis. |

Calculated scores appear in `scores.csv` and the results window. Red response highlighting is available in the Excel workbook; CSV files do not store colors.

## Support

Contact your PSH application administrator for installation assistance, updates, or problems with examination processing. Include the steps that led to the issue and any error message.

## License and attribution

### Software

Copyright (C) 2019 Ian Sanders

This software is distributed under the **GNU General Public License, version 3 or, at your option, any later version (GPL-3.0-or-later)**. It is provided without any warranty, including implied warranties of merchantability or fitness for a particular purpose.

See [license.txt](license.txt) for the full software license. This fork preserves the original author's credit and license notice.

### Multiple-choice answer sheet

The multiple-choice sheet is licensed separately under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license (CC BY-NC-SA 4.0)**. The original notice permits sharing and modification with attribution, under the same license, and for noncommercial purposes. See the [full answer-sheet license](https://creativecommons.org/licenses/by-nc-sa/4.0/).

The original project also explicitly allows distribution of the **unmodified** sheet without attribution when used for educational purposes, provided that it is not presented as your own work. This exception is retained from the original README.

