# NLP Lab Programs (1–26)

This repository contains 26 Python programs covering Natural Language Processing (NLP) concepts and applications.

## 1. Project Structure

Keep all Python files inside one folder:

```text
NLP_Lab_Programs/
│
├── 01_regular_expressions.py
├── 02_finite_state_automaton.py
├── 03_tokenization_lemmatization.py
├── 04_plural_formation_fsm.py
├── 05_porter_stemming.py
├── 06_bigram_text_generation.py
├── 07_pos_tagging.py
├── 08_unigram_tagger.py
├── 09_regexp_tagger.py
├── 10_brill_tagger.py
├── 11_top_down_parsing.py
├── 12_earley_parsing.py
├── 13_cfg_parse_tree.py
├── 14_subject_verb_agreement.py
├── 15_pcfg_viterbi_parser.py
├── 16_named_entity_recognition.py
├── 17_wordnet_synsets.py
├── 18_fopc_predicate_logic.py
├── 19_word_sense_disambiguation.py
├── 20_tfidf_information_retrieval.py
├── 21_syntax_driven_semantic_analysis.py
├── 22_reference_resolution.py
├── 23_text_coherence_evaluation.py
├── 24_dialog_act_recognition.py
├── 25_gpt3_text_generation.py
├── 26_machine_translation_english_to_french.py
│
└── README.md
```

## 2. Software Requirements

- Python 3.10 or above
- Visual Studio Code or any Python IDE
- Internet connection for downloading NLP datasets and pretrained models

Check your Python version:

```bash
python --version
```

## 3. Install Required Libraries

Open the terminal inside the project folder and execute:

```bash
pip install nltk spacy scikit-learn openai transformers torch sentencepiece
```

Download the spaCy English language model:

```bash
python -m spacy download en_core_web_sm
```

### Download NLTK Resources

Run the following command in Python:

```bash
python
```

Then execute:

```python
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('brown')
nltk.download('universal_tagset')
```

Type `exit()` to close the Python interpreter.

## 4. How to Run the Programs

Open the terminal in the `NLP_Lab_Programs` folder.

Use this command to execute any program:

```bash
python filename.py
```

For example:

```bash
python 01_regular_expressions.py
```

Enter the required input when the program asks for it.

## 5. Program-wise Input Requirements

### Program 1: Regular Expressions

**File:** `01_regular_expressions.py`

Input: A text string and the pattern to search for, if prompted.

Sample text:

```text
The student is learning Python programming.
```

Sample pattern:

```text
Python
```

Purpose: Matches and searches for patterns in text using regular expressions.

### Program 2: Finite State Automaton

**File:** `02_finite_state_automaton.py`

Input: A string to check whether it ends with `ab`.

Sample input:

```text
aabb
```

Another input:

```text
abab
```

Purpose: Checks whether the input string is accepted by the finite state automaton.

### Program 3: Tokenization and Lemmatization

**File:** `03_tokenization_lemmatization.py`

Input: An English sentence.

Sample input:

```text
The students are studying natural language processing.
```

Purpose: Splits text into tokens and converts words into their base forms.

### Program 4: Plural Formation Using FSM

**File:** `04_plural_formation_fsm.py`

Input: A singular noun.

Sample inputs:

```text
cat
```

```text
book
```

Purpose: Demonstrates plural word formation using a finite state machine.

### Program 5: Porter Stemming

**File:** `05_porter_stemming.py`

Input: A list of English words.

Sample input:

```text
playing played plays studies studying
```

Purpose: Reduces words to their stems using the Porter stemming algorithm.

### Program 6: Bigram Text Generation

**File:** `06_bigram_text_generation.py`

Input: A sample sentence or text corpus, if prompted.

Sample input:

```text
Natural language processing is interesting. Natural language processing is useful.
```

Purpose: Generates text using a bigram language model.

### Program 7: POS Tagging

**File:** `07_pos_tagging.py`

Input: An English sentence.

Sample input:

```text
The quick brown fox jumps over the lazy dog.
```

Purpose: Identifies grammatical categories such as nouns, verbs, adjectives, and adverbs.

