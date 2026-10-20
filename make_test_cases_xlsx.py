import csv
from openpyxl import Workbook
from openpyxl.styles import Font
from maths.prime_check import is_prime

wb = Workbook()
ws = wb.active
ws.title = "prime_check"
ws.append(["Test ID", "Module", "Function", "Technique", "Input", "Expected", "Actual", "Status"])

with open("tests/data/prime_cases.csv", newline="") as f:
    for i, row in enumerate(csv.DictReader(f), start=1):
        n, exp = int(row["number"]), row["expected"] == "True"
        act = is_prime(n)
        tech = "BVA" if row["category"] == "boundary" else "ECP"
        ws.append([f"TC{i:02d}", "maths/prime_check.py", "is_prime", tech, n, exp, act,
                   "Pass" if act == exp else "Fail"])

for c in ws[1]:
    c.font = Font(bold=True)
for col, w in zip("ABCDEFGH", [9, 24, 12, 11, 10, 10, 10, 9]):
    ws.column_dimensions[col].width = w

wb.save("docs/assignment/test_cases.xlsx")
print("saved")