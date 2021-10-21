import itertools
import os

import pandas as pd
import tweepy
from tweepy.api import API

import listmanager.settings as st


def get_list_id(api: API, screen_name: str) -> int:
    """あるユーザのリストを列挙し，指定したリストIDを返す

    Args:
        api (API): Twitter API
        screen_name (str): Screen_name

    Returns:
        int: List ID
    """

    lists = api.get_lists(screen_name=screen_name)
    for list in lists:
        print(list.id, list.name)
    id = int(input("List ID:"))
    return id


def user_lookup(api: API, id_list: list) -> list:
    """ユーザIDを元にユーザの情報を取得する

    Args:
        api (API): Twitter API
        id_list (list): User ID list

    Returns:
        list: User list
    """

    user_list = [
        ["id", "name", "screen_name", "friends", "followers", "url", "description"]
    ]
    for i in range(0, len(id_list), 100):
        for user in api.lookup_users(user_ids=id_list[i : i + 100]):
            user_list.append(
                [
                    user.id,
                    user.name,
                    user.screen_name,
                    user.friends_count,
                    user.followers_count,
                    user.url,
                    user.description,
                ]
            )
    return user_list


def list_to_csv(api: API, list_id: int) -> None:
    """指定されたリストIDのメンバをCSVファイルに出力する

    Args:
        api (API): Twitter API
        list_id (int): List ID
    """

    list = api.get_list(list_id=list_id)

    file_name = os.path.join(
        st.SAVE_PATH, "{}_{}.csv".format(list.user.screen_name, list.name)
    )

    user_list = [
        ["id", "name", "screen_name", "friends", "followers", "url", "description"]
    ]

    for user in tweepy.Cursor(api.get_list_members, list_id=list_id).items():
        user_list.append(
            [
                user.id,
                user.name,
                user.screen_name,
                user.friends_count,
                user.followers_count,
                user.url,
                user.description,
            ]
        )

    make_csv(user_list, file_name)


def block_list_to_csv(api: API, screen_name: str) -> None:
    """ブロックしているユーザをCSVファイルに出力する

    Args:
        api (API): Twitter API
        screen_name (str): Screen name
    """

    file_name = os.path.join(st.SAVE_PATH, "{}_block.csv".format(screen_name))

    user_list = [
        ["id", "name", "screen_name", "friends", "followers", "url", "description"]
    ]

    for user in tweepy.Cursor(api.get_blocks, screen_name=screen_name).items():
        user_list.append(
            [
                user.id,
                user.name,
                user.screen_name,
                user.friends_count,
                user.followers_count,
                user.url,
                user.description,
            ]
        )

    make_csv(user_list, file_name)


# ====== ====== ======


def make_csv_from_list(api: API, screen_name: str, mode: int) -> None:
    """リストのメンバをCSVファイルに出力する

    Args:
        api (API): Twitter API
        screen_name (str): Screen name
        mode (int): 0: All, 1: Single
    """

    if mode == 0:
        lists = api.get_lists(screen_name=screen_name)
        for list in lists:
            list_to_csv(api, list.id)
    elif mode == 1:
        list_id = get_list_id(api, screen_name)
        list_to_csv(api, list_id)


def make_list_from_csv(api: API, list_id: int, file_name: str) -> None:
    """CSVファイルを読み込んでリストを作成する

    Args:
        api (API): Twitter API
        list_id (int): List ID
        file_name (str): CSV file name
    """

    df = pd.read_csv(file_name, encoding="UTF-8", header=0, chunksize=100, usecols=[0])
    for chunk in df:
        id_list = chunk.to_numpy().tolist()
        id_list = list(itertools.chain.from_iterable(id_list))
        api.add_list_members(list_id=list_id, user_id=id_list)

    print("{} OK".format(file_name))


def make_csv_from_follow(api: API, screen_name: str, mode: int) -> None:
    """フォローしているユーザをCSVファイルに出力する

    Args:
        api (API): Twitter API
        screen_name (str): Screen name
        mode (int): 0: Simple, 1: All
    """

    file_name = os.path.join(st.SAVE_PATH, "{}_follow.csv".format(screen_name))
    id_list = []

    for member in tweepy.Cursor(api.get_friend_ids, screen_name=screen_name).items():
        id_list.append(member)

    if mode == 0:
        user_list = ["id"]
        user_list += id_list
    elif mode == 1:
        user_list = user_lookup(id_list)

    df = pd.DataFrame(user_list)
    df.to_csv(file_name, header=False, index=False, encoding="UTF-8")

    print("{} is created.".format(file_name))


def diff_of_csv(file_name1: str, file_name2: str, new_file_name: str) -> None:
    """与えられたCSVファイル1と2の差分を出力する

    Args:
        file_name1 (str): CSV file name (base)
        file_name2 (str): CSV file name (compare)
        new_file_name (str): new CSV file name
    """

    new_file_name = os.path.join(st.SAVE_PATH, new_file_name)

    df1 = pd.read_csv(file_name1, encoding="UTF-8", header=0)
    df2 = pd.read_csv(file_name2, encoding="UTF-8", header=0)
    df3 = df1[~df1.id.isin(df2.id)]
    df3.to_csv(new_file_name, header=False, index=False, encoding="UTF-8")

    print("{} is created.".format(new_file_name))


def make_csv(list: list, file_name: str) -> None:
    """CSVファイルを作成する

    Args:
        list (list): List
        file_name (str): CSV file name
    """

    df = pd.DataFrame(list)
    df.to_csv(file_name, header=False, index=False, encoding="UTF-8")

    print("{} is created.".format(file_name))


def set_screen_name(api: API) -> str:
    """Screen nameを入力する

    Returns:
        str: Screen name
    """

    screen_name = input("Screen name:")
    if not screen_name:
        screen_name = api.verify_credentials().screen_name
    return screen_name
