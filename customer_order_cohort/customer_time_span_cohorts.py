import datetime
from collections import defaultdict
# from dateutil.parser import parse ??instead??
import csv


class CustomerTimeSpanCohorts:
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, path_csv_file: str = '../data/customers.csv', recent_date: datetime = datetime.datetime.now(),
                 days_interval_length: int = 7, number_of_intervals: int = 13):
        self.customers_and_matching_cohort = defaultdict(tuple)
        self.cohort_cardinality = defaultdict(int)
        self.path_csv_file = path_csv_file
        self.days_interval_length = days_interval_length
        self.recent_date = self.rounded_to_hour_zero(recent_date) + datetime.timedelta(days=1)
        self.recent_date_included = self.recent_date - datetime.timedelta(seconds=1)
        self.number_of_intervals = number_of_intervals
        self.oldest_date = self.recent_date - datetime.timedelta(days=days_interval_length*number_of_intervals)

    @staticmethod
    def parse_date(date_representation: str):
        try:
            return None if date_representation is None else datetime.datetime.strptime(
                date_representation, CustomerTimeSpanCohorts.DATE_FORMAT)
        except ValueError:
            return None
        # or parse(date_representation)

    def convert_date_in_range(self, date_created_representation: str):
        date_created = self.parse_date(date_created_representation)
        return date_created if date_created is not None \
                               and self.oldest_date <= date_created < self.recent_date else None

    @staticmethod
    def rounded_to_hour_zero(full_date_and_time: datetime):
        return datetime.datetime(full_date_and_time.year, full_date_and_time.month, full_date_and_time.day, 0, 0, 0)

    def build_unique_cohort_id(self, creation_date: datetime):
        rounded_down: datetime = self.rounded_to_hour_zero(creation_date)
        from_recent: datetime = self.recent_date_included - creation_date
        days_from_recent: int = from_recent.days
        cohort_recent_date_included: datetime = rounded_down + datetime.timedelta(
            days=(days_from_recent % self.days_interval_length))
        cohort_recent_date: datetime = cohort_recent_date_included + datetime.timedelta(days=1)
        cohort_oldest_date: datetime = cohort_recent_date - datetime.timedelta(days=self.days_interval_length)
        return cohort_oldest_date.strftime('%Y/%m/%d') + '-' +\
               cohort_recent_date_included.strftime('%Y/%m/%d'), cohort_oldest_date, cohort_recent_date

    def track_customer(self, customer_id: str, customer_creation_date: str):
        if customer_id is None:
            return None
        if customer_id in self.customers_and_matching_cohort:
            return None  # raise invalid input exception ?
        creation_date = self.convert_date_in_range(customer_creation_date)
        if creation_date is None:
            return None
        cohort_id, start_date_included, end_date_excluded = self.build_unique_cohort_id(creation_date)
        self.customers_and_matching_cohort[customer_id] = (cohort_id, start_date_included, end_date_excluded)
        self.cohort_cardinality[cohort_id] += 1
        return cohort_id

    def read_all_customer_entries(self, iterator, index_for_id, index_for_created):
        for entry in iterator:
            self.track_customer(entry[index_for_id], entry[index_for_created])

    def read_customers_csv_file(self):
        with open(self.path_csv_file, mode='r') as csv_file:
            entry_reader = csv.reader(csv_file)  # use csv.DictReader instead?
            header = next(entry_reader)  # skip header
            self.read_all_customer_entries(entry_reader, 0, 1)