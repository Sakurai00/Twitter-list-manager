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

    f = open(screen_name + '.csv', 'w', encoding='UTF-8', newline="")
    writer = csv.writer(f)

    writer.writerow(["内部ID", "名前", "ID", "フォロー数", "フォロワー数", "URL", "bio"])
    for member in tweepy.Cursor(api.list_members, list_id=id).items():
        #print(member)
        writer.writerow([member.id, member.name, member.screen_name, member.friends_count, member.followers_count, member.url, member.description])


if __name__ == '__main__':
    main()