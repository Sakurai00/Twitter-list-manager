import csv
import itertools

import tweepy
import pandas as pd

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
    id = input("list id:")
    return id


def list_member_to_csv(list_id):
    """ 指定されたリストIDのメンバをCSVファイルに出力する

    Args:
        list_id (int): List ID
    """

    name = api.get_list(list_id = list_id).full_name.split('/')

    file_name = '{}_{}.csv'.format(name[0], name[1])

    f = open(file_name, "w+", encoding="UTF-8", newline="")
    writer = csv.writer(f)

    writer.writerow(["内部ID", "名前", "ID", "フォロー数", "フォロワー数", "URL", "bio"])
    for member in tweepy.Cursor(api.list_members, list_id = list_id).items():
        writer.writerow([member.id, member.name, member.screen_name, member.friends_count, member.followers_count, member.url, member.description])
    f.close()
    print("{} is created.".format(file_name))


def csv_output():
    """ リストメンバをCSVファイルに出力する
    """

    #screen_name = input("screen_name:")
    screen_name = "Sakurai_Absol"
    mode = int(input("mode(0:all, 1:single):"))

    if mode == 0:
        lists = api.lists_all(screen_name = screen_name)
        for list in lists:
            list_member_to_csv(list.id)
    elif mode == 1:
        list_id = get_list_id(screen_name)
        list_member_to_csv(list_id)


def create_list(list_name, mode) -> int:
    """ 指定された名前のリストを作成する

    Args:
        list_name (String): List name
        mode (String): private or public

    Returns:
        int: List ID
    """

    list = api.create_list(list_name, mode = mode)
    return list.id


def csv_to_list(list_id, file_name):
    """ CSVファイルのメンバをリストに追加する

    Args:
        list_id (int): List ID
        file_name (String): CSV file name
    """

    df = pd.read_csv(file_name, encoding="UTF-8", header = 0, chunksize = 100, usecols = [0])
    for chunk in df:
        id_list = chunk.to_numpy().tolist()
        id_list = list(itertools.chain.from_iterable(id_list))
        api.add_list_members(list_id = list_id, user_id = id_list)
    print("{} OK".format(file_name))


def make_list_from_csv():

    temp = int(input("List ID (0:Create new list):"))

    if temp == 0:
        list_name = input("List name:")
        mode = input("Mode(public or private):")
        list_id = create_list(list_name, mode)
    else:
        list_id = temp

    file_name = input("Input CSV file name:")
    csv_to_list(list_id, file_name)

def main():
    print("API User: {}".format(api.me().screen_name))

    #csv_output()
    make_list_from_csv()


if __name__ == '__main__':
    main()