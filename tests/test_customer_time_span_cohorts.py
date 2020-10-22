import datetime
from customer_order_cohort import customer_time_span_cohorts as ctsc


class TestCustomerTimeSpanCohorts:
    def test_date_utc_conversion(self):
        utc_time_zone = datetime.timezone(datetime.timedelta(), name="GMT")
        customers_cohorts = ctsc.CustomerTimeSpanCohorts(path_csv_file='./data/doesNotExist.csv',
                                                         recent_date=datetime.datetime(2017, 7, 7, 23, 47, 13,
                                                                                       tzinfo=utc_time_zone),
                                                         days_interval_length=14, number_of_intervals=3)
        assert customers_cohorts.recent_date == datetime.datetime(2017, 7, 8, 0, 0, 0)
        assert customers_cohorts.oldest_date == datetime.datetime(2017, 5, 27, 0, 0, 0)
        assert customers_cohorts.delta_time_zone.days == 0
        assert customers_cohorts.delta_time_zone.seconds == 0
        assert customers_cohorts.convert_date_in_range(None) is None
        assert customers_cohorts.convert_date_in_range('') is None
        assert customers_cohorts.convert_date_in_range('2017-06-07  22:51:10') == \
               datetime.datetime(2017, 6, 7, 22, 51, 10)
        assert customers_cohorts.convert_date_in_range('2017-07-08  09:51:10') is None
        assert customers_cohorts.convert_date_in_range('2017-04-07  21:21:12') is None

    def test_date_local_conversion(self):
        customers_cohorts = ctsc.CustomerTimeSpanCohorts(path_csv_file='./data/doesNotExist.csv',
                                                         recent_date=datetime.datetime(2017, 7, 7, 23, 47, 13),
                                                         days_interval_length=7, number_of_intervals=6)
        assert customers_cohorts.recent_date == datetime.datetime(2017, 7, 8, 0, 0, 0)
        assert customers_cohorts.oldest_date == datetime.datetime(2017, 5, 27, 0, 0, 0)
        local_delta = datetime.datetime.now() - datetime.datetime.utcnow()
        local_delta = datetime.timedelta(days=local_delta.days,
                                         seconds=local_delta.seconds+int(round(local_delta.microseconds/10**6)),
                                         microseconds=0)
        assert customers_cohorts.delta_time_zone == local_delta
        assert customers_cohorts.convert_date_in_range('2017-06-07  22:51:10') == \
               datetime.datetime(2017, 6, 7, 22, 51, 10) + local_delta
        # more than a day after recent date
        assert customers_cohorts.convert_date_in_range('2017-07-09  09:51:10') is None
        assert customers_cohorts.convert_date_in_range('2017-04-07  21:21:12') is None

    def test_cohort_id(self):
        pst_time_zone = datetime.timezone(datetime.timedelta(days=-1, seconds=61200), name="PST")
        customers_cohorts = ctsc.CustomerTimeSpanCohorts(path_csv_file='./data/doesNotExist.csv',
                                                         recent_date=datetime.datetime(2015, 7, 7, 23, 47, 13,
                                                                                       tzinfo=pst_time_zone))
        assert customers_cohorts.track_customer('qazaq', '2015-07-07  06:21:42') == '2015/07/01-2015/07/07'
        assert customers_cohorts.track_customer('QaZaQ', '2015-07-07  23:59:59') == '2015/07/01-2015/07/07'
        assert customers_cohorts.track_customer('plokijuh', '2015-07-04  02:21:52') == '2015/07/01-2015/07/07'
        assert customers_cohorts.track_customer('plokijuhy', '2015-07-01  13:10:55') == '2015/07/01-2015/07/07'
        # 7 o'clock in the morning, July 1st, at Greenwich should be midnight in San Francisco, still July 1st
        assert customers_cohorts.track_customer('plokijuhyg', '2015-07-01  07:00:00') == '2015/07/01-2015/07/07'
        assert customers_cohorts.track_customer('hujikolp', '2015-05-23  21:08:56') == '2015/05/20-2015/05/26'
        assert customers_cohorts.track_customer('tressert', '2015-03-21  19:43:27') is None  # out of date range
        assert customers_cohorts.track_customer('wassaw', '2015-07-09  00:00:00') is None  # out of date range
        assert customers_cohorts.track_customer('qazaq', '2015-07-06  07:47:27') is None  # customer id already tracked
        assert 'qazaq' in customers_cohorts.customers_and_matching_cohort
        assert customers_cohorts.customers_and_matching_cohort['qazaq'][0] == '2015/07/01-2015/07/07'
        assert customers_cohorts.customers_and_matching_cohort['qazaq'][1] == datetime.datetime(2015, 7, 1, 0, 0, 0)
        assert customers_cohorts.customers_and_matching_cohort['qazaq'][2] == datetime.datetime(2015, 7, 8, 0, 0, 0)
        assert 'plokijuh' in customers_cohorts.customers_and_matching_cohort
        assert customers_cohorts.customers_and_matching_cohort['plokijuh'][0] ==\
               customers_cohorts.customers_and_matching_cohort['qazaq'][0]
        assert 'hujikolp' in customers_cohorts.customers_and_matching_cohort
        assert customers_cohorts.customers_and_matching_cohort['hujikolp'][0] == '2015/05/20-2015/05/26'
        assert 'tressert' not in customers_cohorts.customers_and_matching_cohort
        assert customers_cohorts.cohort_cardinality['2015/07/01-2015/07/07'] == 5
        assert customers_cohorts.cohort_cardinality['2015/05/20-2015/05/26'] == 1
        assert len(customers_cohorts.customers_and_matching_cohort) == 6
        assert len(customers_cohorts.cohort_cardinality) == 2

    def test_utc_full_customer_file(self):
        utc_time_zone = datetime.timezone(datetime.timedelta(), name="GMT")
        customers_cohorts = ctsc.CustomerTimeSpanCohorts(recent_date=datetime.datetime(2015, 7, 7, 23, 47, 13,
                                                                                       tzinfo=utc_time_zone),
                                                         number_of_intervals=13)
        customers_cohorts.read_customers_csv_file()
        assert customers_cohorts.oldest_date == datetime.datetime(2015, 4, 8, 0, 0, 0)
        assert customers_cohorts.cohort_cardinality['2015/07/01-2015/07/07'] == 1102
        assert customers_cohorts.cohort_cardinality['2015/06/24-2015/06/30'] == 790
        assert len(customers_cohorts.cohort_cardinality) == 13
        assert len(customers_cohorts.customers_and_matching_cohort) == 11444

    def test_pst_full_customer_file(self):
        pst_time_zone = datetime.timezone(datetime.timedelta(days=-1, seconds=61200), name="PST")
        customers_cohorts = ctsc.CustomerTimeSpanCohorts(recent_date=datetime.datetime(2015, 7, 7, 23, 47, 13,
                                                                                       tzinfo=pst_time_zone))
        customers_cohorts.read_customers_csv_file()
        assert customers_cohorts.cohort_cardinality['2015/07/01-2015/07/07'] == 1044
        assert customers_cohorts.cohort_cardinality['2015/06/24-2015/06/30'] == 796
        assert len(customers_cohorts.cohort_cardinality) == 8
        assert len(customers_cohorts.customers_and_matching_cohort) == 7246
