import csv
import datetime
from customer_order_cohort import customer_time_span_cohorts as ctsc


class OrderTimeSpanAggregation:
    """
    Class tracking orders by customer cohort, and aggregating order count by time span.
    Time span are offset from customer cohort interval: recent date plus number of days from order created
    """

    def __init__(self, path_csv_file: str = './data/orders.csv', customer_cohorts: ctsc.CustomerTimeSpanCohorts = None):
        self.customer_group_to_order_accumulated: dict = {}  # SHOULDDO: defaultdict of array?
        self.path_csv_file = path_csv_file
        self.customer_cohorts = customer_cohorts

    def read_orders_csv_file(self) -> int:
        """
        Open the csv file and iterate over its entries to aggregate orders by day intervals
        :returns the total number of customer groups"""

        # same pattern as CustomerTimeSpanCohorts.read_customers_csv_file to get an iterator
        with open(self.path_csv_file, mode='r') as csv_file:
            entry_reader = csv.reader(csv_file)  # use csv.DictReader instead?
            header = next(entry_reader)  # skip header
            # order ID, customer ID, order date, num order by customer
            self.read_all_order_entries(entry_reader, 0, 2, 3, 1)
        return len(self.customer_cohorts.cohort_cardinality)

    def read_all_order_entries(self, entry_reader, order_id_index: int, customer_id_index: int,
                               order_created_index: int, order_sequence_index: int):
        """
        Extract order data for each order entry, and pass it to be filtered and grouped
        :param entry_reader: all entries
        :param order_id_index: index in entry to read order ID; not currently used
        :param customer_id_index: index in entry to read related customer ID
        :param order_created_index: index in entry to read order creation date, string on GMT time zone
        :param order_sequence_index: index in entry to read sequence number of order by customer ID
        :return: number of customer groups
        """

        for entry in entry_reader:
            self.track_order(entry[customer_id_index], entry[order_created_index], entry[order_sequence_index])
        return len(self.customer_cohorts.cohort_cardinality)

    def track_order(self, customer_id: str, order_creation_date: str, order_sequence: str):
        """
        Find matching customer time-span-group by customer_id from customer_time_span_cohorts.
        If there is a match compute matching order time slot index from order creation date
        and aggregate order data for this time slot for this customer time-span-group
        :param customer_id: customer ID that placed the order
        :param order_creation_date: when the order was placed
        :param order_sequence: number of order the customer made (1 indexed)
        :return: array of order counts matching customer cohort and order time slot if withing time range of analysis
        """

        if customer_id is None or customer_id not in self.customer_cohorts.customers_and_matching_cohort:
            return None
        order_created = self.customer_cohorts.convert_date_in_range(order_creation_date)
        if order_created is None:
            return None
        # aggregate order data, simple count increment
        count_and_first_count: [] = self.get_counts_for_date(customer_id, order_created)
        count_and_first_count[0] += 1
        if order_sequence == '1':
            count_and_first_count[1] += 1
        return count_and_first_count

    def get_counts_for_date(self, customer_id: str, order_created: datetime.datetime):
        customer_cohort_key: str = self.customer_cohorts.customers_and_matching_cohort[customer_id][0]
        if customer_cohort_key not in self.customer_group_to_order_accumulated:
            # init time slot with 0 order and 0 first time order
            # we could always init with self.customer_cohorts.number_of_intervals array length ...
            cohort_intervals_delta: datetime.timedelta = \
                self.customer_cohorts.recent_date - self.customer_cohorts.customers_and_matching_cohort[customer_id][1]
            cohort_intervals: int = cohort_intervals_delta.days // self.customer_cohorts.days_interval_length
            self.customer_group_to_order_accumulated[customer_cohort_key] =\
                [[0,0] for i in range(cohort_intervals)]
        time_slot_delta: datetime.timedelta = self.customer_cohorts.recent_date - order_created
        time_slot_index: int = time_slot_delta.days // self.customer_cohorts.days_interval_length
        return self.customer_group_to_order_accumulated[customer_cohort_key][time_slot_index]

