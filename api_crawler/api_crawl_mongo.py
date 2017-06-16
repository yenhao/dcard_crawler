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

def crawl_comments(post_id, db):
    json_list = []
    comment_floor = 0

    while True:
        query_url = basic_comment_url + str(post_id) + '/comments?after=' + str(comment_floor)
        return_json = requests.get(url=query_url).json()
        json_list += [i for i in return_json]
        
        if checkNext(return_json): break

        comment_floor += 30
        time.sleep(1)

    if len(json_list) >0:
        db.comments.insert_many(json_list) # Insert to DB

def crawl(post_id, db):
    """
    Crawl post json first, then crawl comments.
    """
    post_id_str = str(post_id)
    print('Crawling Post : ' + post_id_str)

    query_post_url = basic_post_url + str(post_id)

    """ api query fail check """
    try:
        post_json = requests.get(url=query_post_url).json()
        if post_json.get("error") is not None:
            print('\tError response : ' + post_json.get("message"))
            return None
        
        db.posts.insert(post_json) # Insert to DB
    except:
        print('\tWierd response : No json found! Re-crawl in 15 second..')
        time.sleep(15)
        crawl(post_id, db)
        return None



    crawl_comments(post_id, db)



if __name__ == '__main__':
    conn = MongoClient(host="127.0.0.1", port=27017)    #connect to mongodb
    db = conn.dcard

    for post_id in range(224040289,226000000):
        crawl(post_id, db)
        


