# sqlalchemy-challenge

Added hawaii_sqlite_python_tester.py to check hawaii.sqlite data to ensure code was correct.

In step 5, ensure that with the urls /api/v1.0/<start> and /api/v1.0/<start>/<end> that a start and a start/end date is provided. An example could include /api/v1.0/2016-08-23
and /api/v1.0/2016-08-23/2017-08-23 so that the complete url looks like http://127.0.0.1:5000/api/v1.0/2016-08-23 and http://127.0.0.1:5000/api/v1.0/2016-08-23/2017-08-23. This took me a while to realise and I kept just writing http://127.0.0.1:5000//api/v1.0/<start> and http://127.0.0.1:5000/api/v1.0/<start>/<end> and getting the results 
{
  "TAVG": null,
  "TMAX": null,
  "TMIN": null
}
