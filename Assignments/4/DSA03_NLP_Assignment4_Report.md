
# DSA03 – Natural Language Processing
## Assignment 4 (CO4)
### Meaning-Based Enquiry and Document Search for a Government Pension Helpdesk

**Student name:** ____________________  
**Register number:** ____________________  
**Course / Section:** ____________________  
**Submission date:** ____________________

---

## Abstract

This assignment proposes a meaning-based enquiry and document-search layer for a government pension helpdesk. The system combines first-order predicate calculus (FOPC), a small domain ontology, syntax-driven semantic interpretation, word-sense disambiguation (WSD), and TF-IDF information retrieval. It distinguishes a question that can be answered by applying a rule from one that merely retrieves a relevant circular. The design uses explicit three-valued answers—true, false and unknown—so that missing evidence is not incorrectly treated as a negative decision.

The accompanying Python prototype creates a reproducible synthetic corpus and demonstrates the core pipeline: a small pension knowledge base, rule checks, a simplified Lesk WSD baseline, TF-IDF/cosine retrieval, and tests. The assignment specification requires real or documented corpus material, independent annotation and held-out evaluation. Generated examples are therefore identified as synthetic. Human agreement, real helpdesk accuracy and native-domain validation must be collected before making operational claims.

## 1. Problem definition and experimental plan

The directorate receives questions about family pension, commutation, qualifying service, dependants, revisions and circulars. Keyword matching alone cannot reason over quantified eligibility rules, while a logical representation alone cannot locate the authoritative document or interpret every ambiguous term. The proposed architecture uses a hybrid pipeline:

1. Normalize the enquiry and identify entities, dates and domain terms.
2. Parse the question and map it to a canonical logical form.
3. Disambiguate ambiguous terms using context.
4. Query the FOPC knowledge base for rule-based questions.
5. Search the circular index for supporting documents.
6. Return an answer with the supporting rule/circular, or abstain and request clarification.

### 1.1 Dataset plan

The assignment requires at least 300 circulars/memoranda and 60,000 tokens, 200 helpdesk questions, 40 FOPC rules, 25 ambiguous terms, 600 hand-labelled sense occurrences, 50 semantic grammar rules, and 60 relevance-judged queries. The package includes a synthetic corpus generator and small runnable sample so the pipeline can be executed immediately. It does not claim to contain 300 genuine government circulars or 600 human sense annotations. For a final empirical submission, add approved public circulars, remove personal information, collect real enquiries with consent, and create independent annotations.

Suggested corpus manifest:

| Dataset | Required target | Purpose |
|---|---:|---|
| Circulars and office memoranda | 300 / 60,000 tokens | Retrieval |
| Enquiry questions | 200 | Semantic coverage |
| FOPC rules | 40 | Entitlement reasoning |
| Ambiguous domain terms | 25 | Sense inventory |
| Sense-labelled occurrences | 600 | WSD |
| Semantic grammar rules | 50 | Compositional analysis |
| Relevance-judged queries | 60 | IR evaluation |
| Double annotations | 200 sense instances + 15 queries | Agreement |

Use fixed seed `17` for all generated splits. Keep a held-out set separate from development data. Do not tune thresholds or glosses against the held-out questions.

---

## TASK 1 – Choosing a Meaning Representation

### 1.1 Four required capabilities

1. **Answer a question:** “Does employee E-104 qualify for pension?” The system evaluates the employee's service and age facts against eligibility rules.
2. **Check a claim:** “Every employee with ten qualifying years receives a pension.” The system tests the universal claim against the knowledge base and model.
3. **Infer unstated information:** If an employee is a family pensioner and every family pensioner is a pension beneficiary, infer that the person is a pension beneficiary.
4. **Match different wording:** “Has the retiree completed the required service?” and “Does the retired employee satisfy the qualifying-service condition?” should map to the same canonical predicate.

### 1.2 Representation comparison

| Representation | Expressiveness | Inference | Construction effort | Pension example |
|---|---|---|---|---|
| First-order logic | High for relations, quantifiers and negation | Formal deduction and model checking | High; predicates and rules must be designed | `∀x(Employee(x) ∧ QualifyingYears(x) ≥ 10 → Eligible(x))` |
| Semantic network | Relations represented as labelled graph edges | Inheritance and graph traversal | Medium | Employee —hasService→ ServiceRecord |
| Frames | Structured objects with slots, defaults and constraints | Slot inheritance and procedural checks | Medium | Employee frame: service_years, retirement_date, dependants |
| Slot-filler structure | Simple attribute-value representation | Limited unless rules are added | Low | PensionCase: applicant=E104; claim=family_pension |

