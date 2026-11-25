"""
DSA03 NLP Assignment 5 – reproducible teaching prototype.
Uses Python standard library; scikit-learn is optional for dialogue-act classification.
"""
import argparse, csv, json, os, random, re, time, tracemalloc, math
from collections import Counter, defaultdict

MARKERS = ["because", "therefore", "however", "after that", "meanwhile", "but", "so"]
PRONOUNS = {"it","they","them","he","she","this","that","these","those"}

def segment(text):
    # Lightweight sentence and cue-based segmentation.
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    out=[]
    for s in sentences:
        if not s: continue
        low=s.lower()
        cue=next((m for m in MARKERS if low.startswith(m+" ")), None)
        out.append({"text":s, "cue":cue, "unit":"relation" if cue else "assertion"})
    return out

def shallow_hobbs(text):
    # Approximation: candidate NPs are entity-like noun phrases from prior sentences.
    sents=re.split(r'(?<=[.!?])\s+', text.strip())
    entities=[]
    results=[]
    for i,s in enumerate(sents):
        words=re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", s)
        for w in words:
            if w.lower() in PRONOUNS:
                candidates=list(reversed(entities))
                chosen=candidates[0] if candidates else None
                results.append({"pronoun":w,"sentence":i,"candidate_order":candidates,"antecedent":chosen})
        # noun phrase heuristic: proper nouns and selected common entities
        for m in re.finditer(r"\b(?:the|a|an)\s+([A-Za-z]+(?:\s+[A-Za-z]+){0,2})", s, re.I):
            np=m.group(1).strip()
            if np.lower() not in PRONOUNS: entities.append(np)
        for m in re.finditer(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b", s):
            if m.group(1) not in entities: entities.append(m.group(1))
    return results

def centering(sentences):
    prev=None; rows=[]
    for s in sentences:
        ents=re.findall(r"\b(?:the\s+)?(bridge|road|camp|shelter|river|school)\b",s.lower())
        ents=list(dict.fromkeys(ents))
        cb=next((e for e in ents if e==prev), None)
        if prev is None: trans="Start"
        elif cb==prev: trans="Continue"
        elif cb is not None: trans="Retain"
        else: trans="Shift"
        rows.append({"sentence":s,"Cf":ents,"Cb":cb,"transition":trans})
        if ents: prev=ents[0]
    return rows

def entity_grid(text):
    sents=re.split(r'(?<=[.!?])\s+',text.strip())
    entities=["bridge","road","camp","shelter","river"]
    grid=[]
    for s in sents:
        row={}
        toks=s.lower().split()
        for e in entities:
            if e in toks or e+"s" in toks:
                row[e]="S" if toks and toks[0].strip(".,") in (e,"the") else "X"
            else: row[e]="-"
        grid.append(row)
    trans=Counter()
    for a,b in zip(grid,grid[1:]):
        for e in entities:
            trans[a[e]+b[e]]+=1
    return {"grid":grid,"transitions":dict(trans)}

def frame_manager(utterance, state=None):
    state=dict(state or {})
    low=utterance.lower()
    if any(x in low for x in ["cancel","stop"]):
        state["status"]="cancelled"; return state, "Your request has been cancelled."
    patterns={"location":r"(?:near|at|in)\s+([A-Za-z ]+?)(?:,|\.|$)",
              "family_size":r"\b(\d+)\s+(?:people|persons|members)\b"}
    for slot,pat in patterns.items():
        m=re.search(pat,utterance,re.I)
        if m: state[slot]=int(m.group(1)) if slot=="family_size" else m.group(1).strip()
    if "wheelchair" in low: state["accessibility"]="wheelchair"
    if "walking" in low: state["travel_mode"]="walking"
    missing=[s for s in ("location",) if not state.get(s)]
    return state, ("Which area are you currently in?" if missing else "I will check verified open relief camps near "+state["location"]+".")

def realize(fact):
    typ=fact.get("type")
    if typ=="road": return f"{fact['name']} is {fact['status']}."
    if typ=="camp": return f"{fact['name']} can accommodate {fact['capacity']} people."
    if typ=="outage": return f"A power outage is confirmed in {fact['location']}."
    if typ=="advice": return f"Avoid {fact['location']} until the inspection is complete."
    raise ValueError("Unsupported or incomplete fact")

def generate_bulletin(incidents):
    lines=[]
    for x in incidents:
        if x.get("verification_status")!="verified": continue
        if x["incident_type"]=="road": lines.append(realize({"type":"road","name":x["road_name"],"status":x["status"]}))
        elif x["incident_type"]=="shelter": lines.append(realize({"type":"camp","name":x["shelter_name"],"capacity":x["shelter_capacity"]}))
        elif x["incident_type"]=="power": lines.append(realize({"type":"outage","location":x["location"]}))
    return " ".join(lines)

def ibm1_one_iteration(source, target):
    # Single pair, uniform initialization, one E/M iteration for lexical counts.
    src=source.split(); tgt=target.split()
    vocab=set(tgt)
    t={ (e,f):1/len(vocab) for e in vocab for f in set(src)}
    counts=Counter(); totals=Counter()
    for e in tgt:
        z=sum(t[(e,f)] for f in src)
        for f in src:
            c=t[(e,f)]/z
            counts[(e,f)]+=c; totals[f]+=c
    new={}
    for (e,f),c in counts.items(): new[(e,f)]=c/totals[f]
    return {"fractional_counts":dict((f"{e}|{f}",round(v,4)) for (e,f),v in counts.items()),
            "probabilities":dict((f"{e}|{f}",round(v,4)) for (e,f),v in new.items())}

def make_data(seed=7, n_reports=1200):
    random.seed(seed)
    places=["Market Road","East Bridge","River Road","North Zone","Old Bus Stand","School Camp"]
    reports=[]; refs=[]
    for i in range(n_reports):
        p=random.choice(places)
        kind=random.choice(["flood","road","power","shelter"])
        if kind=="flood":
            txt=f"Floodwater reached {p}. It is rising after heavy rain. Therefore residents should avoid the low area."
        elif kind=="road":
            txt=f"The road at {p} is closed. It remains unsafe for buses. Police have opened a diversion."
        elif kind=="power":
            txt=f"A power failure was reported in {p}. It affected nearby houses. The utility team is checking it."
        else:
            txt=f"The relief camp at {p} is open. It can receive families today. The camp has limited capacity."
        txt += " Control room staff recorded this update and asked residents to follow verified district announcements. Do not cross barricades or enter moving water while response teams inspect the affected location. Officials will publish another status update after field verification is completed."
        reports.append({"report_id":i+1,"incident_id":f"INC-{i//3:04d}","text":txt})
        refs.append({"report_id":i+1,"expression":"it","antecedent":p,"distance":1})
    dialogues=[]
    for i in range(300):
        dialogues.append([
            ("Hello, I am near Market Road.","PROVIDE_SLOT"),
            ("Which relief camp is open?","REQUEST_INFO"),
            ("The School Camp is open.","INFORM"),
            ("Thank you.","THANK")
        ])
    return reports, refs, dialogues

def act_classifier(dialogues):
    X=[]; y=[]
    for d in dialogues:
        for turn,(utt,tag) in enumerate(d):
            X.append(f"{utt} POS{turn}"); y.append(tag)
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.metrics import accuracy_score, confusion_matrix
        Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=7,stratify=y)
        model=make_pipeline(TfidfVectorizer(ngram_range=(1,2)),LogisticRegression(max_iter=500))
        model.fit(Xtr,ytr); pred=model.predict(Xte)
        return {"accuracy":round(accuracy_score(yte,pred),4),
                "labels":sorted(set(y)),"confusion_matrix":confusion_matrix(yte,pred,labels=sorted(set(y))).tolist()}
    except Exception as e:
        return {"status":"scikit-learn unavailable or training failed","detail":str(e)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seed",type=int,default=7)
    ap.add_argument("--reports",type=int,default=1200)
    args=ap.parse_args()
    tracemalloc.start(); t0=time.perf_counter()
    reports,refs,dialogs=make_data(args.seed,args.reports)
    tokens=sum(len(r["text"].split()) for r in reports)
    cross=sum(1 for r in refs if r["expression"]=="it")
    sample=reports[0]["text"]
    result={
      "seed":args.seed,"reports":len(reports),"report_tokens":tokens,
      "multi_sentence_reports":sum(1 for r in reports if len(segment(r["text"]))>1),
      "cross_sentence_reference_rate":round(cross/len(reports),4),
      "sample_segments":segment(sample),
      "sample_hobbs_trace":shallow_hobbs(sample),
      "sample_centering":centering(re.split(r'(?<=[.!?])\s+',sample)),
      "sample_entity_grid":entity_grid(sample),
      "dialogues":len(dialogs),"dialogue_act_classifier":act_classifier(dialogs),
      "frame_trace":frame_manager("I am near Market Road and need wheelchair access"),
      "generated_bulletin":generate_bulletin([{"incident_type":"road","road_name":"East Bridge","status":"closed","verification_status":"verified"}]),
      "ibm1_demo":ibm1_one_iteration("road closed","சாலை மூடப்பட்டது")
    }
    elapsed=time.perf_counter()-t0
    current,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    result["runtime_seconds"]=round(elapsed,4); result["memory_peak_bytes"]=peak
    os.makedirs("outputs",exist_ok=True)
    with open("outputs/run_results.json","w",encoding="utf-8") as f: json.dump(result,f,ensure_ascii=False,indent=2)
    with open("outputs/reports_sample.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=reports[0].keys()); w.writeheader(); w.writerows(reports[:100])
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
