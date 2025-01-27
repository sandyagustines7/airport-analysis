**LGA vs EWR Delay Patterns: Comparative Analysis**

**Project Description**

This project aims to provide an in-depth analysis of departure delays between LaGuardia and Newark International airports. Through exploratory data analysis, machine learning modeling on Python, and interactive visualizations on Tableau, I identify significant causes of delays, peak traffic periods and compare airport performance across specific flight delay metrics. The ultimate goal is to provide tangible recommendations to the underperforming airport to improve on-the-ground operations and reduce total departure delays.

**Data Source:**

- Airline Delay and Cancellation Data, 2009-2018: https://www.kaggle.com/datasets/yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018/data

This dataset contains US domestic airline delay and cancellations from 2009-2018, including estimated and scheduled departure and arrival times, total delays in minutes and reasons for delay / cancellation. 

**Research Questions**

These research questions were created to drive the project and help us better understand individual airport operational performance: 

1. What are significant causes for delays across both airports?
2. How do peak travel times impact departure delays across both airports?
3. Which airport experiences less delays and why?
4. How can these insights be used to optimize on-time performance during non-peak and peak hours?

**Data Cleaning and Feature Engineering Procedure:**

To prepare the data for analysis, the data was thoroughly cleaned and feature engineered: 
- Removing inconsistent and null values.
- Normalizing time stamps to create consistent time formats (DATETIME).
- Filtering out cancelled and diverted flights - focusing on delays only.
- Extracted departure hours and encoded peak travel times (7am-9am, 4pm-7pm).
- Extracted days of the week, months and created weekend indicators in binary (1 = Weekend, 0 = Weekday).
- Creating delay categories to assess delay severity.

**Results**

The results of the analysis have been synthesized into an interactive dashboard on Tableau public, providing a user-friendly interface for exploring my findings. The dashboard allows viewers to toggle between airports at different time periods (daily, monthly and yearly), showcasing metrics like average departure / arrival delays and delay rates.

View the interactive dashboards [here](https://public.tableau.com/views/LGAandEWRDelayStatistics2014-2018ChartsDashboards/DelayProportions?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) and [here](https://public.tableau.com/views/DepartureandArrivalStatistics-LGAandEWR/DepartureandArrivalStats?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link). 
