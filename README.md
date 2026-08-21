# 🌍 Global Seismic Trends

## 1. Project Overview

Global Seismic Trends is a data analysis project that analyzes
earthquake data from around the world.

The project uses API-based data retrieval, Python data cleaning,
MySQL database analysis, SQL queries, and an interactive Streamlit
dashboard to identify earthquake patterns, trends, and risk zones.


## 2. Problem Statement

- Analyze and interpret global earthquake data to identify
  seismic patterns, trends, and risk zones.

- Build a data-driven system using API-based retrieval,
  preprocessing, and SQL analytics for meaningful earthquake insights.


## 3. Project Objectives

- Retrieve earthquake data using the USGS API.
- Clean and preprocess the earthquake dataset.
- Store the cleaned data in MySQL.
- Perform SQL-based analysis.
- Identify earthquake trends and patterns.
- Analyze magnitude and depth.
- Identify strongest and deepest earthquakes.
- Analyze earthquake locations.
- Develop an interactive Streamlit dashboard.
- Present key findings and recommendations.


## 4. Data Source

The earthquake data was retrieved from the United States
Geological Survey (USGS) Earthquake Catalog API.

The dataset covers approximately five years of earthquake events.


## 5. Technologies Used

- Python
- Pandas
- Requests
- Regex
- MySQL
- SQL
- Matplotlib
- PyDeck
- Streamlit
- USGS API


## 6. Data Retrieval

Python was used to retrieve earthquake data from the USGS API.

The data was retrieved for the required time period and converted
into a structured Pandas DataFrame for further processing.


## 7. Data Cleaning

The following preprocessing steps were performed:

- Checked missing values.
- Checked data types.
- Converted date and time values.
- Checked invalid values.
- Checked negative depth values.
- Checked zero values.
- Identified outliers using the IQR method.
- Handled missing values using appropriate methods.
- Removed unnecessary columns.
- Removed the magnitude error column.
- Saved the cleaned dataset as earthquake_cleaned.csv.


## 8. Database

The cleaned earthquake data was stored in MySQL.

Database name:

earthquake_db

Table name:

earthquakes


## 9. SQL Analysis

SQL queries were used to analyze:

- Top 10 strongest earthquakes.
- Top 10 deepest earthquakes.
- Shallow high-magnitude earthquakes.
- Average depth.
- Average magnitude by magnitude type.
- Year with the most earthquakes.
- Month with the highest number of earthquakes.
- Day with the most earthquakes.
- Most active reporting network.
- Reviewed vs automatic earthquakes.
- Earthquake types.
- Tsunami events.
- Year-over-year earthquake growth.
- Seismically active regions.
- Deep-focus earthquake regions.
- Data reliability.


## 10. Streamlit Dashboard

An interactive Streamlit dashboard was developed to present
the earthquake analysis.

The dashboard includes:

- Total earthquake count.
- Average magnitude.
- Maximum magnitude.
- Average depth.
- Year-wise earthquake chart.
- Magnitude distribution.
- Depth distribution.
- Interactive earthquake map.
- Magnitude-based color classification.
- Top earthquake locations.
- Strongest earthquakes.
- Risk-zone analysis.
- Magnitude filter.
- Year filter.
- SQL analysis results.


## 11. Risk Zone Classification

For dashboard visualization, earthquakes were classified as:

| Magnitude | Risk Zone |
|-----------|-----------|
| < 4       | Low Risk |
| 4 to < 5  | Moderate Risk |
| >= 5      | High Risk |

This classification is a project-defined analytical classification
used for visualization and does not represent an official
earthquake hazard standard.


## 12. Project Workflow

USGS API
↓
Data Retrieval
↓
Data Cleaning
↓
Pandas Analysis
↓
MySQL Database
↓
SQL Analysis
↓
Streamlit Dashboard
↓
Insights and Recommendations


## 13. Key Findings

The project identifies patterns in earthquake magnitude, depth,
location and occurrence over time.

The SQL analysis identifies the strongest and deepest earthquake
events, active reporting networks, temporal patterns and
deep-focus earthquake regions.

The Streamlit dashboard provides interactive exploration of
these patterns using filters and visualizations.


## 14. Recommendations

- Monitor high-magnitude earthquake events carefully.
- Study regions with frequent seismic activity.
- Monitor deep-focus earthquakes separately.
- Analyze tsunami-associated earthquake events.
- Use historical earthquake patterns to support disaster
  preparedness.
- Use interactive dashboards to make seismic data easier to
  understand.


## 15. Limitations

- The analysis is based on available USGS records.
- The dataset covers approximately five years.
- Some earthquake fields contain missing values.
- The `place` field does not always provide a clean country name.
- Risk classification is simplified for project visualization.


## 16. Conclusion

The Global Seismic Trends project demonstrates an end-to-end
data analytics workflow.

Earthquake data was retrieved using the USGS API, cleaned using
Python and Pandas, stored in MySQL, analyzed using SQL, and
presented through an interactive Streamlit dashboard.

The project demonstrates how data retrieval, preprocessing,
database management, SQL analytics and visualization can be
combined to generate meaningful insights from real-world
earthquake data.