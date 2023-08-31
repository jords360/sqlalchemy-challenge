from sqlalchemy import create_engine, MetaData, Table

# Create an engine to connect to the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the database schema
metadata = MetaData()
metadata.reflect(bind=engine)  # Associate metadata with the engine

# Access the measurement table using the reflected metadata
measurement_table = metadata.tables['measurement']

# Create a connection and query the first few rows of the measurement table
with engine.connect() as connection:
    query = measurement_table.select().limit(5)
    result = connection.execute(query)

    for row in result:
        print(row)



