import random
from collections import defaultdict

text = "I love natural language processing. I love Python programming. Python is easy."

words = text.lower().replace(".", "").split()
bigrams = defaultdict(list)

for i in range(len(words) - 1):
    bigrams[words[i]].append(words[i + 1])

word = random.choice(list(bigrams.keys()))
result = [word]

for _ in range(10):
    if word not in bigrams:
        break
    word = random.choice(bigrams[word])
    result.append(word)

print("Generated Text:", " ".join(result))