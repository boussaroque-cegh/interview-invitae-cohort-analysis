from customer_order_cohort import customer_time_span_cohorts as ctsc, order_time_span_aggregation as otsa
import datetime
import sys

if __name__ == '__main__':
    if sys.version_info.major < 3 or sys.version_info.minor < 6:
        print('Python 3.6 or higher is required. Currently running Python {}.{}'.
              format(sys.version_info.major, sys.version_info.minor))
        sys.exit(1)
    customers_cohorts = ctsc.CustomerTimeSpanCohorts(recent_date=datetime.datetime(2015, 7, 7, 23, 00, 00))
    customers_cohorts.read_customers_csv_file(path_csv_file='./data/customers.csv')  # or with .1of3 .2of3 .3of3
    orders_by_time_slot: otsa = otsa.OrderTimeSpanAggregation(customer_cohorts=customers_cohorts)
    orders_by_time_slot.read_orders_csv_file(path_csv_file='./data/orders.csv')  # or with .2of2 .1of2
    orders_by_time_slot.write_orders_count_by_cohorts_csv_file('./ordercounts.csv')
