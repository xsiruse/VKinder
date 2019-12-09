from datetime import datetime, date
from pprint import pprint
import vk_api

TOKEN = '8adc8c028adc8c028adc8c02548ab1847688adc8adc8c02d7547fedba187a9a4a0bbbd9'
fields = ['about', 'activities', 'bdate', 'blacklisted', 'blacklisted_by_me', 'books', 'career', 'city', 'common_count',
          'connections', 'counters', 'country', 'education', 'followers_count', 'friend_status', 'games', 'home_town',
          'interests', 'is_favorite', 'lists', 'movies', 'music', 'occupation', 'personal', 'photo_200_orig', 'quotes',
          'relation', 'schools', 'sex', 'timezone', 'tv', 'universities']
fi = ','.join(fields)


def slices(slice, iters):
    a = 1
    b = slice
    lol = []
    for n in range(1, iters):
        lol.append(list(range(a, b)))
        a += slice
        b += slice
    return lol

if __name__ == '__main__':
    pass
