from tests import test_customer_time_span_cohorts

def test_customer_read():
    test_cohort = test_customer_time_span_cohorts.TestCustomerTimeSpanCohorts()
    test_cohort.test_date_conversion()
    test_cohort.test_cohort_id()
    test_cohort.test_full_customer_file()

if __name__ == '__main__':
    test_customer_read()
