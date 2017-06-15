from pymongo import MongoClient
import requests
import time
import json

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
        
        if checkNext(return_json): break

        comment_floor += 30
        time.sleep(1)

    return json_list

def crawl(db, post_id):
    """
    Crawl post json first, then crawl comments.
    """
    post_id_str = str(post_id)
    print('Crawling Post : ' + post_id_str)

    query_post_url = basic_post_url + str(post_id)

    """ api query fail check """
    try:
        post_json = requests.get(url=query_post_url).json()
    except:
        print('\tWierd response : No json found!')
        time.sleep(15)
        return None

    if post_json.get("error"):
        print('\tError response : ' + post_json.get("message"))
        return None

    """ Save files """
    if os.path.isdir(folder_name + post_id_str):
        print('\tDuplicated File! ')
    else:
        os.makedirs(folder_name + post_id_str)
        time.sleep(3)

    with open(folder_name + post_id_str + '/post.json', 'w') as f:
        json.dump(post_json,f)

    with open(folder_name + post_id_str + '/comments.json', 'w') as f:
        json.dump(crawl_comments(post_id),f)



if __name__ == '__main__':
    conn = MongoClient(host="127.0.0.1", port=27017)    #connect to mongodb
    db = conn.dcard

    for post_id in reversed(range(220000000,226000000)):
        crawl(db, post_id)
        


