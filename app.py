import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

# Load and cache the dataset for fast reloading
@st.cache_data
def load_data():
    # Load the dataset
    df = pd.read_csv("data/nyc_crime_data.csv")
    df.dropna(subset=['latitude', 'longitude', 'boro_nm', 'law_cat_cd'], inplace=True)  # Clean up missing data
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)
    return df

# Load data
data = load_data()

# Sidebar for filter options
st.sidebar.title("Filter Options")
boroughs = st.sidebar.multiselect("Select Borough(s):", options=data['boro_nm'].unique(), default=data['boro_nm'].unique())
crime_types = st.sidebar.multiselect("Select Crime Type(s):", options=data['law_cat_cd'].unique(), default=data['law_cat_cd'].unique())

# Filter dataset
filtered_data = data[(data['boro_nm'].isin(boroughs)) & (data['law_cat_cd'].isin(crime_types))]

# Main App
st.title("NYC Crime Analysis Dashboard")
st.write("Analyze crime data to identify trends and patterns in different boroughs of New York City.")

# Display basic stats
st.header("Basic Insights")
st.write(f"**Total Crimes in Selected Data:** {len(filtered_data)}")
st.write(f"**Average Crime Latitude:** {filtered_data['latitude'].mean():.3f}")
st.write(f"**Average Crime Longitude:** {filtered_data['longitude'].mean():.3f}")

# Insight 1: Crimes by Borough
st.subheader("Crimes by Borough")
borough_counts = filtered_data['boro_nm'].value_counts()
fig_borough = px.bar(borough_counts, x=borough_counts.index, y=borough_counts.values, labels={'x':'Borough', 'y':'Crime Count'}, title="Crime Count by Borough")
st.plotly_chart(fig_borough)

# Insight 2: Crime Category Distribution
st.subheader("Crime Category Distribution")
crime_category_counts = filtered_data['law_cat_cd'].value_counts()
fig_category = px.pie(crime_category_counts, names=crime_category_counts.index, values=crime_category_counts.values, title="Crime Distribution by Category")
st.plotly_chart(fig_category)

# Insight 3: Crime Heatmap
st.subheader("Crime Heatmap")
m = folium.Map(location=[40.7128, -74.0060], zoom_start=11)
heat_data = [[row['latitude'], row['longitude']] for index, row in filtered_data.iterrows()]
HeatMap(heat_data).add_to(m)
st_folium(m)

# Insight 4: Time Series of Crimes
st.subheader("Time Series of Crimes")
filtered_data['date'] = pd.to_datetime(filtered_data['cmplnt_fr_dt'], errors='coerce')
filtered_data['year'] = filtered_data['date'].dt.year
crimes_by_year = filtered_data.groupby('year').size()
fig_timeseries = go.Figure(data=go.Scatter(x=crimes_by_year.index, y=crimes_by_year.values, mode='lines+markers'))
fig_timeseries.update_layout(title="Crimes Over Time", xaxis_title="Year", yaxis_title="Number of Crimes")
st.plotly_chart(fig_timeseries)

# Insight 5: Top Crime Precincts
st.subheader("Top 10 Crime Precincts")
top_precincts = filtered_data['addr_pct_cd'].value_counts().nlargest(10)
fig_precinct = px.bar(top_precincts, x=top_precincts.index, y=top_precincts.values, labels={'x':'Precinct', 'y':'Crime Count'}, title="Top 10 Crime Precincts")
st.plotly_chart(fig_precinct)

# Insight 6: Common Crime Locations
st.subheader("Common Crime Locations")
common_locations = filtered_data['prem_typ_desc'].value_counts().nlargest(10)
fig_locations = px.bar(common_locations, x=common_locations.index, y=common_locations.values, labels={'x':'Location Type', 'y':'Count'}, title="Top 10 Crime Locations")
st.plotly_chart(fig_locations)

# Insight 7: Gender Percentage of Crime
if 'susp_sex' in filtered_data.columns:
    st.subheader("Gender Percentage of Crime")
    gender_counts = filtered_data['susp_sex'].value_counts()
    fig_gender = px.pie(gender_counts, names=gender_counts.index, values=gender_counts.values, title="Gender Distribution of Crime")
    st.plotly_chart(fig_gender)

# Insight 8: Age Distribution of Criminals
if 'vic_age_group' in filtered_data.columns:
    st.subheader("Age Distribution of Criminals")
    age_counts = filtered_data['vic_age_group'].value_counts()
    fig_age = px.bar(age_counts, x=age_counts.index, y=age_counts.values, labels={'x':'Age Group', 'y':'Count'}, title="Age Distribution of Criminals")
    st.plotly_chart(fig_age)
