import streamlit as st
import pandas as pd

# Page title
st.title("🌍 Global Seismic Trends")

st.write("Earthquake Data Analysis Dashboard")

# Load earthquake data
df_new = pd.read_csv("notebooks/earthquake_cleaned.csv")


#filters 
#convert year column to datetime
df_new["time"] = pd.to_datetime(df_new["time"])

#extract year
df_new["year"] = df_new["time"].dt.year



#sidebar filters

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

# Apply filters
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


#Dashboard Metrics
total_earthquakes = len(filtered_df)
average_mangnitude = filtered_df['mag'].mean()
maximum_magnitude = filtered_df['mag'].max()
average_depth = filtered_df['depth_km'].mean()

#create column
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Earthquakes", total_earthquakes)
col2.metric("Average Magnitude", round(average_mangnitude, 2))
col3.metric("Maximum Magnitude", round(maximum_magnitude, 2))
col4.metric("Average Depth (km)", round(average_depth, 2))

# Display data
st.header("Earthquake Data")

st.dataframe(filtered_df)

#Year-wise earthquake chart 
#convert year column to datetime
df_new["time"] = pd.to_datetime(df_new['time'])

#extract year
df_new["year"] = df_new["time"].dt.year

#count earthquakes by year
yearly_earthquakes = filtered_df["year"].value_counts().sort_index()

## Year-wise earthquake chart
st.header(" Earthquakes by Year")


st.bar_chart(    
    yearly_earthquakes,
    height=400
)

#Magnitude diistribution by using histogram
import matplotlib.pyplot as plt
st.header("📈 Magnitude Distribution ")

fig, ax = plt.subplots(figsize=(8, 4))

ax.hist(filtered_df["mag"], bins= 20)
ax.set_xlabel("Magnitude")
ax.set_ylabel("Number of Earthquakes")
ax.set_title("Distribution of Earthquake Magnitudes") 

st.pyplot(fig) #this tells the streamlit to display 

#depth analysis 
# Depth Analysis
st.header("🌊 Earthquake Depth Distribution")

fig, ax = plt.subplots(figsize=(8, 4))

ax.hist(filtered_df["depth_km"], bins=20)

ax.set_xlabel("Depth (km)")
ax.set_ylabel("Number of Earthquakes")
ax.set_title("Distribution of Earthquake Depths")

st.pyplot(fig)

#earthquake locations
import pydeck as pdk

st.header("🌍 Earthquake Locations")

# Assign colors
def get_color(magnitude):
    if magnitude < 4:
        return [0, 255, 0]
    elif magnitude < 5:
        return [255, 255, 0]
    else:
        return [255, 0, 0]
    
filtered_df = filtered_df.copy()
filtered_df["color"] = filtered_df["mag"].apply(get_color)

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

st.markdown("""
🟢 **Green** — Magnitude < 4  
🟡 **Yellow** — Magnitude 4 to 4.99  
🔴 **Red** — Magnitude ≥ 5
""")


#Top earthquake locattions 
st.header("🌍 Top Earthquake Locations")

# Count earthquakes by location
top_locations = filtered_df["place"].value_counts().head(10)

# Display chart
st.bar_chart(
    top_locations,
    height=400
)


#risk zone analysis
st.header("⚠️ Risk Zones ")

def get_risk_zone(magnitude):
    if magnitude < 4:
        return "Low Risk"
    elif magnitude < 5:
        return "Moderate Risk"
    else:
        return "High Risk"


filtered_df = filtered_df.copy()
filtered_df["risk_zone"] = filtered_df["mag"].apply(get_risk_zone)
risk_counts = filtered_df["risk_zone"].value_counts()

st.bar_chart(
    risk_counts,
    height=400
)

st.subheader("Risk Zone Summary")

st.dataframe(
    risk_counts.rename("Number of Earthquakes"),
    use_container_width=True
)  

#SQL connection

import mysql.connector 

df_new = pd.read_csv("notebooks/earthquake_cleaned.csv")


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2910",
    database="earthquake_db"
)


# sql analysis results

st.header("🗄️ sql analysis results")

st.write(
    "the following insights are retrieved directly "
    "from the mysql earthquake database."
)


# 1. top 10 strongest earthquakes

st.subheader("🏆 top 10 strongest earthquakes")

query1 = """
select id, time, place, mag
from earthquakes
order by mag desc
limit 10
"""

strongest_sql = pd.read_sql(query1, conn)

st.dataframe(
    strongest_sql,
    use_container_width=True
)


# 2. top 10 deepest earthquakes

st.subheader("🌊 top 10 deepest earthquakes")

query2 = """
select id, time, place, depth_km
from earthquakes
order by depth_km desc
limit 10
"""

deepest_sql = pd.read_sql(query2, conn)

st.dataframe(
    deepest_sql,
    use_container_width=True
)


# 3. year with most earthquakes

st.subheader("📅 year with most earthquakes")

