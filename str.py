import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk
import mysql.connector


# PAGE TITLE

st.title("🌍 Global Seismic Trends")
st.write("Earthquake Data Analysis Dashboard")


# LOAD EARTHQUAKE DATA

df_new = pd.read_csv(
    r"C:\Projects\Global_Seismic_Trends\notebooks\earthquake_cleaned.csv"
)


# FILTERS

# Convert time column to datetime
df_new["time"] = pd.to_datetime(df_new["time"])

# Extract year
df_new["year"] = df_new["time"].dt.year


# SIDEBAR FILTERS

st.sidebar.header("🔎 Earthquake Filters")


# Magnitude Filter
min_mag = float(df_new["mag"].min())
max_mag = float(df_new["mag"].max())

magnitude_range = st.sidebar.slider(
    "Select Magnitude Range",
    min_value=min_mag,
    max_value=max_mag,
    value=(min_mag, max_mag)
)


# Year Filter
years = sorted(df_new["year"].unique())

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + years
)



# APPLY FILTERS

filtered_df = df_new[
    (df_new["mag"] >= magnitude_range[0]) &
    (df_new["mag"] <= magnitude_range[1])
]


if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["year"] == selected_year
    ]


# Show filtered count
st.sidebar.metric(
    "Earthquakes Shown",
    len(filtered_df)
)


# DASHBOARD METRICS

total_earthquakes = len(filtered_df)
average_magnitude = filtered_df["mag"].mean()
maximum_magnitude = filtered_df["mag"].max()
average_depth = filtered_df["depth_km"].mean()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Earthquakes",
    total_earthquakes
)

col2.metric(
    "Average Magnitude",
    round(average_magnitude, 2)
)

col3.metric(
    "Maximum Magnitude",
    round(maximum_magnitude, 2)
)

col4.metric(
    "Average Depth (km)",
    round(average_depth, 2)
)


# DISPLAY DATA

st.header("Earthquake Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)



# YEAR-WISE EARTHQUAKE CHART

yearly_earthquakes = (
    filtered_df["year"]
    .value_counts()
    .sort_index()
)

st.header("📅 Earthquakes by Year")

st.bar_chart(
    yearly_earthquakes,
    height=400
)


# MAGNITUDE DISTRIBUTION

st.header("📈 Magnitude Distribution")

fig, ax = plt.subplots(figsize=(8, 4))

ax.hist(
    filtered_df["mag"],
    bins=20
)

ax.set_xlabel("Magnitude")
ax.set_ylabel("Number of Earthquakes")
ax.set_title("Distribution of Earthquake Magnitudes")

st.pyplot(fig)


# DEPTH ANALYSIS

st.header("🌊 Earthquake Depth Distribution")

fig, ax = plt.subplots(figsize=(8, 4))

ax.hist(
    filtered_df["depth_km"],
    bins=20
)

ax.set_xlabel("Depth (km)")
ax.set_ylabel("Number of Earthquakes")
ax.set_title("Distribution of Earthquake Depths")

st.pyplot(fig)


# EARTHQUAKE LOCATIONS

st.header("🌍 Earthquake Locations")


# Assign colors based on magnitude
def get_color(magnitude):

    if magnitude < 4:
        return [0, 255, 0]

    elif magnitude < 5:
        return [255, 255, 0]

    else:
        return [255, 0, 0]


filtered_df = filtered_df.copy()

filtered_df["color"] = filtered_df["mag"].apply(
    get_color
)


# Create map layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df,
    get_position="[longitude, latitude]",
    get_fill_color="color",
    get_radius=30000,
    pickable=True
)


# Set map view
view_state = pdk.ViewState(
    latitude=filtered_df["latitude"].mean(),
    longitude=filtered_df["longitude"].mean(),
    zoom=1
)


# Create map
deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state
)


# Display map
st.pydeck_chart(deck)


# Legend
st.markdown("### 🌋 Magnitude Legend")

st.markdown(
    """
    🟢 **Green** — Magnitude < 4  
    🟡 **Yellow** — Magnitude 4 to 4.99  
    🔴 **Red** — Magnitude ≥ 5
    """
)


# TOP EARTHQUAKE LOCATIONS

st.header("🌍 Top Earthquake Locations")

top_locations = (
    filtered_df["place"]
    .value_counts()
    .head(10)
)

