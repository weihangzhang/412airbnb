file = open('./countries.csv')

for line in file:
	line = line.strip()
	print line