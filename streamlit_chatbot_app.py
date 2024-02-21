import streamlit as st
import requests
from bs4 import BeautifulSoup
import spacy

# Loading the spaCy language model
nlp = spacy.load("en_core_web_sm")

def fetch_webpage_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = ' '.join(soup.stripped_strings)
    return text

def process_text_with_spacy(text):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    return sentences

def find_answer_with_spacy(query, sentences):
    query_doc = nlp(query)
    query_keywords = [token.lemma_.lower() for token in query_doc if token.is_stop == False and token.is_punct == False]
    best_match = None
    best_score = 0
    for sentence in sentences:
        sentence_doc = nlp(sentence)
        sentence_keywords = [token.lemma_.lower() for token in sentence_doc if token.is_stop == False and token.is_punct == False]
        score = len(set(query_keywords) & set(sentence_keywords))
        if score > best_score:
            best_score = score
            best_match = sentence
    return best_match if best_match else "Sorry, I couldn't find an answer to your question."

def chatbot(url, query):
    content = fetch_webpage_content(url)
    sentences = process_text_with_spacy(content)
    answer = find_answer_with_spacy(query, sentences)
    return answer

# Streamlit interface
st.title('Web Content-based Chatbot')

url = st.text_input('Enter the URL of the webpage:', 'https://www.cranberry.fit/post/why-don-t-i-sleep-well-before-my-period')
query = st.text_input('Enter your query:', 'What causes period cramps?')

if st.button('Find Answer'):
    response = chatbot(url, query)
    st.text_area("Answer", value=response, height=150, max_chars=None, help=None)

