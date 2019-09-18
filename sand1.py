import csv

header = ['Títulos','Preço','Fração']
data = [['PETR4','100,12','8,04%'],['VALE3','9,12','5,04%']]

csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

f = open('fiis.csv','w', newline='')
writer = csv.writer(f, dialect='myDialect')
writer.writerow(header)
writer.writerow(data[0])
writer.writerow(data[1])
f.close()

print(header)
print(data)

