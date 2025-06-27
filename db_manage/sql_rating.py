import psycopg2

def connect_db():
    return psycopg2.connect(
        host="localhost",
        dbname="ratings",
        user="postgres",
        password="phoom089",
        port=5432
    )


def manage_rating(score=3, user_id='A00', books_id=['101', '102', '103'], user_query="Hello world", time_query=100001):
    conn = connect_db()
    cursor = conn.cursor()

    # set value serial id เพราะตอน update มันนับเพิ่มทำให้เลข id มันกระโดด เลยต้องเช็ค id ล่าสุดเสมอ
    sql = """
    SELECT setval('user_ratings_id_seq', (SELECT COALESCE(MAX(id)) FROM user_ratings));
    """

    cursor.execute(sql)
    conn.commit()
    
    sql = """
    INSERT INTO public.user_ratings (score, user_id, books_id, user_query, time_query)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id, time_query)  
    DO UPDATE SET 
        score = EXCLUDED.score      
    RETURNING id, score, user_query;
    """

    cursor.execute(sql, (score, user_id, books_id, user_query, time_query))
     
    result = cursor.fetchone() # tuple --> (id, score, user_query)

    print(f'id {result[0]} has {result[1]} scores now. [{result[2]}].')
    conn.commit()
    

    cursor.close()  
    conn.close() 


if __name__ == "__main__":
    manage_rating()
