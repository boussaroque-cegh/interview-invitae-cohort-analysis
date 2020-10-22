from tests import test_customer_time_span_cohorts

def test_customer_read():
    test_cohort = test_customer_time_span_cohorts.TestCustomerTimeSpanCohorts()
    test_cohort.test_date_utc_conversion()
    test_cohort.test_date_local_conversion()
    test_cohort.test_cohort_id()
    test_cohort.test_utc_full_customer_file()
    test_cohort.test_pst_full_customer_file()

if __name__ == '__main__':
    test_customer_read()
