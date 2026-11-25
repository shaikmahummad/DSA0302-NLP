"""
DSA03 NLP Assignment 4 – meaning, WSD and retrieval prototype.
Synthetic teaching demo; not a legal pension eligibility engine.
"""
import re, json, math, csv, time, random, argparse, os
from collections import Counter, defaultdict

STOP={"the","is","a","an","of","for","to","and","does","has","do","in","on","my","i","am"}

RULES=[
 ("Employee(E1)","ServiceYears(E1,12)"),
 ("Employee(E2)","ServiceYears(E2,7)"),
 ("Employee(E3)","ServiceYears(E3,10)"),
]
FACTS={"Employee(E1)","Employee(E2)","Employee(E3)","FamilyPensioner(F1)"}
def truth(query):
    if query in FACTS: return "true"
    if query.startswith("NOT "):
        q=query[4:]
        return "false" if q in FACTS else "unknown"
    return "unknown"

def infer_service():
    out=set(FACTS)
    for e,y in [("E1",12),("E2",7),("E3",10)]:
        if y>=10: out.add(f"ServiceConditionMet({e})")
    if "FamilyPensioner(F1)" in out: out.add("PensionBeneficiary(F1)")
    return out

def ner(text):
    patterns={
      "EMPLOYEE_ID":r"\bE[-_]?\d{1,5}\b",
      "CIRCULAR_ID":r"\b(?:CIRC(?:ULAR)?)[-_ ]?(?:NO\.?\s*)?[\w/-]+\b",
      "DATE":r"\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}-\d{2}-\d{2})\b",
      "SCHEME":r"\b(?:SCHEME[_ ]?[A-Z0-9]+)\b"
    }
    return {k:re.findall(p,text,re.I) for k,p in patterns.items()}

SENSES={
 "service":[
  {"id":"qualifying_service","gloss":"period of employment counted for pension qualifying service"},
  {"id":"public_service","gloss":"department or organization providing public services"}
 ],
 "dependent":[
  {"id":"family_dependent","gloss":"family member financially dependent on employee"},
  {"id":"general_dependent","gloss":"person or thing relying on another"}
 ],
 "revision":[
  {"id":"pension_revision","gloss":"change or recalculation of pension amount"},
  {"id":"document_revision","gloss":"amendment to an official circular or document"}
 ],
 "benefit":[
  {"id":"pension_benefit","gloss":"pension payment or entitlement"},
  {"id":"general_advantage","gloss":"advantage or positive result"}
 ],
 "award":[
  {"id":"grant_award","gloss":"pension or gratuity officially granted"},
  {"id":"tribunal_award","gloss":"formal decision made by a tribunal"}
 ]
}
def words(s):
    return [w for w in re.findall(r"[a-z0-9_]+",s.lower()) if w not in STOP]
def lesk(context, term):
    ctx=set(words(context))
    senses=SENSES.get(term.lower(),[])
    scored=[]
    for s in senses:
        sig=set(words(s["gloss"]))
        scored.append((len(ctx & sig),s["id"],sorted(ctx & sig)))
    scored.sort(reverse=True)
    return {"scores":[{"overlap":a,"sense":b,"words":c} for a,b,c in scored],
            "selected":scored[0][1] if scored else None}

DOCS=[
 {"id":"CIRC_01","text":"Qualifying service is the period of employment counted for pension eligibility. Employees with ten qualifying years satisfy the service condition."},
 {"id":"CIRC_02","text":"Family pension is a benefit payable to an eligible dependent family member after the employee dies, subject to scheme conditions."},
 {"id":"CIRC_03","text":"Commutation converts a portion of pension into a lump sum payment under the applicable rules."},
 {"id":"CIRC_04","text":"A revised circular changes the pension amount from its effective date. Earlier provisions may be superseded."},
 {"id":"CIRC_05","text":"The service department maintains service books and verifies qualifying periods and breaks in service."},
 {"id":"CIRC_06","text":"A dependent must meet the definition and conditions in the relevant family pension scheme."}
]
def build_index(docs):
    tf=[]; df=Counter(); inv=defaultdict(list)
    for d in docs:
        c=Counter(words(d["text"])); tf.append(c)
        for term,n in c.items():
            df[term]+=1; inv[term].append((d["id"],n))
    N=len(docs); vecs=[]
    for c in tf:
        v={t:n*math.log((N+1)/(df[t]+1)) for t,n in c.items()}
        vecs.append(v)
    return {"df":df,"inv":inv,"vectors":vecs,"docs":docs}
