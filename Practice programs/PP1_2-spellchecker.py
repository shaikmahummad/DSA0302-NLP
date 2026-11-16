from collections import Counter

text = """
the cat sat on the mat
the man went to the park
the cat and the man walked in the park
the man saw a cat in the park
"""

words = text.lower().split()
word_counts = Counter(words)


def edits1(word):

    letters = "abcdefghijklmnopqrstuvwxyz"
    result = set()

    for i in range(len(word)):
        result.add(word[:i] + word[i + 1:])

    for i in range(len(word) + 1):
        for letter in letters:
            result.add(word[:i] + letter + word[i:])

    for i in range(len(word)):
        for letter in letters:
            result.add(word[:i] + letter + word[i + 1:])

    for i in range(len(word) - 1):
        result.add(
            word[:i] + word[i + 1] + word[i] + word[i + 2:]
        )

    return result


def correct(word):

    candidates = edits1(word)

    valid_words = []

    for candidate in candidates:
        if candidate in word_counts:
            valid_words.append(candidate)

    if not valid_words:
        return word

    return max(valid_words, key=lambda x: word_counts[x])


incorrect_words = ["teh", "cta", "mann", "park"]

print("Word Corrections:")

for word in incorrect_words:
    print(word, "->", correct(word))
    