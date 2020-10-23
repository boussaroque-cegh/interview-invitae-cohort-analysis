from customer_order_cohort import customer_time_span_cohorts as ctsc, order_time_span_aggregation as otsa
import datetime

if __name__ == '__main__':
    customers_cohorts = ctsc.CustomerTimeSpanCohorts(recent_date=datetime.datetime(2015, 7, 7, 23, 00, 00))
    customers_cohorts.read_customers_csv_file()
    orders_by_time_slot: otsa = otsa.OrderTimeSpanAggregation(customer_cohorts=customers_cohorts)
    orders_by_time_slot.read_orders_csv_file()
    orders_by_time_slot.write_orders_count_by_cohorts_csv_file('./ordercounts.csv')
