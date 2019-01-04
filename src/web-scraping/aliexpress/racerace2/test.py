import csv

dict1 = {}
dict2 = {}

dict1['one'] = 'one'
dict1['two'] = 'two'

dict2['one'] = 'one'
dict2['two'] = 'two'
with open('output.csv', 'wb') as output:
    writer = csv.writer(output)
    for key, value in dict1.
        writer.writerow([key, value])
    for key, value in dict2.iteritems():
        writer.writerow([key, value])