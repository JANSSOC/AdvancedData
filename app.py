from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,inspect, func
   
#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

session = Session(engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

date = dt.datetime(2016, 8, 23)
#'Preciptiation'
results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > date).order_by(Measurement.date).all()

df = pd.DataFrame(results, columns=['date', 'prcp'])
df.fillna(0, inplace=True)   
di = df.to_dict('records')

#'Stations '
results1 = session.query(Station.station).all()
df2 = pd.DataFrame(results1)
li = df2['station'].values.tolist() 

#'tobs'
date = dt.datetime(2016, 8, 23)
results2 = session.query(Measurement.date,Measurement.tobs).\
    filter((Measurement.date > date)).all()
df5 = pd.DataFrame(results2)
li1 = df5['tobs'].values.tolist()
#################################################
# Flask Setup

app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Vacation Climate API !<br/>"
        f"Available Routes:{Base.classes.keys()}<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"calculate `TMIN`, `TAVG`, and `TMAX`, use the following syntax YYYY-MM-DD <br/>"
        f"/api/v1.0/--START DT--<br/>"
        f"/api/v1.0/2012-02-28<br/>"
        f"/api/v1.0/--START DT--/--FINISH DT--<br/>"
        f"/api/v1.0/2012-02-28/2014-03-05<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(di)

@app.route("/api/v1.0/stations")
def stations():
    return jsonify(li)

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(li1)

@app.route("/api/v1.0/<start>")
def tavg_start(start):
    engine = create_engine("sqlite:///hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)
    Measurement = Base.classes.measurement
    def calc_temps(start_date, end_date):   
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    li3 = calc_temps(start, '2018-03-05')        
    return jsonify(li3)

@app.route("/api/v1.0/<start>/<end>")
def tavg_rng(start,end):
    engine = create_engine("sqlite:///hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)
    Measurement = Base.classes.measurement
    def calc_temps(start_date, end_date):   
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    li3 = calc_temps(start, end)        
    return jsonify(li3)




"""
* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
"""











if __name__ == "__main__":
    app.run(debug=True)
