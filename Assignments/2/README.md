# DSA03 – Natural Language Processing Assignment 2

## Assignment overview

**Title:** Build and Evaluate an N-gram Language Model and a Part-of-Speech Tagger for a Public Transport Enquiry Helpline  
**Course outcome:** CO2  
**Total marks:** 50  
**Duration:** 1 week  
**Nature:** Individual assignment

The assignment models a public transport enquiry helpline that receives calls about bus and train timings, routes, fares, cancellations and refunds. Speech recognition may produce several competing transcript hypotheses. The language model is used to rescore those hypotheses, and POS tagging helps identify information such as origin, destination, date and fare.

The assignment has two broad parts:

1. Build and evaluate language models and POS taggers using a documented corpus.
2. Re-evaluate the design when the helpline expands to metro/intercity rail and code-mixed speech, with more than 15% unseen words.

## Assignment requirements

The original brief specifies the following data and evaluation requirements:

- At least **20,000 transcribed utterances** and **150,000 word tokens**.
- An **80% / 10% / 10%** train, development and test split, with no utterance shared across splits.
- At least **200 ASR utterances**, each with five competing hypotheses and a correct reference transcript.
- A custom tagset containing **20–30 tags**, with an explicit mapping to the Penn Treebank tagset.
- At least **3,000 manually POS-tagged tokens**.
- At least **500 tokens independently tagged by two annotators**, so inter-annotator agreement can be measured.
- A fixed random seed and a held-out test set that is not used for training or tuning.

> **Important:** The included Python file is a starter experiment using synthetic transport-related utterances. It is not a complete implementation of every model in the assignment and does not generate genuine human annotations or ASR hypothesis/reference sets. Do not present synthetic or unmeasured results as real experimental evidence. Complete the missing experiments using the required data before making final empirical claims.

## Tasks covered by the assignment

| Task | Topic | Main work expected |
|---|---|---|
| 1 | Counting words and vocabulary | Types, tokens, lemmas, word forms, tokenisation, Zipf's law, vocabulary thresholds and OOV rate |
| 2 | Unsmoothed n-gram models | Unigram, bigram and trigram models, sentence probabilities, zero probabilities, sparsity and generation |
| 3 | Smoothing and discounting | Laplace, add-k and Good–Turing smoothing; compare development perplexity |
| 4 | Backoff and deleted interpolation | Katz backoff, stupid backoff, linear interpolation and deleted interpolation |
| 5 | Entropy and perplexity | Entropy, cross-entropy, perplexity and ASR hypothesis rescoring using WER |
| 6 | Word classes and tagset design | Open/closed classes, custom tagset, Penn Treebank mapping and annotation agreement |
| 7 | Rule-based POS tagging | Tag dictionary, at least 15 disambiguation rules and evaluation |
| 8 | Stochastic/HMM tagging | Transition/emission probabilities, Viterbi trellis and unknown-word handling |
| 9 | Transformation-based tagging | Brill-style templates, learned transformations and accuracy curve |
| 10 | Implementation and testing | Python implementation, reproducibility, runtime, memory and plots |
| 11 | Comparison and recommendation | Compare models and justify the recommended language model and tagger |
| 12 | Day-4 design challenge | Adapt the system for new station names, rail services and code-mixed speech |

## Project files

The package contains:

- `NLP_Assignment_2_Worked_Draft.docx` – a written worked draft explaining the concepts, proposed tagset, model design and evaluation plan.
- `nlp_assignment2_starter.py` – a Python starter program that generates a synthetic corpus and runs basic corpus and bigram experiments.
- `NLP_Assignment_2_Worked_Draft.md` – the worked draft converted to Markdown (optional reference copy).

This README describes the assignment and how to run the starter program; it is not a replacement for the assignment report.

## Requirements

The starter program uses only the Python standard library. No external Python packages are required.

Recommended:

- Python 3.9 or later
- VS Code or another Python editor
- A terminal / PowerShell window

Check that Python is installed:

```bash
python --version
```

On some Windows installations, use:

```powershell
py --version
```

## How to run the Python code

### 1. Extract the package

Download and extract `NLP_Assignment_2_Package.zip`, or place `nlp_assignment2_starter.py` in a project folder.

### 2. Open the project folder

Open the folder in VS Code, then open its integrated terminal:

**Terminal → New Terminal**

### 3. Run the script

Windows:

```powershell
python nlp_assignment2_starter.py
```