FOPC is selected as the authoritative rule representation because it expresses universal conditions, exceptions, negation and relations between people, events and records. Frames are retained for enquiry state and employee records; the circular index handles document retrieval.

### 1.3 Why a parse tree is insufficient

Question: “Does a retired employee with ten years of qualifying service receive pension?” A parse tree records syntactic structure, but it does not contain the pension rule, the meaning of “qualifying service”, the employee's verified service record, or the effective date of the rule. The tree can show that “ten years” modifies “service”; it cannot decide entitlement without domain semantics and facts.

### 1.4 Information not captured by a bare logical form

- **Speaker:** whether the question came from the pensioner, a family member or an officer affects authorization and response style.
- **Utterance time:** rules may change; the system needs a timestamp and the relevant effective date.
- **Certainty:** “I think my service was ten years” is not equivalent to a verified service record.

These are stored as metadata alongside the logical form rather than discarded.

### 1.5 Pipeline

`Enquiry text → tokenization / entity extraction → syntactic parse → semantic composition (lambda terms) → canonical FOPC → WSD + entity normalization → rule engine + TF-IDF retrieval → answer with evidence / clarification`

Each stage has an explicit input and output. The semantic grammar creates a logical form; WSD resolves domain terms; FOPC evaluates entitlement; retrieval finds the governing circular.

---

## TASK 2 – The Meaning Structure of Language

### 2.1 Properties

- **Verifiability:** a representation can be evaluated against a model; every well-formed claim has a truth value under that model.
- **Unambiguous representation:** one intended reading maps to one formal structure.
- **Canonical form:** paraphrases with the same meaning map to the same normalized representation.
- **Inference:** facts and rules can entail conclusions not explicitly stored.
- **Expressiveness:** the formalism can represent the distinctions the application requires.

### 2.2 Three-valued verification

Knowledge base example:
- Verified fact: `Employee(E1)` and `QualifyingYears(E1, 12)`.
- Rule: `Employee(x) ∧ QualifyingYears(x,y) ∧ y ≥ 10 → ServiceConditionMet(x)`.

Results:
1. E1 has met the service condition – **True**, because the fact and rule establish it.
2. E1 has fewer than ten qualifying years – **False**, because the verified record says twelve.
3. E2 has met the service condition – **Unknown**, because no verified service record for E2 exists.

Unknown is necessary because absence of a record is not proof that the person is ineligible.

### 2.3 Canonical form

Paraphrases:
- “Has E1 completed ten years of qualifying service?”
- “Does E1 satisfy the ten-year service requirement?”
- “Is E1's qualifying service at least ten years?”
- “Has E1 served for the minimum qualifying period?”

Canonical representation: `GE(QualifyingYears(E1), 10)`.

A problematic collapse:
- “Does E1 have ten years of service?”
- “Does E1 have ten years of qualifying service?”

Both might be incorrectly mapped to `GE(ServiceYears(E1),10)`. This loses the distinction between total service and service counted under pension rules. The ontology must preserve separate predicates.

### 2.4 Ambiguity

“Does the dependent receive the benefit?” can mean:
1. `EligibleFor(dependent, family_pension)`
2. `EligibleFor(dependent, medical_benefit)`

The context, scheme name or circular reference is required to choose. The system should ask which benefit is intended rather than silently select one.

### 2.5 Expressiveness gaps

Classical FOPC does not natively represent graded uncertainty (“probably eligible”) or statements about the truth of other statements (“the officer stated that the rule applies”). Add confidence/provenance metadata or a probabilistic layer for uncertainty, and reification/modal predicates for statements and sources.

---

## TASK 3 – First Order Predicate Calculus

### 3.1 Elements and truth conditions

- **Terms:** constants, variables and function terms denoting objects.
- **Constants:** `E1`, `CIRC_12`, `SCHEME_A`.
- **Variables:** `x`, `y`, `d`.
- **Functions:** `spouseOf(x)`, `effectiveDate(rule)`.
- **Predicates:** `Employee(x)`, `Dependent(x,y)`, `Eligible(x)`.
- **Connectives:** `¬P` true when P is false; `P ∧ Q` true when both are true; `P ∨ Q` true when at least one is true; `P → Q` false only when P is true and Q false; `P ↔ Q` true when both have the same truth value.
- **Quantifiers:** `∀x P(x)` means every domain object satisfies P; `∃x P(x)` means at least one does.

### 3.2 Pension rules and enquiries

The following are illustrative logical rules, not statements of any particular state's current pension law.

1. Every employee with at least ten qualifying years satisfies the service condition:  
   `∀x∀y((Employee(x) ∧ QualifyingYears(x,y) ∧ y≥10) → ServiceConditionMet(x))`
