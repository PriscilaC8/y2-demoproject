from flask import Flask, render_template, url_for, redirect, jsonify
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
app = Flask(__name__)

# Google Maps Config 
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDkbYFo8lquHs3dhFxiH0RTTgqt-epz1-0"
GoogleMaps(app)

# SQLAlchemy stuff
from database_setup import Base, Comment, Commenter, Vote
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///comments.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#YOUR WEB APP CODE GOES HERE
@app.route("/")
def main():
    # TODO: NEED DATA
    demomap = Map(
        identifier = 'demomap',
        varname= 'demomap',
        lat = 37.4419,
        lng= -122.1419,
        markers = [
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': 37.4419,
                'lng': -122.1419,
                'infobox' : "<b>Hello</b>"
            }
        ]
    )
    
    return render_template('index.html', demomap=demomap)

@app.route("/get_disagreement_demographics")
def get_disagreement_demographics():
    import queries
    demo = queries.get_demographics_who_agree(False)
    return jsonify(**demo)

@app.route("/get_map_demographics")
def get_map_demographics(lat_start, lat_end, lon_start, lon_end):
    import queries
    demo = queries.get_demographics_in_region(lat_start, lat_end, lon_start, lon_end)
    return jsonify(**demo)

if __name__ == '__main__':
    app.run(debug=True)
