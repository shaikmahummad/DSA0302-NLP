import random
from collections import Counter

corpus = [
    "i like python",
    "i like machine learning",
    "python is easy",
    "machine learning is interesting",
    "i like learning",
    "python is interesting"
]

sentences = [s.lower().split() for s in corpus]

word_counts = Counter()
bigram_counts = Counter()

for sentence in sentences:
    words = ["<s>"] + sentence + ["</s>"]
    word_counts.update(words)

    for i in range(len(words) - 1):
        bigram_counts[(words[i], words[i + 1])] += 1


def bigram_probability(w1, w2):
    if word_counts[w1] == 0:
        return 0
    return bigram_counts[(w1, w2)] / word_counts[w1]


print("Bigram Probabilities:")

for (w1, w2), count in bigram_counts.items():
    print(f"P({w2} | {w1}) = {bigram_probability(w1, w2):.2f}")


def sentence_probability(sentence):
    words = ["<s>"] + sentence.lower().split() + ["</s>"]
    probability = 1.0

    for i in range(len(words) - 1):
        probability *= bigram_probability(words[i], words[i + 1])

    return probability


test_sentence = "i like python"
print("\nSentence:", test_sentence)
print("Sentence Probability:", sentence_probability(test_sentence))


def generate_sentence(max_words=10):
    current_word = "<s>"
    result = []

    for _ in range(max_words):
        candidates = []

        for (w1, w2), count in bigram_counts.items():
            if w1 == current_word:
                candidates.extend([w2] * count)

        if not candidates:
            break

        next_word = random.choice(candidates)

        if next_word == "</s>":
            break

        result.append(next_word)
        current_word = next_word

    return " ".join(result)


print("\nGenerated Sentences:")

for i in range(3):
    print(generate_sentence())