2. A person who satisfies all applicable conditions is eligible:  
   `∀x((Employee(x) ∧ ServiceConditionMet(x) ∧ AgeConditionMet(x)) → PensionEligible(x))`
3. No person with a disqualifying dismissal is eligible under this sample rule:  
   `∀x(DismissedForMisconduct(x) → ¬PensionEligible(x))`
4. Every family pensioner is a pension beneficiary:  
   `∀x(FamilyPensioner(x) → PensionBeneficiary(x))`
5. A dependent is eligible for family pension only if the dependency and scheme conditions hold:  
   `∀x∀y((Dependent(x,y) ∧ SchemeConditionMet(x)) → FamilyPensionCandidate(x,y))`
6. Every verified circular has an issuing authority:  
   `∀c(VerifiedCircular(c) → ∃a IssuedBy(c,a))`
7. Each employee has exactly one employee identifier:  
   `∀x(Employee(x) → ∃i(EmployeeId(x,i) ∧ ∀j(EmployeeId(x,j) → j=i)))`
8. No circular can be both superseded and currently operative for the same provision:  
   `∀c∀p((SupersededFor(c,p) ∧ OperativeFor(c,p)) → ⊥)`
9. If a person is a spouse of an employee and meets the dependency rule, the person is a family claimant:  
   `∀x∀y((SpouseOf(x,y) ∧ Employee(y) ∧ Dependent(x,y)) → FamilyClaimant(x))`
10. A circular applies to a case only if the case date falls within its effective interval:  
    `∀c∀d((EffectiveFrom(c)≤d ∧ d<EffectiveTo(c)) → ApplicableOn(c,d))`
11. If a claimant is a family pensioner, their eligible ancestor chain can be recursively related:  
    `∀x Ancestor(x,x)` and `∀x∀y∀z((ParentOf(x,y) ∧ Ancestor(y,z)) → Ancestor(x,z))`
12. Enquiry: “Does E1 satisfy the service condition?”  
    `ServiceConditionMet(E1)?`

### 3.3 Model

Domain: `{E1, E2, E3, F1, C1}`. Example extensions:
- `Employee = {E1,E2,E3}`
- `QualifyingYears = {(E1,12),(E2,7),(E3,10)}`
- `ServiceConditionMet = {E1,E3}`
- `DismissedForMisconduct = {E2}`
- `PensionEligible = {E1,E3}`
- `FamilyPensioner = {F1}`
- `PensionBeneficiary = {E1,E3,F1}`

Formula evaluations:
1. `Employee(E1)` – True; E1 is in the extension.
2. `ServiceConditionMet(E2)` – False; E2 is not in the extension.
3. `PensionBeneficiary(F1)` – True; F1 is in the extension.
4. `PensionEligible(E2)` – False; E2 is not eligible in this model.
5. `Employee(F1)` – False; F1 is not an employee.
6. `Dependent(F1,E1)` – Unknown if the relation is not specified in the model; under an open-world interpretation, missing is unknown, not false.

### 3.4 Inference examples

**Inference A:** `FamilyPensioner(F1)` and `∀x(FamilyPensioner(x)→PensionBeneficiary(x))`; by universal instantiation and modus ponens, infer `PensionBeneficiary(F1)`.

**Inference B:** `Employee(E3)`, `QualifyingYears(E3,10)`, and rule 1. By conjunction introduction, form the antecedent; by universal instantiation and modus ponens, infer `ServiceConditionMet(E3)`.

### 3.5 Scope ambiguity

1. “Every employee has a dependent.”  
   `∀x(Employee(x)→∃y Dependent(y,x))` versus `∃y∀x(Employee(x)→Dependent(y,x))`. The first allows a different dependent for each employee; the second says one person is dependent for every employee.
2. “A dependent receives every benefit.”  
   `∃x(Dependent(x) ∧ ∀b Receives(x,b))` versus `∀b∃x(Dependent(x) ∧ Receives(x,b))`.
3. “Every officer checked a circular.”  
   `∀o∃c Checked(o,c)` versus `∃c∀o Checked(o,c)`. Different officers may check different circulars in the first reading.

---

## TASK 4 – Representing Linguistically Relevant Concepts

### 4.1 Categories

Represent categories as unary predicates when membership is being asserted: `Employee(x)`, `Pensioner(x)`, `FamilyPensioner(x)`, `Dependent(x)`. Representing a category as an object (for example, `instanceOf(E1, EmployeeClass)`) is useful for metamodels and category hierarchies, but predicates are simpler for ordinary FOPC inference.

Relations include `DependentOf(person, employee)`, `SpouseOf(person, employee)`, `ParentOf(parent, child)`, `IssuedBy(circular, authority)`, and `AppliesTo(circular, scheme)`.

### 4.2 Event variables

