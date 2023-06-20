# titanic-flask

### A web app made with Flask, SQLAlchemy, SQLite, Swagger

##### Retrieves data & statistics from the very well known famous Titanic CSV

Exposes three _get_ endpoints.. 

2. **/passengers** retrieves all the data for all the passengers.
3. **/passenger/<passenger_id>** retrieves the data for the passenger with the specified id. 
Optionally, can be passed a list of desired fields. If doing so, only that data is retrieved. For example,
call **/passenger/7?attributes=age%20name%20fare** in order to retrieve only age, name and fare for passenger 7.
4. **/histogram** retrieves a plot of the histogram of fare prices in percentiles.

Through the root "/" Swagger specification can be accesed.

The data is retrieved from either one of two sources - which is defined in configuration in config.ini -> DATA -> source

If source="db" the data is retrieved from the already existing titanic.db
If source="csv" the data is loaded from the csv into memory when running the server.

In order to run, simply execute "python app.py".

