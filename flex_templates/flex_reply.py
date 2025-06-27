import json

def flex_no_book():
    flex_pattern_no_books = {
                        "type": "bubble",
                        "header": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": "There are no books that match your interests.",
                                "size": "md",
                                "color": "#FFFFF0",
                                "weight": "bold",
                                "wrap": True,
                            }
                            ]
                        },
                        "styles": {
                            "header": {
                            "backgroundColor": "#990000"
                            }
                        }
                        }
    
    flex_json = json.dumps(flex_pattern_no_books)

    return flex_json

def flex_pattern_first():
    flex_pattern_1 = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "RECOMMENDED",
                            "size": "xl",
                            "weight": "bold"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Name",
                                    "color": "#a9a7b5",
                                    "size": "xs"
                                },
                                {
                                    "type": "text",
                                    "text": "BIBID",
                                    "align": "end",
                                    "size": "xs",
                                    "color": "#a9a7b5"
                                }
                            ]
                        },
                        {
                            "type": "separator"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "BOOK1",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "text",
                                            "text": "100001",
                                            "align": "end",
                                            "size": "sm"
                                        }
                                    ],
                                    "margin": "xs",
                                    "spacing": "none",
                                    "action": {
                                        "type": "uri",
                                        "label": "action",
                                        "uri": "https://www.youtube.com/watch?v=qIBWRPqJcGQ"
                                    }
                                },
                                {
                                    "type": "separator",
                                    "margin": "md"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "BOOK2",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "text",
                                            "text": "100002",
                                            "align": "end",
                                            "size": "sm"
                                        }
                                    ],
                                    "margin": "md",
                                    "spacing": "none",
                                    "action": {
                                        "type": "uri",
                                        "label": "action",
                                        "uri": "https://www.youtube.com/watch?v=XIOoqJyx8E4"
                                    }
                                },
                                {
                                    "type": "separator",
                                    "margin": "md"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "BOOK3",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "text",
                                            "text": "100003",
                                            "align": "end",
                                            "size": "sm"
                                        }
                                    ],
                                    "margin": "md",
                                    "action": {
                                        "type": "uri",
                                        "label": "action",
                                        "uri": "https://www.youtube.com/watch?v=NyUTYwZe_l4"
                                    }
                                }
                            ]
                        },
                        {
                            "type": "separator"
                        }
                    ],
                    "margin": "none",
                    "spacing": "md"
                },
                "size": "giga"
            }
    
    flex_json = json.dumps(flex_pattern_1)

    return flex_json
    

# ต้องใช้ wrap ถึงใช้ \n ได้
def flex_pattern_second():
    flex_pattern_2 = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "BOOK1",
                            "color": "#FFFFFF",
                            "margin": "none",
                            "size": "md",
                            "weight": "bold"
                        }
                    ],
                    "spacing": "xs"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Description:",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
                            "size": "xs",
                            "wrap": True
                        }
                    ],
                    "height": "200px"
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "separator",
                            "margin": "none"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "Views",
                                "uri": "https://www.youtube.com/watch?v=afMgZy2lAWs"
                            },
                            "style": "secondary",
                            "margin": "lg"
                        }
                    ]
                },
                "styles": {
                    "header": {
                        "backgroundColor": "#000000"
                    }
                }
            },

            {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "BOOK2",
                            "color": "#FFFFFF",
                            "margin": "none",
                            "size": "md",
                            "weight": "bold"
                        }
                    ],
                    "spacing": "xs"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Description:",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit,sed do eiusmod",
                            "size": "xs",
                            "wrap": True
                        }
                    ],
                    "height": "200px"
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "separator",
                            "margin": "none"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "Views",
                                "uri": "https://www.youtube.com/watch?v=afMgZy2lAWs"
                            },
                            "style": "secondary",
                            "margin": "lg"
                        }
                    ]
                },
                "styles": {
                    "header": {
                        "backgroundColor": "#000000"
                    }
                }
            },

            {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "BOOK3",
                            "color": "#FFFFFF",
                            "margin": "none",
                            "size": "md",
                            "weight": "bold"
                        }
                    ],
                    "spacing": "xs"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Description:",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit,\\nsed do eiusmod",
                            "size": "xs",
                            "wrap": True
                        }
                    ],
                    "height": "200px"
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "separator",
                            "margin": "none"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "Views",
                                "uri": "https://www.youtube.com/watch?v=afMgZy2lAWs"
                            },
                            "style": "secondary",
                            "margin": "lg"
                        }
                    ]
                },
                "styles": {
                    "header": {
                        "backgroundColor": "#000000"
                    }
                }
            },

            {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "BOOK4",
                            "color": "#FFFFFF",
                            "margin": "none",
                            "size": "md",
                            "weight": "bold"
                        }
                    ],
                    "spacing": "xs"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Description:",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit,\\nsed do eiusmod",
                            "size": "xs",
                            "wrap": True
                        }
                    ],
                    "height": "200px"
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "separator",
                            "margin": "none"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "Views",
                                "uri": "https://www.youtube.com/watch?v=afMgZy2lAWs"
                            },
                            "style": "secondary",
                            "margin": "lg"
                        }
                    ]
                },
                "styles": {
                    "header": {
                        "backgroundColor": "#000000"
                    }
                }
            },

            {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "BOOK5",
                            "color": "#FFFFFF",
                            "margin": "none",
                            "size": "md",
                            "weight": "bold"
                        }
                    ],
                    "spacing": "xs"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Description:",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit,\\nsed do eiusmod",
                            "size": "xs",
                            "wrap": True
                        }
                    ],
                    "height": "200px"
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "separator",
                            "margin": "none"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "Views",
                                "uri": "https://www.youtube.com/watch?v=afMgZy2lAWs"
                            },
                            "style": "secondary",
                            "margin": "lg"
                        }
                    ]
                },
                "styles": {
                    "header": {
                        "backgroundColor": "#000000"
                    }
                }
            }
        ]
    }

    flex_json = json.dumps(flex_pattern_2)

    return flex_json

