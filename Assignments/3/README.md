# DSA03 NLP Assignment 3 – Code Package

This package accompanies `DSA03_NLP_Assignment3_Completed_Draft.docx`.

## Contents
- `src/run_parsers.py` – runnable CFG, top-down chart parser, Earley parser, small PCFG/Viterbi demo, lightweight agreement checks, and experiment runner.
- `data/test_queries.txt` – the 30-query test set in plain text.
- `results/` – populated when the script runs (CSV, Viterbi output and chart-size plot).
- `requirements.txt` – Python dependencies.
- `DSA03_NLP_Assignment3_Completed_Draft.docx` – written report.

## Setup
Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python src/run_parsers.py
```

The script writes:
- `results/parser_results.csv`
- `results/viterbi_demo.txt`
- `results/chart_edges_vs_length.png`

## Important scope notes
1. The executable grammar is a compact, runnable subset of the larger grammar described in the report. It is not a complete implementation of every construction or all 60+ lexical entries.
2. NLTK's `TopDownChartParser` is a chart-based top-down strategy, not a naive recursive-descent parser. It avoids repeated work by storing chart edges.
3. The agreement/case and valence checks are deliberately small explicit checks for selected test patterns. They are not a full attribute-value unification engine.
4. The PCFG is a tiny illustrative model for demonstrating Viterbi parsing. Its probabilities are hand-set demonstration values, not estimated from a real annotated corpus.
5. Timings and chart-edge counts are machine- and version-dependent. Run the script on your own system and use the generated CSV/plot for your report. Do not present example timings as universal measurements.

## Reproducibility
Run from the package root with `python src/run_parsers.py`. The program prints a summary and recreates the files under `results/`.
