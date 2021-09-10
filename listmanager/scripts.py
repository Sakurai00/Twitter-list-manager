from listmanager.function import *
from twapi.twapi import generate_api


def main() -> None:
    api = generate_api()
    if not os.path.exists(st.SAVE_PATH):
        os.makedirs(st.SAVE_PATH)

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
        make_csv_from_list(api, screen_name, mode)
    elif menu_id == 1:
        list_id = input("List ID:")
        file_name = input("CSV file name:")
        make_list_from_csv(api, list_id, file_name)
    elif menu_id == 2:
        screen_name = input("Screen name:")
        mode = int(input("Mode (0:Simple, 1:More info):"))
        make_csv_from_follow(api, screen_name, mode)
    elif menu_id == 3:
        file_name1 = input("File name 1:")
        file_name2 = input("File name 2:")
        diff_of_csv(file_name1, file_name2)
    elif menu_id == 4:
        list_name = input("List name:")
        mode = input("Mode(public or private):")
        list_id = create_list(api, list_name, mode)
        print("List ID: {}".format(list_id))
    elif menu_id == 5:
        screen_name = input("Screen name:")
        list_id = get_list_id(api, screen_name)
        print("List ID: {}".format(list_id))