Use an event predicate with event variables and thematic roles:
- `Retire(e) ∧ Agent(e,E1) ∧ Time(e,2020-06-30)`
- `SubmitClaim(e) ∧ Agent(e,F1) ∧ Patient(e,Claim42)`
- `IssueCircular(e) ∧ Agent(e,Directorate) ∧ Patient(e,CIRC12)`
- `VerifyService(e) ∧ Agent(e,Officer7) ∧ Theme(e,RecordE1)`
- `CommutePension(e) ∧ Agent(e,E1) ∧ Theme(e,PensionEntitlement)`

An event variable allows optional participants such as instrument, location or beneficiary to be added without changing a fixed-arity predicate.

### 4.3 Temporal distinctions

- “E1 retired on 30 June 2020.” `Retire(e) ∧ Time(e,2020-06-30)` – bounded past event.
- “E1 was serving in 2019.” `Serve(e) ∧ Overlap(e,2019)` – event overlaps a past interval.
- “E1 has submitted a claim.” `SubmitClaim(e) ∧ Before(e,now)` – completed event with present relevance.
- “E1 will receive a revision from 1 January 2027.” `ReceiveRevision(e) ∧ Time(e,2027-01-01)` – future event.
- “E1 had completed ten years before retirement.” `CompleteService(e1) ∧ Before(e1,RetireEvent(E1))` – service completion precedes retirement.

Tense and aspect affect event time and reference time; a timeless predicate alone cannot preserve them.

### 4.4 Thematic roles

| Predicate / event | Agent | Theme / Patient | Recipient / Beneficiary |
|---|---|---|---|
| SubmitClaim | claimant | claim | — |
| ApproveClaim | officer | claim | claimant |
| IssueCircular | directorate | circular | public |
| VerifyService | auditor | service record | employee |
| PayPension | treasury | pension amount | pensioner |
| NotifyRevision | directorate | revision | pensioner |

Active/passive alternation preserves roles: “The officer approved the claim” and “The claim was approved by the officer” share `Agent=officer` and `Theme=claim`; grammatical subject changes, semantic roles do not.

### 4.5 Named entity recognition

The prototype includes a rule-based recognizer for employee IDs, circular IDs, dates and scheme labels. Evaluate it on 200 manually checked mentions using exact-span precision, recall and F1. The provided synthetic run can count extracted entity types, but its labels are generated from patterns and cannot be described as a 200-mention human gold evaluation. In deployment, NER outputs normalize entities in FOPC, e.g. `E-104` becomes the constant `E104`, and `Circular No. 12/2024` becomes `CIRC_12_2024`.

---

## TASK 5 – Syntax-Driven Semantic Analysis

### 5.1 Compositionality

The principle of compositionality states that sentence meaning is determined by the meanings of its parts and the way they are syntactically combined. The grammar must therefore attach a semantic operation to each production.

Structural contrast:
- “Every employee has a dependent.” `∀x(Employee(x)→∃y Dependent(y,x))`
- “A dependent has every employee.” `∃y(Dependent(y) ∧ ∀x(Employee(x)→Has(y,x)))`
Changing structure changes who is quantified and what relation is asserted.

### 5.2 Lambda notation and sample attachments

Lambda abstraction creates a function; beta reduction substitutes an argument into the function. Example: `(λx.Employee(x))(E1) → Employee(E1)`.

| Grammar rule | Semantic attachment |
|---|---|
| NP → ProperName | constant `e1` |
| N → employee | `λx.Employee(x)` |
| N → dependent | `λx.Dependent(x)` |
| Det → every | `λP.λQ.∀x(P(x)→Q(x))` |
| Det → some | `λP.λQ.∃x(P(x)∧Q(x))` |
| VP → qualifies | `λx.Qualifies(x)` |
| VP → receives pension | `λx.PensionBeneficiary(x)` |
| TV → supports | `λy.λx.Supports(x,y)` |
| PP → of employee | `λx.DependentOf(x,employee)` |
| S → NP VP | application of VP to NP |
| NP → Det N | apply determiner to noun predicate |
| S → S and S | conjunction `φ ∧ ψ` |
| Adj → retired | `λx.Retired(x)` |

The package implements a small pattern-based semantic parser for common enquiry forms. A full feature grammar of 50 productions is a substantial manual resource; the report provides representative attachments and the code explicitly identifies its limited coverage rather than claiming 50 tested rules.

### 5.3 Worked derivations

1. “Is E1 an employee?”  
   NP(E1) = `E1`; VP(employee) = `Employee(x)`; application gives `Employee(E1)`.

2. “Does E1 qualify?”  
   VP(qualify) = `QualifyingServiceMet(x)`; application gives `QualifyingServiceMet(E1)`.