st.bar_chart(
    top_locations,
    height=400
)


# RISK ZONE ANALYSIS

st.header("⚠️ Risk Zones")


def get_risk_zone(magnitude):

    if magnitude < 4:
        return "Low Risk"

    elif magnitude < 5:
        return "Moderate Risk"

    else:
        return "High Risk"


filtered_df = filtered_df.copy()

filtered_df["risk_zone"] = filtered_df["mag"].apply(
    get_risk_zone
)

risk_counts = (
    filtered_df["risk_zone"]
    .value_counts()
)


st.bar_chart(
    risk_counts,
    height=400
)


st.subheader("Risk Zone Summary")

st.dataframe(
    risk_counts.rename("Number of Earthquakes"),
    use_container_width=True
)


# MYSQL CONNECTION

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2910",
    database="earthquake_db"
)


# SQL ANALYSIS RESULTS

st.header("🗄️ SQL Analysis Results")

st.write(
    "The following insights are retrieved directly "
    "from the MySQL earthquake database."
)


# 1. TOP 10 STRONGEST EARTHQUAKES

st.subheader("🏆 Top 10 Strongest Earthquakes")

query1 = """
SELECT id, time, place, mag
FROM earthquakes
ORDER BY mag DESC
LIMIT 10
"""

strongest_sql = pd.read_sql(
    query1,
    conn
)

st.dataframe(
    strongest_sql,
    use_container_width=True
)


# 2. TOP 10 DEEPEST EARTHQUAKES


st.subheader("🌊 Top 10 Deepest Earthquakes")

query2 = """
SELECT id, time, place, depth_km
FROM earthquakes
ORDER BY depth_km DESC
LIMIT 10
"""

deepest_sql = pd.read_sql(
    query2,
    conn
)

st.dataframe(
    deepest_sql,
    use_container_width=True
)


# 3. YEAR WITH MOST EARTHQUAKES

st.subheader("📅 Year with Most Earthquakes")

query3 = """
SELECT
    YEAR(time) AS year,
    COUNT(*) AS no_of_earthquakes
FROM earthquakes
GROUP BY YEAR(time)
ORDER BY no_of_earthquakes DESC
LIMIT 1
"""

year_sql = pd.read_sql(
    query3,
    conn
)

st.dataframe(
    year_sql,
    use_container_width=True
)


# 4. MONTH WITH HIGHEST NUMBER OF EARTHQUAKES

st.subheader("📅 Month with Highest Number of Earthquakes")

query4 = """
SELECT
    MONTHNAME(time) AS month,
    COUNT(*) AS highest_earthquakes
FROM earthquakes
GROUP BY MONTHNAME(time)
ORDER BY highest_earthquakes DESC
LIMIT 1
"""

month_sql = pd.read_sql(
    query4,
    conn
)

st.dataframe(
    month_sql,
    use_container_width=True
)


# 5. DAY WITH MOST EARTHQUAKES


st.subheader("📅 Day with Most Earthquakes")

query5 = """
SELECT
    DAYNAME(time) AS day,
    COUNT(*) AS no_of_earthquakes
FROM earthquakes
GROUP BY DAYNAME(time)
ORDER BY no_of_earthquakes DESC
LIMIT 1
"""

day_sql = pd.read_sql(
    query5,
    conn
)

st.dataframe(
    day_sql,
    use_container_width=True
)


# 6. MOST ACTIVE REPORTING NETWORK

st.subheader("🌐 Most Active Reporting Network")

query6 = """
SELECT
    net AS active_network,
    COUNT(*) AS earthquakes
FROM earthquakes
GROUP BY net
ORDER BY earthquakes DESC
LIMIT 1
"""

network_sql = pd.read_sql(
    query6,
    conn
)

st.dataframe(
    network_sql,
    use_container_width=True
)


# 7. REVIEWED VS AUTOMATIC EARTHQUAKES

st.subheader("🔍 Reviewed vs Automatic Earthquakes")

query7 = """
SELECT
    status,
    COUNT(*) AS no_of_earthquakes
FROM earthquakes
GROUP BY status
"""

status_sql = pd.read_sql(
    query7,
    conn
)

st.bar_chart(
    status_sql.set_index("status")["no_of_earthquakes"]
)


# 8. EARTHQUAKES BY TYPE

st.subheader("🌋 Earthquakes by Type")

