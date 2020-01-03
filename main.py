from datetime import datetime
from collections import Counter
import time
import operator
from pprint import pprint

import vk_api
import json

fields = ['about', 'activities', 'bdate', 'blacklisted', 'blacklisted_by_me', 'books', 'career', 'city', 'common_count',
          'counters', 'country', 'education', 'followers_count', 'friend_status', 'games', 'home_town',
          'interests', 'is_favorite', 'lists', 'movies', 'music', 'occupation', 'personal', 'photo_200_orig', 'quotes',
          'relation', 'schools', 'sex', 'timezone', 'tv', 'universities']
fi = ','.join(fields)

TOKEN = '8adc8c028adc8c028adc8c02548ab1847688adc8adc8c02d7547fedba187a9a4a0bbbd9'


def auth():
    u_login = input('Введите номер телефона или логин: ')
    u_password = input('Введите пароль: ')
    return u_login, u_password


login, password = auth()


def set_age():
    print('\nВозрастной диапазон')
    age_from = int(input('Возраст от: '))
    age_to = int(input('Возраст до: '))
    age = range(age_from, age_to + 1)
    return age_from, age_to, age


age_from, age_to, age = set_age()


def vk(login, password):
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
        return vk_session

    except vk_api.AuthError as error_msg:
        print(error_msg)
        return


session = vk(login, password)
print(session)
opse = session.get_api()


class User:

    def __init__(self, uid):
        interests = opse.users.get(user_ids=uid, fields='%s' % fi)[0]
        if 'bdate' in interests.keys():
            bdate = datetime.strptime(interests['bdate'], '%d.%m.%Y')
        else:
            bdate = datetime.strptime(input('Введите дату рождения в формате дд.мм.гггг: '), '%d.%m.%Y')
        self.gender = interests['sex']
        self.relation = interests['relation']
        self.groups = opse.groups.get()
        self.friends = opse.friends.get()
        self.interests = {}
        self.country = interests['country']
        self.city = interests['city']['id']
        self.age = datetime.now().year - bdate.year - (
                (datetime.now().month, datetime.now().day) < (bdate.month, bdate.day))
        self.sex = interests['sex']

    def search(self):
        res = opse.users.search(v='5.103', city=self.city, age_from=age_from, age_to=age_to,
                                count=1000)
        print(res['count'])
        offset = 0
        tries = 0
        users_list = []
        while offset < res['count']:
            try:

                users = opse.users.search(v='5.103', city=self.city, sex=self.sex, age_from=age_from,
                                          age_to=age_to,
                                          count=10, offset=offset)

            except vk_api.exceptions.ApiError:
                time.sleep(1)
                continue

            for user in users['items']:
                tries += 1
                if tries / 100 != 0:
                    print('.', end='')
                else:
                    print(tries)
                users_list.append(user['id'])
            offset += 1000
            if offset % 10000 == 0:
                print(offset)
            else:
                print('.', end='')
        self.users_list = users_list

    def count_groups_match_points(self):
        group_matches = {}
        for uid in self.users_list:
            try:
                groups = opse.groups.get(v='5.103', user_id=str(uid))
                print('...')
                group_matches[uid] = len(set(self.groups).intersection(set(groups['items'])))
            except vk_api.exceptions.ApiError:
                print('...')
                time.sleep(1)
                continue
        group_matches = sorted(group_matches.items(), key=operator.itemgetter(1), reverse=True)
        self.group_matches = dict(group_matches)

    def count_interests_match_points(self):
        interests_matches = {}
        for uid in self.users_list:
            try:
                user = opse.users.get(v='5.103', user_id=str(uid), fields='interests, books, music')
                print('..u')
                time.sleep(0.34)
                try:
                    interests = \
                        (user[0]['music'] + ' ' + user[0]['interests'] + ' ' + user[0]['books']
                         ).replace(',', '').split(' ')
                    interests_filter = [item for item in interests if item != '']
                except KeyError:
                    continue
                except vk_api.exceptions.ApiError:
                    time.sleep(1)
                interests_matches[uid] = len(set(self.interests).intersection(set(interests_filter)))
            except vk_api.exceptions.ApiError:
                print('..e')
                time.sleep(1)
                continue
        interests_matches = sorted(interests_matches.items(), key=operator.itemgetter(1), reverse=True)
        self.interests_matches = dict(interests_matches)

    def count_total_match_points(self):
        groups_and_interests_match = (self.interests_matches, self.group_matches)
        total_match_points = Counter()
        for item in groups_and_interests_match:
            total_match_points.update(item)
        total_match_points = dict(total_match_points)
        total_match_points = sorted(total_match_points.items(), key=operator.itemgetter(1), reverse=True)
        print(total_match_points)
        self.total_match_points = total_match_points

    def get_top10users(self):
        self.top_10_users = []
        for uid in self.total_match_points[0:10]:
            self.top_10_users.append(uid[0])
        print(self.top_10_users)

    def get_photos(self):
        self.to_write = []
        for uid in self.top_10_users:
            top_likes_list = []
            photo = opse.photos.get(v='5.103', owner_id=uid, album_id='profile', extended='likes')
            time.sleep(0.34)
            user = opse.users.get(v='5.103', user_ids=uid)
            print('...', end='')
            time.sleep(0.34)
            top_3_photo = []
            for i in photo['items']:
                top_likes_list.append(i['likes']['count'])
                top_likes_list.sort(reverse=True)
            for i in photo['items']:
                if i['likes']['count'] in top_likes_list[:3]:
                    top_3_photo.append(i['sizes'][-1]['url'])
            self.to_write.append({'id': uid, 'first_name': user[0]['first_name'], 'last_name': user[0]['last_name'],
                                  'url': top_3_photo})
        pprint(self.to_write)

    def write_top10users(self):
        with open('top10users.json', 'w', encoding='utf-8') as file:
            json.dump(self.to_write, file, ensure_ascii=False, indent=2)


def main():
    me = User(opse.users.get()[0]['id'])
    me.search()
    me.count_groups_match_points()
    me.count_interests_match_points()
    me.count_total_match_points()
    me.get_top10users()
    me.get_photos()
    me.write_top10users()


if __name__ == '__main__':
    main()
