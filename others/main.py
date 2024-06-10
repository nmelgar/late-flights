# %%
# import the usual libraries
import pandas as pd
import altair as alt
import numpy as np
from scipy import stats

# %%
# url to data
flights_url = "https://raw.githubusercontent.com/byuidatascience/data4missing/master/data-raw/flights_missing/flights_missing.json"

# read data as JSON file
flights = pd.read_json(flights_url)

# %%
# information about the dataset
flights.shape

# %%
# first and last rows/columns of the data set
flights
# %%
# data set column names
flights.columns

# %%
# type of data in the data set columns
flights.info()

# %%
# check for missing values
flights.isna()

# %%
# count the missing values in each column
missing_count = flights.isna().sum()
missing_count

# %%
# unique values for airport_name
flights.airport_name.value_counts()

# %%
# unique values for airport_code column
flights.airport_code.value_counts()

# %%
# this code will assign airport name based on
# airport codes
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
# unique values for airport_name
flights.airport_name.value_counts()

# %%
# unique values for airport_code
flights.airport_code.value_counts()

# %%
flights.year.value_counts().sum()
flights.year.mean()

# %%
# drop columns with missing year, we cannot use mean because 2010 will
# be too high to follow patterns in the data
flights = flights.dropna(subset=["year"])
flights

# %%
# replace NaN in minutes_delayed_carrier column with the mean value for the column
mean_minutes_delayed_carrier = flights["minutes_delayed_carrier"].mean()
flights["minutes_delayed_carrier"].fillna(mean_minutes_delayed_carrier, inplace=True)

# %%
# replace all n/a values with NA
flights["month"] = flights["month"].replace("n/a", pd.NA)

# %%
flights["month"].fillna(method="ffill", inplace=True)
flights.month.value_counts()

# %%
flights

# %%
# replace n/a with NaN
# flights.replace('n/a', np.nan, inplace=True)

# %%
# %% remove rows with missing values
# flights = flights.dropna()

#
data_columns = [
    "airport_code",
    "airport_name",
    "month",
    "year",
    "num_of_flights_total",
    "num_of_delays_carrier",
    "num_of_delays_late_aircraft",
    "num_of_delays_nas",
    "num_of_delays_security",
    "num_of_delays_weather",
    "num_of_delays_total",
    "minutes_delayed_carrier",
    "minutes_delayed_late_aircraft",
    "minutes_delayed_nas",
    "minutes_delayed_security",
    "minutes_delayed_weather",
    "minutes_delayed_total",
]
# %%
# QUESTION 1

# Which airport has the worst delays? Discuss the metric you chose, and why
# you chose it to determine the “worst” airport. Your answer should include
# a summary table that lists (for each airport) the total number of flights,
# total number of delayed flights, proportion of delayed flights, and
# average delay time in hours.

# get total flights for each airport
flight_totals = flights.groupby("airport_code")["num_of_flights_total"].sum()
print(flight_totals)

# # get total delays for each airport
delay_totals = flights.groupby("airport_code")["num_of_delays_total"].sum()
print(delay_totals)

# %%
# get minutes delay time in hours
delay_totals_minutes = flights.groupby("airport_code")["minutes_delayed_total"].sum()
print(delay_totals_minutes)
delay_totals_hours = delay_totals_minutes / 60
print(delay_totals_hours)

# %%
# get a

delay_proportion = (delay_totals * 100) / flight_totals
# create data frame with the information about delays
worst_df = pd.DataFrame(
    {
        "Airport Code": flight_totals.index,
        "Total Flights": flight_totals.values,
        "Total Delays": delay_totals.values,
        "Delay proportion": delay_proportion,
    }
)

# chart = (
#     (alt.Chart(worst_df))
#     .encode(x=alt.X("Total Delays"), y=alt.Y("Total Flights"))
#     .mark_bar()
# )

# chart

# %%
# QUESTION 2

# What is the best month to fly if you want to avoid delays of any length?
# Discuss the metric you chose and why you chose it to calculate your answer.
# Include one chart to help support your answer, with the x-axis ordered by month.
# (To answer this question, you will need to remove any rows that are missing
#  the Month variable.)

# QUESTION 3

# According to the BTS website, the “Weather” category only accounts for severe
# weather delays. Mild weather delays are not counted in the “Weather” category,
# but are actually included in both the “NAS” and “Late-Arriving Aircraft” categories.
# Your job is to create a new column that calculates the total number of flights
# delayed by weather (both severe and mild). You will need to replace all the
# missing values in the Late Aircraft variable with the mean. Show your work
# by printing the first 5 rows of data in a table. Use these three rules for
# your calculations:__

#     100% of delayed flights in the Weather category are due to weather
#     30% of all delayed flights in the Late-Arriving category are due to weather.
#     From April to August, 40% of delayed flights in the NAS category are due to weather. The rest of the months, the proportion rises to 65%.

#  QUESTION 4

# Using the new weather variable calculated above, create a barplot showing the
# proportion of all flights that are delayed by weather at each airport. Discuss
# what you learn from this graph.

# QUESTION 5

# Fix all of the varied missing data types in the data to be consistent (all missing
# values should be displayed as “NaN”). In your report include one record example
# (one row) from your new data, in the raw JSON format. Your example should display
# the “NaN” for at least one missing value.__
