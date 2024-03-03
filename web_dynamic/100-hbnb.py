#!/usr/bin/python3
"""
Flask App that intergrates with AirBnB static HTML Template
"""
import uuid
from flask import Flask, render_template, url_for
from models import storage

#flask setup
app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'

#begin flask page rendering

@app.teardown_appcontext
def teardown_db(exception):
    """
    after each reaquest, this method calls .close() (i.e remove()) on the current SQLAchemy session
    """
    storage.close()

@app.route('/100-hbnb/')
def hbnb_filters():
    """
    handles request custom tamplate with states, cities, & amenities
    """
    states = list(storage.all('State').values())
    amens = list(storage.all('Amenity').values())
    places = list(storage.all('Place').values())
    users = {user.id: f"{user.first_name} {user.last_name}"
            for user in storage.all('User').values()}
    cache_id =str(uuid.uuid4())
    return render_template('100-hbnb.html',
            states=states,
            amens=amens,
            places=places,
            users=users,
            cache_id=cache_id)

if __name__ =="__main__":
    """
    MAIN Flask App
    """
    app.run(host=host, port=port)
