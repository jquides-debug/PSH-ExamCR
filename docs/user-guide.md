# PSH-Examination Checker
User guide for the Philippine Society of Hypertension

## 1. Prepare a batch
Use the approved 150-question answer-sheet layout. The app reads Examinee ID bubbles and answer bubbles, and records the source filename. Written names are not transcribed.

Scan each sheet as an individual PNG, JPG, JPEG, BMP, TIFF or TIF image. Place one batch in its own input folder. PDF and Excel files are not scan inputs. Subfolders are ignored.

Keep the corner markers and all bubble areas visible. Avoid cropped, blurred or heavily skewed scans. A redesigned sheet must retain the configured ID, answer and corner-marker positions to be read correctly.

Open Templates and use the Printable answer sheet section to save the bundled 150-question form. Confirm that this is your organization's approved layout before distributing it; saving a form does not automatically load a redesigned layout into the checker.

## 2. Choose folders and options
In Scans & output, use Browse under Select Input Folder to choose the batch. Use Browse under Select Output Folder to choose where exports will be saved. A separate output folder for each examination helps keep records organized.

Save multiple answers as 'F': when enabled, two or more detected choices are exported as F. When disabled, the choices are retained, for example [A|B]. Both formats are highlighted red in the Excel review workbook.

Save empty answers as 'G': when enabled, unanswered questions are exported as G. When disabled, they remain blank. G and blank answers are not highlighted red.

F and G describe detected responses; they are not grades or additional answer choices.

Sort results by Examinee ID: sorts exported examinees by ID. Otherwise, the processing order is retained.

Output additional files for MCTA: creates extra CSV files for Multiple Choice Test Analysis. Leave this off for ordinary Excel review.

## 3. Add an optional answer key
For automatic scoring, select one CSV file under Answer key CSV (optional). Use exactly one answer row per batch. Different examinations with different keys must be processed separately.

A three-question example:
```csv
Q1,Q2,Q3
A,C,B
```
Continue the columns through the last question to be scored, up to Q150. Use the correct answer for each question. An optional Source File column before Q1 is supported. Save the file as CSV, not XLSX.

Without an answer key, you can still export and review detected answers. Scores are calculated against the supplied key; multiple or blank responses do not match an ordinary single-choice answer.

## Add an optional examinee list
Under Answer key & examinees, click Add examinee list and choose an Excel (.xlsx) or UTF-8 CSV (.csv) file. Put column headings on the first row; Excel imports the first worksheet. Include one row per examinee with their ID and any details you want in the results, such as name, email or department.

The app finds the Examinee ID header automatically, ignoring capitalization, spaces, underscores and hyphens. No column selection is needed. A missing or ambiguous ID header blocks processing with instructions to correct it. For an existing list headed #, NAME and EMAIL ADDRESS:, rename # to Examinee ID only if its values are the IDs marked on the answer sheets, rather than unrelated row numbers.

Numeric IDs match regardless of leading zeroes: 1 matches 0000000001. The scanned ID is preserved in the results. Other IDs match exactly after trimming surrounding spaces. Each list ID must be present and unique; blank or duplicate IDs block processing until the list is corrected and added again. Completely empty rows are ignored.

The app loads the list when you select it. After editing the file externally, click Add examinee list again to reload it. Use Remove to process without a list.

Click Templates at the bottom of the main window to see the available templates, instructions for using each file, and buttons to save your own copies:

- Examinee list - Excel (.xlsx): saves examinee-list.xlsx with Examinee-ID, NAME and EMAIL ADDRESS: headings. Enter your examinees, keeping the headings. Store IDs as text to retain leading zeroes. You may add other detail columns. Import the completed file using Add examinee list.
- Answer key - CSV, 150 questions (.csv): saves answer-key.csv. The supplied file contains headings only. Add exactly one answer row with the correct answers under Q1 through Q150; the Answer Key column may be blank. For a shorter exam, remove unused trailing question columns and their answers. Import the completed file using Answer key CSV.
- Printable answer sheet - 150 questions (.png): saves examination-sheet.png. Print the form for examinees, then provide individual scans of the completed sheets in your input folder.

Each section in Templates explains how to fill and import its file. Saving a template does not select it for processing; complete and save your own copy, then import it using the corresponding picker. Do not submit the blank answer-key template for scoring.

After checking, the app adds matching list details and an Examinee list match column to the results window, results.csv, results.xlsx and scores.csv (when scored). Scroll horizontally in the results list to see additional columns. Imported headings that conflict with result or scoring columns are prefixed with List:.

