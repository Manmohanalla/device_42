import csv,os
    
def cpy():
    if os.stat('devicehardlog.csv').st_size==0:
        return 'empty'
    csv1 = list(csv.DictReader(open('devicehardlog.csv')))
    csv2 = list(csv.DictReader(open('deviceupdate.csv')))

    for row in csv1:
        if row not in csv2 and row['id'] not in [x['id'] for x in csv2]: 
         
            print 'delete',row['id']
            print
            
    for row in csv2:
        if row not in csv1:
            if row['id'] not in [x['id'] for x in csv1]:
                print 'added',row['id']
                print
            else:
                print 'update',row['id']
cpy()