prefixes = [
    "un", "re", "dis", "mis", "pre", "over",
    "under", "in", "im", "non", "anti"
]

suffixes = [
    "ing", "ed", "er", "est", "ly", "ness",
    "ment", "ful", "less", "able", "tion", "s"
]

word = input("Enter a word: ").lower()

original_word = word
prefix = ""
suffix = ""

for p in prefixes:
    if word.startswith(p) and len(word) > len(p):
        prefix = p
        word = word[len(p):]
        break

for s in suffixes:
    if word.endswith(s) and len(word) > len(s):
        suffix = s
        word = word[:-len(s)]
        break

root = word

print("\nWord:", original_word)
print("Prefix:", prefix if prefix else "None")
print("Root:", root)
print("Suffix:", suffix if suffix else "None")