import csv

with open('data/phone_book.csv', mode='r' ) as csv_file:
    csv_reader = csv.DictReader(csv_file, skipinitialspace=True)
    for row in csv_reader:
        #print(f"Row Type : {type(row)}")
        print(f"{row['last_name']}: {row['phone_number']}")

        