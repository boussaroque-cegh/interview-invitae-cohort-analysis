import datetime
from customer_order_cohort import customer_time_span_cohorts as ctsc
from customer_order_cohort import order_time_span_aggregation as otsa

class TestOrderTimeSpanAggregation:
    def test_pst_read_all_order_entries(self):
        customers: ctsc.CustomerTimeSpanCohorts = self.make_pst_test_customer_cohorts()
        orders_by_time_slot: otsa = otsa.OrderTimeSpanAggregation(
            path_csv_file='./data/doesNotExist.csv', customer_cohorts = customers)
        raw_orders = [
            ['QAZAQ', '2020-10-05 11:43:17','2'],['QAZAQ','2020-09-23 07:18:23','1'],
            ['qazaq','2020-10-06 20:43:17','2'],['qazaq','2020-10-05 23:13:33','1'],
            ['plokijuh','2020-10-09 08:43:57','1'],['plokijuh','2020-10-12 01:04:07','2'],
            ['qazaq','2020-10-14 21:34:07','3'], ['hujikolp','2020-10-17 12:21:32', '1'],
            ['qazaq','2020-10-19 03:34:07','4'], ['wassaw','2020-10-11 00:00:01','1']]
        # we should not care about 'QAZAQ', not part of the cohorts
        # for 'plokijuh' first oder after customer creation date
        assert orders_by_time_slot.read_all_order_entries(raw_orders, -1, 0, 1, 2) == 3
        assert '2020/09/28-2020/10/04' in orders_by_time_slot.customer_group_to_order_accumulated
        order_counts_first_cohort = orders_by_time_slot.customer_group_to_order_accumulated['2020/09/28-2020/10/04']
        # qazaq order none the first week, 2 the second week, and 2 the last week
        assert order_counts_first_cohort == [[2, 0], [2, 1], [0, 0]]
        assert '2020/10/05-2020/10/11' in orders_by_time_slot.customer_group_to_order_accumulated
        order_counts_second_cohort = orders_by_time_slot.customer_group_to_order_accumulated['2020/10/05-2020/10/11']
        # plokijuh and wassaw only put orders the second week
        assert order_counts_second_cohort == [[0, 0], [3, 2]]
        assert '2020/10/12-2020/10/18' in orders_by_time_slot.customer_group_to_order_accumulated
        order_counts_recent_cohort = orders_by_time_slot.customer_group_to_order_accumulated['2020/10/12-2020/10/18']
        # single order for hujikolp the most recent week
        assert order_counts_recent_cohort == [[1, 1]]

    @staticmethod
    def make_pst_test_customer_cohorts() ->ctsc.CustomerTimeSpanCohorts:
        pst_time_zone = datetime.timezone(datetime.timedelta(days=-1, seconds=61200), name="PST")
        customers_cohorts = ctsc.CustomerTimeSpanCohorts(
            path_csv_file='./data/doesNotExist.csv',
            recent_date=datetime.datetime(2020, 10, 18, 23, 47, 13,tzinfo=pst_time_zone),
            number_of_intervals=3
        )  # from Sunday Oct 18 down to Monday Sept 28
        customers_cohorts.track_customer('hujikolp', '2020-10-17 08:24:52')
        customers_cohorts.track_customer('plokijuh', '2020-10-09 08:44:02')
        customers_cohorts.track_customer('wassaw', '2020-10-10 02:44:02')
        customers_cohorts.track_customer('qazaq', '2020-09-30 18:24:52')
        customers_cohorts.track_customer('QAZAQ', '2020-09-23 06:18:23')
        customers_cohorts.track_customer('QaZaQ', '2020-10-01 08:51:52')
        return customers_cohorts
