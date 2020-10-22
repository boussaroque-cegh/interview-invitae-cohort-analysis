import datetime as dtm
from collections import defaultdict
import csv


class CustomerTimeSpanCohorts:
    """
    Class collecting input data for customers cohort analysis
    """

    # format use for date string representation in input data
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    # from dateutil.parser import parse ??instead / also??

    def __init__(self, path_csv_file: str = './data/customers.csv', recent_date: dtm.datetime = dtm.datetime.now(),
                 days_interval_length: int = 7, number_of_intervals: int = 8):
        self.customers_and_matching_cohort: dict = defaultdict(tuple)
        self.cohort_cardinality: dict = defaultdict(int)
        self.path_csv_file: str = path_csv_file
        self.days_interval_length: int = days_interval_length
        # try to use tzinfo but not sure it is useful. No default implementation. Should import pytz maybe
        self.delta_time_zone: dtm.timedelta = recent_date.utcoffset() # delta with GMT time
        if self.delta_time_zone is None:
            self.delta_time_zone = dtm.datetime.now() - dtm.datetime.utcnow()  # default to local offset
            # rounding to the second, seems test failure on github with 3 or 4 microseconds diff
            self.delta_time_zone = dtm.timedelta(days=self.delta_time_zone.days,
                                             seconds=self.delta_time_zone.seconds + int(
                                                 round(self.delta_time_zone.microseconds / 10 ** 6)),
                                             microseconds=0)
            #  if recent_date.dstzinfo.dst() if recent_date.tzinfo is not None else datetime.timezone.utc
        self.recent_date = self.rounded_to_hour_zero(recent_date) + dtm.timedelta(days=1)  # midnight the next day
        self.recent_date_included = self.recent_date - dtm.timedelta(seconds=1) # almost midnight on most recent date
        self.number_of_intervals = number_of_intervals
        self.oldest_date = self.recent_date - dtm.timedelta(days=days_interval_length*number_of_intervals)

    @staticmethod
    def parse_date(date_representation: str) -> dtm.datetime:
        """
        :returns datetime instance from its string representation.
        Ignore None or mal formatted string.
        Assume resulting date is on GMT timezone
        """

        try:
            return None if date_representation is None else dtm.datetime.strptime(
                date_representation, CustomerTimeSpanCohorts.DATE_FORMAT)
        except ValueError:
            return None
        # or parse(date_representation)

    def convert_date_in_range(self, date_created_representation: str) -> dtm.datetime:
        """
        :returns datetime instance from its string representation, IF string representation looks valid
        and IF the date is with the overall study date range.
        """

        date_created = self.parse_date(date_created_representation)
        if date_created is not None:  # put in same time zone as self.recent_date
            date_created = date_created + self.delta_time_zone
        return date_created if date_created is not None \
                               and self.oldest_date <= date_created < self.recent_date else None

    @staticmethod
    def rounded_to_hour_zero(full_date_and_time: dtm.datetime) -> dtm.datetime:
        """Helper function to set to zero hours, minutes, seconds on a given datetime.
        similar to rounding datetime to its date only but keep datetime class
        :param full_date_and_time: date time, with any time between 00:00:00 and 23:59:59
        :returns datet time for same day at 00:00:00"""

        return dtm.datetime(full_date_and_time.year, full_date_and_time.month, full_date_and_time.day, 0, 0, 0)

    def build_unique_cohort_id(self, creation_date: dtm.datetime) -> tuple:
        """
        Create a string matching the cohort identifier for an input date.
        The given date should be within the study date range.
        Based the number of days per interval, and the end date of the analysis,
        compute the upper and lower date range for the given date.
        :param creation_date: date time value when customer entry was created
        :returns the cohort identifier with the oldest and most recent date of the matching interval"""

        rounded_down: dtm.datetime = self.rounded_to_hour_zero(creation_date)
        from_recent: dtm.timedelta = self.recent_date_included - creation_date
        days_from_recent: int = from_recent.days
        cohort_recent_date_included: dtm.datetime = rounded_down + dtm.timedelta(
            days=(days_from_recent % self.days_interval_length))
        cohort_recent_date: dtm.datetime = cohort_recent_date_included + dtm.timedelta(days=1)
        cohort_oldest_date: dtm.datetime = cohort_recent_date - dtm.timedelta(days=self.days_interval_length)
        return cohort_oldest_date.strftime('%Y/%m/%d') + '-' +\
            cohort_recent_date_included.strftime('%Y/%m/%d'), cohort_oldest_date, cohort_recent_date

    def track_customer(self, customer_id: str, customer_creation_date: str) -> str:
        """
        Check that the customer ID and its creation date are valid for this cohort analysis.
        If they are, remember them for later use in the class dictionaries.
        :param customer_id: a unique customer ID
        :param customer_creation_date: when the customer entry was created in the input data set
        :returns the cohort identifier linked by the given customer ID, based on its creation date"""

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

    def read_all_customer_entries(self, iterator, index_for_id: int, index_for_created: int) ->int:
        """
        Reads each input entry and record its customer cohort
        :param iterator: the iterator to get all entries, full scan. ??Don't know how to specify iterator type??
        :param index_for_id: index on entry to get customer ID value
        :param index_for_created: index on entry to get customer created date value
        :returns the total number of costumer groups recorded from all entries, matching date range for this analysis
        """

        for entry in iterator:
            self.track_customer(entry[index_for_id], entry[index_for_created])
        return len(self.cohort_cardinality)

    def read_customers_csv_file(self) -> int:
        """
        Open the csv file and iterate over its entries to build customer cohorts.
        :returns the total number of customer groups from all entries of the csv file
        in the date range of the analysis"""

        with open(self.path_csv_file, mode='r') as csv_file:
            entry_reader = csv.reader(csv_file)  # use csv.DictReader instead?
            header = next(entry_reader)  # skip header
            self.read_all_customer_entries(entry_reader, 0, 1)
        return len(self.cohort_cardinality)