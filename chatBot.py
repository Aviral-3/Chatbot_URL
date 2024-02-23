import requests
from bs4 import BeautifulSoup
import spacy

nlp = spacy.load("en_core_web_sm")

def fetch_webpage_content(url):
    """Fetching the webpage content at the specified URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = ' '.join(soup.stripped_strings)
    return text

def process_text_with_spacy(text):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    return sentences

def find_answer_with_spacy(query, sentences):
    """Finding the answer to the query within the given sentences using SpaCy."""
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
    return best_match if best_match else "Sorry, I couldn't find an answer to the question."

def chatbot(url, query):
    """The chatbot function to get an answer for the query from the webpage at the given URL."""
    content = fetch_webpage_content(url)
    sentences = process_text_with_spacy(content)
    answer = find_answer_with_spacy(query, sentences)
    return answer

# Example usage
if __name__ == "__main__":
    url = input("Enter the URL of the webpage: ")
    query = input("Enter your query: ")
    response = chatbot(url, query)
    print("Answer:", response)
