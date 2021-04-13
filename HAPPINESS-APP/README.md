
The application is designed for data preprocessing and manipulation using SQL and Dataframes in flask application.
app.py is the main application file that could be imported as the package to access the various functions. In the application each api is designed for their respective function.

templates folder contains the UI files which are integrated with the backend api call using routing.

The application is designed to perform the following tasks:

1. Home page which is integrated with other pages as it is easier to navigate
2. Upload page - Multiple file upload facility is enabled in the flask application
3. Result of the upload page is message of successful upload of the list od files names
4. Main page of the link of files uploaded for display and subsequent page for displaying initial 2 rows and shape of the data files uploaded into the system.
6. Coverting from dataframe to sqlite table
7. Coverting from sqlite table to dataframe
8. Finding the intersection or common columns for two dataframes
9. Finding the nth percentile of the numerical columns
10. Next page is displays percentiles
