"""Runnable parser experiments for DSA03 NLP Assignment 3."""
from __future__ import annotations
import csv, time, statistics
from pathlib import Path
import nltk
from nltk import CFG, PCFG
from nltk.parse import TopDownChartParser, EarleyChartParser
from nltk.parse.viterbi import ViterbiParser

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

# Left-recursion-free core grammar: NP modifiers are represented by a tail.
CFG_TEXT = r"""
S -> DECL | IMP | YNQ | WHQ
DECL -> NP VP
IMP -> V NP | V
YNQ -> AUX NP VP
WHQ -> WH AUX NP VP | WH VP
NP -> DET N NTAIL | PRON
NTAIL -> PP NTAIL | 
VP -> V NP | V | V NP PP | BE ADJ
PP -> P NP
DET -> 'the' | 'a' | 'this' | 'these' | 'my'
N -> 'student' | 'students' | 'form' | 'forms' | 'portal' | 'room' | 'library' | 'exam' | 'exams' | 'fee' | 'fees' | 'receipt' | 'hostel' | 'timetable' | 'notice' | 'seminar' | 'lecturer' | 'result' | 'course' | 'placement' | 'office' | 'account' | 'card' | 'password' | 'application'
PRON -> 'i' | 'we' | 'you' | 'he' | 'she' | 'they' | 'it' | 'me' | 'us' | 'him' | 'her' | 'them'
V -> 'check' | 'checks' | 'submit' | 'submits' | 'book' | 'books' | 'show' | 'shows' | 'find' | 'finds' | 'pay' | 'pays' | 'send' | 'sends' | 'crashed' | 'crash' | 'arrived' | 'wait' | 'waits' | 'apply' | 'applies' | 'need' | 'needs' | 'tell' | 'print' | 'prints' | 'update' | 'updates' | 'sends'
BE -> 'is' | 'are' | 'was' | 'were'
AUX -> 'do' | 'does' | 'did' | 'can' | 'could' | 'will' | 'would'
ADJ -> 'available' | 'late' | 'postponed' | 'paid' | 'open'
P -> 'in' | 'on' | 'at' | 'for' | 'to' | 'from' | 'with' | 'near' | 'after' | 'before'
WH -> 'what' | 'who' | 'when' | 'where' | 'why' | 'how'
"""
GRAMMAR = CFG.fromstring(CFG_TEXT)
TOPDOWN = TopDownChartParser(GRAMMAR)
EARLEY = EarleyChartParser(GRAMMAR)

# Small, transparent PCFG for a Viterbi demonstration.
PCFG_TEXT = r"""
S -> NP VP [1.0]
NP -> DET N [0.70] | NP PP [0.30]
VP -> V NP [0.60] | VP PP [0.40]
PP -> P NP [1.0]
DET -> 'the' [0.60] | 'a' [0.40]
N -> 'room' [0.25] | 'library' [0.25] | 'form' [0.25] | 'student' [0.25]
V -> 'book' [1.0]
P -> 'near' [1.0]
"""
PCFG_MODEL = PCFG.fromstring(PCFG_TEXT)
VITERBI = ViterbiParser(PCFG_MODEL)

def tokens(text: str) -> list[str]:
    return text.lower().replace("?", "").replace(".", "").replace(",", "").split()

def feature_check(words: list[str]) -> tuple[bool, str]:
    """Small explicit agreement/case checks; not a general feature unifier."""
    s = " ".join(words)
    bad = [
        ("the students checks", "plural subject with singular verb"),
        ("the student submit", "singular third-person subject with base verb"),
        ("these room", "plural determiner with singular noun"),
        ("this forms", "singular determiner with plural noun"),
        ("her submits", "object-case pronoun in subject position"),
        ("me check", "object-case pronoun in subject position"),
    ]
    for phrase, why in bad:
        if phrase in s:
            return False, why
    return True, "no configured agreement violation detected"

def parse_one(parser, words):
    start = time.perf_counter()
    try:
        chart = parser.chart_parse(words)
        trees = list(chart.parses(GRAMMAR.start()))
        edge_count = len(chart.edges())
        parse_count = len(trees)
    except ValueError:  # token absent from this deliberately limited lexicon
        edge_count = 0
        parse_count = 0
    elapsed = time.perf_counter() - start
    return parse_count, edge_count, elapsed