### Program 8: Unigram Tagger

**File:** `08_unigram_tagger.py`

Input: A sample sentence, if prompted.

Sample input:

```text
The students are learning Python.
```

Purpose: Demonstrates unigram-based part-of-speech tagging using a trained corpus.

### Program 9: Regexp Tagger

**File:** `09_regexp_tagger.py`

Input: An English sentence, if prompted.

Sample input:

```text
The boy is playing football.
```

Purpose: Assigns grammatical tags using regular expression patterns.

### Program 10: Brill Tagger

**File:** `10_brill_tagger.py`

Input: Usually uses a predefined training corpus and sample sentence within the program.

Sample sentence, if prompted:

```text
The dog runs quickly.
```

Purpose: Demonstrates transformation-based POS tagging.

### Program 11: Top-Down Parsing

**File:** `11_top_down_parsing.py`

Input: A sentence matching the grammar defined in the program.

Sample input:

```text
the student reads a book
```

Purpose: Parses a sentence using a top-down parsing approach.

### Program 12: Earley Parsing

**File:** `12_earley_parsing.py`

Input: A sentence matching the grammar defined in the program.

Sample input:

```text
the student reads a book
```

Purpose: Demonstrates sentence parsing using the Earley parsing algorithm.

### Program 13: CFG Parse Tree

**File:** `13_cfg_parse_tree.py`

Input: A sentence matching the context-free grammar.

Sample input:

```text
the dog chased a cat
```

Purpose: Generates a parse tree using a context-free grammar.

### Program 14: Subject-Verb Agreement

**File:** `14_subject_verb_agreement.py`

Input: A sentence matching the grammar rules.

Sample input:

```text
the boy eats
```

Another possible input:

```text
the boys eat
```

Purpose: Demonstrates subject-verb agreement using grammar rules.

### Program 15: PCFG Viterbi Parser

**File:** `15_pcfg_viterbi_parser.py`

Input: A sentence matching the probabilistic grammar.

Sample input:

```text
the dog chased a cat
```

Purpose: Parses sentences using a probabilistic context-free grammar and Viterbi parsing.

### Program 16: Named Entity Recognition

**File:** `16_named_entity_recognition.py`

Input: An English sentence containing names, locations, organizations, or dates.

Sample input:

```text
Sundar Pichai is the CEO of Google and works in California.
```

Purpose: Identifies named entities such as people, organizations, and locations.

### Program 17: WordNet Synsets

**File:** `17_wordnet_synsets.py`

Input: An English word.

Sample input:

```text
computer
```

Another input:

```text
bank
```

Purpose: Retrieves word meanings and synonyms using WordNet.

### Program 18: First-Order Predicate Logic

**File:** `18_fopc_predicate_logic.py`

Input: A logical statement or predicate in the format expected by the program.

Sample input:

```text
Human(Socrates)
```

Purpose: Demonstrates basic predicate representation and parsing.

### Program 19: Word Sense Disambiguation

**File:** `19_word_sense_disambiguation.py`

Input: A sentence and the target ambiguous word, if prompted.

Sample sentence:

```text
I deposited money in the bank.
```

Target word:

```text
bank
```

Another example:

```text
He sat on the bank of the river.
```

Target word:

```text
bank
```

Purpose: Identifies the intended meaning of a word based on its context.

### Program 20: TF-IDF Information Retrieval

**File:** `20_tfidf_information_retrieval.py`

Input: A search query.

Sample query:

```text
machine learning and artificial intelligence
```

Purpose: Retrieves relevant documents using TF-IDF and cosine similarity.

### Program 21: Syntax-Driven Semantic Analysis

**File:** `21_syntax_driven_semantic_analysis.py`

Input: A sentence matching the grammar defined in the program.

Sample input:

```text
the young student reads a book
```

Purpose: Extracts noun phrases and displays their meanings using WordNet.

Note: The grammar accepts only the words and sentence structures defined in the program.

### Program 22: Reference Resolution

**File:** `22_reference_resolution.py`

Input: An English paragraph containing pronouns.

Sample input:

```text
John bought a new laptop. He uses it every day.
```

