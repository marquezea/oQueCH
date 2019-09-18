import csv

for x in range(5):
    print(x)

with open('sand1.csv', mode='w') as testfile:
    sand_writer = csv.writer(testfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    sand_writer.writerow(['John Smith', 'Accounting', 'November'])
    sand_writer.writerow(['Erica Meyers', 'IT', 'March'])
    for x in range(5):
        sand_writer.writerow([x])