query3 = """
select year(time) as year,
count(*) as no_of_earthquakes
from earthquakes
group by year(time)
order by no_of_earthquakes desc
limit 1
"""

year_sql = pd.read_sql(query3, conn)

st.dataframe(
    year_sql,
    use_container_width=True
)


# 4. month with highest number of earthquakes

st.subheader("📅 month with highest number of earthquakes")

query4 = """
select monthname(time) as month,
count(*) as highest_earthquakes
from earthquakes
group by monthname(time)
order by highest_earthquakes desc
limit 1
"""

month_sql = pd.read_sql(query4, conn)

st.dataframe(
    month_sql,
    use_container_width=True
)


# 5. day with most earthquakes

st.subheader("📅 day with most earthquakes")

query5 = """
select dayname(time) as day,
count(*) as no_of_earthquakes
from earthquakes
group by dayname(time)
order by no_of_earthquakes desc
limit 1
"""

day_sql = pd.read_sql(query5, conn)

st.dataframe(
    day_sql,
    use_container_width=True
)


# 6. most active reporting network

st.subheader("🌐 most active reporting network")

query6 = """
select net as active_network,
count(*) as earthquakes
from earthquakes
group by net
order by earthquakes desc
limit 1
"""

network_sql = pd.read_sql(query6, conn)

st.dataframe(
    network_sql,
    use_container_width=True
)


# 7. reviewed vs automatic earthquakes

st.subheader("🔍 reviewed vs automatic earthquakes")

query7 = """
select status,
count(*) as no_of_earthquakes
from earthquakes
group by status
"""

status_sql = pd.read_sql(query7, conn)

st.bar_chart(
    status_sql.set_index("status")[
        "no_of_earthquakes"
    ]
)



# 8. earthquakes by type

st.subheader("🌋 earthquakes by type")

query8 = """
select type as earthquake_type,
count(*) as no_of_earthquakes
from earthquakes
group by type
order by no_of_earthquakes desc
"""

type_sql = pd.read_sql(query8, conn)

st.bar_chart(
    type_sql.set_index("earthquake_type")[
        "no_of_earthquakes"
    ]
)



# 9. tsunamis triggered per year

st.subheader("🌊 tsunamis triggered per year")

query9 = """
select year(time) as year,
count(*) as tsunami_events
from earthquakes
where tsunami = 1
group by year(time)
order by year
"""

tsunami_sql = pd.read_sql(query9, conn)

st.bar_chart(
    tsunami_sql.set_index("year")[
        "tsunami_events"
    ]
)


# 10. year over year earthquake growth

st.subheader("📈 year over year earthquake growth")

query10 = """
select year,
       no_of_earthquakes,
       previous_year,
       round(
           ((no_of_earthquakes - previous_year)
           / previous_year) * 100,
           2
       ) as growth_rate
from (
    select year,
           no_of_earthquakes,
           lag(no_of_earthquakes)
           over (order by year) as previous_year
    from (
        select year(time) as year,
               count(*) as no_of_earthquakes
        from earthquakes
        group by year(time)
    ) as yearly_data
) as growth_data
order by year
"""

growth_sql = pd.read_sql(
    query10,
    conn
)

st.dataframe(
    growth_sql,
    use_container_width=True
)


# 11. top 3 seismically active regions

st.subheader("🌍 top 3 seismically active regions")

query11 = """
with network_stats as (
    select
        net,
        count(*) as frequency,
        avg(mag) as average_magnitude
    from earthquakes
    group by net
),

scores as (
    select
        net,
        frequency,
        average_magnitude,

        (frequency - min(frequency) over ())
        /
        nullif(
            max(frequency) over ()
            - min(frequency) over (),
            0
        ) as frequency_score,

        (average_magnitude
        - min(average_magnitude) over ())
        /
        nullif(
            max(average_magnitude) over ()
            - min(average_magnitude) over (),
            0
        ) as magnitude_score

    from network_stats
)

select
    net,
    frequency,
    round(average_magnitude, 3)
        as average_magnitude,
    round(
        (frequency_score + magnitude_score) / 2,
        3
    ) as combined_score
from scores
order by combined_score desc
limit 3
"""

active_regions_sql = pd.read_sql(
    query11,
    conn
)

st.dataframe(
    active_regions_sql,
    use_container_width=True
)


# 12. lowest data reliability


st.subheader("⚠️ events with lowest data reliability")

query12 = """
select
    id,
    time,
    place,
    gap,
    rms,

    round(
        (gap + rms) / 2,
        3
    ) as average_error

from earthquakes

where gap is not null
and rms is not null

order by average_error desc

limit 10
"""

reliability_sql = pd.read_sql(
    query12,
    conn
)

st.dataframe(
    reliability_sql,
    use_container_width=True
)


# 13. deep focus earthquake regions

st.subheader("🌑 top deep focus earthquake regions")

query13 = """
select
    net as region,
    count(*) as deep_earthquakes
from earthquakes
where depth_km > 300
group by net
order by deep_earthquakes desc
limit 3
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

# close mysql connection

conn.close()