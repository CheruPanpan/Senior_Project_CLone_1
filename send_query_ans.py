import json
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

def reformat_json(books, message_id):
    return [{"title": book["Title"], "author":book["Author"], "isbn": book["ISBN"], "query_id": str(message_id)} for book in books]

def send_query_success(message_id, user_id, user_message, bibid_list, time_stamp_query, books):
    # response_success_str = ",".join(map(str, bibid_list))

    books = reformat_json(books, message_id)

    if len(bibid_list) > 0:
        status = "true"
    else:
        status = "false"

    data = {
        "userId": str(user_id),
        "books": books,
        "userQueries": [  
                {
                    "query_id": str(message_id),
                    "user_line_id":str(user_id),
                    "user_query": str(user_message),
                    "response_success": status,
                    "timestamp": str(time_stamp_query),
                }          
            ]
        }
    

    #api_url = "https://ab2f3a9f0805.ngrok.app/api/sync-books"
    api_url=os.getenv("api_url")

    headers = {"Content-Type": "application/json"} 
    response_api = requests.post(api_url, data=json.dumps(data), headers=headers)
    print("Status Code:", response_api.status_code)
    # print("Response:", response_api.text)