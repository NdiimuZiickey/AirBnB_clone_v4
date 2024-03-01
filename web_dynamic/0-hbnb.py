#!/usr/bin/python3
""" Starts Flask web app """
from models import storage
from os import environ
from flask import Flask, render_template
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
import uuid
import shutil

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    """ Removes current SQLAlchemy Session """
    storage.close()

@app.route('/0-hbnb/', strict_slashes=False)
def hbnb():
    """ HBNB is alive! """
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    st_ct = []

    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    return render_template('0-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           cache_id=uuid.uuid4())

def setup():
    """Copies and renames files, updates route"""
    # Copy files
    shutil.copytree('web_flask/static', 'static')
    shutil.copy('web_flask/__init__.py', '.')
    shutil.copy('web_flask/100-hbnb.py', '0-hbnb.py')

    # Copy 100-hbnb.html or 8-hbnb.html
    html_file = '100-hbnb.html'
    if not os.path.exists('web_flask/templates/' + html_file):
        html_file = '8-hbnb.html'
    shutil.copy('web_flask/templates/' + html_file, 'templates/0-hbnb.html')

    # Update route in 0-hbnb.py
    with open('0-hbnb.py', 'r') as file:
        content = file.read()
    content = content.replace('@app.route("/0-hbnb/")', '@app.route("/0-hbnb/")')
    with open('0-hbnb.py', 'w') as file:
        file.write(content)

if __name__ == "__main__":
    setup()
    app.run(host='0.0.0.0', port=5001)
