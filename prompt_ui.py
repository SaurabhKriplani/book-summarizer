from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate, load_prompt
import requests
from urllib.parse import quote

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    task = "text-generation"
)

model = ChatHuggingFace(llm = llm)



st.header('Book Summarizer Tool')

genre_input = st.selectbox( " Select Genre of book", ["Classic Literature", "Science Fiction", "Fantasy", "Self-Help / Productivity", "History / Non-Fiction"])

books = {
    "Classic Literature": [
        "Pride and Prejudice",
        "To Kill a Mockingbird",
        "The Great Gatsby",
        "Jane Eyre",
        "Wuthering Heights",
        "Crime and Punishment",
        "Anna Karenina",
        "The Catcher in the Rye",
        "The Adventures of Huckleberry Finn",
        "Moby-Dick"
    ],

    "Science Fiction": [
        "1984",
        "Dune",
        "The War of the Worlds",
        "The Time Machine",
        "Foundation",
        "Brave New World",
        "Fahrenheit 451",
        "Neuromancer",
        "The Martian",
        "Ender's Game"
    ],

    "Fantasy": [
        "The Hobbit",
        "The Lord of the Rings",
        "Harry Potter and the Philosopher's Stone",
        "Harry Potter and the Chamber of Secrets",
        "The Lion, the Witch and the Wardrobe",
        "The Name of the Wind",
        "A Game of Thrones",
        "The Eye of the World",
        "Eragon",
        "The Last Unicorn"
    ],

    "Self Help": [
        "Atomic Habits",
        "The 7 Habits of Highly Effective People",
        "Deep Work",
        "Think and Grow Rich",
        "The Power of Habit",
        "The Subtle Art of Not Giving a F*ck",
        "How to Win Friends and Influence People",
        "The Psychology of Money",
        "The One Thing",
        "Mindset"
    ],

    "History": [
        "Sapiens: A Brief History of Humankind",
        "Homo Deus",
        "Guns, Germs, and Steel",
        "The Silk Roads",
        "A People's History of the United States",
        "The Wright Brothers",
        "The Diary of a Young Girl",
        "The Rise and Fall of the Third Reich",
        "The Immortal Life of Henrietta Lacks",
        "The Second World War"
    ]
}

book_input = st.selectbox(" Select Book", books[genre_input])

length_input = st.selectbox(" Select Explaination Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explaination)"])

template = load_prompt('template.json')

# prompt = template.invoke({
#     'genre_input': genre_input,
#     'book_input': book_input,
#     'length_input': length_input
# })

if st.button('Summarize'):
    chain = template | model
    result = chain.invoke({
        'genre_input': genre_input,
        'book_input': book_input,
        'length_input': length_input
    })

# for image
    url = f"https://openlibrary.org/search.json?title={quote(book_input)}"
    data = requests.get(url).json()

    if data.get("docs"):
        cover_id = data["docs"][0].get("cover_i")

        if cover_id:
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
            left, center, right = st.columns([1, 2, 1])

            with center:
                st.image(cover_url, width=250)
        else:
            st.warning("No cover found.")
    else:
        st.error("Book not found.")
# for image ends


    # result = model.invoke(prompt)
    st.write(result.content)  
