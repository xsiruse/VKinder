from pymongo import MongoClient


def start_db():
    client = MongoClient()
    vk_db = client['VK_db']
    skip_ids = vk_db['skip_ids']
    top10_users_mongo = vk_db['top10users']
    skip_ids.insert_one({'ID': [0]})
    return skip_ids, top10_users_mongo


def get_skip_ids_list(skip_ids):
    skip_ids_list = skip_ids.find_one()['ID']
    return skip_ids_list


def write_users_in_skip_id_db(top10_users, skip_ids):
    for uid in top10_users:
        skip_ids.update_one({'ID': skip_ids.find_one()['ID']}, {'$push': {'ID': uid}})


def write_top10users_db(data, top10_users_mongo):
    top10_users_mongo.insert_one({'users': data})
