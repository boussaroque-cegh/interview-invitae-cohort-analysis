# interview-invitae-cohort-analysis
 Implementation of cohort analysis for customer data available from https://github.com/invitae/cohort-analysis-assignment

 Specifications.

 Provide implementation to read customer data and order data from csv file. Transform the data to group customers by their creation date. Create cohorts of customer for creation date interval of a week (7 days). Track orders per customer cohort and date of order, also aggregated on weekly intervals. The output will be a csv file. Each line will have the customer cohort identifier, the number of customer per cohort, and total number of orders per time interval with total number of first oder on same time interval.

 Assumptions.

The number of days to group customer and order are equal.
The input data is currently not sorted. A full scan of customer and order data will be performed.
The customer and order data will be filtered using a broad time interval: most recent date down to most recent date minus number of week.

