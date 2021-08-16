import csv

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


def main():
    print("API User: {}".format(api.me().screen_name))

    #screen_name = input("screen_name:")
    screen_name = 'Sakurai_Absol'

    list_id = get_list_id(screen_name)

    list_member_to_csv(list_id)


if __name__ == '__main__':
    main()