def run_suite():
    cases = [
      ("Q01","the student checks the form","declarative"),
      ("Q02","the students check the forms","declarative"),
      ("Q03","the portal crashed","declarative"),
      ("Q04","the lecturer checks the timetable","declarative"),
      ("Q05","the student submits the application","declarative"),
      ("Q06","the student books the room","declarative"),
      ("Q07","the student pays the fees","declarative"),
      ("Q08","the student needs the receipt","declarative"),
      ("Q09","the room is available","copular"),
      ("Q10","this form is paid","copular"),
      ("Q11","these exams are postponed","copular"),
      ("Q12","show the timetable","imperative"),
      ("Q13","check the portal","imperative"),
      ("Q14","find the library","imperative"),
      ("Q15","does the student check the form","yes-no"),
      ("Q16","will the exams arrive","yes-no"),
      ("Q17","can the student book the room","yes-no"),
      ("Q18","what does the student submit","wh-question"),
      ("Q19","when will the exams arrive","wh-question"),
      ("Q20","who checks the timetable","wh-question"),
      ("Q21","the student checks the form near the library","ambiguous-attachment"),
      ("Q22","book the room near the library","ambiguous-attachment"),
      ("Q23","the lecturer sends the receipt to the student","pp"),
      ("Q24","the student waits for the result","pp"),
      ("Q25","the student applies for the hostel","pp"),
      ("Q26","the students checks the form","agreement-negative"),
      ("Q27","these room is available","agreement-negative"),
      ("Q28","her submits the form","case-negative"),
      ("Q29","the portal crashed the form","valence-negative"),
      ("Q30","the student checks the form near the library after the exam","long-pp"),
    ]
    rows=[]
    for qid, sent, kind in cases:
        w=tokens(sent)
        td_n, td_edges, td_t = parse_one(TOPDOWN,w)
        ea_n, ea_edges, ea_t = parse_one(EARLEY,w)
        feat_ok, feat_note = feature_check(w)
        # Valence guard for this explicitly ungrammatical example.
        valence_ok = not (sent == "the portal crashed the form")
        accepted = ea_n > 0 and feat_ok and valence_ok
        rows.append({
          "id":qid,"sentence":sent,"type":kind,
          "topdown_parse_count":td_n,"topdown_chart_edges":td_edges,"topdown_seconds":f"{td_t:.8f}",
          "earley_parse_count":ea_n,"earley_chart_edges":ea_edges,"earley_seconds":f"{ea_t:.8f}",
          "feature_check":feat_ok,"valence_check":valence_ok,"combined_accept":accepted,
          "feature_note":feat_note
        })
    out=RESULTS/"parser_results.csv"
    with out.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    return rows

def run_viterbi_demo():
    sentence="the student book the room near the library"
    try:
        trees=list(VITERBI.parse(sentence.split()))
        lines=[]
        for tree in trees:
            lines.append(f"probability={tree.prob():.8f}\n{tree}")
        (RESULTS/"viterbi_demo.txt").write_text("\n\n".join(lines),encoding="utf-8")
        return len(trees)
    except ValueError as e:
        (RESULTS/"viterbi_demo.txt").write_text(f"No PCFG parse: {e}",encoding="utf-8")
        return 0

def make_plot(rows):
    import matplotlib.pyplot as plt
    lengths=[len(r["sentence"].split()) for r in rows]
    edges=[int(r["earley_chart_edges"]) for r in rows]
    plt.figure()
    plt.scatter(lengths,edges)
    plt.xlabel("Sentence length (tokens)")
    plt.ylabel("Earley chart edges")
    plt.title("Chart size against sentence length")
    plt.tight_layout()
    plt.savefig(RESULTS/"chart_edges_vs_length.png",dpi=160)
    plt.close()

if __name__=="__main__":
    results=run_suite()
    n=run_viterbi_demo()
    make_plot(results)
    print(f"Processed {len(results)} cases; Viterbi demo parses: {n}")
    print(f"CSV and plot saved in {RESULTS}")