query8 = """
SELECT
    type AS earthquake_type,
    COUNT(*) AS no_of_earthquakes
FROM earthquakes
GROUP BY type
ORDER BY no_of_earthquakes DESC
"""

type_sql = pd.read_sql(
    query8,
    conn
)

st.bar_chart(
    type_sql.set_index("earthquake_type")[
        "no_of_earthquakes"
    ]
)


# 9. TSUNAMIS PER YEAR

st.subheader("🌊 Tsunamis per Year")

query9 = """
SELECT
    YEAR(time) AS year,
    COUNT(*) AS tsunami_events
FROM earthquakes
WHERE tsunami = 1
GROUP BY YEAR(time)
ORDER BY year
"""

tsunami_sql = pd.read_sql(
    query9,
    conn
)

st.bar_chart(
    tsunami_sql.set_index("year")[
        "tsunami_events"
    ]
)



# 10. YEAR-OVER-YEAR EARTHQUAKE GROWTH

st.subheader("📈 Year-over-Year Earthquake Growth")

query10 = """
SELECT
    year,
    no_of_earthquakes,
    previous_year,
    ROUND(
        (
            (no_of_earthquakes - previous_year)
            / previous_year
        ) * 100,
        2
    ) AS growth_rate
FROM
(
    SELECT
        year,
        no_of_earthquakes,
        LAG(no_of_earthquakes)
        OVER (ORDER BY year) AS previous_year
    FROM
    (
        SELECT
            YEAR(time) AS year,
            COUNT(*) AS no_of_earthquakes
        FROM earthquakes
        GROUP BY YEAR(time)
    ) AS yearly_data
) AS growth_data
ORDER BY year
"""

growth_sql = pd.read_sql(
    query10,
    conn
)

st.dataframe(
    growth_sql,
    use_container_width=True
)


# 11. TOP 3 SEISMICALLY ACTIVE REGIONS


st.subheader("🌍 Top 3 Seismically Active Regions")

query11 = """
WITH network_stats AS
(
    SELECT
        net,
        COUNT(*) AS frequency,
        AVG(mag) AS average_magnitude
    FROM earthquakes
    GROUP BY net
),

scores AS
(
    SELECT
        net,
        frequency,
        average_magnitude,

        (
            frequency - MIN(frequency) OVER ()
        )
        /
        NULLIF(
            MAX(frequency) OVER ()
            - MIN(frequency) OVER (),
            0
        ) AS frequency_score,

        (
            average_magnitude
            - MIN(average_magnitude) OVER ()
        )
        /
        NULLIF(
            MAX(average_magnitude) OVER ()
            - MIN(average_magnitude) OVER (),
            0
        ) AS magnitude_score

    FROM network_stats
)

SELECT
    net,
    frequency,
    ROUND(
        average_magnitude,
        3
    ) AS average_magnitude,

    ROUND(
        (
            frequency_score
            + magnitude_score
        ) / 2,
        3
    ) AS combined_score

FROM scores

ORDER BY combined_score DESC

LIMIT 3
"""

active_regions_sql = pd.read_sql(
    query11,
    conn
)

st.dataframe(
    active_regions_sql,
    use_container_width=True
)


# 12. LOWEST DATA RELIABILITY

st.subheader("⚠️ Events with Lowest Data Reliability")

query12 = """
SELECT
    id,
    time,
    place,
    gap,
    rms,

    ROUND(
        (gap + rms) / 2,
        3
    ) AS average_error

FROM earthquakes

WHERE gap IS NOT NULL
AND rms IS NOT NULL

ORDER BY average_error DESC

LIMIT 10
"""

reliability_sql = pd.read_sql(
    query12,
    conn
)

st.dataframe(
    reliability_sql,
    use_container_width=True
)


# 13. DEEP-FOCUS EARTHQUAKE REGIONS

st.subheader("🌑 Top Deep-Focus Earthquake Regions")

query13 = """
SELECT
    net AS region,
    COUNT(*) AS deep_earthquakes
FROM earthquakes
WHERE depth_km > 300
GROUP BY net
ORDER BY deep_earthquakes DESC
LIMIT 3
"""

deep_region_sql = pd.read_sql(
    query13,
    conn
)

st.bar_chart(
    deep_region_sql.set_index("region")[
        "deep_earthquakes"
    ]
)


# CLOSE MYSQL CONNECTION

conn.close()