3. “Does every employee qualify?”  
   N = `λx.Employee(x)`; VP = `λx.QualifyingServiceMet(x)`; determiner every gives `∀x(Employee(x)→QualifyingServiceMet(x))`.

4. “Does some dependent receive family pension?”  
   N = `λx.Dependent(x)`; VP = `λx.FamilyPensioner(x)`; some gives `∃x(Dependent(x)∧FamilyPensioner(x))`.

### 5.4 Quantifier scope

“Every employee supports some dependent” has at least two readings:
- `∀x(Employee(x)→∃y(Dependent(y)∧Supports(x,y)))`: each employee may support a different dependent.
- `∃y(Dependent(y)∧∀x(Employee(x)→Supports(x,y)))`: one dependent is supported by all employees.

The default surface-scope attachment produces the first reading. Obtaining the second requires quantifier storage or an alternative scope-ordering mechanism.

### 5.5 Coverage

Coverage is the percentage of enquiry questions receiving a well-formed logical form. The script reports coverage over its generated test questions. Failures are classified as unknown vocabulary, unsupported construction, unresolved entity, ambiguous scope or missing date. The 200 real enquiry coverage figure must be measured after the helpdesk questions are collected.

---

## TASK 6 – Lexemes and Their Senses

### 6.1 Definitions and sense inventory

A **lexeme** is an abstract vocabulary item; a **lemma** is its dictionary headword; a **word form** is an inflected surface form; a **sense** is one meaning of a lexeme; a **synset** groups near-synonymous lexical items for a particular sense.

| Term | Sense 1 | Sense 2 | Sense 3 |
|---|---|---|---|
| service | qualifying employment period | public service department | service provided to a user |
| dependent | financially dependent family member | software variable dependency (out of domain) | person legally recognized as dependent |
| award | pension/gratuity granted | decision by a tribunal | prize |
| benefit | pension entitlement | medical/social welfare facility | advantage or positive effect |
| revision | pension amount recalculation | amendment to a circular | proofreading/editing |
| claim | pension application | assertion of fact | insurance claim |
| commutation | conversion of pension portion to lump sum | general conversion/exchange | — |
| qualifying | counted under pension rules | meeting a general standard | — |
| contribution | employee/employer payment | contribution to discussion | — |
| sanction | official approval | penalty | legal provision |
| charge | fee/deduction | responsibility | accusation |
| account | pension payment account | report/description | calculation record |
| order | official government direction | sequence | request/order in conversation |
| authority | government body | legal power | source/citation |
| family | eligible relation group | household | family as institution |
| retirement | end of service | retirement benefit event | withdrawal from activity |
| pension | periodic retirement payment | general support payment | — |
| arrears | unpaid past amount | overdue debt | — |
| service book | official employment record | book about customer service | — |
| leave | authorized absence | permission to depart | — |
| break | interruption in qualifying service | rest interval | mechanical failure |
| record | service history document | stored data | achievement |
| dependent child | child satisfying scheme dependency rules | any child financially supported | — |
| nominee | person nominated to receive payment | candidate for a position | — |
| family pension | survivor pension entitlement | informal family support | — |

The inventory above contains 25 terms with multiple contextual readings. Each final sense should have a precise gloss, examples and a domain label. The required 600 occurrence annotations are not fabricated here; the package includes a schema for collecting them.

### 6.2 Homonymy and polysemy

Homonymy examples:
- `bank`: financial institution vs river bank (same spelling, unrelated meanings).
- `charge`: fee vs criminal accusation (historically distinct readings in ordinary use).
- `order`: official direction vs sequence/order arrangement (can be treated as homonymous in a strict domain lexicon, though related senses may be analyzed as polysemy).

Polysemy examples:
- `service`: employment period vs public service; related by institutional/service concept (metonymy).
- `revision`: revising a pension amount vs revising a circular; shared “change after review” meaning (generalization).
- `benefit`: pension payment vs advantage; related by a beneficial outcome (metaphorical extension).

The distinction can depend on lexical theory; the inventory records the operational distinction used by this system.

### 6.3 WordNet-style relations

- pension → hypernym: financial benefit → economic resource
- family pension → hyponym: pension → financial benefit
- service record → meronym: record has entries, dates and service periods
- eligible ↔ ineligible: antonyms
- approve ↔ reject: antonyms
- employee → hyponym of person; person → entity
- circular → document → information artifact

Hypernym chains:
1. `family pension → pension → financial benefit → benefit → entity`
2. `employee → worker → person → living entity → entity`

### 6.4 Ambiguity and vagueness

