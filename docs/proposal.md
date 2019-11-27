# Supermarket Sales Dashboard: Proposal

Authors: Reiko Okamoto, Monique Wong and Haoyu Su

Date: November 23, 2019

## 1. Motivation and purpose
Managers of supermarkets can influence the profitability of their supermarket in a number of ways. One of the decisions that they have to make on a weekly basis is how to staff their stores. Optimal staffing levels refers to not overstaffing in periods of time of low customer traffic and not understaffing when there is a possibility of high customer traffic. Deciding how many staff to have working at a given point in time should consider not only customer traffic but also how much customers spend and how satisfied customers are during those periods. A manager may choose to staff less in times of low spending or when customers are already highly satisfied with their shopping experience. 

We propose to build a dashboard that allows a manager to visualize historical data on customer traffic, average spend and customer satisfaction on different days of the week and times of the day. In order to determine which department to staff, we will also build functionality to allow managers to view traffic, spend and satisfaction data by department. 

## 2. Description of the data
We have quarterly sales data of three branches of a supermarket chain located in three cities in Myanmar. The dataset contains 1000 customer purchase records with 17 variables. The variables of interest in our project are the following: the identification number of each successful transaction (`Invoice ID`), the the location of the transaction (`City`, `Branch`), the date and time of purchase (`Date`, `Time`), the number of goods purchased by a customer (`Quantity`), the transaction total (`Total`), the type of goods purchased (`Product line`) and the customer satisfaction score on the overall shopping experience (`Rating`).

## 3. Research questions and usage scenarios
The overarching research question we are interested in is:
> For which days of the week, time of day and departments can staffing be improved?

We imagine our dashboard being used by regional and store managers of the supermarkets. We will use Michael as an example below.

Michael Scott is responsible for operating three large supermarkets in three different cities. One of his most important responsibilities is staffing. He is determined to schedule his employees effectively in order to maximize profit and customer satisfaction. Michael leads a busy life so he's looking for a solution that'll allow him to easily explore historical data on total sales, number of transactions, average spend, average customer satisfaction and product lines (departments). When Michael opens the supermarket staffing dashboard, he'll select the store of interest and see four figures. This first row consists of four heat maps showing total sales, number of transactions, average spend and customer satisfaction on different days of the week and times of day. Using these heat maps, Michael can gain insight into which day of the week and/or time of day requires staffing recoordination. 

Let's consider three situations of interest.

| Scenario | Total sales | # of transactions | Avg. transaction size| Avg. customer satisfaction |
|:-:|:-:|:-:|:-:|:-:|
| 1 | High | High | High | High |
| 2 | Low  | High | Low  | Low  |
| 3 | High | High | High | Low  |

*Scenario 1*

Looking at the heat maps, Michael discovers that on Monday evenings, the number of transactions, average transaction size and average customer satisfaction are all *high*. This is good news! Nothing needs to be changed here because the store is performing optimally: the stores have healthy customer traffic, customers are making large purchases and they are pleased with their shopping experience.

*Scenario 2*

Michael discovers that on Saturday mornings, the number of transactions is *high*, the average spend is *low* and the average customer satisfaction is *low*. Although the subpar customer satisfaction may indicate that staffing levels need to be tweaked for future Saturday mornings, he looks to the total sales data for confirmation before making his decision. Since total sales on Saturday mornings are not significant, he decides that it's not worth scheduling in more staff during that time.

*Scenario 3*

Using the dashboard, Michael discovers that on Friday afternoons, the total sales are *high* but the average customer satisfaction is *low*. This presents an interesting case. Michael decides that the store needs more staff in order to improve the level of customer satisfaction. In order to decide which department could benefit from extra help, he uses the drop-down menu to select the day and time of interest (i.e. 'Friday' and 'afternoon'). After making his selection, Michael will see four barplots showing total sales, number of transactions, average transaction size and average customer satisfaction for each department. He observes that many transactions were performed in the home and lifestyle department during this time (i.e. this department experienced high customer traffic during this period). He suspects that although many customers are purchasing goods in this department, they may not be receiving the help they want from the staff or the department may not be sufficiently stocked or cleaned to their standards. Therefore, Michael decides to schedule more people in the home and lifestyle department on Friday afternoons in an attempt to increase customer satisfaction. He hopes that improved shopping experiences can contribute to customer retention, and in the long run, customer loyalty will bring in more revenue.
