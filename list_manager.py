import itertools

import pandas as pd
import tweepy

from twapi import generate_api
import settings as st

api = generate_api()


def get_list_id(screen_name: str) -> int:
    """ あるユーザのリストを列挙し，指定したリストIDを返す

    Args:
        screen_name (str): Screen_name

    Returns:
        int: List ID
    """

    lists = api.lists_all(screen_name = screen_name)
    for l in lists:
        print(l.id, l.name)
    id = int(input("List ID:"))
    return id


def create_list(list_name: str, mode: str) -> int:
    """ リストを作成する

    Args:
        list_name (str): List name
        mode (str): "pubric", "private"

    Returns:
        int: List ID
    """

    l = api.create_list(name = list_name, mode = mode)
    return l.id


def user_lookup(id_list: list) -> list:
    """ ユーザIDを元にユーザの情報を取得する

    Args:
        id_list (list): User ID list

    Returns:
        list: User list
    """

    user_list = [["id", "name", "screen_name", "friends", "followers", "url", "description"]]
    for i in range(0, len(id_list), 100):
        for user in api.lookup_users(user_ids = id_list[i:i+100]):
            user_list.append([user.id, user.name, user.screen_name, user.friends_count, user.followers_count, user.url, user.description])
    return user_list


def list_to_csv(list_id: int) -> None:
    """ 指定されたリストIDのメンバをCSVファイルに出力する

    Args:
        list_id (int): List ID
    """

    l = api.get_list(list_id = list_id)
    file_name = '{}_{}.csv'.format(l.user.screen_name, l.name)

    user_list = [["id", "name", "screen_name", "friends", "followers", "url", "description"]]

    for user in tweepy.Cursor(api.list_members, list_id = list_id).items():
        user_list.append([user.id, user.name, user.screen_name, user.friends_count, user.followers_count, user.url, user.description])

    df = pd.DataFrame(user_list)
    df.to_csv(file_name, header = False, index = False, encoding = "UTF-8")

    print("{} is created.".format(file_name))



# ====== ====== ======

def make_csv_from_list(screen_name: str, mode: int) -> None:
    """ リストのメンバをCSVファイルに出力する

    Args:
        screen_name (str): Screen name
        mode (int): 0: All, 1: Single
    """

    if mode == 0:
        lists = api.lists_all(screen_name = screen_name)
        for l in lists:
            list_to_csv(l.id)
    elif mode == 1:
        list_id = get_list_id(screen_name)
        list_to_csv(list_id)


def make_list_from_csv(list_id: int, file_name: str) -> None:
    """ CSVファイルを読み込んでリストを作成する

    Args:
        list_id (int): List ID
        file_name (str): CSV file name
    """

    df = pd.read_csv(file_name, encoding = "UTF-8", header = 0, chunksize = 100, usecols = [0])
    for chunk in df:
        id_list = chunk.to_numpy().tolist()
        id_list = list(itertools.chain.from_iterable(id_list))
        api.add_list_members(list_id = list_id, user_id = id_list)

    print("{} OK".format(file_name))


def make_csv_from_follow(screen_name: str, mode: int) -> None:
    """ フォローしているユーザをCSVファイルに出力する

    Args:
        screen_name (str): Screen name
        mode (int): 0: Simple, 1: All
    """

    file_name = '{}_follow.csv'.format(screen_name)
    id_list = []

    for member in tweepy.Cursor(api.friends_ids, screen_name = screen_name).items():
        id_list.append(member)

    if mode == 0:
        user_list = ["id"]
        user_list += id_list
    elif mode == 1:
        user_list = user_lookup(id_list)

    df = pd.DataFrame(user_list)
    df.to_csv(file_name, header = False, index = False, encoding = "UTF-8")

    print("{} is created.".format(file_name))


def diff_of_csv(file_name1: str, file_name2: str) -> None:
    """ 与えられたCSVファイル1と2の差分を出力する

    Args:
        file_name1 (str): CSV file name (base)
        file_name2 (str): CSV file name (compare)
    """

    new_file_name = '{}_{}.csv'.format(file_name1[:-4], file_name2[:-4])
    df1 = pd.read_csv(file_name1, encoding = "UTF-8", header = 0)
    df2 = pd.read_csv(file_name2, encoding = "UTF-8", header = 0)
    df3 = df1[~df1.id.isin(df2.id)]
    df3.to_csv(new_file_name, header = False, index = False, encoding = "UTF-8")

    print("{} is created.".format(new_file_name))



# ====== ====== ======

def main() -> None:
    print("API User: {}".format(api.me().screen_name))
    print("Menu\n\
        0: list -> csv\n\
        1: csv -> list\n\
        2: follow -> csv\n\
        3: diff of csv\n\
        4: create list\n\
        5: list up Lists")
    menu_id = int(input("Menu ID:"))

    screen_name = api.me().screen_name

    if menu_id == 0:
        screen_name = input("Screen name:")
        mode = int(input("Mode (0:All, 1:Single):"))
        make_csv_from_list(screen_name, mode)
    elif menu_id == 1:
        list_id = input("List ID:")
        file_name = input("CSV file name:")
        make_list_from_csv(list_id, file_name)
    elif menu_id == 2:
        screen_name = input("Screen name:")
        mode = int(input("Mode (0:Simple, 1:More info):"))
        make_csv_from_follow(screen_name, mode)
    elif menu_id == 3:
        file_name1 = input("File name 1:")
        file_name2 = input("File name 2:")
        diff_of_csv(file_name1, file_name2)
    elif menu_id == 4:
        list_name = input("List name:")
        mode = input("Mode(public or private):")
        list_id = create_list(list_name, mode)
        print("List ID: {}".format(list_id))
    elif menu_id == 5:
        screen_name = input("Screen name:")
        list_id = get_list_id(screen_name)
        print("List ID: {}".format(list_id))


if __name__ == '__main__':
    main()
