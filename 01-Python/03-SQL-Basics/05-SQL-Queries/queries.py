# pylint: disable=C0103, missing-docstring

def detailed_movies(db):
    # return the list of movies with their genres and director name
    query="""
        SELECT m.title, m.genres, d.name
        FROM movies m 
        INNER JOIN directors d 
        ON m.director_id  = d.id;
    """
    db.execute(query)
    results = db.fetchall()
    return results

def top_five_youngest_newly_directors(db):
    # return the top 5 youngest directors when they direct their first movie
    query="""
        SELECT d.name, (m.start_year - d.birth_year) AS age_when_first_time_director
        FROM directors d
        INNER JOIN movies m
        ON m.director_id  = d.id
        WHERE age_when_first_time_director IS NOT NULL
        ORDER BY age_when_first_time_director ASC 
        LIMIT 5;
    """
    db.execute(query)
    results = db.fetchall()
    return results

def late_released_movies(db):
    # return the list of all movies released after their director death
    query="""
        SELECT m.title
        FROM movies m
        INNER JOIN directors d ON m.director_id  = d.id
        WHERE m.start_year > d.death_year
        ORDER BY m.title ASC;
    """
    db.execute(query)
    results = db.fetchall()
    return [r[0] for r in results]
    
def stats_on(db, genre_name):
    # return a dict of stats for a given genre
    genre_name = (genre_name,)
    query = """
        SELECT 
	    COUNT(m.id) AS number_of_movies, 
	    ROUND(AVG(m.minutes),2) AS avg_length	
        FROM movies m
        WHERE m.genres = ?
    """
    db.execute(query, genre_name)
    results = db.fetchone()
    results = {
        'genre': genre_name[0],
        'number_of_movies': results[0],
        'avg_length': results[1]
    }
    return results

def top_five_directors_for(db, genre_name):
    # return the top 5 of the directors with the most movies for a given genre
    pass

def movie_duration_buckets(db):
    # return the movie counts grouped by bucket of 30 min duration
    pass
