from collections import Counter

corpus = [
    "i like python",
    "i like java",
    "i love python"
]

sentences = [
    ["<s>"] + sentence.split() + ["</s>"]
    for sentence in corpus
]

word_counts = Counter()
bigram_counts = Counter()

for sentence in sentences:
    word_counts.update(sentence)
    for i in range(len(sentence) - 1):
        bigram_counts[(sentence[i], sentence[i + 1])] += 1

V = len(word_counts)

def show_probability(w1, w2):
    count = bigram_counts[(w1, w2)]
    total = word_counts[w1]
    before = count / total if total else 0
    after = (count + 1) / (total + V)

    print(f"P({w2} | {w1})")
    print("Before Laplace Smoothing:", round(before, 4))
    print("After Laplace Smoothing :", round(after, 4))
    print()

show_probability("i", "like")
show_probability("i", "love")
show_probability("i", "java")
show_probability("i", "machine")