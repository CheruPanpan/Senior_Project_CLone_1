from groq import Groq
import os
from dotenv import load_dotenv

# โหลดตัวแปรจาก .env
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY_2"))

def recommend_book_groq(User_query, Book_Title_list, model):
  completion = client.chat.completions.create(
    model= model,
    messages=[{
            "role": "system",
            "content": f"""
    ### Instruction:
    You are a knowledgeable and friendly book guide.
    Besides, your speech is not repetitive.

    Your job is to recommending books based on user's query and list of books that you received. Provide thoughtful recommendations and brief summaries, considering genre, author, and themes.
    Provide a direct and concise recommendation, including a brief summary of the book.

    ### Details of input:
    User's query: {User_query}
    You will recommend this list of books: {Book_Title_list}
    
    ### Notes:
    - Do not ask follow-up questions or make conversational remarks.
    - Do not repeat the recommendation in the response.
    - VERY IMPORTANT, In each book's recommendation MUST NOT over 175 words.
    - After finish each book's recommendation, you must start a next book's recommendation in the new line.
    - You must recommend book in the order within the list of books provided
    - You can say "Sorry, I don't know about this book." if you do not know about that book, you must not give a created fake information.

    Now respond in a friendly way:
    """,
        }
              ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
  )
  return completion.choices[0].message.content

# This function use list of books, user query, model
def Book_Recommendation(List_of_books, User_query, model= "llama-3.3-70b-versatile"):

  # LLM generates recommendation for each book
  Recommendation = recommend_book_groq(User_query, List_of_books, model) # create recommendation for each book

  Recommendation_list = Recommendation.split("\n\n \n") # split each recommendation with \n\n \n and for containing recommendation for each book

  # Return list of recommendation
  return Recommendation_list

if __name__ == "__main__":
    books = ["Python Programming : an introduction to computer science",
             "Learning Python",
             "Python for everybody : exploring data using Python 3",
             ]
    generate_answer = Book_Recommendation(books, "Beginner for python books.")
    for i in range(len(generate_answer)):
      print(f"Description {i+1} : {generate_answer[i]} \n")