
# Dependency
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

# Database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references
measurement = Base.classes.measurement
station = Base.classes.station

# Create an app, being sure to pass __name__
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def home():
     return (
    "Welcome to the Climate App</br>"
    "You can pick any of the following routes: </br>"
    f"/api/v1.0/precipitation</br>"
    f"/api/v1.0/stations</br>"
    f"/api/v1.0/tobs</br>"
    f"/api/v1.0/start</br>"
    f"/api/v1.0/start/end</br>"
    )

# Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")

    # Create our session (link) from Python to the DB
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    session = Session(engine)

    # query
    results = session.query(measurement.date, measurement.prcp).all()

    # Return the JSON representation of your dictionary.
    # Empty list
    percip_items= []

    # Add dates and percipitation into list
    for date, prcp in results:
        dictionary= {}
        dictionary['Date'] = date
        dictionary['Precipitation'] = prcp
        percip_items.append(dictionary) 


    session.close()

    return jsonify (percip_items)

# Define what to do when a user hits the /stations route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")

   # Create our session (link) from Python to the DB
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    session = Session(engine)

    # query
    results = session.query(measurement.station).distinct().all()


    # Convert list of tuples into normal list
    station_items = list(np.ravel(results))

    return jsonify (station_items)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperature Observation' page...")

   # Create our session (link) from Python to the DB
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    session = Session(engine)

    active = session.query(measurement.station, func.count(measurement.station)).\
    group_by(measurement.station).\
    order_by(func.count(measurement.station).desc()).all()

    most_active = active[0][0]

    # query
    results = session.query(measurement.date, measurement.tobs).filter(measurement.date >= '2016-8-24').filter(measurement.station == most_active).all()

    # Return the JSON representation of your dictionary.
    # Empty list
    tobs_items= []

    # Add dates and percipitation into list
    for date, tobs in results:
        dictionary= {}
        dictionary['Date'] = date
        dictionary['Temperature Observation'] = tobs
        tobs_items.append(dictionary) 

    return jsonify (tobs_items)

if __name__ == "__main__":
    app.run(debug=True)




