import datetime
import pathlib
import unittest
import functions
import json
ex1 = pathlib.Path(__file__).parent.joinpath("example_1.json")
ex2 = pathlib.Path(__file__).parent.joinpath("example_2.json")
ex3 = pathlib.Path(__file__).parent.joinpath("example_3.json")
class MyTestCase(unittest.TestCase):

    def test_summ_elements_1(self):
        list1 = [0,1,2,3,4]
        res = functions.summ_elements(list1)
        self.assertEqual(res, [0,1,3,6,10])

    def test_summ_elements_2(self):
        list1 = [1,0,-1,-2,-3]
        res = functions.summ_elements(list1)
        self.assertEqual(res, [1,1,0,-2,-5])

    def test_summ_elements_3(self):
        list1 = [0,0,0,0,0]
        res = functions.summ_elements(list1)
        self.assertEqual(res, [0,0,0,0,0])

    def test_summ_elements_4(self):
        list1 = []
        res = functions.summ_elements(list1)
        self.assertEqual(res, [])

    def test_make_lists_name_num_1(self):
        #a-1,b-2,c-3,d-4,e-5
        list_users=['a','b','c','d','e',  'b','c','d','e',  'c','d','e',  'd','e',  'e']
        count = 3
        list_names, list_nums = functions.make_lists_name_num(list_users, count)
        self.assertEqual(list_names, ['e','d','c'])
        self.assertEqual(list_nums, [5, 4,3])

    def test_make_lists_name_num_2(self):
        #a-1,b-2,c-8,d-4,e-5
        list_users=['a','b','c','d','e','c',  'b','c','d','e','c',  'c','d','e','c',  'd','e','c',  'e','c',]
        count = 3
        list_names, list_nums = functions.make_lists_name_num(list_users, count)
        self.assertEqual(list_names, ['c','e','d'])
        self.assertEqual(list_nums, [8, 5, 4])


    def test_make_lists_name_num_3(self):
        #a-1,b-2,c-8,d-4,e-5
        list_users=['a','b','c','d','e','c',  'b','c','d','e','c',  'c','d','e','c',  'd','e','c',  'e','c',]
        count = 5
        list_names, list_nums = functions.make_lists_name_num(list_users, count)
        self.assertEqual(list_names, ['c','e','d','b','a'])
        self.assertEqual(list_nums, [8, 5, 4,2,1])

    def test_make_lists_name_num_4(self):
        #a-1,b-2,c-8,d-4,e-5
        list_users=['a','b','c','d','e','c',  'b','c','d','e','c',  'c','d','e','c',  'd','e','c',  'e','c',]
        count = 1
        list_names, list_nums = functions.make_lists_name_num(list_users, count)
        self.assertEqual(list_names, ['c'])
        self.assertEqual(list_nums, [8])

    def test_make_lists_name_num_5(self):
        #a-1,b-2,c-8,d-4,e-5
        list_users=['a','b','c','d','e','c',  'b','c','d','e','c',  'c','d','e','c',  'd','e','c',  'e','c',]
        count = 0
        list_names, list_nums = functions.make_lists_name_num(list_users, count)
        self.assertEqual(list_names, [])
        self.assertEqual(list_nums, [])

    def test_make_lists_name_num_6(self):
        # a-1,b-2,c-8,d-4,e-5
        list_users = ['a', 'b', 'c', 'd', 'e', 'c', 'b', 'c', 'd', 'e', 'c', 'c', 'd', 'e', 'c', 'd', 'e', 'c', 'e',
                      'c', ]
        count = 6
        list_names, list_nums = functions.make_lists_name_num(list_users, count)
        self.assertEqual(list_names, ['c', 'e', 'd', 'b', 'a'])
        self.assertEqual(list_nums, [8, 5, 4, 2, 1])

    def test_make_lists_name_num_7(self):
        # a-1,b-1,c-1,d-1,e-1
        list_users = ['a', 'b', 'c', 'd', 'e']
        count = 3
        list_names, list_nums = functions.make_lists_name_num(list_users, count)
        self.assertEqual(list_names, ['a', 'b', 'c'])
        self.assertEqual(list_nums, [1,1,1])

    def test_make_lists_name_num_8(self):
        # a-1,b-1,c-1,d-1,e-1
        list_users = []
        count = 3
        list_names, list_nums = functions.make_lists_name_num(list_users, count)
        self.assertEqual(list_names, [])
        self.assertEqual(list_nums, [])

    def test_get_issue_item_to_time_1(self):
        f=ex1.open()
        data = json.load(f)
        f.close()
        field = 'status'
        toString = 'Closed'
        res = functions.get_issue_item_to_time(data,field,toString)
        base = datetime.datetime.strptime('2022-06-22T08:27:32.763+0000', '%Y-%m-%dT%H:%M:%S.%f%z')
        self.assertEqual(res,[base])

    def test_get_issue_item_to_time_2(self):
        f = ex1.open()
        data = json.load(f)
        f.close()
        field = 'status'
        to = '6'
        res = functions.get_issue_item_to_time(data, field, to)
        base = datetime.datetime.strptime('2022-06-22T08:27:32.763+0000', '%Y-%m-%dT%H:%M:%S.%f%z')
        self.assertEqual(res, [base])

    def test_get_issue_item_to_time_3(self):
        f = ex2.open()
        data = json.load(f)
        f.close()
        field = 'status'
        to = '5'
        res = functions.get_issue_item_to_time(data, field, to)
        base1 = datetime.datetime.strptime('2020-06-26T22:20:00.460+0000', '%Y-%m-%dT%H:%M:%S.%f%z')
        base2 = datetime.datetime.strptime('2020-07-07T00:19:28.976+0000', '%Y-%m-%dT%H:%M:%S.%f%z')
        self.assertEqual(res, [base1,base2])

    def test_get_issue_item_to_time_4(self):
        f = ex2.open()
        data = json.load(f)
        f.close()
        field = 'sss'
        to = '5'
        res = functions.get_issue_item_to_time(data, field, to)
        self.assertEqual(res, [])

    def test_get_issue_item_to_time_5(self):
        f = ex2.open()
        data = json.load(f)
        f.close()
        field = 'status'
        to = '777'
        res = functions.get_issue_item_to_time(data, field, to)
        self.assertEqual(res, [])

    def test_status_statistic_1(self):
        f = ex1.open()
        data = json.load(f)
        f.close()
        opened, in_progress, resolved, reopened, patch_available = functions.status_statistic(data)
        base_open = datetime.timedelta(days=2,hours=1,minutes=0, seconds=4, milliseconds=984)
        base_in_prog = datetime.timedelta(days=27,hours=18,minutes=50, seconds=20, milliseconds=586)
        base_resolved = datetime.timedelta(seconds=8, milliseconds=624)
        base_reopened = datetime.timedelta(0)
        base_patch_available = datetime.timedelta(0)
        self.assertEqual(opened, base_open)
        self.assertEqual(in_progress, base_in_prog)
        self.assertEqual(resolved, base_resolved)
        self.assertEqual(reopened, base_reopened)
        self.assertEqual(patch_available, base_patch_available)


    def test_status_statistic_2(self):
        #состояние Решено повторяется
        f = ex2.open()
        data = json.load(f)
        f.close()
        opened, in_progress, resolved, reopened, patch_available = functions.status_statistic(data)
        base_resolved_1 = datetime.timedelta(days=3,hours=23,minutes=46, seconds=58, milliseconds=476)
        base_resolved_2 = datetime.timedelta(days=245,hours=9,minutes=1, seconds=1, milliseconds=967)
        self.assertEqual(resolved, base_resolved_1+base_resolved_2)

    def test_get_resolved_time_for_assignee_1(self):
        f = ex1.open()
        data = json.load(f)
        f.close()
        res = functions.get_resolved_time_for_assignee(data,'cadonna')
        base = datetime.timedelta(days=27, hours=19, minutes=59, seconds=23, milliseconds=440)
        self.assertEqual(res, base.total_seconds() / 3600)

    def test_get_resolved_time_for_assignee_2(self):
        f = ex3.open()
        data = json.load(f)
        f.close()
        res = functions.get_resolved_time_for_assignee(data,'nehanarkhede')
        base = datetime.timedelta(days=49, hours=22, minutes=40, seconds=3, milliseconds=492)
        self.assertEqual(res, base.total_seconds() / 3600)


if __name__ == '__main__':
    unittest.main()
