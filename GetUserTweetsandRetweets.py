import requests
import json
import time 
import sys 
import pandas as pd
import csv


bearer_token = ""


df = pd.read_csv('likesdata.csv')

id_list = df['AuthorID']


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2LikedTweetsPython"
    return r


def get_parameters(): 
    params = { 
        
        
        "tweet.fields": "author_id,created_at",
        "max_results": "100",
        
    }

    return (params)




def connect_to_endpoint(parameters):
    replies = []

    

    search_url = f"https://api.twitter.com/2/users/1059197545/tweets"

    while True:
        response = requests.request(
            "GET", search_url, auth=bearer_oauth, params=parameters
        )
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        response_payload = response.json()
        meta = response_payload["meta"]
        if meta["result_count"] == 0:
            sys.exit("No replies to analyze")
        for reply in response_payload["data"]:
            replies.append(reply)
            with open('Warlockyone.csv', 'a') as csv_file:  
                writer = csv.writer(csv_file , delimiter=',')
                
                writer.writerows(zip([reply['text']],[reply['author_id']],[reply['id']],[reply['created_at']]))
        
        if "next_token" not in meta:
                break
        next_token = meta["next_token"]
        parameters.update(pagination_token=next_token)
        
        time.sleep(1)