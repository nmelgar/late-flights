# %%
# import the usual libraries
import pandas as pd
import altair as alt
import numpy as np
from scipy import stats

# %%
# url to data
flights_url = "https://raw.githubusercontent.com/byuidatascience/data4missing/master/data-raw/flights_missing/flights_missing.json"

# %%
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
# %%
# replace all n/a values with NA
flights["month"] = flights["month"].replace("n/a", pd.NA)
# %%
# check for missing values
flights["month"].isna().value_counts()
# %%
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
delays_subset.value_counts()
# %%
# *****clean num_of_delays_late_aircraft column******


# %%
# *****clean minutes_delayed_Carrier column******


# %%
# *****clean minutes_delayed_nas column******
