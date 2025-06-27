import json
import time 
import pandas as pd
from groq import Groq
from fuzzywuzzy import fuzz
import os
from dotenv import load_dotenv

# โหลดตัวแปรจาก .env
load_dotenv()

df_search = pd.read_csv('df_search.csv')

def recommended(query, df_search=df_search):
    start_time = time.time()

    json_books_matched, json_books_llm = llm_recommended_search(query, df_search)
    end_time = time.time()
    answer = create_answer(json_books_matched)
    llm_books_json = create_llm_books(json_books_llm)
    
    if len(answer) == 0:
        return [], [], llm_books_json
    
    title_list = answer['Matched Title'].tolist()
    bibid_list = answer['BIBID'].tolist()
    # print(title_list)
    # print(bibid_list)
    # print(llm_books_json)
    print(f"Execution Time: {end_time - start_time} second")

    return title_list, bibid_list, llm_books_json


def llm_recommended_search(query, df_search, chunk=1):
    json_books_llm = []
    all_matched_books = []
    bibid_track = set()

    for i in range(chunk):

        json_books = llm_recommended(query, 30, json_books_llm)
        json_books_llm.extend(json_books)

        df_llm = clean_df_llm(json_books)

        matched_books, bibid_result = search_books(df_search, df_llm, bibid_track)

        bibid_track = bibid_track.union(bibid_result)

        all_matched_books.extend(matched_books)

        print(f"Chunk {i+1} completed, found {len(matched_books)} books, total {len(all_matched_books)} books")


    return all_matched_books, json_books_llm

def create_llm_books(json_books_llm):
    df = pd.DataFrame(json_books_llm)
    df_unique = df.drop_duplicates(subset=['Title', 'Author'])

    json_output = df_unique.to_json(orient="records", indent=4, force_ascii=False)

    return json_output

def create_answer(json_books_matched):
    if len(json_books_matched) > 0:
        df_books_matched = pd.DataFrame(json_books_matched)
        df_unique_matched = df_books_matched.drop_duplicates(subset=['Matched Title'], keep='first')

        if len(df_unique_matched) > 5:
            df_answer = df_unique_matched.sample(n=5)
            return df_answer

        return df_unique_matched
    return pd.DataFrame()

def clean_df_llm(json_books):
    df_llm = pd.DataFrame(json_books)

    if 'Title' not in df_llm.columns or 'Author' not in df_llm.columns:
        print("Warning: Missing 'Title' or 'Author' in DataFrame")
        # print(df_llm.head())  
        return pd.DataFrame() 
    
    df_llm['Title'] = df_llm['Title'].apply(lambda x: x.lower().strip())
    df_llm['Author'] = df_llm['Author'].apply(lambda x: x.lower().strip())

    return df_llm

def llm_recommended(query, request_count, existing_books):
    client = Groq(api_key=os.getenv("GROQ_API_KEY_1"))
    prompt = f"""You are an AI assistant recommending books.
    Please suggest {request_count} books related to the following query: "{query}". For each book, provide the title and author, separated by a comma.

    Example:
      Book Title 1, Author Name, ISBN
      Book Title 2, Author Name, ISBN

    Do not include books from the following list:
    {existing_books if existing_books else 'None'}

    Respond with the list of books in this format, each on a new line. Do not include any other explanations or text."""

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        stop=None,
    )

    response_text = completion.choices[0].message.content

    books_list = response_text.strip().split("\n")

    books_data = {
        "books": []
    }

    for book in books_list:
        parts = book.split(",")
        if len(parts) == 3:
            title = parts[0].strip()
            author = parts[1].strip()
            isbn = parts[2].strip()
            books_data["books"].append({"Title": title, "Author": author, "ISBN": isbn})

    return books_data.get("books", [])

def search_books(df, df_llm, bibid_track):
    results = []

    for _, row in df_llm.iterrows():
        title_query = row["Title"].lower()
        author_query = row["Author"].lower()

        filt = df['Title'].str.contains(title_query, case=False, na=False, regex=False)

        matched_rows = df[filt]

        for _, book in matched_rows.iterrows():
            book_author = book["Author"]
            book_bibid = book["BIBID"]

            author_score = fuzz.partial_token_sort_ratio(author_query, book_author)
            author_match = author_score > 78

            if author_match and (book_bibid not in bibid_track):
                bibid_track.add(book_bibid)
                results.append({
                    "BIBID": book["BIBID"],
                    "Matched Title": book["Title"],
                    "Matched Author": book["Author"],
                    "Original Title": row["Title"],
                    "Original Author": row["Author"],
                    "Fuzzy Score": author_score
                })


    return results, bibid_track

if __name__ == "__main__":
    recommended("Beginner for python books.", df_search)