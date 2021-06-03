
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


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
        f"/api/v1.0/<startdate><br/>"
        f"/api/v1.0/<startdate>/<enddate>"
    )



@app.route("/api/v1.0/precipitation")
def precip():
    print("Server received request for STATIONS...")
 
    prcp_results = session.query(Station.prcp).all()

    # Convert list of tuples into normal list
    prcp_list = list(np.ravel(prcp_results))

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for STATIONS...")
 # Query all stations
    station_results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_results))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for TOBS...")

    # Query all tobs
    tobs_results = session.query(Measurement.tobs).all()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(tobs_results))

    return jsonify(tobs_list)


@app.route("/api/v1.0/<startdate>")
def tobs_by_date(startdate):
    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).all())


@app.route("/api/v1.0/<startdate>/<enddate>")
def tobs_by_date_range(startdate, enddate):
    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all())





if __name__ == "__main__":
    app.run(debug=True)

