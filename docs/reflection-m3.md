# Reflection for Milestone 3

Authors: Reiko Okamoto, Monique Wong and Haoyu Su

Date: December 7, 2019

## What our dashboard does well
Our Supermarket Staffing dashboard was designed to solve a real issue that supermarket managers face and our implementation of the dashboard sufficiently meets the need. 

Specifically, our dashboard:

* **is purpose-driven**: We are helping a manager answer how to adjust the staffing levels in their store by department, by day of week and time of day based on past trends.
* **is appropriately sequenced for decision making**: Overall store performance by the day of week and time of day is presented first before managers decide which time frames to focus on in their department-specific analysis. 
* **is appropriately interactive**: We limited the options that a user could choose when exploring the data to what we believe is most useful in the context of the decision. For example, we picked the store, day of week, time of day and department as options since store associates are staffed in shifts by department in each store.
* **is simple to understand**: We purposely used simple to interpret charts such as heat maps and bar charts so that the focus is on analysis and decision-making instead of learning how to read the visualization. We also picked simple color schemes that don't distract from interpretation. Colors were only used if they provide meaning (e.g., on the heatmaps). Axis labels have been chosen to improve interpretability.

  
## User feedback

We obtained user feedback from 3 of our MDS peers, prior to and post a walk-through of the dashboard. Being able to watch an unguided experience of the dashboard was the most informative since the user was not influenced by the explanations and justifications of our design. The feedback we received had several common elements:

- **Lack of user instruction and context setting:** Our minimalist dashboard without text instructions left the user wondering what the purpose of the dashboard is and what types of questions they could answer or decisions they could make with our dashboard. In particular, the user desired more information about the dataset itself such as how morning, afternoon and evening were defined and where the dataset came from. 
- **Chart labels are unclear:** Without context, it was unclear that MMK is the currency or that "average satisfaction" represented average customer satisfaction. 
- **Aesthetics did not suggest how we expect the user to interact with the dashboard:** Our chocie of interactivity tools were not ideal for guiding interaction and allowing the user to extract insights from the dashboard. For example, our summary and by department charts required the user to scroll excessively while interacting with the dashboard. The dropdown bars spanned across the page, taking up more screen real estate than necessary. Our tooltip included too much information and was too big preventing the user from seeing the chart in the presence of the tooltip.
- **The scale of our plots changed with interactivity, preventing useful comparison across different store and timeslot selections:** As each plot loaded with different store or day of week / time of day selections, the colour scale (heat map) and y-axis scale (bar plots) updated to the unique values of the filtered selection. While this allows the user to compare the values within the selection (charts are normalized to scale every time), it limits the ability for users to compare between selections. For instance with the heat maps, a dark green in total sales of one store is not equivalent to a dark green in the total sales of another store but not fixing the color scale allows for the maximum variance in color when the user is looking at one store alone. 

We also heard feedback that we are finding difficult to address or does not make sense for our use case:
- **Desire for additional summary data by store:** Within the confines of our dataset, we have identified the metrics that would be most useful for staffing a supermarket. Data such as whether customers were members or not or their payment type would have been much less useful and therefore not included in our dashboard. In the spirit of keeping our dashboard purpose-driven, we are valuing this feedback less. 
- **Desire to select multiple stores to see average between stores:** We do not believe this is functionality that would be useful for our use case since staffing happens by store. We have also deprioritized this suggestion. 

We believe the feedback we received has helped us identify improvements that we weren't aware were needed (e.g., axis labels) and prioritize those that were most needed (e.g., adding instructions). The feedback that was most valuable were the comments that took into account the use case of the dashboard. This required the test user to be in the mindset of our target user - a store manager - instead of a data analyst / scientist. 

## Improvements we have implemented

Based on the above user feedback, we compiled a wish list of improvements we would like to see:

- **Add user instruction and context** to better orient users to our dashboard; we will add an introduction as well as guiding questions and examples where appropriate
- **Change confusing chart labels** to better describe the data that is being shown; we will rename unclear chart titles and axes labels
- **Improve aesthetics** to limit user scrolling, make better use of screen space and ensure charts aren't obfuscated by tooltips; we will do this by moving our by department charts to a second tab, reducing the size of the drop down menus so that two will fit on one row and removing information from our tooltip to reduce the size of the tooltip

We did not implement changes that addressed the changing scales of our plots. The intent of our dashboard is not to compare between different stores since our use case (staffing a supermarket) does not require this analysis - staff are usually unique to each store. While being able to compare between different day of week and time of day selections with a store has merit, we prioritized adding functionality to make that possible. We did this by adding an extra row of bar plots where the user can select a different day of week and time of day for comparison. We deprioritized fixing the scale due to the higher difficulty of fixing two sets of charts to a scale that allowed both to be interpretable yet comparable. 

In general, our prioritization strategy was to implement improvements that most significantly improved the user experience with the least effort first. We deprioritized features that were difficult to achieve technically and features where we did not hear explicit user feedback on. 
  
## Limitations and future improvements, including wish-list features

While our dashboard is a sufficient minimum viable product, it has its limitations. The limitations and potential future improvements we have identified are:

* Summary data of all weeks are displayed instead of allowing users to select the week they want to see.
  * A supermarket manager may want to see store performance data for a specific week or subset of weeks instead of all historical data to make their decision. This may be a useful functionality if our manager was staffing for Black Friday weekend and wants to see store performance details in previous holiday weekends.
  * Adding this functionality would involve adding a slider at the top of the dashboard that enables users to select the weeks for which they want to see the visualizations on the dashboard.
* Days of the week and time of day are selected separately and combinations of choices are not possible.
  * A supermarket manager may be interested in staffing not only 4 hour shifts but 8 hour shifts which would require analyzing the data by "Morning" and "Afternoon" or "Afternoon" and "Evening".
  * A supermarket manager may also be interested in seeing performance separated by weekend and weekdays which would require selecting multiple days of the week.
  * Implementing this functionality would require changing the drop down selector to a checkbox selector so that users can select multiple days of the week and/or times of the day in the analysis.
* Without prior staffing data, it is difficult to understand what impact past staffing decisions had on performance and where we may have overstaffed in the past.
  * Solving this limitation would require access to past staffing data so that we can compare staffing levels to performance to make more informed staffing decisions
