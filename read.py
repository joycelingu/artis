
file = open('constituents_csv.csv','r')
outfile = open('sp500.txt','w')

data = []
file.readline()

for line in file:
    line = line.rstrip('\n')
    line = line.split(',')
    data.append(line)

print(data)
for i in data:
    outfile.write('{ label: "' + i[1] + '", value: "' + i[0] + '" },\n')