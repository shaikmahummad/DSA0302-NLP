import nltk

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

text = "The cats are playing and the dogs are running"

words = word_tokenize(text)
lemmatizer = WordNetLemmatizer()

for word in words:
    print(word, ":", lemmatizer.lemmatize(word))