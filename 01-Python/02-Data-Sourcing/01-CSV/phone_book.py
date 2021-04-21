import csv

with open('data/phone_book.csv', mode='r' ) as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        #print(f"Row Type : {type(row)}")
        if line_count == 0:
            line_count += 1 
            continue
        print(f"{row[1]}: {row[2]}")
        line_count += 1