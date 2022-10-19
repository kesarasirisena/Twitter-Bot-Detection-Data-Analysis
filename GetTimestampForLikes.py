import requests
import json
import time 
import sys 
import pandas as pd



bearer_token = ""
tweet_id = ""

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

    for i in id_list: 

        search_url = f"https://api.twitter.com/2/users/{i}/liked_tweets"

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
                
                if(reply['id'] == "1524897605322387456"): 
                    print(i)
                    print(reply)
            # if "next_token" not in meta:
                    break
            next_token = meta["next_token"]
            parameters.update(pagination_token=next_token)
            
            time.sleep(1)


    


def main():
    parameters = get_parameters()
    connect_to_endpoint(parameters)
    


if __name__ == "__main__":
    main()