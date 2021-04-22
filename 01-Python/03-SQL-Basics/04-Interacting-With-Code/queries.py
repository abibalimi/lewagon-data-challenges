# pylint: disable=missing-docstring, C0103,line-too-long

def directors_count(db):
    # Return the number of directors contained in the database
    query = """
        SELECT COUNT(id) 
        FROM directors
    """
    db.execute(query)
    results = db.fetchone() # results in a list (rows) of tuples (columns)
    return results[0]

def directors_list(db):
    # Return the list of all the directors sorted in alphabetical order
    query ="""
        SELECT d.name 
        FROM directors d
        ORDER BY d.name ASC;
    """
    db.execute(query)
    results = db.fetchall() # results in a list (rows) of tuples (columns)
    results = [r[0] for r in results]
    return results


def love_movies(db):
    # return the list of all movies which contain the word "love" in their title, sorted in alphabetical order
    query="""
        SELECT m.title 
        FROM movies m
        WHERE UPPER(m.title) LIKE  '%LOVE%'
        ORDER BY m.title ASC;
    """
    db.execute(query)
    results = db.fetchall() # results in a list (rows) of tuples (columns)
    results = [r[0] for r in results]
    return results


def directors_named_like_count(db, name):
    # return the number of directors which contain a given word in their name
    name = (f'%{name.upper()}%',)
    query = """
        SELECT COUNT(d.id) 
        FROM directors d
        WHERE UPPER(d.name) LIKE ?
    """
    db.execute(query, name)
    results = db.fetchone() # results in a list (rows) of tuples (columns)
    return results[0]


def movies_longer_than(db, min_length):
    # return this list of all movies which are longer than a given duration, sorted in the alphabetical order
    min_length = (min_length,)
    query = """
        SELECT m.title 
        FROM movies m
        WHERE m.minutes > ?
        ORDER BY m.title ASC
    """
    db.execute(query, min_length)
    results = db.fetchall() # results in a list (rows) of tuples (columns)
    return [r[0] for r in results]
