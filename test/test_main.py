import unittest
from unittest.mock import patch
from main import User
import vk_api
import time


class Test_VKinder(unittest.TestCase):
    def setUp(self):
        with open('fixture/token.txt', 'r', encoding='UTF-8') as f:
            token = f.read()
        session = vk_api.VkApi(token=token)
        self.op_se = session.get_api()
        self.user_id = 202538602
        self.user_info = self.op_se.users.get(v='5.101', user_ids=self.user_id,
                                              fields='interests, sex, city, books, music')
        time.sleep(0.34)
        self.fake_user_info = ['try', 'la', 2]
        self.break_api = 'not session'

    @patch('builtins.input', lambda *args: 'any string')
    def test_set_age_for_search_not_number_input(self):
        with self.assertRaises(ValueError):
            User(self.user_id, self.op_se)

    def test_get_user_info_user_if_api_is_breack(self):
        time.sleep(0.34)
        with self.assertRaises(AttributeError):
            User(self.user_id, self.break_api)

    def test_search_incorrect_age_line(self):
        time.sleep(0.34)
        self.assertNotEqual(User.search(self.op_se, 18, 9), [1])

    def test_count_groups_match_points(self):
        self.assertDictEqual(User.count_groups_match_points(self.op_se, users_list=[1, 2]), {1: 0})

    def test_count_interests_match_points(self):
        self.assertDictEqual(User.count_interests_match_points(self.op_se, users_list=[1, 2]), {1: 0})

    def test_count_total_match_points(self):
        self.assertListEqual(User.count_total_match_points(interests_matches={1: 0}, group_matches={1: 0, 2: 0}),
                             [(1, 0), (2, 0)])

    def test_get_top10_users(self):
        with self.assertRaises(NameError):
            User.get_top10users(self, skip_ids=range(0, 12), total_match_points={1: 0})

    def test_get_photos(self):
        self.assertListEqual(User.get_photos(self, top_10_users=[1]),
                             [{'first_name': 'Pavel',
                               'id': 1,
                               'last_name': 'Durov',
                               'url': ['https://sun9-42.userapi.com/c9591/u00001/136592355/w_818d6f79.jpg',
                                       'https://sun9-42.userapi.com/c9591/u00001/136592355/w_f6a60338.jpg',
                                       'https://sun1-14.userapi.com/c7003/v7003978/1ed9/yoeGXOWmW-M.jpg']}])


if __name__ == '__main__':
    unittest.main()
