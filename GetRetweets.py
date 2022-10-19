import requests
import os
import json
import sys 
import time 
import csv

bearer_token = ""
tweet_id = ""

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


def get_parameters(): 
    params = { 
        
        "user.fields": "username,created_at",
        "tweet.fields": "created_at",
        "max_results": "100",
        
    }

    return (params)


def get_replies(parameters):

    replies = []

    search_url = f"https://api.twitter.com/2/tweets/{tweet_id}/retweeted_by"
    
    
    
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
            with open('retweetsdata.csv', 'a') as csv_file:  
                writer = csv.writer(csv_file , delimiter=',')
                
                writer.writerows(zip([reply['username']],[reply['id']],[reply['created_at']]))
       
        if "next_token" not in meta:
            break
        next_token = meta["next_token"]
        parameters.update(pagination_token=next_token)
        # parameters["pagination_token"] = meta["next_token"]
        time.sleep(1)

    return replies

def main():
    parameters = get_parameters()
    replies = get_replies(parameters)
    print(replies)


if __name__ == "__main__":
    main()