If `python` is not recognised:

```powershell
py nlp_assignment2_starter.py
```

macOS / Linux:

```bash
python3 nlp_assignment2_starter.py
```

### 4. Check the generated output

The script creates a folder named `nlp_assignment2_outputs` in the current working directory. It writes:

| Output | Description |
|---|---|
| `experiment_summary.json` | Corpus split sizes, token/type counts, vocabulary threshold results, development OOV rate, add-k bigram evaluation and an unseen development bigram |
| `zipf_rank_frequency.csv` | Word frequency sorted by rank, suitable for plotting a Zipf curve |

The script also prints the experiment summary in the terminal.

To run it again, execute the same command. The fixed seed makes the synthetic data and random unigram samples reproducible.

## What the starter code currently does

1. Generates **20,000 synthetic transport enquiry utterances** from predefined templates and a list of place names.
2. Shuffles the utterances using a fixed random seed.
3. Splits the utterances into training (80%), development (10%) and test (10%).
4. Counts training tokens and word types.
5. Builds vocabularies at rare-word thresholds 1, 2, 3 and 5, mapping words at or below each threshold to `<UNK>`.
6. Calculates the development-set OOV rate against the selected training vocabulary.
7. Exports word rank and frequency values for a Zipf plot.
8. Builds training bigram counts and evaluates an add-k-smoothed bigram model on development data.
9. Finds an example of a development bigram that was not observed in training.
10. Generates ten sample sequences from a unigram frequency distribution.

## Understanding the experiment summary

The JSON report contains fields such as:

- `utterances`: number of utterances in the complete corpus and each split.
- `train_tokens`: number of lexical tokens in the training split.
- `train_types`: number of distinct training word forms.
- `vocabulary_thresholds_le_count`: vocabulary size and percentage of training tokens mapped to `<UNK>` for each threshold.
- `dev_oov_percent`: percentage of development tokens not found in the selected training vocabulary.
- `bigram_add_k_dev`: number of evaluated events, zero-event count, cross-entropy and perplexity (if all events have finite probability).
- `first_unseen_dev_bigram`: an example of a bigram in development data that did not occur in training.
- `unigram_samples`: ten sample sequences generated from unigram frequencies.

The script's vocabulary threshold is defined as **count less than or equal to the threshold** being mapped to `<UNK>`. The retained vocabulary therefore contains words whose training count is greater than the threshold.

## Suggested next implementation steps

The starter code is intentionally limited. To complete the assignment, extend it in this order:

1. Add unigram, bigram and trigram probability functions and sentence scoring.
2. Implement Laplace and add-k smoothing for the required n-gram orders.
3. Add Good–Turing discounting and a frequency-of-frequencies table.
4. Implement Katz backoff, stupid backoff, linear interpolation and deleted interpolation.
5. Calculate held-out entropy, cross-entropy and perplexity using the same vocabulary and `<UNK>` policy for every model.
6. Add the 200 ASR hypothesis sets and calculate WER before and after rescoring.
7. Collect and document 3,000 manually POS-tagged tokens, including 500 independently double-annotated tokens.
8. Implement and evaluate the rule-based tagger, HMM/Viterbi tagger and transformation-based tagger.
9. Add runtime, memory, accuracy and speed measurements, plus at least two plots.
10. Evaluate the modified system on a new-domain sample containing unseen stations and code-mixed utterances.

## Important evaluation notes

- Split by utterance, not by randomly splitting individual tokens.
- Use development data to tune parameters; keep the test set untouched until final evaluation.
- Keep tokenisation, vocabulary, `<UNK>` mapping and sentence-boundary handling consistent when comparing perplexity.
- Report measured results from your own runs. Do not invent model accuracy, WER, Cohen's kappa, runtime or memory values.
- Synthetic corpus labels cannot be used as evidence of independent human annotation.
- Record the source or generation method of the corpus and the time spent on transcription, annotation, rule writing and testing.

## Suggested final submission structure

1. Cover page
2. Assignment overview and problem statement
3. Dataset description, preprocessing and split methodology
4. Tasks 1–5: language modelling and evaluation
5. Tasks 6–9: tagset and POS taggers
6. Task 10: implementation, tests, runtime and plots
7. Task 11: comparison and deployment recommendation
8. Task 12: Day-4 design challenge
9. Conclusion
10. References
11. Appendix: source code, corpus details, annotation guidelines and experiment outputs
