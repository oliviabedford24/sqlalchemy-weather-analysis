import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(autoload_with=engine)

measurement = Base.classes.measurement

app = Flask(__name__)

@app.route("/")
def home():
    """List all available API routes"""
    return (f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start/end<br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Return hawaii precipitation dictionary"""
    results = session.query(measurement.date, measurement.prcp).order_by(measurement.date).all()
    session.close()
    all_prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp_data.append(prcp_dict)
    return jsonify(all_prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return station data as list"""
    results = session.query(measurement.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

tobs_date = dt.date(year=2016, month=1, day=1)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= tobs_date).all()
    session.close()
    temp_obs = list(np.ravel(results))
    return jsonify(temp_obs)


@app.route("/api/v1.0/<start_date>")
def start(start_date):
    session = Session(engine)
    start_date = dt.datetime.strptime(start_date, "%Y%m%d")
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs),
        func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    session.close()
    start_list = list(np.ravel(results))
    return jsonify(start_list)


@app.route("/api/v1.0/<second_start>/<end_date>")
def start_end(second_start, end_date):
    session = Session(engine)
    second_start = dt.datetime.strptime(second_start, "%Y%m%d")
    end_date = dt.datetime.strptime(end_date, "%Y%m%d")
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs),
        func.avg(measurement.tobs)).\
        filter(measurement.date <= end_date, measurement.date >= second_start).all()
    session.close()
    start_end_date = list(np.ravel(results))
    return jsonify(start_end_date)

if __name__ == "__main__":
    app.run()