from collections import Counter

corpus = [
    "i love python",
    "i love programming",
    "i like python",
    "i like coding",
    "we love python"
]

bigram_counts = Counter()

for sentence in corpus:
    words = sentence.split()
    for i in range(len(words) - 1):
        bigram_counts[(words[i], words[i+1])] += 1

word = "i"
candidates = {}

for (first, second), count in bigram_counts.items():
    if first == word:
        candidates[second] = count

print("Input word:", word)
print("Next word counts:", candidates)

if candidates:
    print("Predicted next word:", max(candidates, key=candidates.get))
else:
    print("No prediction available.")