import json
import time

def flex_rating_bub(query, bibid_list, user_id):
    unix_time = int(time.time())
    flex_pattern_no_books ={
                                "type": "bubble",
                                "header": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "Rating ",
                                        "size": "xl",
                                        "weight": "bold"
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "lg"
                                    }
                                    ]
                                },
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
                                        }
                                        ],
                                        "action": {
                                        "type": "postback",
                                        "label": "rating1",
                                        "displayText": "rating1",
                                        "data": f"1|{user_id}|{bibid_list}|{query}|{unix_time}"
                                        }
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "margin": "none"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
                                        }
                                        ],
                                        "margin": "xxl",
                                        "action": {
                                        "type": "postback",
                                        "label": "rating2",
                                        "data": f"2|{user_id}|{bibid_list}|{query}|{unix_time}",
                                        "displayText": "rating2"
                                        }
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
                                        }
                                        ],
                                        "margin": "xxl",
                                        "action": {
                                        "type": "postback",
                                        "label": "rating3",
                                        "data": f"3|{user_id}|{bibid_list}|{query}|{unix_time}",
                                        "displayText": "rating3"
                                        }
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
                                        }
                                        ],
                                        "margin": "xxl",
                                        "action": {
                                        "type": "postback",
                                        "label": "rating4",
                                        "data": f"4|{user_id}|{bibid_list}|{query}|{unix_time}",
                                        "displayText": "rating4"
                                        }
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                        }
                                        ],
                                        "margin": "xxl",
                                        "action": {
                                        "type": "postback",
                                        "label": "rating5",
                                        "data": f"5|{user_id}|{bibid_list}|{query}|{unix_time}",
                                        "displayText": "rating5"
                                        }
                                    }
                                    ]
                                },
                                "size": "nano"
                                }
    
    flex_json = json.dumps(flex_pattern_no_books)

    return flex_json