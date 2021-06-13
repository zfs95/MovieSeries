from data import data_manager
from psycopg2 import sql


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')

def get_actors():
    return data_manager.execute_select('SELECT id, name FROM actors;')

def get_single_actor(id):
    query='''SELECT name FROM actors WHERE id=%s;'''
    return data_manager.execute_select(query, (id, ))


def get_most_rated_shows(offset, column, direction):
    if direction =='descending':
        query = """SELECT  shows.id, shows.title,shows.year, shows.runtime, 
        ROUND(shows.rating,1) as rating,
        string_agg(genres.name, ',' ORDER BY genres.name ASC) as genres,
        shows.trailer, shows.homepage
        FROM shows 
        LEFT JOIN show_genres
        ON show_genres.show_id = shows.id
        LEFT JOIN genres ON
        genres.id = show_genres.genre_id
        GROUP BY shows.id
        ORDER BY {sorting} DESC
        OFFSET %s
        LIMIT 15;"""
    else:
        query = """SELECT  shows.id, shows.title,shows.year, shows.runtime, 
        ROUND(shows.rating,1) as rating,
        string_agg(genres.name, ',' ORDER BY genres.name ASC) as genres,
        shows.trailer, shows.homepage
        FROM shows 
        LEFT JOIN show_genres
        ON show_genres.show_id = shows.id
        LEFT JOIN genres ON
        genres.id = show_genres.genre_id
        GROUP BY shows.id
        ORDER BY {sorting} ASC
        OFFSET %s
        LIMIT 15;"""
    return data_manager.execute_select(sql.SQL(query).format(sorting=sql.Identifier(column)),(offset, ))


def get_single_show(id):
    query="""
    SELECT  shows.title, shows.runtime, shows.overview,shows.year,
    ROUND(shows.rating,1) as rating,
    string_agg(DISTINCT genres.name, ',' ORDER BY genres.name ASC) as genres,
    shows.trailer
    FROM shows 
    LEFT JOIN show_genres
    ON show_genres.show_id = shows.id
    LEFT JOIN genres
    ON genres.id = show_genres.genre_id
    WHERE shows.id = %s
    GROUP BY shows.id;  """
    return data_manager.execute_select(query,(id, ))

def get_actors_name_and_id(show_id):
    query="""
    SELECT
    actors.id, actors.name
    FROM show_characters
    LEFT JOIN actors 
    ON show_characters.actor_id = actors.id
    WHERE show_characters.show_id = %s
    LIMIT 3;
    """
    return data_manager.execute_select(query,(show_id, ))

# sql.SQL("insert into {} values (%s, %s)")
#         .format(sql.Identifier('my_table')),
#     [10, 20])


def get_show_number_of_seasons(id):
    query="""
    SELECT  COUNT(seasons.title) as numberofseasons
    FROM seasons
    INNER JOIN shows
    ON seasons.show_id = shows.id
    WHERE shows.id = %s"""
    return data_manager.execute_select(query, (id, ))


def get_seasons_title_and_overview(id):
    query="""
    SELECT seasons.title,seasons.overview
    FROM seasons
    INNER JOIN shows
    ON seasons.show_id = shows.id
	WHERE shows.id = %s
    GROUP BY seasons.id
"""
    return data_manager.execute_select(query, (id, ))

def first_page():
    return data_manager.execute_select('SELECT COUNT(id)/COUNT(id) AS firstpageno FROM shows;')

def last_page():
    return data_manager.execute_select('SELECT CEILING(COUNT(id)/15::FLOAT)::INT AS lastpageno FROM shows;')

def get_actor_shows(id):
    query="""
    SELECT  shows.id,shows.title, shows.runtime, shows.overview,shows.year,shows.homepage,
    ROUND(shows.rating,1) as rating,
    string_agg(DISTINCT actors.name, ',') as actors,
    string_agg(DISTINCT genres.name, ',' ORDER BY genres.name ASC) as genres,
    shows.trailer
    FROM shows 
    LEFT JOIN show_genres
    ON show_genres.show_id = shows.id
    LEFT JOIN genres ON
    genres.id = show_genres.genre_id
    INNER JOIN show_characters 
    ON show_characters.show_id = shows.id
    INNER JOIN actors 
    ON show_characters.actor_id = actors.id
    WHERE actors.id = %s
    GROUP BY shows.id;  """
    return data_manager.execute_select(query,(id, ))


def get_actor_character_by_id(id):
    query="""
    SELECT shows.id,show_characters.character_name
    FROM show_characters
    INNER JOIN shows
    ON shows.id = show_characters.show_id
    INNER JOIN actors
    ON actors.id = show_characters.actor_id
    WHERE show_characters.actor_id = %s; """
    return data_manager.execute_select(query, (id, ))

def get_actor_information_by_id(id):
    query="""SELECT
    birthday, death, biography
    FROM actors
    WHERE id = %s; """
    return data_manager.execute_select(query, (id, ))