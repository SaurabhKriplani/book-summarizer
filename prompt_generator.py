from langchain_core.prompts import PromptTemplate


template = PromptTemplate(
    input_variables=["genre_input", "book_input", "length_input"],
    template="""You are a knowledgeable book summarization assistant.

Book Genre: {genre_input}
Book Title: {book_input}
Summary Length: {length_input}

Generate a well-written summary according to the requested length.

If the requested length is:
- Short: 100-150 words
- Medium: 250-350 words
- Detailed: 500-700 words

Summary:"""
)

template.save('template.json')


