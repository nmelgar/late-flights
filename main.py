# %%
# import the usual libraries
import pandas as pd
import altair as alt
import numpy as np
from scipy import stats

# %%

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
# replace n/a with NaN
# flights.replace('n/a', np.nan, inplace=True)

# %%
# %% remove rows with missing values
# flights = flights.dropna()

# %%
# QUESTION 1

# Which airport has the worst delays? Discuss the metric you chose, and why
# you chose it to determine the “worst” airport. Your answer should include
# a summary table that lists (for each airport) the total number of flights,
# total number of delayed flights, proportion of delayed flights, and
# average delay time in hours.

worst = flights.groupby("airport_code").agg(
    count=("airport_code", "size"),
    minutes=("minutes_delayed_total", np.mean),
    delays=("num_of_delays_total", np.mean),
)

worst_base = alt.Chart(worst).encode(
    x=alt.X("minutes"),
    y=alt.Y("delays"),
    color=alt.Color("airport_code:N"),
)

chart = (
    worst_base.mark_point()
    + worst_base.transform_loess("minutes", "delays").mark_line()
)
chart
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
