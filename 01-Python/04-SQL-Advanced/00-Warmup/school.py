# pylint:disable=C0111,C0103,W0621
import sqlite3
conn = sqlite3.connect('data/school.sqlite')
db = conn.cursor()

#import pdb; pdb.set_trace()

def students_from_city(db, city):
    """return a list of students from a specific city"""
    city = (f'{city.upper()}',)
    query="""
        SELECT first_name, last_name
        FROM students
        WHERE UPPER(birth_city) = ?
    """
    db.execute(query, city)
    results = db.fetchall() # results in a list (rows) of tuples (columns)
    return results

# To test your code, you can **run it** before running `make`
#   => Uncomment the following lines + run:
#   $ python school.py
#

print(students_from_city(db, 'berlin'))
