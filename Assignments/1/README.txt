DSA03 NLP Assignment 1 - submission package

Files:
- DSA03_NLP_Assignment1_Complete.docx : written response to Tasks 1-12
- nlp_pipeline.py : runnable Python reference implementation
- synthetic_clinical_corpus.csv : 500 synthetic records across four record types
- annotated_200_forms.csv : 200-row starter annotation set
- clinician_queries_40.csv : 40-query starter evaluation fixture
- record_type_distribution.png : corpus composition plot

Run:
  python nlp_pipeline.py --corpus synthetic_clinical_corpus.csv

Optional:
  python -m pip install nltk

Dataset notice:
All records are synthetic. The 40 queries and 200 annotations are teaching fixtures,
not clinician-validated ground truth. Do not represent illustrative examples as
real hospital measurements. Replace placeholder lexicon entries with curated
clinical vocabulary before any real deployment.

Measured run summary:
{
  "records": 500,
  "tokens": 71710,
  "entity_matches": 6375,
  "analysed_tokens": 11665,
  "runtime_seconds": 0.1928,
  "lexicon_stems": 303,
  "inflectional_affixes": 7,
  "derivational_affixes": 15
}
