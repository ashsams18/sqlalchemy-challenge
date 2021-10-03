from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)
@app.route("/")
def welcome():
    
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    last12months = dt.datetime.strptime('2017-08-23', '%Y-%m-%d') - dt.timedelta(days=366)
    results = (session.query(Measurement.date,Measurement.prcp)
    .filter(Measurement.date >= last12months).all())
    session.close()
    resultsdp = {}
    for date, prcp in results:
        results_dict = {}
        results_dict[date] = prcp
        resultsdp.update(results_dict)
    return jsonify(resultsdp)
    
@app.route("/api/v1.0/stations")
def station():
    resultst = session.query(Station.station).all()
    session.close()
    resultstation = list(np.ravel(resultst))
    return jsonify (resultstation)

@app.route("/api/v1.0/tobs")
def tobs():
    last12months = dt.datetime.strptime('2017-08-23', '%Y-%m-%d') - dt.timedelta(days=366)
    resultobs = (session.query(Measurement.tobs)
    .filter(Measurement.date >= last12months)
    .filter(Measurement.station == 'USC00519281')
    .all()
    )
    session.close()
    resultstationtob = list(np.ravel(resultobs))
    return jsonify (resultstationtob)

@app.route("/api/v1.0/<start>") 
@app.route("/api/v1.0/<start>/<end>")
def tempdate(start,end = None):
       
    if end:
        # End here is defined
        # We want to filter using start and end
        datestart = dt.datetime.strptime(start, '%Y-%m-%d')
        dateend = dt.datetime.strptime(end,'%Y-%m-%d')
        
        customss = (session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))
        .filter(Measurement.date >= datestart,Measurement.date <= dateend)
        .all())
        session.close()
    else:
        datestart = dt.datetime.strptime(start, '%Y-%m-%d')
        customss = (session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))
        .filter(Measurement.date >= datestart)
        .all())
        session.close()

    startend = list(np.ravel(customss))

    return jsonify (startend)
   
if __name__ == '__main__':
    app.run(debug=True)


