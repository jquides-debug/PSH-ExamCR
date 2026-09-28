# Tests

Run the current regression suite from the project root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

The top-level tests cover examinee-list matching, scoring integration and Excel exports. `fixtures/reports/examinee-scores-layout.xlsx` is a blank report-layout fixture with no examinee records.

The historical scan datasets and their CLI test harness were removed because they contained populated identity fields. Keep test data synthetic; do not add real examinee lists, completed answer-sheet scans or identifiable results as fixtures.
