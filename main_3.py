# %%
# import the usual libraries
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats

# %%
# url to data
flights_url = "https://raw.githubusercontent.com/byuidatascience/data4missing/master/data-raw/flights_missing/flights_missing.json"

# read data as JSON file
flights = pd.read_json(flights_url)

# %%
# QUESTION 1
# Fix all of the varied missing data types in the data to be consistent
# (all missing values should be displayed as “NaN”). In your report include
# one record example (one row) from your new data, in the raw JSON format.
# Your example should display the “NaN” for at least one missing value.__

# ***fill missing values to display NaN***
# run this cell and avoid all the other cleansing for missing values in general
missing_values = [None, "NA", "N/A", "na", "n/a", "null", "", " ", np.nan]
flights.replace(missing_values, np.nan, inplace=True)

flights.tail()

# %%
# IMPROVED CLEANSING
# Improve the cleansing by using different techniques
# ***call flights again to clean it deeper***
flights = pd.read_json(flights_url)

# CLEANG COLUMN BY COLUMN
# %%
# ***clean airport_name column***
# this code will assign airport name based on airport codes
airport_names = [
    "Atlanta, GA: Hartsfield-Jackson Atlanta International",
    "Denver, CO: Denver International",
    "Washington, DC: Washington Dulles International",
    "Chicago, IL: Chicago O'Hare International",
    "San Francisco, CA: San Francisco International",
    "San Diego, CA: San Diego International",
    "Salt Lake City, UT: Salt Lake City International",
]

airport_codes = ["ATL", "DEN", "IAD", "ORD", "SAN", "SFO", "SLC"]
counter = 0
while counter < flights.shape[0]:
    if flights.loc[counter, "airport_code"] == airport_codes[0]:
        flights.at[counter, "airport_name"] = airport_names[0]
    elif flights.loc[counter, "airport_code"] == airport_codes[1]:
        flights.at[counter, "airport_name"] = airport_names[1]
    elif flights.loc[counter, "airport_code"] == airport_codes[2]:
        flights.at[counter, "airport_name"] = airport_names[2]
    elif flights.loc[counter, "airport_code"] == airport_codes[3]:
        flights.at[counter, "airport_name"] = airport_names[3]
    elif flights.loc[counter, "airport_code"] == airport_codes[4]:
        flights.at[counter, "airport_name"] = airport_names[4]
    elif flights.loc[counter, "airport_code"] == airport_codes[5]:
        flights.at[counter, "airport_name"] = airport_names[5]
    elif flights.loc[counter, "airport_code"] == airport_codes[6]:
        flights.at[counter, "airport_name"] = airport_names[6]
    counter += 1

# %%
# ***clean month column***
flights["month"].value_counts()
# replace all n/a values with NA
flights["month"] = flights["month"].replace("n/a", pd.NA)
# flights.replace("n/a", np.nan, inplace=True)
# check for missing values
flights["month"].isna().value_counts()
# The "ffill" method fills in missing values by forward-filling, which means
# that it uses the last known value to fill in subsequent missing values.
flights["month"].fillna(method="ffill", inplace=True)

# %%
# ***clean year column***
flights["year"].fillna(method="ffill", inplace=True)

# %%
# ***clean num_of_delays_carrier column***
flights["num_of_delays_carrier"].value_counts()
delays_subset = flights["num_of_delays_carrier"].replace("1500+", pd.NA)
delays_subset.dropna()
# convert column to numeric values and get the mean
delays_subset_numeric = pd.to_numeric(delays_subset, errors="coerce")
mean_delay = round(delays_subset_numeric.mean())
# add the mean of the column to replace those cells with a 1500+ value
flights["num_of_delays_carrier"] = flights["num_of_delays_carrier"].replace(
    "1500+", mean_delay
)

