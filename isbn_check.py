import requests
import json
def check_books(data):
    print("start check llm books")
    valid_books = []

    for book in data:
        isbn = book.get("ISBN")
        title = book.get("Title")
        author = book.get("Author")

        if isbn:
            url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
            response = requests.get(url).json()
            if "items" in response:
                # print(title, "found by isbn")
                valid_books.append(book)
                continue  
        
        if title and author:
            url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}+inauthor:{author}"
            response = requests.get(url).json()
            if "items" in response:
                # print(title, "found by title and author")
                valid_books.append(book)

    return valid_books

if __name__ == "__main__":
    books_data = [
        {
            "Title":"python crash course",
            "Author":"eric matthes",
            "ISBN":"1593279280"
        },
        {
            "Title":"python for data analysis",
            "Author":"wes mckinney",
            "ISBN":"1449319793"
        },
        {
            "Title":"a byte of python",
            "Author":"swaroop c h",
            "ISBN":"1449355730"
        },
        {
            "Title":"python basics: a practical introduction to python 3",
            "Author":"felix zumstein",
            "ISBN":"1484232736"
        },
        {
            "Title":"automate the boring stuff with python",
            "Author":"al sweigart",
            "ISBN":"1593275994"
        },
        {
            "Title":"python: the ultimate beginner's guide",
            "Author":"joshua r. brown",
            "ISBN":"1984563842"
        },
        {
            "Title":"python from scratch",
            "Author":"kenneth love",
            "ISBN":"1984563850"
        },
        {
            "Title":"introduction to machine learning with python",
            "Author":"andreas c. müller",
            "ISBN":"1449369413"
        },
        {
            "Title":"head first python",
            "Author":"paul barry",
            "ISBN":"1449340115"
        },
        {
            "Title":"python for beginners",
            "Author":"mike mcgrath",
            "ISBN":"1484232744"
        },
        {
            "Title":"python 3 object-oriented programming",
            "Author":"dusty phillips",
            "ISBN":"1787287717"
        },
        {
            "Title":"python: a crash course",
            "Author":"john paul mueller",
            "ISBN":"1119231307"
        },
        {
            "Title":"python algorithms",
            "Author":"magnus lie hetland",
            "ISBN":"1593274041"
        },
        {
            "Title":"learning python application development",
            "Author":"ninad sathaye",
            "ISBN":"1484232752"
        },
        {
            "Title":"python: the complete guide for beginners",
            "Author":"william sullivan",
            "ISBN":"1984563869"
        },
        {
            "Title":"python: a pocket guide",
            "Author":"mark lutz",
            "ISBN":"1449340114"
        },
        {
            "Title":"a practical introduction to python for beginners",
            "Author":"ahmed fawzy gad",
            "ISBN":"1984563877"
        },
        {
            "Title":"python programming for beginners",
            "Author":"jeeva s. chelladhurai",
            "ISBN":"1484232779"
        },
        {
            "Title":"python: an introduction to programming",
            "Author":"michael dawson",
            "ISBN":"1449340122"
        },
        {
            "Title":"python programming for rookies",
            "Author":"kirill eremenko",
            "ISBN":"1984563885"
        },
        {
            "Title":"python: the fundamentals",
            "Author":"peter cook",
            "ISBN":"1984563893"
        },
        {
            "Title":"python: a quick-start guide for beginners",
            "Author":"daniel p. fults",
            "ISBN":"1984563907"
        },
        {
            "Title":"python for scientists",
            "Author":"john paul mueller",
            "ISBN":"1119231315"
        },
        {
            "Title":"python: the ultimate guide",
            "Author":"thomas w. deters",
            "ISBN":"1984563915"
        },
        {
            "Title":"python in 24 hours",
            "Author":"kumar saurabh",
            "ISBN":"1984563923"
        },
        {
            "Title":"python: a step-by-step guide",
            "Author":"robert t. olson",
            "ISBN":"1984563931"
        }
    ]

    valid_books = check_books(books_data)

    # print(valid_books)
