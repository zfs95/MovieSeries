from flask import Flask, render_template, url_for, request, redirect, flash, session
from data import queries
import math
from util import json_response
from dotenv import load_dotenv
import password_manager

load_dotenv()
app = Flask('codecool_series')
app.jinja_env.filters['zip'] = zip
app.secret_key = "alRsihgalShwieudDruwgy123971294r83efi"



@app.route('/')
def index():

    return render_template('index.html')

@app.route('/get_info_for_home_page')
@json_response
def get_info_for_home_page():
    shows = queries.get_shows()
    return shows




@app.route('/shows/most-rated/<int:page_number>')
def show_most_rated(page_number):

    first_page = queries.first_page()
    last_page = queries.last_page()

    if(page_number<first_page[0]['firstpageno'] or page_number>last_page[0]['lastpageno']):
        return redirect(url_for('not_available'))

    offset= page_number*15-15
    order = request.args.get("order_by")
    direction = request.args.get("order_direction")

    if not order:
        order = "rating"
        direction = "descending"

    shows = queries.get_most_rated_shows(offset, order, direction)
 
    return render_template('show_most_rated.html', shows=shows, page_number=page_number, first_page=first_page[0]['firstpageno'], last_page=last_page[0]['lastpageno'])



@app.route('/show/<int:id>')
def display_show(id):

    number_of_seasons = queries.get_show_number_of_seasons(id)
    season_info = queries.get_seasons_title_and_overview(id)
    show = queries.get_single_show(id)
    actors = queries.get_actors_name_and_id(id)

    return render_template('display_show.html', show=show, number_of_seasons=number_of_seasons, season_info=season_info, actors=actors)



@app.route('/actors')
def actors():

    actors = queries.get_actors()
    return render_template('display_actors.html', actors=actors)



@app.route('/actor/<int:id>')
def display_actors_show(id):

    actor_name = queries.get_single_actor(id)
    shows = queries.get_actor_shows(id)
    character = queries.get_actor_character_by_id(id)
    actor_info = queries.get_actor_information_by_id(id)

    return render_template('actor_shows.html', shows=shows, actor_name=actor_name, character=character, actor_info=actor_info)



@app.route('/not-available')
def not_available():

    return render_template('pagenotavailable.html')



def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