def cosine(a,b):
    dot=sum(v*b.get(k,0) for k,v in a.items())
    na=math.sqrt(sum(v*v for v in a.values())); nb=math.sqrt(sum(v*v for v in b.values()))
    return dot/(na*nb) if na and nb else 0.0
def search(query,index,expand=False):
    q=Counter(words(query))
    if expand:
        for term in list(q):
            r=lesk(query,term)
            if r["selected"]:
                gloss=next((s["gloss"] for s in SENSES.get(term,[]) if s["id"]==r["selected"]),"")
                q.update(words(gloss))
    df=index["df"]; N=len(index["docs"])
    qv={t:n*math.log((N+1)/(df.get(t,0)+1)) for t,n in q.items()}
    scores=[]
    for d,v in zip(index["docs"],index["vectors"]):
        scores.append((round(cosine(qv,v),4),d["id"]))
    return sorted(scores,reverse=True)
def retrieval_metrics(retrieved,relevant,k=10):
    got=set(retrieved[:k]); rel=set(relevant)
    p=len(got&rel)/len(got) if got else 0
    r=len(got&rel)/len(rel) if rel else 0
    f=2*p*r/(p+r) if p+r else 0
    hits=0; ap=0
    for rank,x in enumerate(retrieved,1):
        if x in rel:
            hits+=1; ap+=hits/rank
    ap=ap/len(rel) if rel else 0
    return {"precision":p,"recall":r,"f1":f,"p_at_10":p,"average_precision":ap}
def parse_enquiry(q):
    low=q.lower()
    m=re.search(r"\b(e[-_]?\d+)\b",low)
    ent=m.group(1).replace("-","").upper() if m else None
    if ent and ("qualifying service" in low or "service condition" in low):
        return f"ServiceConditionMet({ent})"
    if ent and ("employee" in low):
        return f"Employee({ent})"
    if "family pension" in low:
        return "FamilyPension"
    return None
def answer(q):
    lf=parse_enquiry(q)
    if not lf: return {"logical_form":None,"answer":"clarification_required"}
    facts=infer_service()
    if lf in facts: return {"logical_form":lf,"answer":"true"}
    if lf.startswith("ServiceConditionMet(") and lf not in facts:
        return {"logical_form":lf,"answer":"false"}
    return {"logical_form":lf,"answer":"unknown"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seed",type=int,default=17)
    args=ap.parse_args()
    random.seed(args.seed)
    t=time.perf_counter()
    idx=build_index(DOCS)
    qs=["What is qualifying service?","How is family pension paid?","What is commutation of pension?","Which circular revises pension amount?","Who is a dependent?","How are service breaks counted?"]
    results=[]
    for q in qs:
        results.append({"query":q,"lexical":search(q,idx,False)[:3],"sense_aware":search(q,idx,True)[:3]})
    payload={
      "seed":args.seed,
      "documents":len(DOCS),
      "sample_questions":len(qs),
      "semantic_answers":[answer("Does E1 satisfy the qualifying service condition?"),answer("Does E2 satisfy the qualifying service condition?")],
      "ner_demo":ner("Employee E-104 retired on 2020-06-30 under SCHEME_A; see CIRC_12_2024."),
      "lesk_demo":lesk("The employee qualifying service is twelve years","service"),
      "retrieval":results,
      "runtime_seconds":round(time.perf_counter()-t,6),
      "warning":"Synthetic demonstration only; not an authoritative pension rules engine."
    }
    os.makedirs("outputs",exist_ok=True)
    with open("outputs/results.json","w",encoding="utf-8") as f: json.dump(payload,f,indent=2)
    with open("outputs/retrieval.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["query","lexical","sense_aware"]);w.writeheader();w.writerows(results)
    print(json.dumps(payload,indent=2))
if __name__=="__main__": main()
