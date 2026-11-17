import spacy

nlp = spacy.load("en_core_web_sm")

text = "Google was founded in California by Larry Page and Sergey Brin."

doc = nlp(text)

for ent in doc.ents:
    print(ent.text, ":", ent.label_)