def flex_answer_custom(books=["Book 1", "Book 2", "Book 3", "Book 4"], bibid=["101", "102", "103", "104"]): # n = number of bubble
    content_list_bubbles = []

    for i in range(len(books)):
        contents = {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": books[i].title(),
                                "color": "#FFFFFF",
                                "margin": "none",
                                "size": "md",
                                "weight": "bold",
                            }
                        ],
                        "spacing": "xs"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Description:",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
                                "size": "xs",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": f"BIBID: {bibid[i]}",
                                "align": "end",
                                "size": "xs",
                                "style": "italic",
                                "decoration": "underline",
                                "margin": "xxl"
                            },
                        ],
                        "height": "200px"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "separator",
                                "margin": "none"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "Views",
                                    "uri": f"https://opac.lib.kmutt.ac.th/vufind/Record/{bibid[i]}"
                                },
                                "style": "secondary",
                                "margin": "lg"
                            }
                        ]
                    },
                    "styles": {
                        "header": {
                            "backgroundColor": "#000000"
                        }
                    }
                }
        content_list_bubbles.append(contents)
        
    flex_pattern_2 = {
        "type": "carousel",
        "contents": content_list_bubbles
    }

    flex_json = json.dumps(flex_pattern_2)

    return flex_json



def flex_answer(books=["Book 1", "Book 2", "Book 3", "Book 4"], bibid=["101", "102", "103", "104"], description=["Des1", "Des2", "Des3"]):
    content_list_bubbles = []

    for i in range(len(books)):
        contents = {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": books[i].title(),
                                "color": "#FFFFFF",
                                "margin": "none",
                                "size": "md",
                                "weight": "bold",
                            }
                        ],
                        "spacing": "xs"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Description:",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": f"\n{description[i]}",
                                "size": "xs",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": f"BIBID: {bibid[i]}",
                                "align": "end",
                                "size": "xs",
                                "style": "italic",
                                "decoration": "underline",
                                "margin": "xxl"
                            },
                        ],
                        "height": "275px"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "separator",
                                "margin": "none"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "Views",
                                    "uri": f"https://opac.lib.kmutt.ac.th/vufind/Record/{bibid[i]}"
                                },
                                "style": "secondary",
                                "margin": "lg"
                            }
                        ]
                    },
                    "styles": {
                        "header": {
                            "backgroundColor": "#000000"
                        }
                    }
                }
        content_list_bubbles.append(contents)
        
    flex_pattern_2 = {
        "type": "carousel",
        "contents": content_list_bubbles
    }

    flex_json = json.dumps(flex_pattern_2)

    return flex_json