
from flask import Flask, jsonify
import datetime as dt
from types import FunctionType
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, inspect
from sqlalchemy import func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#Base.classes.keys()
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
##################################################
# see whats in the  tables & columns
#inspector = inspect(engine)
#inspector.get_table_names()

#columns = inspector.get_columns('measurement')
#for c in columns:
#   print(c['name'], c["type"])
    
#columns2 = inspector.get_columns('station')
#for c in columns2:
#    print(c['name'], c["type"]) 
    
#session.query(Measurement.station, Station.station, Station.id).count()


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start.end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precip():
    print("Server received request for precipitation...")
 
    prcp_results = session.query(Measurement.prcp).all()

    # Convert list of tuples into normal list
    prcp_list = list(np.ravel(prcp_results))

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for stations...")
 # Query all stations
    station_results = session.query(Measurement.station).all()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_results))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for tobs...")

    # Query all tobs
    tobs_results = session.query(Measurement.tobs).all()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(tobs_results))

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def temperatures_start(start):
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    
    # Convert list of tuples into normal list
    temperatures_start = list(np.ravel(results))

    return jsonify(temperatures_start)


@app.route("/api/v1.0/<start>/<end>")
def temperatures_start_end(start, end):
  
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
    
    # Convert list of tuples into normal list
    temperatures_start_end = list(np.ravel(results))

    return jsonify(temperatures_start_end)


if __name__ == "__main__":
    app.run(debug=True)
