import csv

with open("data/doctors_schedules.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    rows = list(reader)

print("Number of rows:", len(rows))

for row in rows[:5]:
    print(row)