import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('punkt_tab')

text = input("Enter a paragraph: ")

sentences = nltk.sent_tokenize(text)

if len(sentences) < 2:
    print("Enter at least two sentences to evaluate coherence.")
else:
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(sentences)

    similarities = []

    print("\nSentence Similarity Scores:")

    for i in range(len(sentences) - 1):
        score = cosine_similarity(
            vectors[i], vectors[i + 1]
        )[0][0]

        similarities.append(score)

        print(f"Sentence {i + 1} and {i + 2}: {score:.2f}")

    coherence = sum(similarities) / len(similarities)

    print("\nOverall Coherence Score:", round(coherence, 2))

    if coherence >= 0.5:
        print("The text has relatively high lexical coherence.")
    elif coherence >= 0.2:
        print("The text has moderate lexical coherence.")
    else:
        print("The text has low lexical coherence.")