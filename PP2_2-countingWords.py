text = "I love Python and I love NLP"
tokens = text.lower().split()
types = set(tokens)

print("Text:", text)
print("Tokens:", tokens)
print("Total Tokens:", len(tokens))
print("Types:", types)
print("Total Types:", len(types))