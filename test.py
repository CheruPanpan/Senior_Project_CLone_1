import json
import requests
from datetime import datetime
import pytz  # เพิ่ม import pytz
import uuid  # เพิ่ม import uuid สำหรับสร้าง unique ID
import time  # เพิ่ม import time สำหรับ delay ระหว่าง requests

def generate_mock_books_with_queries(user_id, test_case="normal"):
    books = []
    user_queries = []
    
    # สร้างเวลาในโซน Asia/Bangkok
    tz = pytz.timezone('Asia/Bangkok')

    if test_case == "sequential_prompts":
        # สร้าง prompts และหนังสือแนะนำเป็นลำดับ (เพิ่มเป็น 5 queries)
        conversations = [
            {
                "prompt": "แนะนำหนังสือเกี่ยวกับ Python สำหรับผู้เริ่มต้น",
                "books": [
                    {"title": "Python Crash Course", "author": "Eric Matthes", "isbn": "1593279280"},
                    {"title": "Learning Python", "author": "Mark Lutz", "isbn": "1449355730"}
                ]
            },
            {
                "prompt": "อยากได้หนังสือ Data Science",
                "books": [
                    {"title": "Data Science from Scratch", "author": "Joel Grus", "isbn": "1492041130"},
                    {"title": "Python for Data Analysis", "author": "Wes McKinney", "isbn": "1449319793"},
                    {"title": "Practical Statistics for Data Scientists", "author": "Peter Bruce", "isbn": "1491952962"}
                ]
            },
            {
                "prompt": "แนะนำหนังสือ Machine Learning",
                "books": [
                    {"title": "Hands-On Machine Learning", "author": "Aurélien Géron", "isbn": "1492032646"},
                    {"title": "Introduction to Machine Learning with Python", "author": "Andreas Müller", "isbn": "1449369413"}
                ]
            },
            {
                "prompt": "อยากได้หนังสือเกี่ยวกับ Deep Learning",
                "books": [
                    {"title": "Deep Learning with Python", "author": "François Chollet", "isbn": "1617294438"},
                    {"title": "Deep Learning for Vision Systems", "author": "Mohamed Elgendy", "isbn": "1617296198"},
                    {"title": "Deep Learning from Scratch", "author": "Seth Weidman", "isbn": "1492041416"}
                ]
            },
            {
                "prompt": "แนะนำหนังสือ AI และ Neural Networks",
                "books": [
                    {"title": "Neural Networks from Scratch", "author": "Harrison Kinsley", "isbn": "0992461227"},
                    {"title": "Artificial Intelligence: A Modern Approach", "author": "Stuart Russell", "isbn": "0134610997"}
                ]
            }
        ]

        for conv in conversations:
            query_id = str(uuid.uuid4()).replace("-", "")[:16]
            time_stamp = int(datetime.now(tz).timestamp())
            
            # สร้าง user query
            user_queries.append({
                "query_id": query_id,
                "user_line_id": user_id,
                "user_query": conv["prompt"],
                "response_success": "false",
                "time_stamp": time_stamp
            })
            
            # สร้างหนังสือแนะนำสำหรับ query นี้
            for book in conv["books"]:
                books.append({
                    "title": book["title"],
                    "author": book["author"],
                    "isbn": book["isbn"],
                    "query_id": query_id
                })

    elif test_case == "normal":
        # กรณีปกติ: 1 query, 5 books
        query_id = str(uuid.uuid4()).replace("-", "")[:16]
        books = [
            {"title": "Deep Learning for Computer Vision with Python", "author": "Adrian Rosebrock", "isbn": "1491974653"},
            {"title": "Deep Learning: A Practitioner's Approach", "author": "Josh Patterson", "isbn": "1484225335"},
            {"title": "Hands-On Machine Learning for .NET Developers", "author": "Jason De Oliveira", "isbn": "148424447X"},
            {"title": "Hands-On Machine Learning with AutoML", "author": "Ahmed Fawzy Gad", "isbn": "180107333X"},
            {"title": "Hands-On Machine Learning with JavaScript", "author": "Dustin H. Butler", "isbn": "1801811305"},
        ]
        user_queries.append({
            "query_id": query_id,
            "user_line_id": user_id,
            "user_query": "I want books about machine learning",
            "response_success": "false",
            "time_stamp": time_stamp
        })
        books = [{"title": b["title"], "author": b["author"], "isbn": b["isbn"], "query_id": query_id} for b in books]

    elif test_case == "multiple_queries":
        # กรณีหลาย queries พร้อมกัน
        topics = ["python", "javascript", "machine learning"]
        for topic in topics:
            query_id = str(uuid.uuid4()).replace("-", "")[:16]
            user_queries.append({
                "query_id": query_id,
                "user_line_id": user_id,
                "user_query": f"I want books about {topic}",
                "response_success": "false",
                "time_stamp": time_stamp
            })
            # สร้างหนังสือ 2 เล่มต่อ query
            topic_books = [
                {"title": f"Learning {topic.title()} Vol.1", "author": f"Author {topic}", "isbn": str(uuid.uuid4())[:10]},
                {"title": f"Advanced {topic.title()} Vol.2", "author": f"Author {topic}", "isbn": str(uuid.uuid4())[:10]}
            ]
            books.extend([{"title": b["title"], "author": b["author"], "isbn": b["isbn"], "query_id": query_id} for b in topic_books])

    elif test_case == "no_books":
        # กรณีไม่มีหนังสือแนะนำ
        query_id = str(uuid.uuid4()).replace("-", "")[:16]
        user_queries.append({
            "query_id": query_id,
            "user_line_id": user_id,
            "user_query": "I want books about quantum computing",
            "response_success": "false",
            "time_stamp": time_stamp
        })

    elif test_case == "invalid_data":
        # กรณีข้อมูลไม่สมบูรณ์
        query_id = str(uuid.uuid4()).replace("-", "")[:16]
        books = [
            {"title": "Invalid Book", "isbn": "1234567890"},  # ไม่มี author
            {"author": "Unknown Author"},  # ไม่มี title
            {"title": "Complete Book", "author": "Valid Author", "isbn": "0987654321"}
        ]
        user_queries.append({
            "query_id": query_id,
            "user_line_id": user_id,
            "user_query": "Test invalid data",
            "response_success": "false",
            "time_stamp": time_stamp
        })
        books = [dict(b, query_id=query_id) for b in books]

    return books, user_queries

