# Import the dependencies.
import numpy as np
import datetime as dt
import pandas as pd
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func





#################################################
# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
#################################################


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
app = Flask(__name__)
#################################################




#################################################
# Flask Routes
@app.route('/')
def welcome():
    return (
        f"Welcome to the Weather App<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    last_date = session.query(func.max(Measurement.date)).first()[0]
    last_date = dt.time.strptime(last_date, "%Y-%m-%d")
    one_year_ago = last_date - dt.timedelta(days=365)
    precipitation_scores_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > one_year_ago).all()
    precip_dict = {date: prcp for date, prcp in precipitation_scores_data}
    return jsonify(precip_dict)



@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = [station[0] for station in results]
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(func.max(Measurement.date)).first()[0]
    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
    one_year_ago = last_date - dt.timedelta(days=365)
    most_active_station = most_active_station[0][0]
    tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station).filter(Measurement.date > one_year_ago).all()
    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
def start(start):
    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    temp_dict = {"TMIN": temps[0][0], "TAVG": temps[0][1], "TMAX": temps[0][2]}
    return jsonify(temp_dict)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temp_dict = {"TMIN": temps[0][0], "TAVG": temps[0][1], "TMAX": temps[0][2]}
    return jsonify(temp_dict)

if __name__ == "__main__":
    app.run(debug=True)
    
#################################################


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
