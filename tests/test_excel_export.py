"""Regression checks for the Excel answer-review export."""
import sys
import tempfile
import unittest
from pathlib import Path

from openpyxl import load_workbook

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from data_exporting import OutputSheet
from grid_info import Field


class ExcelExportTests(unittest.TestCase):
    def test_highlights_only_multiple_answers_after_sorting(self):
        answers = OutputSheet([Field.STUDENT_ID, Field.IMAGE_FILE], 5)
        answers.add({Field.STUDENT_ID: "002", Field.IMAGE_FILE: "=scan.jpg"},
                    ["A", "[A|B]", "F", "G", ""])
        answers.add({Field.STUDENT_ID: "001", Field.IMAGE_FILE: "F"},
                    ["[B|C|D]", "B", "C", "D", "E"])
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            csv_path = answers.save(folder, "results", True, None)
            workbook = load_workbook(answers.save_excel(folder, None))
            sheet = workbook.active
            self.assertTrue(csv_path.exists())
            self.assertEqual(sheet["A2"].value, "001")
            self.assertEqual(sheet["A3"].value, "002")
            self.assertEqual(sheet["B3"].data_type, "s")
            self.assertEqual(sheet["B3"].value, "=scan.jpg")
            for address in ("C2", "D3", "E3"):
                self.assertEqual(sheet[address].fill.fgColor.rgb, "FFFFC7CE")
            for address in ("B2", "C3", "F3", "G3", "D2"):
                self.assertIsNone(sheet[address].fill.patternType)
            self.assertEqual(sheet.freeze_panes, "C2")
            workbook.close()


if __name__ == "__main__":
    unittest.main()
