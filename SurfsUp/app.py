# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
#Enter your desktop username in the username
username = ""
engine = create_engine(f"sqlite:////Users/{username}/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(autoload_with=engine)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List All Available Routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start date (YYYY-MM-DD) <br/>"
        f"/api/v1.0/start date/end date (YYYY-MM-DD) <start><end>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)

    stop = '2016-08-23'

    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > stop).all()
    session.close()

    precip_info = []
    for date, prcpt in precipitation:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcpt
        precip_info.append(precip_dict)
    return jsonify(precip_info)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    station_ = session.query(Measurement.station).distinct().all()
    session.close()

    station_info = []
    for station in station_:
        station_dict = {}
        station_dict['station name'] = station[0]
        station_info.append(station_dict)
    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    stop12 = '2016-08-23'
    results = session.query(Measurement.date, Measurement.tobs).filter((Measurement.station == 'USC00519281') & (Measurement.date > stop12)).all()
    session.close()

    tobs_info = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['Date'] = date
        tobs_dict['Observed Temperature'] = tobs
        tobs_info.append(tobs_dict)

    return jsonify(tobs_info)

@app.route("/api/v1.0/<start_date>")
def temps_start(start_date):
    session = Session(engine)

    results = session.query(func.avg(Measurement.tobs), func.min(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    temp_info = []
    for tobs in results:
        temp_dict={}
        temp_dict['Average'] = results[0][0]
        temp_dict['Minimum'] = results[0][1]
        temp_dict['Maximum'] = results[0][2]
        temp_info.append(temp_dict)

    return jsonify(temp_info)

@app.route("/api/v1.0/<start_date>/<end_date>")
def temps_start_end(start_date=None, end_date=None):
    session = Session(engine)

    results = session.query(func.avg(Measurement.tobs), func.min(Measurement.tobs), func.max(Measurement.tobs)).\
        filter((Measurement.date >= start_date)&(Measurement.date <= end_date)).\
        all()

    temp_data = []
    for tobs in results:
        temp_dict = {}
        temp_dict["Average"] = results[0][0]
        temp_dict["Minimum"] = results[0][1]
        temp_dict["Maximum"] = results[0][2]
        temp_data.append(temp_dict)

    return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)