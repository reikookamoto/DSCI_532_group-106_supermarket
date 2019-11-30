# Reflection

Authors: Reiko Okamoto, Monique Wong and Haoyu Su

Date: November 30, 2019

## What our dashboard does well
Our Supermarket Staffing dashboard was designed to solve a real issue that supermarket managers face and our implementation of the dashboard sufficiently meets the need. 

Specifically, our dashboard:

* **is purpose-driven**: We are helping a manager answer how to adjust the staffing levels in their store by department, by day of week and time of day based on past trends.
* **is appropriately sequenced for decision making**: Overall store performance by the day of week and time of day is presented first before managers decide which time frames to focus on in their department-specific analysis. 
* **is appropriately interactive**: We limited the options that a user could choose when exploring the data to what we believe is most useful in the context of the decision. For example, we picked the store, day of week, time of day and department as options since store associates are staffed in shifts by department in each store.
* **is simple to understand**: We purposely used simple to interpret charts such as heat maps and bar charts so that the focus is on analysis and decision-making instead of learning how to read the visualization. We also picked simple color schemes that don't distract from interpretation. Colors were only used if they provide meaning (e.g., on the heatmaps). Axis labels have been chosen to improve interpretability.

## Limitations and future improvements
While our dashboard is a sufficient minimum viable product, it has its limitations. The limitations and potential future improvements we have identified are:

* Stores are selected with radio buttons instead of tabs.
  * Using tabs to represent different stores would have been more interpretable since it would imply that the entire dashboard is specific to the store. 
* Summary data of all weeks are displayed instead of allowing users to select the week they want to see.
  * A supermarket manager may want to see store performance data for a specific week or subset of weeks instead of all historical data to make their decision. This may be a useful functionality if our manager was staffing for Black Friday weekend and wants to see store performance details in previous holiday weekends.
  * Adding this functionality would involve adding a slider at the top of the dashboard that enables users to select the weeks for which they want to see the visualizations on the dashboard.
* Performance visualizations by department show data for only one time slot at a time.
  * A supermarket manager may want to compare department-specific performance across 2 or 3 different time slots to determine staffing, especially if there are limited staff available to work. A manager would have to compare between multiple time slots to prioritize which times and departments to staff first.
  * We can build this functionality by repeating the department-specific visualizations (i.e., the bar charts) 2 or 3 times to allow the user to select different time slots to compare side by side.
* Days of the week and time of day are selected separately and combinations of choices are not possible.
  * A supermarket manager may be interested in staffing not only 4 hour shifts but 8 hour shifts which would require analyzing the data by "Morning" and "Afternoon" or "Afternoon" and "Evening".
  * A supermarket manager may also be interested in seeing performance separated by weekend and weekdays which would require selecting multiple days of the week.
  * Implementing this functionality would require changing the drop down selector to a checkbox selector so that users can select multiple days of the week and/or times of the day in the analysis.
* Without prior staffing data, it is difficult to understand what impact past staffing decisions had on performance and where we may have overstaffed in the past.
  * Solving this limitation would require access to past staffing data so that we can compare staffing levels to performance to make more informed staffing decisions

## Responding to GitHub issues
* Work distribution: This week, work was split up as follows:
- Initial charts on Jupyter notebook: Reiko and Monique
- Implementing app.py without interactivity: Reiko
- Adding store selection interactivity: Monique
- Department-specific interactivity: Haoyu (Clara)
- Deployment: everyone during lab
- Reflection: Monique
