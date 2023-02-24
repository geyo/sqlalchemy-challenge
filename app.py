import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
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
    # List all available routes
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    #Start session
    session = Session(engine)

    # YEAR AGO
    # Find the most recent date in the data set.
    recent_query = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # Convert date to datetime object. 
    most_recent_date = dt.datetime.strptime(recent_query[0],'%Y-%m-%d')
    # Calculate the date one year from the last date in data set.
    year_ago = most_recent_date - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    sel = [Measurement.date, Measurement.prcp]
    results = session.query(*sel).filter(Measurement.date >= year_ago).all()

    # Close session
    session.close()    

    # Create a dictionary from the row data and append to a list
    years_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp  #  use date as the key and prcp as the value.   
        years_data.append(prcp_dict)

    # Return the JSON representation of your dictionary.
    return jsonify(years_data)

@app.route("/api/v1.0/stations")
#Return a JSON list of stations from the dataset.
def stations():
    session = Session(engine)
    result = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(result))
    
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # YEAR AGO
    # Find the most recent date in the data set.
    recent_query = session.query(Measurement.date) \
                          .order_by(Measurement.date.desc())\
                          .first()
    # Convert date to datetime object. 
    most_recent_date = dt.datetime.strptime(recent_query[0],'%Y-%m-%d')
    # Calculate the date one year from the last date in data set.
    year_ago = most_recent_date - dt.timedelta(days=365)

    # MOST ACTIVE STATION
    # List the stations and the counts in descending order.
    stations_counts = session.query(Measurement.station, func.count(Measurement.station)) \
                             .group_by(Measurement.station) \
                             .order_by(func.count(Measurement.station).desc()) \
                             .all()
    # Store station string in most_active variable. 
    most_active = stations_counts[0][0]

    #Query the dates and temperature observations of the most-active station for the previous year of data.
    result = session.query(Measurement.date, Measurement.tobs) \
                    .filter(Measurement.station == most_active) \
                    .filter(Measurement.date > year_ago).all()
    
    # Use a for-loop to store data in a list of dictionaries
    most_active_temps = []
    for date, temp in result:
        dt_dict = {}
        dt_dict[date] = temp
        most_active_temps.append(dt_dict)
    #Return a JSON list of temperature observations for the previous year.
    return jsonify(most_active_temps)

# API DYNAMIC ROUTE

#Start Route
@app.route("/api/v1.0/<start>")
def get_temps_by_date(start):
    #convert start date from url to date time object.
    date_obj = dt.datetime.strptime(start,'%Y-%m-%d')
    
    #start session
    session = Session(engine)

    #Find min/max/avg temp, and filter by date. 
    result = session.query(func.min(Measurement.tobs), \
                           func.max(Measurement.tobs), \
                           func.avg(Measurement.tobs)) \
                    .filter(Measurement.date >= date_obj) \
                    .all()
    
    # Convert list of tuples into normal list
    response = list(np.ravel(result))
    
    #close sesion
    session.close()
    
    #return jsonified response
    return jsonify(response)

#Start/End Route
@app.route("/api/v1.0/<start>/<end>")
def get_temps_by_date_range(start, end):
    #convert both dates to date time objects.
    start_date_obj = dt.datetime.strptime(start,'%Y-%m-%d')
    end_date_obj = dt.datetime.strptime(end,'%Y-%m-%d')

    #start session
    session = Session(engine)

    #Find min/max/avg temp, and filter by date. 
    result = session.query(func.min(Measurement.tobs), \
                           func.max(Measurement.tobs), \
                           func.avg(Measurement.tobs)) \
                    .filter(Measurement.date.between(start_date_obj, end_date_obj)) \
                    .all()
    
    # Convert list of tuples into normal list
    response = list(np.ravel(result))
    
    #close sesion
    session.close()
    
    #return jsonified response
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)

