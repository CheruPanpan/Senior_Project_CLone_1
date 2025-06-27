import os
import re
import time
import json
import pandas as pd
import requests
import random

from flex_templates.flex_reply import *
from flex_templates.flex_rating import *
from db_manage.sql_rating import *
from recommend_package.recommended import recommended
from recommend_package.rec_test import recommended_test
from isbn_check import check_books
from generate_answer import Book_Recommendation
from send_query_ans import send_query_success
from dotenv import load_dotenv
from flex_templates.loading import loading_animation
from cleaned_text.cleaned_title import clened_title_thai

from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage,
    Emoji,
    FlexMessage,
)

from linebot.v3.messaging.models.flex_container import FlexContainer

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    PostbackEvent
)

app = Flask(__name__)

# โหลดตัวแปรจาก .env
load_dotenv()

# oa library
configuration = Configuration(access_token=os.getenv("LINE_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    
    # get request body as text
    body = request.get_data(as_text=True)

    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(PostbackEvent)
def handle_postback(event: PostbackEvent):
    current_timestamp = int(time.time())

    postback_data = event.postback.data
    
    part_sep = postback_data.split("|")
    score, user_id, books_id, user_query, postback_timestamp = int(part_sep[0]), part_sep[1], eval(part_sep[2]), part_sep[3], int(part_sep[4])
    
    time_difference = current_timestamp - postback_timestamp
    

    if time_difference > 900:
        send_back = "Cant rating now : time-expired!"
    else:
        manage_rating(score, user_id, books_id, user_query, postback_timestamp)
        send_back = "Thank you for your rating🌟⭐️."

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=send_back)]
                )
            )

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    status_send = False
    user_message = event.message.text.lower()
    message_id = event.message.id
    user_id = event.source.user_id
    time_stamp_query = event.timestamp

    response=[]

    if re.search(r'[\u0E00-\u0E7F]', event.message.text):
        response = [ TextMessage(text="📢 Please use English, Thai is not supported. ⚠️")]

    elif user_message == "pattern1":
        bubble_dict = flex_pattern_first()
        response = [ FlexMessage(alt_text="hello", contents=FlexContainer.from_json(bubble_dict)),
                     TextMessage(text="Descript Book1 ............"),
                     TextMessage(text="Descript Book2 ............"),
                     TextMessage(text="Descript Book3 ............")
                   ]
    elif user_message == "pattern2":
        bubble_dict = flex_pattern_second()
        response = [ TextMessage(text="From flex pattern 2!"),
                      FlexMessage(alt_text="hello", contents=FlexContainer.from_json(bubble_dict))
                   ]
    elif user_message == "pattern3":
        bubble_dict = flex_answer_custom()
        response = [ TextMessage(text="From flex pattern 3!"),
                     FlexMessage(alt_text="hello", contents=FlexContainer.from_json(bubble_dict))
                   ]
    elif user_message == "pattern4":
        response = [ TextMessage(text="📚❌ There are no books that match your interests.")]

    elif user_message == "rating":
        bubble_dict = flex_rating_bub("Hello world!", ["101", "102", "103"], event.source.user_id)
        response = [ FlexMessage(alt_text="Rating", contents=FlexContainer.from_json(bubble_dict))]
    elif user_message == "help":
        help_message = (
            "📚 Welcome to the Book Recommendation Chatbot! Here's how to use me:\n\n"
            "1️⃣ ✨Search for Books✨: Type a topic, genre, or keyword (e.g., 'mystery novels', 'science fiction') to get book recommendations.\n"
            "   - Example: 'mystery novels', 'romance books', 'artificial intelligence'\n"
            "2️⃣ ✨Rate Recommendations✨: After receiving book suggestions, use the rating buttons to let me know how you like them! ⭐️\n"
            "3️⃣ ✨Request New Books✨: If the recommendations aren't what you want, tap the 'Requesting books' option in the Rich Menu below.\n"
            "4️⃣ ✨Use English✨: I currently support English only, so please type your queries in English.\n"
            "💡 **Need help again?** Just type 'help' anytime!\n"
            "Happy reading! 📖✨"
        )
        response = [TextMessage(text=help_message)]
    else:
        print("START RECOMMEND")
        loading_animation(user_id)
        status_send = True
        title_list, bibid_list, llm_books_json = recommended_test(user_message)
        #title_list = clened_title_thai(title_list)

        if len(title_list) > 0:
            description = Book_Recommendation(title_list, user_message)
            
            # ปรับความยาวให้เท่ากันเพื่อป้องกัน IndexError
            if len(description) < len(title_list):
                for _ in range(len(title_list) - len(description)):
                     description.append("No description available.")
            elif len(description) > len(title_list):
                description = description[:len(title_list)] 
                
            bubble_dict = flex_answer(title_list, bibid_list, description)
            buble_dict_rating = flex_rating_bub(event.message.text, bibid_list, event.source.user_id)

            # ปรับข้อความให้ conversational และหลากหลายขึ้น
            greeting = random.choice([
                f"Wow, I found some great books for '{user_message}'! 📚✨",
                f"Here’s what I picked for '{user_message}'! Hope you love these! 😊",
                f"Check out these awesome books for '{user_message}'! 🎉"
            ])

            # ส่งข้อความทักทายก่อน
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=greeting)]
                    )
                )

            # ส่ง Flex Message, ข้อความแนะนำ, และการให้คะแนน (เรียงลำดับใหม่)
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.push_message(
                    PushMessageRequest(
                        to=user_id,
                        messages=[
                            FlexMessage(alt_text="Success!", contents=FlexContainer.from_json(bubble_dict)),
                            TextMessage(text="If the recommendations aren't what you want, tap the 'Requesting books' option in the Rich Menu below. 📚"),
                            FlexMessage(alt_text="Rating!", contents=FlexContainer.from_json(buble_dict_rating)),
                            TextMessage(text="We’d love your rate! ⭐️ Please rate the book suggestions above so we can improve your next recommendations. 🙏")
                        ]
                    )
                )
            
            # ส่งข้อมูลไปยัง API
            send_query_success(message_id, user_id, user_message, bibid_list, time_stamp_query, llm_books_json)
            return
        
            #response = [
             #   FlexMessage(alt_text="Success!", contents=FlexContainer.from_json(bubble_dict)),
              #  TextMessage(text=greeting),
               # FlexMessage(alt_text="Rating!", contents=FlexContainer.from_json(buble_dict_rating))
            #]
        else:
            # ปรับข้อความเมื่อไม่พบผลลัพธ์ให้เป็นมิตรและแนะนำทางเลือก
            response = [TextMessage(text=random.choice([
                f"Oops, I couldn’t find any books for '{user_message}.",
                f"Hmm, no matches for '{user_message}' yet. 📚 How about trying a different topic or keyword?",
                f"Sorry, nothing came up for '{user_message}'. 😔 Want to try another genre or topic?"
            ]))]
            
  
    if len(response) != 0:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=response
                )
            )

        if status_send:
            print("Send books")
            send_query_success(message_id, user_id, user_message, bibid_list, time_stamp_query, llm_books_json)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)

