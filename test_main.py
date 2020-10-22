from tests import test_customer_time_span_cohorts, test_order_time_span_aggregation

def test_customer_read():
    test_cohort = test_customer_time_span_cohorts.TestCustomerTimeSpanCohorts()
    test_cohort.test_date_utc_conversion()
    test_cohort.test_date_local_conversion()
    test_cohort.test_cohort_id()
    test_cohort.test_utc_full_customer_file()
    test_cohort.test_pst_full_customer_file()


def test_order_read():
    test_summary = test_order_time_span_aggregation.TestOrderTimeSpanAggregation()
    test_summary.test_pst_read_all_order_entries()
    test_summary.test_utc_full_customer_and_order_file()


if __name__ == '__main__':
    test_customer_read()
    test_order_read()