Ambiguity offers distinct readings; vagueness has a boundary that is not sharply specified.
- “service” in “service is ten years” – ambiguous: total employment or qualifying service.
- “dependent” – ambiguous: scheme-defined dependent or ordinary financial dependent.
- “long service” – vague: no precise threshold stated.
- “near retirement age” – vague: boundary depends on policy.
- “benefit” – ambiguous: pension, medical or other benefit.
- “substantial break” – vague unless a rule defines its duration.

### 6.5 Selectional restrictions

| Verb | Expected roles | Satisfying sentence | Violating sentence |
|---|---|---|---|
| retire | person/employee | “E1 retired in 2020.” | “The circular retired in 2020.” |
| approve | authorized agent + claim | “The officer approved the claim.” | “The pension amount approved the officer.” |
| receive | recipient + transferable item | “E1 received pension.” | “The date received pension.” |
| issue | authority + document/order | “The directorate issued a circular.” | “The qualifying years issued a circular.” |
| depend on | outcome + condition | “Eligibility depends on qualifying service.” | “The circular depends the officer.” |

Restrictions are preferences, not always hard constraints. Metaphor, ellipsis and unusual institutional language can violate typical selection patterns while remaining interpretable.

---

## TASK 7 – Word Sense Disambiguation

### 7.1 Simplified Lesk

Lesk selects the sense whose gloss has the greatest word overlap with the context. Remove stop words and compare normalized tokens.

Trace 1: “The employee's qualifying service is twelve years.”
- `service` sense A gloss: “period of employment counted for pension”.
- sense B gloss: “department that provides public services”.
- Context signature overlaps: A = `{employment, counted, pension}`; B = `{department, public, provides}`.
- Select A.

Trace 2: “The officer issued a revised circular.”
- `revision` sense A: “change to pension amount”.
- sense B: “amendment to an official document”.
- Context includes “officer, issued, circular”; B has strongest overlap; select B.

Trace 3: “The dependent submitted a family pension claim.”
- `dependent` sense A: “family member relying on employee for support”.
- sense B: “person or component dependent on another item”.
- Context “family pension claim” supports A.

### 7.2 Variants and baseline

Compare:
1. Lesk with raw glosses.
2. Lesk after stop-word removal.
3. Extended Lesk using glosses of related senses.
4. Most-frequent-sense (MFS) baseline from training labels.

MFS is the necessary baseline because domain terms often have a dominant sense. A WSD system that does not beat MFS may be adding complexity without improving decisions. Accuracy must be reported on held-out human-labelled occurrences, with per-term results.

### 7.3 Supervised method

Use contextual features: target lemma, ±2 surrounding lemmas, part-of-speech tags and collocations. A linear SVM or logistic regression with word n-grams is a suitable baseline. Use five-fold cross-validation grouped by document so near-duplicate contexts do not leak across folds. The included prototype implements a simplified Lesk and MFS baseline; supervised evaluation requires the collected 600 labelled occurrences.

### 7.4 Downstream impact

Run 60 relevance-judged questions with and without sense expansion. Compare answer accuracy and retrieval measures. Sense-aware retrieval should help when a query uses a term in a non-dominant domain sense, but it may harm a query if the WSD module selects the wrong sense. The system should retain the original query terms and use expansion as additional weighted evidence rather than replacing the query.

---

## TASK 8 – Information Retrieval over the Circulars

### 8.1 Index construction

Tokenization: lowercase, split into alphabetic/numeric tokens, preserve identifiers such as `CIRC_12_2024`, remove a documented stop list (`the, is, a, an, of, for, to, and, does, has`), and do not stem identifiers. An inverted index maps each term to document IDs and term frequencies. The term-document matrix stores TF-IDF weights.

### 8.2 TF-IDF

`tf(t,d)` is the number of occurrences of term t in document d (or normalized frequency). `df(t)` is the number of documents containing t. `idf(t)=ln(N/df(t))` (optionally with smoothing). `tfidf=tf×idf`.

Illustrative six-term calculation for N=300:
| Term | df | idf = ln(300/df) | Interpretation |
|---|---:|---:|---|
| pension | 270 | 0.105 | Common term; low discrimination |
| qualifying | 90 | 1.204 | Useful domain discriminator |
| commutation | 25 | 2.485 | Highly specific |
| dependent | 60 | 1.609 | Moderately specific |
| circular | 290 | 0.034 | Nearly universal; almost zero |
| family | 75 | 1.386 | Useful for family-pension queries |

A term present in almost every circular provides little evidence about which circular is relevant, so its IDF approaches zero.

### 8.3 Cosine ranking

For query vector q and document vector d:

`cos(q,d) = (q·d) / (||q|| ||d||)`.

Cosine normalizes for document length. A raw dot product can favour long circulars simply because they contain more terms.

