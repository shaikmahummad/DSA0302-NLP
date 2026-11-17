from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = [
    "Python is a programming language",
    "Natural language processing uses Python",
    "Machine learning is a part of artificial intelligence",
    "Information retrieval finds relevant documents"
]

query = input("Enter search query: ")

vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(documents)

query_vector = vectorizer.transform([query])

scores = cosine_similarity(query_vector, tfidf_matrix)

ranked = scores.flatten().argsort()[::-1]

for index in ranked:
    print("Document:", documents[index])
    print("Score:", round(scores[0][index], 4))
    print()