from flask import Flask, render_template
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
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