Example query: “qualifying service ten years”. If the query weights are `q=(qualifying:1.2, service:0.8, years:1.0)` and a document vector is `d=(1.2,0.8,0.0)`, then dot product = `1.44+0.64=2.08`; norms are `||q||=sqrt(1.44+0.64+1)=1.755` and `||d||=sqrt(1.44+0.64)=1.442`; cosine ≈ `2.08/(1.755×1.442)=0.822`. The actual code calculates the ranking from the corpus vectors.

### 8.4 Evaluation measures

- **Precision:** fraction of retrieved documents that are relevant.
- **Recall:** fraction of all relevant documents that were retrieved.
- **F1:** harmonic mean of precision and recall.
- **P@10:** precision among the first ten results; useful for the officer's first screen.
- **MAP:** mean of average precision across queries; rewards placing relevant documents early.

Use 60 queries with adjudicated relevant circular IDs. Report lexical and sense-expanded retrieval on the same split. The prototype reports metrics on generated synthetic relevance labels only.

---

## TASK 9 – Annotation, Gold Standard and Evaluation Design

### 9.1 Sense annotation guidelines

Annotators receive the sentence, two sentences of context, target term and candidate glosses. Select the sense that best fits the context; use `OTHER/UNCERTAIN` when no gloss fits. Do not infer a legal meaning from personal knowledge if the circular context does not support it. Borderline cases are independently labelled and adjudicated by a third reviewer.

### 9.2 Relevance judgement guidelines

A circular is relevant if it directly governs the rule or provides authoritative interpretation for the question's scheme and effective date. Label 2 = directly authoritative; 1 = useful background; 0 = not relevant. If a circular is superseded, it may be relevant historically but not as current authority. Annotators record the date and reason.

### 9.3 Agreement

For both sense labels and relevance judgements, report raw agreement and Cohen's kappa. Kappa adjusts for chance agreement. The required independent 200 sense annotations and 15 query judgements must be performed by two people. The synthetic generator cannot provide independent annotators, so this package does not invent agreement figures.

### 9.4 Leakage and confidence

The held-out set must not be used for gloss writing, threshold selection, query expansion tuning or model selection. The greatest leakage risk is manually adding a synonym to a sense signature after inspecting a held-out query. Keep the test questions hidden until the pipeline is frozen. Small evaluation sets have wide uncertainty; report sample sizes and confidence intervals, not only point estimates.

---

## TASK 10 – Implement and Test the Pipeline

### 10.1 Included implementation

The Python package includes:
- FOPC rule facts and a small forward-chaining inference routine;
- three-valued fact lookup;
- rule-based NER for employee/circular IDs and dates;
- simplified Lesk WSD and an MFS baseline;
- TF-IDF vectors, inverted index and cosine ranking;
- query metrics (precision, recall, F1, P@10 and AP);
- tests for representative rules, WSD, and retrieval.

Run:
```bash
python -m pip install -r requirements.txt
python run_assignment.py
python -m unittest discover -s tests -v
```

The prototype is deliberately transparent and dependency-light. It does not claim a 50-rule feature grammar, 600 manual sense labels or 60 human-judged queries. Those are corpus and annotation tasks, not something a script can truthfully manufacture.

### 10.2 Results and plots

The script prints counts, semantic coverage on its sample questions, WSD decisions, retrieval rankings and run time. It saves JSON and CSV output under `outputs/`. For the final report, add at least two plots:
1. Retrieval MAP against vocabulary size.
2. WSD accuracy against the number of annotated training examples.

The package includes plotting code that can be run when matplotlib is available; plots from synthetic data must be labelled synthetic.

---

## TASK 11 – Compare, Recommend and Defend the Semantic Design

| Approach | Answer accuracy | Coverage | Runtime | Maintenance |
|---|---|---|---|---|
| Keyword retrieval only | Cannot logically prove eligibility | Broad document coverage | Low | Low–medium |
| Retrieval + sense expansion | Better when domain terms are ambiguous | Broad, dependent on WSD | Low–medium | Medium; glosses need updates |
| Logical form + FOPC KB | Strong for explicitly encoded rules | Limited to grammar and KB coverage | Low for small KB | High; rules need legal review |
| Hybrid: FOPC + WSD + retrieval | Combines rule answers and documentary evidence | Highest expected coverage | Medium | Highest initial effort |

Recommendation: use the hybrid architecture. If the enquiry is a well-formed eligibility question and the relevant facts are verified, answer through the rule engine and cite the governing circular. If the question asks “which circular”, use retrieval and rank authoritative documents. If the logical form is ambiguous or the evidence is incomplete, ask a clarification or route to an officer. Never convert unknown into “not eligible”.

A pensioner should see a clear status: “The available record is insufficient to decide; please provide the service-book extract” rather than a fabricated yes/no answer. Legal rules must be reviewed by pension-domain officers whenever a circular changes.

