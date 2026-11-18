import spacy

nlp = spacy.load("en_core_web_sm")

text = input("Enter a paragraph: ")
doc = nlp(text)

entities = []

for token in doc:
    if token.pos_ in ["NOUN", "PROPN"] and token.dep_ in ["nsubj", "dobj", "pobj", "attr"]:
        entities.append(token)

print("\nReference Resolution:")

for token in doc:
    if token.pos_ == "PRON":
        antecedent = None

        for entity in reversed(entities):
            if entity.i < token.i:
                if token.tag_ in ["PRP", "PRP$"]:
                    antecedent = entity
                    break

        if antecedent:
            print(token.text, "->", antecedent.text)
        else:
            print(token.text, "-> Antecedent not identified")