from datetime import datetime, date

import vk_api

TOKEN = '8adc8c028adc8c028adc8c02548ab1847688adc8adc8c02d7547fedba187a9a4a0bbbd9'
fields = ['about', 'activities', 'bdate', 'blacklisted', 'blacklisted_by_me', 'books', 'career', 'city', 'common_count',
          'connections', 'counters', 'country', 'education', 'followers_count', 'friend_status', 'games', 'home_town',
          'interests', 'is_favorite', 'lists', 'movies', 'music', 'occupation', 'personal', 'photo_200_orig', 'quotes',
          'relation', 'schools', 'sex', 'timezone', 'tv', 'universities']
fi = ','.join(fields)

def vk(login, password):
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()
    return vk_session.get_api()





class User:

    def __init__(self, id):
        interests = opse.users.get(user_ids=id, fields='%s' % fi)[0]
        self.b_date = datetime.strptime(interests['bdate'], '%d.%m.%Y')
        self.age = date.today().year - self.b_date.year - ((date.today().month, date.today().day) <
                                                           (self.b_date.month, self.b_date.day))
        self.gender = interests['sex']
        self.relation = interests['relation']
        self.groups = opse.groups.get()
        self.friends = opse.friends.get()
        self.interests = {}
        self.country = interests['country']
        self.city = interests['city']


if __name__ == "__main__":
    login = input('Введите номер телефона или логин: ')
    password = input('Введите пароль: ')
    opse = vk(login, password)

    me = User(opse.users.get()[0]['id'])

