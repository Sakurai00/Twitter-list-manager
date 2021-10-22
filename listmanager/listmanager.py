import os

from twapi.twapi import generate_api_v1, generate_api_v2

import listmanager.settings as st
from listmanager.function import (
    block_to_csv,
    make_csv_from_list,
    make_list_from_csv,
    follow_to_csv,
    diff_of_csv,
    get_list_id,
    set_screen_name,
)


def main() -> None:
    api = generate_api_v1()
    client = generate_api_v2()

    if not os.path.exists(st.SAVE_PATH):
        os.makedirs(st.SAVE_PATH)

    print("API User: {}".format(api.verify_credentials().screen_name))
    print(
        "Menu\n\
        0: list -> csv\n\
        1: csv -> list\n\
        2: follow -> csv\n\
        3: diff of csv\n\
        4: create list\n\
        5: list up Lists\n\
        6: block user -> csv"
    )
    menu_id = int(input("Menu ID:"))

    if menu_id == 0:
        screen_name = set_screen_name(api)
        mode = int(input("Mode (0:All, 1:Single):"))
        make_csv_from_list(api, screen_name, mode)

    elif menu_id == 1:
        list_id = input("List ID:")
        file_name = input("CSV file name:")
        make_list_from_csv(api, list_id, file_name)

    elif menu_id == 2:
        username = set_screen_name(api)
        follow_to_csv(client, username)

    elif menu_id == 3:
        file_name1 = input("File name 1:")
        file_name2 = input("File name 2:")
        new_file_name = input("New file name:")
        diff_of_csv(file_name1, file_name2, new_file_name)

    elif menu_id == 4:
        list_name = input("List name:")
        mode = input("Mode(public or private):")
        # API v2は存在するが，tweepy非対応．
        list_id = api.create_list(name=list_name, mode=mode).id
        print("List ID: {}".format(list_id))

    elif menu_id == 5:
        screen_name = set_screen_name(api)
        list_id = get_list_id(api, screen_name)
        print("List ID: {}".format(list_id))
    elif menu_id == 6:
        block_to_csv(api, client)
