import sys
import requests
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
        "query": f"conversation_id:{tweet_id}",
        "tweet.fields": "in_reply_to_user_id,author_id,conversation_id,entities,created_at",
        "max_results": "100",
    }
    

    return (params, tweet_id)


def get_replies(parameters):

    replies = []

    search_url = "https://api.twitter.com/2/tweets/search/recent"
    

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
       
        if "next_token" not in meta:
            break
        next_token = meta["next_token"]
        parameters.update(next_token=next_token)
        time.sleep(1)

    return replies


def get_author(tweet_id):
    tweet_lookup_url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    parameters = {
        "tweet.fields": "author_id",
        "expansions": "author_id",
        "user.fields": "username",
    }

    response = requests.request(
        "GET", tweet_lookup_url, auth=bearer_oauth, params=parameters
    )

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    response_payload = response.json()
    author_id = response_payload["data"]["author_id"]
    for user in response_payload["includes"]["users"]:
        author_username = user["username"]

    return (author_id, author_username)


def get_usernames(author_id, replies): 
    usernames = []
    texts = []
    timestamps = []
    authorids = []

    for reply in replies:
        
        if reply["in_reply_to_user_id"] == author_id:
            for mention in reply["entities"]["mentions"]:
                usernames.append(mention["username"])
            timestamps.append(reply["created_at"])
            texts.append(reply["text"])
            authorids.append(reply['author_id'])

    return usernames, texts, timestamps, authorids




def results(texts, timestamps, authorids):
    headers = ["Text", "AuthorID","Timestamp"]
    
    with open('tweetdatanew.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file , delimiter=',')
        writer.writerow(headers)
        for i,j,k in zip(texts, authorids, timestamps):
            writer.writerows(zip([i],[j],[k]))
        
        


if __name__ == "__main__":
    parameters, original_tweet_id = get_parameters()
    replies = get_replies(parameters)
    author_id, author_username = get_author(original_tweet_id)
    usernames, texts, timestamps, authorids = get_usernames(author_id, replies)
    
    results(texts, timestamps, authorids)