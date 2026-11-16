import nltk
from collections import Counter

nltk.download('punkt')

paragraph = input("Enter a paragraph: ")

sentences = nltk.sent_tokenize(paragraph)

print("\nSentences:")
for sentence in sentences:
    print(sentence)

words = nltk.word_tokenize(paragraph)

words = [word.lower() for word in words if word.isalnum()]

print("\nWords:")
print(words)

print("\nTotal number of words:", len(words))

frequency = Counter(words)

print("\nWord Frequency:")
for word, count in frequency.items():
    print(word, ":", count)

most_frequent = frequency.most_common()
highest_count = most_frequent[0][1]

print("\nMost Frequent Words:")
for word, count in most_frequent:
    if count == highest_count:
        print(word, ":", count)