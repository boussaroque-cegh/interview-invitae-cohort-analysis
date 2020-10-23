# interview-invitae-cohort-analysis
 Implementation of cohort analysis for customer data available from https://github.com/invitae/cohort-analysis-assignment

 ## Speedy-quick
 
 Get all files, load them in your IDE and run main.py. You should get the same file as 'ordercounts.csv'
 
 ## Note to interviewers
 
 I am not fluent in Python or GitHub. I can read and understand code and configurations, but I usually play in other sandboxes.
 My intention is to build a fairly good quality project while still doing my day to day work.
 
 ## Dependencies and build steps
 
 This project uses Python, with version 3.6 or above. GitHub actions has been added for test and code conformance (lint).
 
 For anyone cloning, copying, this project you should also run test and code check before commiting changes.
 
    python -m venv .env
    python -m pip install --upgrade pip
    pip install flake8 pytest
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    pytest ./test_main.py

 ## Specifications.

 Provide implementation to read customer data and order data from csv file. Transform the data to group customers by their creation date. Create cohorts of customer for creation date interval of a week (7 days). Track orders per customer cohort and date of order, also aggregated on weekly intervals. The output will be a csv file. Each line will have the customer cohort identifier, the number of customer per cohort, and total number of orders per time interval with total number of first oder on same time interval.

 ## Assumptions.

* The number of days to group customer and order are equal.
* The input data is currently not sorted. A full scan of customer and order data will be performed.
* The customer and order data will be filtered using a large time interval: most recent date down to most recent date minus number of week.

