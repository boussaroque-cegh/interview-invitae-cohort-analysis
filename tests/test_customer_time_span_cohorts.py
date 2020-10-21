import datetime
from customer_order_cohort import customer_time_span_cohorts as ctsc


def test_date_conversion():
    customers_cohorts = ctsc.CustomerTimeSpanCohorts(path_csv_file='./data/doesNotExist.csv',
                                                     recent_date=datetime.datetime(2017, 7, 7, 23, 47, 13),
                                                     days_interval_length=14, number_of_intervals=3)
    assert customers_cohorts.recent_date == datetime.datetime(2017, 7, 8, 0, 0, 0)
    assert customers_cohorts.oldest_date == datetime.datetime(2017, 5, 27, 0, 0, 0)
    assert customers_cohorts.convert_date_in_range(None) is None
    assert customers_cohorts.convert_date_in_range('') is None
    assert customers_cohorts.convert_date_in_range('2017-06-07  22:51:10') == datetime.datetime(2017, 6, 7, 22, 51, 10)
    assert customers_cohorts.convert_date_in_range('2017-07-08  09:51:10') is None
    assert customers_cohorts.convert_date_in_range('2017-04-07  21:21:12') is None


def test_cohort_id():
    customers_cohorts = ctsc.CustomerTimeSpanCohorts(path_csv_file='./data/doesNotExist.csv',
                                                     recent_date=datetime.datetime(2015, 7, 7, 23, 47, 13))
    assert customers_cohorts.track_customer('qazaq', '2015-07-07  06:21:42') == '2015/07/01-2015/07/07'
    assert customers_cohorts.track_customer('QaZaQ', '2015-07-07  23:59:59') == '2015/07/01-2015/07/07'
    assert customers_cohorts.track_customer('plokijuh', '2015-07-04  02:21:52') == '2015/07/01-2015/07/07'
    assert customers_cohorts.track_customer('plokijuhy', '2015-07-01  13:10:55') == '2015/07/01-2015/07/07'
    assert customers_cohorts.track_customer('plokijuhyg', '2015-07-01  00:00:00') == '2015/07/01-2015/07/07'
    assert customers_cohorts.track_customer('hujikolp', '2015-05-23  21:08:56') == '2015/05/20-2015/05/26'
    assert customers_cohorts.track_customer('tressert', '2015-03-21  19:43:27') is None  # out of date range
    assert customers_cohorts.track_customer('wassaw', '2015-07-08  00:00:00') is None  # out of date range
    assert customers_cohorts.track_customer('qazaq', '2015-07-07  07:47:27') is None  # customer id already tracked
    assert 'qazaq' in customers_cohorts.customers_and_matching_cohort
    assert 'plokijuh' in customers_cohorts.customers_and_matching_cohort
    assert 'hujikolp' in customers_cohorts.customers_and_matching_cohort
    assert 'tressert' not in customers_cohorts.customers_and_matching_cohort
    assert customers_cohorts.cohort_cardinality['2015/07/01-2015/07/07'] == 5
    assert customers_cohorts.cohort_cardinality['2015/05/20-2015/05/26'] == 1
    assert len(customers_cohorts.customers_and_matching_cohort) == 6
    assert len(customers_cohorts.cohort_cardinality) == 2


def test_full_customer_file():
    customers_cohorts = ctsc.CustomerTimeSpanCohorts(recent_date=datetime.datetime(2015, 7, 7, 23, 47, 13))
    customers_cohorts.read_customers_csv_file()
    assert customers_cohorts.cohort_cardinality['2015/07/01-2015/07/07'] == 1102
    assert customers_cohorts.cohort_cardinality['2015/06/24-2015/06/30'] == 790
    assert len(customers_cohorts.cohort_cardinality) == 13
    assert len(customers_cohorts.customers_and_matching_cohort) == 11444


if __name__ == '__main__':
    test_date_conversion()
    test_cohort_id()
    test_full_customer_file()