Every processed scan is retained. A scan with no matching ID is marked Not in list with blank imported details. The summary reports matched scans, unmatched scans and list entries without a processed scan. The results page also lists every examinee from the imported list: those without a processed scan are highlighted yellow and marked No scan detected, with blank scores. Selecting one shows that answers and a score are unavailable. Automatic result, score and analysis exports contain processed scans only; the separate Export results to Excel report includes everyone shown on the results page. Rejected scans cannot be matched because their IDs were not read successfully.

## 4. Process the sheets
Review the configuration summary. Process sheets is enabled only when the required folders are selected, images are found, and any selected CSV key and examinee list pass validation.

Click Process sheets once and wait for processing to finish. The progress area shows the current file. The results window opens after successful export.

## 5. Review the results window
Select an examinee on the left to see their detected answers on the right. The list includes Examinee ID, Source File and Score (%), or Not scored when no score is available.

Red answer rows indicate multiple detected answers. Compare these with the original scan before finalizing the examination results. The preview is for review, not editing.

Click a column header to sort. Click it again to reverse the order. You can sort by Examinee ID, Source File, Score, Question or Detected answer. Question numbers sort naturally, and unscored entries remain below numeric scores. Sorting this preview does not rewrite exported files.

Open Excel opens the review workbook in your associated spreadsheet app. Open output folder shows the exported files. The header also reports rejected scans.

Export results to Excel saves a separate score-summary workbook using the PSH Examinee Scores with Names layout. Choose the filename and location in the save dialog. The workbook contains Examinee No., Examinee Name, Score (%) and Points, with matching notes on the right. The points heading reflects the number of questions actually scored. It includes every row shown in the results page, in the current table sort order, including listed examinees without a scan. Missing scores remain blank and those rows are highlighted. A genuine zero score is exported as zero. Names require an imported examinee list with a Name, Examinee Name, Full Name, or separate first/last-name columns.

## 6. Understand the output files
Files have a timestamp prefix identifying their batch.

- results.xlsx: detected answers for Excel review. Multiple-answer cells have a light red fill and dark red text. Examinee IDs are stored as text to retain leading zeroes. Column headings and identity columns remain visible while scrolling.
- results.csv: the detected answers in plain CSV format. CSV cannot store colors. When importing CSV into Excel, set Examinee ID to Text to preserve leading zeroes.
- scores.csv: generated when scoring is available. Includes Total Score (%), Total Points and per-question values of 1 for correct or 0 for incorrect.
- keys.csv: the answer key used for the batch, when available.
- rejected_files.csv: lists scans whose corner markers could not be located. Review and rescan those sheets as needed.
- mcta_*.csv: optional files for the analysis software.
- PSH_[year]_Examinee_Scores_with_Names.xlsx: a score summary saved on demand using Export results to Excel. Includes names, percentage scores, points and highlighted rows with no score available, including examinees without scans.

The red highlights are in results.xlsx, not in the CSV files. The automatic results.xlsx workbook contains detected responses; calculated scores are in scores.csv, the results window and the score-summary workbook saved using Export results to Excel.

## 7. Run another batch
Click Another batch, or close the results window, to return to setup. Both input and output folder selections are cleared. Choose both folders again before processing.

Other options and the selected answer key remain selected. Check that the key and options are correct for the next examination. Canceling the answer-key Browse dialog clears that selection if you want to run without it.

The examinee list also remains selected. Remove or replace the list if the next batch uses different examinees. Canceling Add examinee list leaves the current list selected.

Each run creates a new set of timestamped files. You do not need to restart the app. Close the main application window when you are finished.

## 8. Troubleshooting
Process sheets is disabled: select both folders, confirm the input folder contains supported images, and check any selected answer-key CSV.

An answer-key file is rejected: check that it contains a Q1 header and exactly one answer row. Remove extra rows and save as CSV.

An Examinee ID or answer looks wrong: compare the scan and bubble positions with the approved template. Clear marks and correct layout alignment matter; this app reads bubble areas rather than arbitrary text.

A scan is rejected: check the corner markers, crop and scan quality. Review rejected_files.csv and process corrected scans in a new batch.

No red highlighting appears: open results.xlsx rather than results.csv. Only multiple answers are highlighted; G and blank answers are not.

Open Excel does not work: use Open output folder and open results.xlsx in an application that supports Excel workbooks.

Processing reports an error: use Back to setup, correct the input or key, and select the folders again. Check whether files were already written before rerunning.

Help opens this bundled guide inside the application. It does not require internet access or a PDF reader.
