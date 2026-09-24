# PSH-Examination Checker
User guide for the Philippine Society of Hypertension

## 1. Prepare a batch
Use the approved 150-question answer-sheet layout. The app reads Examinee ID bubbles and answer bubbles, and records the source filename. Written names are not transcribed.

Scan each sheet as an individual PNG, JPG, JPEG, BMP, TIFF or TIF image. Place one batch in its own input folder. PDF and Excel files are not scan inputs. Subfolders are ignored.

Keep the corner markers and all bubble areas visible. Avoid cropped, blurred or heavily skewed scans. A redesigned sheet must retain the configured ID, answer and corner-marker positions to be read correctly.

Print Form opens the bundled 150-question PDF. Confirm that this is your organization's approved layout before distributing it; this button does not automatically load a redesigned template.

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

## 4. Process the sheets
Review the configuration summary. Process sheets is enabled only when the required folders are selected, images are found, and any selected CSV key passes validation.

Click Process sheets once and wait for processing to finish. The progress area shows the current file. The results window opens after successful export.

## 5. Review the results window
Select an examinee on the left to see their detected answers on the right. The list includes Examinee ID, Source File and Score (%), or Not scored when no score is available.

Red answer rows indicate multiple detected answers. Compare these with the original scan before finalizing the examination results. The preview is for review, not editing.

Click a column header to sort. Click it again to reverse the order. You can sort by Examinee ID, Source File, Score, Question or Detected answer. Question numbers sort naturally, and unscored entries remain below numeric scores. Sorting this preview does not rewrite exported files.

Open Excel opens the review workbook in your associated spreadsheet app. Open output folder shows the exported files. The header also reports rejected scans.

## 6. Understand the output files
Files have a timestamp prefix identifying their batch.

- results.xlsx: detected answers for Excel review. Multiple-answer cells have a light red fill and dark red text. Examinee IDs are stored as text to retain leading zeroes. Column headings and identity columns remain visible while scrolling.
- results.csv: the detected answers in plain CSV format. CSV cannot store colors. When importing CSV into Excel, set Examinee ID to Text to preserve leading zeroes.
- scores.csv: generated when scoring is available. Includes Total Score (%), Total Points and per-question values of 1 for correct or 0 for incorrect.
- keys.csv: the answer key used for the batch, when available.
- rejected_files.csv: lists scans whose corner markers could not be located. Review and rescan those sheets as needed.
- mcta_*.csv: optional files for the analysis software.

The red highlights are in results.xlsx, not in the CSV files. The workbook contains detected responses; calculated scores are in scores.csv and the results window.

## 7. Run another batch
Click Another batch, or close the results window, to return to setup. Both input and output folder selections are cleared. Choose both folders again before processing.

Other options and the selected answer key remain selected. Check that the key and options are correct for the next examination. Canceling the answer-key Browse dialog clears that selection if you want to run without it.

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
