import os
import sys
import csv

ofile = open(sys.argv[1]+'points.csv',"wb")
writer = csv.writer(ofile)

for files in os.listdir(sys.argv[1]):
    if files.endswith('.3pts') or files.endswith('.dat'):
        ifile = open(sys.argv[1]+files,"rb")
        reader = csv.reader(ifile, delimiter=' ')
        files = files.replace('.3pts','.jpg').replace('.3pts','.jpg')
        row = [files]
        for i in reader:
            a = float(i[0])
            b = float(i[1])
            row.append(a)
            row.append(b)

        writer.writerow(row)
        ifile.close()

ofile.close()
