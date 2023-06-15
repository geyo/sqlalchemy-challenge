# Hawaii Climate App

By Grace Yoo

**Programming Languages & Tools Used:** Python, SQLAlchemy

## Purpose

The purpose of this project are as follows:
1. Analyze and explore climate data using Python and SQLAlchemy.
2. Design a Climate App using Flask API.

## Climate Data Analysis

I used the automap_base() function to explore the data stored in a sqlite database. I designed a query to retrieve the last 12 months of precipitation data and plotted the results.

<img src="https://github.com/geyo/sqlalchemy-challenge/assets/8386502/c0e89c20-b9e4-45ef-87ee-53adc00cc586" alt="image" style="width: 40%;">

I also queried the last 12 months of temperature to plot a histogram of the most frequent temperature ranges.  

<img src="https://github.com/geyo/sqlalchemy-challenge/assets/8386502/67164d1a-c238-4fa8-bb86-4a9b21e45e8b" alt="image" style="width: 40%;">

## Flask App

After performing the initial analysis, I used Flask so that any user could theoretically could query the data on their own by editing the URL as directed. The following routes were used:

- <code> / </code>
  Landing page that lists all available routes. 
  
- <code> /api/v1.0/precipitation </code>
  Converts query results from precipitation analysis in a JSON format (date/precipitation). 
  
- <code> /api/v1.0/stations </code>
  Returns list of stations in JSON format

- <code> /api/v1.0/tobs </code>
  Queries dates/temperatures of most-active stationand returns a JSON list of temperature observations for the previous year. 

- <code> /api/v1.0/<start> </code> and <code> /api/v1.0/<start>/<end> </code>
  Returns a JSON list of min temp, average temp, max temp for a specified start and end range. 

## Results

 Here are the results:
  
### Landing page
<img src="https://github.com/geyo/sqlalchemy-challenge/assets/8386502/1854497c-cb0e-44a1-8960-47730184be37" alt="image" style="width: 40%;">

  ### Querying precipitation
<img src="https://github.com/geyo/sqlalchemy-challenge/assets/8386502/037f9365-df67-4470-b573-ad25f885c966" alt="image" style="width: 40%;">
  
  ### Querying list of stations
<img src="https://github.com/geyo/sqlalchemy-challenge/assets/8386502/250bd6de-57b9-49a1-ba20-8f0b40d98f9d" alt="image" style="width: 40%;">
  
  ### Querying list of temperature observations
<img src="https://github.com/geyo/sqlalchemy-challenge/assets/8386502/1b82d029-e995-49b4-be4a-58948edea9dc" alt="image" style="width: 40%;">
  
  ### Querying min/max/average temperatures for date range
<img src="https://github.com/geyo/sqlalchemy-challenge/assets/8386502/1b82d029-e995-49b4-be4a-58948edea9dc" alt="image" style="width: 40%;">
