import itertools

import pandas as pd
import tweepy

from twapi import generate_api

api = generate_api()


def get_list_id(screen_name) -> int:
    """ あるユーザのリストを列挙し，指定したリストIDを返す

    Args:
        screen_name (String): User's screen_name

    Returns:
        int: List ID
    """

    lists = api.lists_all(screen_name = screen_name)
    for list in lists:
        print(list.id, list.name)
    id = input("List ID:")
    return id


def create_list() -> int:
    """ 指定された名前のリストを作成する

    Returns:
        int: List ID
    """

    list_name = input("List name:")
    mode = input("Mode(public or private):")
    list_temp = api.create_list(list_name = list_name, mode = mode)
    return list_temp.id


def user_lookup(id_list) -> list:
    """ ユーザIDを元にユーザの情報を取得する

    Args:
        id_list (list): User ID list

    Returns:
        list: User list
    """

    user_list = [["id", "name", "screen_name", "friends", "followers", "url", "description"]]
    for i in range(0, len(id_list), 100):
        for member in api.lookup_users(user_ids = id_list[i:i+100]):
            user_list.append([member.id, member.name, member.screen_name, member.friends_count, member.followers_count, member.url, member.description])
    return user_list


def list_to_csv(list_id):
    """ 指定されたリストIDのメンバをCSVファイルに出力する

    Args:
        list_id (int): List ID
    """

    name = api.get_list(list_id = list_id).full_name.split('/')
    file_name = '{}_{}.csv'.format(name[0], name[1])

    user_list = [["id", "name", "screen_name", "friends", "followers", "url", "description"]]

    for member in tweepy.Cursor(api.list_members, list_id = list_id).items():
        user_list.append([member.id, member.name, member.screen_name, member.friends_count, member.followers_count, member.url, member.description])

    df = pd.DataFrame(user_list)
    df.to_csv(file_name, header = False, index = False, encoding="UTF-8")

    print("{} is created.".format(file_name))



# ====== ====== ======

def make_csv_from_list():
    """ リストメンバをCSVファイルに出力する
    """

    screen_name = input("Screen name:")
    mode = int(input("Mode (0:All, 1:Single):"))

    if mode == 0:
        lists = api.lists_all(screen_name = screen_name)
        for list in lists:
            list_to_csv(list.id)
    elif mode == 1:
        list_id = get_list_id(screen_name)
        list_to_csv(list_id)


def make_list_from_csv():
    """ CSVファイルのメンバをリストに追加する
    """

    mode = int(input("Mode (0:Create new list, 1:List up):"))

    if mode == 0:
        list_id = create_list()
    elif mode == 1:
        screen_name = input("Screen name:")
        list_id = get_list_id(screen_name)

    file_name = input("CSV file name:")

    df = pd.read_csv(file_name, encoding="UTF-8", header = 0, chunksize = 100, usecols = [0])
    for chunk in df:
        id_list = chunk.to_numpy().tolist()
        id_list = list(itertools.chain.from_iterable(id_list))
        api.add_list_members(list_id = list_id, user_id = id_list)

    print("{} OK".format(file_name))


def make_csv_from_follow():
    """ フォローしているユーザをCSVファイルに出力する
    """

    screen_name = input("Screen name:")
    mode = int(input("Mode (0:Simple, 1:More info):"))


    file_name = '{}_follow.csv'.format(screen_name)
    id_temp = []

    for member in tweepy.Cursor(api.friends_ids, screen_name = screen_name).items():
        id_temp.append(member)

    if mode == 0:
        user_list = ["id"]
        user_list += id_temp
    elif mode == 1:
        user_list = user_lookup(id_temp)

    df = pd.DataFrame(user_list)
    df.to_csv(file_name, header = False, index = False, encoding="UTF-8")

    print("{} is created.".format(file_name))



def main():
    print("API User: {}".format(api.me().screen_name))
    print("Menu\n\
        0: list -> csv\n\
        1: csv -> list\n\
        2: follow -> csv")
    menu_id = int(input("Menu ID:"))

    if menu_id == 0:
        make_csv_from_list()
    elif menu_id == 1:
        make_list_from_csv()
    elif menu_id == 2:
        make_csv_from_follow()



if __name__ == '__main__':
    main()