# Late flights and missing data (JSON files)
Data Science Programming project to work with missing data and search for insights about flight delays.

## Background

Delayed flights are not something most people look forward to. In the best case scenario you may only wait a few extra minutes for the plane to be cleaned. However, those few minutes can stretch into hours if a mechanical issue is discovered or a storm develops. Arriving hours late may result in you missing a connecting flight, job interview, or your best friend’s wedding. </br>

In 2003 the Bureau of Transportation Statistics (BTS) began collecting data on the causes of delayed flights. The categories they use are Air Carrier, National Aviation System, Weather, Late-Arriving Aircraft, and Security. You can visit the [BTS website](https://www.bts.gov/topics/airlines-and-airports/understanding-reporting-causes-flight-delays-and-cancellations) to read definitions of these categories. </br>

The JSON file for this project contains information on delays at 7 airports over 10 years. Your task is to clean the data, search for insights about flight delays, and communicate your results using the provided template. </br>

## Data

[JSON File](https://github.com/byuidatascience/data4missing/raw/master/data-raw/flights_missing/flights_missing.json)
[Information](https://github.com/byuidatascience/data4missing/blob/master/data.md)

## Questions and Tasks

For Project 1 the answer to each question should include a chart and a written response. The years labels on your charts should not include a comma. At least two of your charts must include reference marks.

- Which airport has the worst delays? Discuss the metric you chose, and why you chose it to determine the “worst” airport. Your answer should include a summary table that lists (for each airport) the total number of flights, total number of delayed flights, proportion of delayed flights, and average delay time in hours.
- What is the best month to fly if you want to avoid delays of any length? Discuss the metric you chose and why you chose it to calculate your answer. Include one chart to help support your answer, with the x-axis ordered by month. (To answer this question, you will need to remove any rows that are missing the Month variable.)
- According to the BTS website, the “Weather” category only accounts for severe weather delays. Mild weather delays are not counted in the “Weather” category, but are actually included in both the “NAS” and “Late-Arriving Aircraft” categories. Your job is to create a new column that calculates the total number of flights delayed by weather (both severe and mild). You will need to replace all the missing values in the Late Aircraft variable with the mean. Show your work by printing the first 5 rows of data in a table. Use these three rules for your calculations:
    + 100% of delayed flights in the Weather category are due to weather
    + 30% of all delayed flights in the Late-Arriving category are due to weather.
    + From April to August, 40% of delayed flights in the NAS category are due to weather. The rest of the months, the proportion rises to 65%.
- Using the new weather variable calculated above, create a barplot showing the proportion of all flights that are delayed by weather at each airport. Discuss what you learn from this graph.
- Fix all of the varied missing data types in the data to be consistent (all missing values should be displayed as “NaN”). In your report include one record example (one row) from your new data, in the raw JSON format. Your example should display the “NaN” for at least one missing value.
