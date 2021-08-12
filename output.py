import csv

import tweepy

import settings as st

auth = tweepy.OAuthHandler(st.CONSUMER_KEY, st.CONSUMER_SECRET)
auth.set_access_token(st.ACCESS_TOKEN_KEY, st.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def main():
    #screen_name = input("screen_name:")
    screen_name = '_r046'

    lists = api.lists_all(screen_name = screen_name)
    for list in lists:
        print(list.id, list.name)

    #id = input("choose id:")
    id = 885894452958470146

    f = open(screen_name + '.csv', 'a', encoding='UTF-8', newline="")
    writer = csv.writer(f)

    for member in tweepy.Cursor(api.list_members, list_id=id).items():
        #内部ID, 名前，ID
        writer.writerow([member.id, member.name, member.screen_name])


if __name__ == '__main__':
    main()