Manual work includes legal rule extraction, ontology design, grammar writing, sense annotation, relevance judgement and adjudication. More annotated data is more valuable than more hand-written rules when the rules already cover the question form but WSD or entity extraction remains inaccurate. Conversely, a missing legal exception requires a rule update, not more training examples.

---

## TASK 12 – Day-4 Design Challenge

### A. Impact analysis

The new scheme introduces cross-referenced rules, effective dates, broken-service aggregation and threshold conditions. The original timeless FOPC representation does not record which version of a rule applies. Plain FOPC can express finite arithmetic facts if expanded into predicates, but it is awkward for aggregation over many service intervals, date arithmetic and database-scale joins. The original grammar also handles mostly single-clause questions and may fail on nested questions combining retirement date, breaks and family-pension status.

Expected impact: semantic coverage falls because the grammar lacks temporal and aggregation constructions; answer accuracy falls if the system applies a current rule to a historical retirement date. The amount of degradation must be measured on a separately created challenge set rather than guessed.

### B. Original-design traces

1. **Cross-reference:** “Does clause 4 apply if clause 2 is satisfied?” Original parser may produce `Applies(Clause4,Case)` but cannot recursively resolve the dependency without a rule-reference graph. First failure: rule engine.
2. **Date:** “I retired in 2019; which revision applies?” A timeless predicate cannot select the correct effective version. First failure: temporal applicability stage.
3. **Aggregation:** “I had two breaks; do my completed periods total ten qualifying years?” A simple predicate `QualifyingYears(E1,10)` requires the total to be calculated from interval records. First failure: missing aggregation/query layer.

The challenge set should be evaluated for semantic coverage, answer accuracy and retrieval quality against the original baseline. The sample traces expose structural failures; they are not a substitute for measured evaluation.

### C. Adaptation decision: MODIFY

Retain FOPC for rule relationships, but add:
- **Temporal arguments:** `Applies(rule,case,date)` and `EffectiveInterval(rule,start,end)`.
- **Versioned rules:** each rule has `valid_from`, `valid_to`, source circular and supersession metadata.
- **Event/service intervals:** `ServicePeriod(employee,start,end,qualifying_status)`.
- **Aggregation layer:** SQL/database query calculates total qualifying days/years after applying break-counting policy.
- **Rule engine:** forward chaining for cross-references and dependency graphs, with cycle detection.
- **Grammar:** attachments for “as of date”, “before retirement”, “including breaks”, “total years” and nested clause references.
- **Index:** add effective-date, scheme, clause, superseded/current and cross-reference fields; use date-aware filtering before ranking.

The revised pipeline is: parse enquiry → temporal and entity extraction → logical form → resolve rule dependencies → query service-period database → evaluate versioned rules → retrieve supporting circulars → explain result with provenance.

### D. Evidence-based defence

Modification is preferable to replacing everything. FOPC remains useful for quantified eligibility and rule implications, while SQL is better for summing many service intervals and temporal databases are better for date validity. A rule graph handles clause dependencies. The decision follows from the original architecture's identified gaps: timeless predicates cannot choose historical rules, and a fixed service-years fact cannot derive totals from multiple intervals.

Remaining limitations include poorly worded enquiries, incomplete service records, legal ambiguity in a circular, contradictory amendments and rules that require human legal interpretation. The system must abstain and escalate if the effective circular is disputed, a service interval is missing, a dependency cycle is detected, or the legal meaning cannot be represented safely.

---

## Conclusion

A pension helpdesk needs both symbolic meaning and document evidence. FOPC provides explicit, inspectable rules; syntax-driven semantics maps enquiries into logical forms; WSD distinguishes domain senses; and TF-IDF retrieval finds relevant circulars. A hybrid system is safer than keyword search alone because it can separate a proved entitlement condition from a merely relevant document. The Day-4 scheme requires temporal rule versioning, cross-reference resolution and database aggregation while retaining FOPC for logical constraints.

## References

1. Russell, S. J., & Norvig, P. *Artificial Intelligence: A Modern Approach*. Sections on first-order logic and knowledge representation.
2. Jurafsky, D., & Martin, J. H. *Speech and Language Processing*. Sections on lexical semantics, WSD and information retrieval.
3. Lesk, M. (1986). Automatic Sense Disambiguation Using Machine Readable Dictionaries: How to Tell a Pine Cone from an Ice Cream Cone. *Proceedings of SIGDOC*.
4. Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
5. WordNet: A Lexical Database for English. Princeton University.
6. Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, 20(1), 37–46.
7. Gruber, T. R. (1993). A translation approach to portable ontology specifications. *Knowledge Acquisition*, 5(2), 199–220.
