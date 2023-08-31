# Step 1
# Import the necessary libraries
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Create an instance of the Flask app
app = Flask(__name__)

# Reflect the database tables and define the classes
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Define the route for the homepage ("/")
@app.route("/")
def home():
    return (
        "Welcome to the Climate App API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/&lt;start&gt;<br/>"
        "/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

# Step 2
# Define the /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create an engine to connect to the SQLite database
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    # Reflect the database tables
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    # Create a session
    session = Session(engine)

    # Calculate the date one year ago from the most recent date
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Query the precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).\
              filter(Measurement.date >= one_year_ago).all()

    # Convert query results to a dictionary with date as the key and prcp as the value
    precipitation_data = {date: prcp if prcp is not None else 0 for date, prcp in results}

    # Close the session
    session.close()

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data)

# Step 3
# Define the /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create an engine to connect to the SQLite database
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    # Reflect the database tables
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    # Create a session
    session = Session(engine)

    # Query the list of station names
    stations = session.query(Station.station).all()

    # Convert query results to a list of station names
    station_list = [station[0] for station in stations]

    # Close the session
    session.close()

    # Return the JSON list of station names
    return jsonify(station_list)

# Step 4
# Define the /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create an engine to connect to the SQLite database
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    # Reflect the database tables
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    # Create a session
    session = Session(engine)

    # Query the most active station from the previous step
    most_active_station = session.query(Measurement.station).\
                          group_by(Measurement.station).\
                          order_by(func.count(Measurement.station).desc()).first()[0]

    # Calculate the date one year ago from the most recent date
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Query temperature observations for the most-active station in the last year
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
                       filter(Measurement.station == most_active_station).\
                       filter(Measurement.date >= one_year_ago).all()

    # Close the session
    session.close()

    # Convert query results to a list of dictionaries
    temperature_list = [{"date": date, "tobs": tobs} for date, tobs in temperature_data]

    # Return the JSON list of temperature observations
    return jsonify(temperature_list)

# Step 5 (First part)
# Define the /api/v1.0/<start> route
@app.route("/api/v1.0/<start>")
def temperature_stats_start(start):
    # print("Start Date:", start)  # Add this line to print the start date for debugging
    # Create an engine to connect to the SQLite database
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    # Reflect the database tables
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    # Create a session
    session = Session(engine)

    # Query the minimum, average, and maximum temperatures for the specified start date
    temperature_stats = session.query(func.min(Measurement.tobs),
                                      func.avg(Measurement.tobs),
                                      func.max(Measurement.tobs)).\
                         filter(Measurement.date >= start).all()

    # Close the session
    session.close()

    # Check if any temperature data was returned
    # if temperature_stats[0][0] is None:
    #     return jsonify({"error": "No temperature data available for the specified start date."})

    # Convert query results to a dictionary
    stats_dict = {
        "TMIN": temperature_stats[0][0],
        "TAVG": temperature_stats[0][1],
        "TMAX": temperature_stats[0][2]
    }

    # Return the JSON representation of the temperature statistics
    return jsonify(stats_dict)

# Step 5 (Second part)
# Define the /api/v1.0/<start>/<end> route
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_start_end(start, end):
    # print("Start Date:", start, end)  # Add this line to print the start/end date for debugging
    # Create an engine to connect to the SQLite database
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    # Reflect the database tables
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    # Create a session
    session = Session(engine)

    # Query the minimum, average, and maximum temperatures for the specified date range
    temperature_stats = session.query(func.min(Measurement.tobs),
                                      func.avg(Measurement.tobs),
                                      func.max(Measurement.tobs)).\
                         filter(Measurement.date >= start, Measurement.date <= end).all()

    # Close the session
    session.close()

    # Check if any temperature data was returned
    # if temperature_stats[0][0] is None:
    #     return jsonify({"error": "No temperature data available for the specified date range."})

    # Convert query results to a dictionary
    stats_dict = {
        "TMIN": temperature_stats[0][0],
        "TAVG": temperature_stats[0][1],
        "TMAX": temperature_stats[0][2]
    }

    # Return the JSON representation of the temperature statistics
    return jsonify(stats_dict)

# Run the app if this file is the main program
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

