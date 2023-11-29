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
flights

# %%
# check for missing values
flights.isna()

# %%
# count n/a values in each column
missing_count = flights.isna().sum()
missing_count

# %%
# count empty string value in each column
empty_count = (flights == "").sum()
print(empty_count)

# %%
# ***clean airport_name column******
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
# ***clean month column******
flights["month"].value_counts()
# replace all n/a values with NA
flights["month"] = flights["month"].replace("n/a", pd.NA)
# check for missing values
flights["month"].isna().value_counts()
# The "ffill" method fills in missing values by forward-filling, which means
# that it uses the last known value to fill in subsequent missing values.
flights["month"].fillna(method="ffill", inplace=True)

# %%
# *****clean year column******
flights["year"].fillna(method="ffill", inplace=True)

# %%
# *****clean num_of_delays_carrier column******
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
# *****clean num_of_delays_late_aircraft column******
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
# *****clean minutes_delayed_Carrier column******
flights["minutes_delayed_carrier"].value_counts()
min_delayed_carrier_mean = round(flights["minutes_delayed_carrier"].mean())
flights["minutes_delayed_carrier"].fillna(min_delayed_carrier_mean, inplace=True)


# %%
# *****clean minutes_delayed_nas column******
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
# QUESTION 1

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
        "AirportCode": flight_totals.index,
        "TotalFlights": flight_totals,
        "TotalDelays": delayed_totals,
        "DelayProportion": delayed_proportion,
        "DelayTime(Hours)": delay_totals_hours,
    }
)

worst_df = worst_df.sort_values(by="DelayTime(Hours)", ascending=False)

# print(worst_df)

# %%
# QUESTION 2

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

chart = (
    alt.Chart(flights_month)
    .mark_point()
    .encode(
        y=alt.Y(
            "minutes_delayed_total:Q",
            title="Average Minutes",
            scale=alt.Scale(domain=[(min_delay - 15000), (max_delay + 15000)]),
        ),
        x=alt.X("month:N", title="Month"),
    )
    .properties(title="Average time (minutes) by month")
)

chart
# %%
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
weather_100 = flights["num_of_delays_weather"]
#     30% of all delayed flights in the Late-Arriving category are due to weather.
weather_30 = flights["num_of_delays_late_aircraft"].sample(frac=0.3)
#     From April to August, 40% of delayed flights in the NAS category are due to weather.
#     The rest of the months, the proportion rises to 65%.
months_40 = ["April", "May", "June", "July", "August"]
months_65 = [
    "January",
    "February",
    "March",
    "September",
    "October",
    "November",
    "December",
]
df_40 = flights.query(f"month in @months_40")
weather_40 = df_40["num_of_delays_nas"].sample(frac=0.4)

df_65 = flights.query(f"month in @months_65")
weather_65 = df_65["num_of_delays_nas"].sample(frac=0.65)

print(flights)
# %%
#  QUESTION 4

# Using the new weather variable calculated above, create a barplot showing the
# proportion of all flights that are delayed by weather at each airport. Discuss
# what you learn from this graph.

# %%
# QUESTION 5

# Fix all of the varied missing data types in the data to be consistent (all missing
# values should be displayed as “NaN”). In your report include one record example
# (one row) from your new data, in the raw JSON format. Your example should display
# the “NaN” for at least one missing value.__