# %%
# ***clean num_of_delays_late_aircraft column***
flights["num_of_delays_late_aircraft"].value_counts()
delays_late_subset = flights["num_of_delays_late_aircraft"].replace("-999", pd.NA)
delays_late_subset.dropna()
# convert column to numeric values and get the mean
delays_late_subset_numeric = pd.to_numeric(delays_late_subset, errors="coerce")
mean_delays_late = round(delays_late_subset_numeric.mean())
# add the mean of the column to replace those cells with a -999 value
flights["num_of_delays_late_aircraft"] = flights["num_of_delays_late_aircraft"].replace(
    -999, mean_delays_late
)

# %%
# ***clean minutes_delayed_Carrier column***
flights["minutes_delayed_carrier"].value_counts()
min_delayed_carrier_mean = round(flights["minutes_delayed_carrier"].mean())
flights["minutes_delayed_carrier"].fillna(min_delayed_carrier_mean, inplace=True)

# %%
# ***clean minutes_delayed_nas column***
flights["minutes_delayed_nas"].isna().value_counts()
mins_delayed_nas_subset = flights["minutes_delayed_nas"].replace("-999", pd.NA)
mins_delayed_nas_subset.dropna()
mins_delayed_nas_mean = round(mins_delayed_nas_subset.mean())
# add the mean of the column to replace those cells with a -999 value
flights["minutes_delayed_nas"] = flights["minutes_delayed_nas"].replace(
    -999, mins_delayed_nas_mean
)
flights["minutes_delayed_nas"].fillna(mins_delayed_nas_mean, inplace=True)

# %%
# ***check if there's any NaN value in the df***
has_nan = flights.isnull().any().any()
print("Does the DataFrame have any NaN values?", has_nan)

# %%
# ***check if there's any NaN values in the df using columns***
nan_columns = flights.isnull().any()
print("Columns with NaN values:\n", nan_columns)

# %%
# QUESTION 2

# Which airport has the worst delays? Discuss the metric you chose, and why
# you chose it to determine the “worst” airport. Your answer should include
# a summary table that lists (for each airport) the total number of flights,
# total number of delayed flights, proportion of delayed flights, and
# average delay time in hours.

# get total flights for each airport
flight_totals = flights.groupby("airport_code")["num_of_flights_total"].sum()

# get total delays for each airport
delayed_totals = flights.groupby("airport_code")["num_of_delays_total"].sum()

# get proportion of delayed flights
delayed_proportion = delayed_totals / flight_totals

# get minutes delay time in hours
delay_totals_minutes = flights.groupby("airport_code")["minutes_delayed_total"].sum()
delay_totals_hours = round(delay_totals_minutes / 60, 2)

# create the worst airport data frame
worst_df = pd.DataFrame(
    {
        # "AirportCode": flight_totals.index,
        "TotalFlights": flight_totals,
        "TotalDelays": delayed_totals,
        "DelayProportion": delayed_proportion,
        "DelayTime(Hours)": delay_totals_hours,
    }
)

worst_df = worst_df.sort_values(by="DelayTime(Hours)", ascending=False)

worst_df

# %%
# QUESTION 3

# What is the best month to fly if you want to avoid delays of any length?
# Discuss the metric you chose and why you chose it to calculate your answer.
# Include one chart to help support your answer, with the x-axis ordered by month.
# (To answer this question, you will need to remove any rows that are missing
#  the Month variable.)

# average delay time per each month, reset index and convert to dataframe
flights_month = (
    flights.groupby("month")["minutes_delayed_total"].mean().round(2).reset_index()
)

# flights_month = flights_month.sort_values(ascending=False)

max_delay = flights_month["minutes_delayed_total"].max()
min_delay = flights_month["minutes_delayed_total"].min()

fig = px.scatter(
    flights_month,
    x="month",
    y="minutes_delayed_total",
    title="Avg. delay time (mins) by month (2005-2015)",
    labels={"minutes_delayed_total": "Average Minutes", "month": "Month"},
)

# format amounts to show (,) and round them, display each 30,000
fig.update_yaxes(tickformat=",.0f", dtick=30000)
fig.show()