def send_books_to_server(test_case="normal"):
    user_id = "Ud307c81b47562cb25928828706f081a9"
    
    if test_case == "sequential_prompts":
        books, user_queries = generate_mock_books_with_queries(user_id, test_case)
        # แบ่ง queries และ books ตาม conversation
        query_groups = {}
        for query in user_queries:
            query_groups[query["query_id"]] = {
                "query": query,
                "books": [b for b in books if b["query_id"] == query["query_id"]]
            }
        
        print(f"\nทดสอบการส่ง {len(query_groups)} queries ตามลำดับ:")
        print("="*50)
        
        # ส่งข้อมูลทีละ conversation
        for i, (query_id, data) in enumerate(query_groups.items(), 1):
            url = "http://localhost:3001/api/sync-books"
            headers = {"Content-Type": "application/json"}
            
            payload = {
                "userId": user_id,
                "books": data["books"],
                "userQueries": [data["query"]]
            }
            
            try:
                print(f"\nQuery ที่ {i}/{len(query_groups)}")
                print(f"Prompt: {data['query']['user_query']}")
                print(f"จำนวนหนังสือที่แนะนำ: {len(data['books'])} เล่ม")
                print("\nส่งข้อมูลไปที่ server...")
                
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    result = response.json()
                    print(f"สถานะ: สำเร็จ")
                    print(f"จำนวนหนังสือที่ verified: {len(result.get('data', []))} เล่ม")
                else:
                    print(f"สถานะ: ล้มเหลว ({response.status_code})")
                    print(f"ข้อผิดพลาด: {response.text}")
                
                print("-"*50)
                # รอ 2 วินาทีก่อนส่ง request ถัดไป
                time.sleep(2)
                
            except requests.exceptions.RequestException as e:
                print(f"เกิดข้อผิดพลาดในการส่งข้อมูล: {e}")
                print("-"*50)
    
    else:
        # โค้ดเดิมสำหรับ test cases อื่นๆ
        books, user_queries = generate_mock_books_with_queries(user_id, test_case)
        url = "http://localhost:3001/api/sync-books"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "userId": user_id,
            "books": books,
            "userQueries": user_queries
        }
        
        try:
            print(f"\nTesting case: {test_case}")
            print("Sending payload:", json.dumps(payload, indent=2))
            
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                print(f"Test case '{test_case}' successful:", response.json())
            else:
                print(f"Test case '{test_case}' failed: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error in test case '{test_case}': {e}")

if __name__ == "__main__":
    # ทดสอบเฉพาะกรณี sequential_prompts
    send_books_to_server("sequential_prompts")