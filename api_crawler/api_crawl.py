import requests
import time
import json
import sys
import os

basic_post_url = 'https://www.dcard.tw/_api/posts/'
basic_comment_url = 'https://www.dcard.tw/_api/posts/'

def checkNext(return_json, lower_bound = 30):
    if len(return_json) < lower_bound:
        return True
    else:
        return False


def crawl_comments(post_id):
    json_list = []
    comment_floor = 0

    while True:
        query_url = basic_comment_url + str(post_id) + '/comments?after=' + str(comment_floor)
        return_json = requests.get(url=query_url).json()
        
        json_list += [i for i in return_json]
        comment_floor += 30

        if checkNext(return_json): break

        time.sleep(1)

    return json_list

def crawl(post_id):
    """
    Crawl post json first, then crawl comments.
    """

    post_id_str = str(post_id)
    print('Crawling Post : ' + post_id_str)

    query_post_url = basic_post_url + str(post_id)
    post_json = requests.get(url=query_post_url).json()

    """ api query fail check """
    if post_json.get("error"):
        print('Error response : ' + post_json.get("message"))
        return None

    """ Save files """
    if not os.path.isdir(folder_name + post_id_str):
        os.makedirs(folder_name + post_id_str)

    with open(folder_name + post_id_str + '/post.json', 'w') as f:
        json.dump(post_json,f)

    with open(folder_name + post_id_str + '/comments.json', 'w') as f:
        json.dump(crawl_comments(post_id),f)

if __name__ == '__main__':
    folder_name = 'range_post/'

    for post_id in range(226580000,226590000):
        crawl(post_id)
        time.sleep(5)