Purpose: Demonstrates basic identification of possible pronoun references.

### Program 23: Text Coherence Evaluation

**File:** `23_text_coherence_evaluation.py`

Input: A paragraph containing at least two sentences.

Sample input:

```text
Artificial intelligence is transforming technology. Machine learning is an important part of artificial intelligence. It helps computers learn from data.
```

Purpose: Calculates sentence similarity and estimates lexical coherence.

### Program 24: Dialog Act Recognition

**File:** `24_dialog_act_recognition.py`

Input: Individual dialog messages. Type `exit` to stop.

Sample conversation:

```text
Hello
How are you?
Thank you
Can you help me?
Goodbye
exit
```

Purpose: Identifies dialog acts such as greeting, question, request, thanking, agreement, and farewell.

### Program 25: GPT Text Generation

**File:** `25_gpt3_text_generation.py`

Input: A text-generation prompt.

Sample input:

```text
Write a short paragraph about artificial intelligence.
```

Purpose: Generates text using an OpenAI model.

Requirements:

1. Install the OpenAI library.
2. Obtain an OpenAI API key.
3. Set the API key as an environment variable.

Windows CMD:

```bash
set OPENAI_API_KEY=your_api_key
```

PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key"
```

The API requires an active account, available API credits or billing, and access to the selected model.

### Program 26: Machine Translation

**File:** `26_machine_translation_english_to_french.py`

Input: An English sentence.

Sample input:

```text
Hello, how are you?
```

Another input:

```text
Artificial intelligence is changing the world.
```

Purpose: Translates English text into French using the Hugging Face Transformers library.

The first execution downloads the pretrained translation model, so an internet connection is required.

## 6. Running All Programs

Execute the programs individually in numerical order:

```bash
python 01_regular_expressions.py
python 02_finite_state_automaton.py
python 03_tokenization_lemmatization.py
python 04_plural_formation_fsm.py
python 05_porter_stemming.py
python 06_bigram_text_generation.py
python 07_pos_tagging.py
python 08_unigram_tagger.py
python 09_regexp_tagger.py
python 10_brill_tagger.py
python 11_top_down_parsing.py
python 12_earley_parsing.py
python 13_cfg_parse_tree.py
python 14_subject_verb_agreement.py
python 15_pcfg_viterbi_parser.py
python 16_named_entity_recognition.py
python 17_wordnet_synsets.py
python 18_fopc_predicate_logic.py
python 19_word_sense_disambiguation.py
python 20_tfidf_information_retrieval.py
python 21_syntax_driven_semantic_analysis.py
python 22_reference_resolution.py
python 23_text_coherence_evaluation.py
python 24_dialog_act_recognition.py
python 25_gpt3_text_generation.py
python 26_machine_translation_english_to_french.py
```

## 7. Troubleshooting

| Error | Solution |
|---|---|
| `ModuleNotFoundError` | Install the missing library using `pip install library_name`. |
| NLTK resource not found | Download the required NLTK dataset using `nltk.download()`. |
| spaCy model not found | Run `python -m spacy download en_core_web_sm`. |
| OpenAI API authentication error | Check whether `OPENAI_API_KEY` is correctly configured. |
| OpenAI model access error | Verify that the selected model is available to your API account. |
| Hugging Face download error | Check your internet connection and try again. |
| No parse tree generated | Enter a sentence that matches the grammar defined in the program. |

## 8. Important Notes

- Run each program separately.
- Use the sample inputs provided above as a starting point.
- Some programs use predefined training data instead of accepting interactive input.
- Programs involving pretrained models or external APIs may require internet access.
- The GPT text generation program requires an OpenAI API key.
- The Hugging Face translation program downloads its model during the first execution.
- The outputs depend on the input sentence, available datasets, and installed library versions.

## 9. Conclusion

These 26 programs demonstrate fundamental and advanced concepts in Natural Language Processing, including regular expressions, finite state machines, tokenization, stemming, lemmatization, POS tagging, parsing, semantic analysis, information retrieval, reference resolution, coherence evaluation, dialog act recognition, text generation, and machine translation.
