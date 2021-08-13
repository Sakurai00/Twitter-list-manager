import csv

import tweepy

from twapi import generate_api


api = generate_api()

def main():
    #screen_name = input("screen_name:")
    screen_name = 'Sakurai_Absol'

    lists = api.lists_all(screen_name = screen_name)
    for list in lists:
        print(list.id, list.name)

    id = input("choose id:")
    #id = 885894452958470146

    f = open(screen_name + '.csv', 'a', encoding='UTF-8', newline="")
    writer = csv.writer(f)

    for member in tweepy.Cursor(api.list_members, list_id=id).items():
        #内部ID, 名前，ID
        writer.writerow([member.id, member.name, member.screen_name])


if __name__ == '__main__':
    main()
