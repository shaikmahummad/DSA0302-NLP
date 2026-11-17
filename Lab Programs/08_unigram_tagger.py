import nltk
from nltk.tag import UnigramTagger
from nltk.corpus import brown

nltk.download('brown')
nltk.download('universal_tagset')

data = brown.tagged_sents(tagset='universal')

train_data = data[:4000]
test_data = data[4000:4100]

tagger = UnigramTagger(train_data)

sentence = "The dog is running in the garden".split()

print(tagger.tag(sentence))
print("Accuracy:", tagger.accuracy(test_data))