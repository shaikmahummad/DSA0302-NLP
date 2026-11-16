"""
DSA03 NLP Assignment 2 – reproducible synthetic corpus and n-gram starter.
IMPORTANT: Synthetic data is for pipeline testing only. It is not human annotation
and cannot satisfy the assignment's double-annotation or real ASR requirements.
Python standard library only. Run: python nlp_assignment2_starter.py
"""
import random, re, math, json, time, collections
from pathlib import Path

SEED = 42
N_UTTERANCES = 20000
OUT = Path("nlp_assignment2_outputs")
OUT.mkdir(exist_ok=True)

templates = [
    ["please", "book", "a", "ticket", "from", "{origin}", "to", "{dest}"],
    ["what", "time", "does", "the", "bus", "to", "{dest}", "leave"],
    ["is", "there", "a", "train", "from", "{origin}", "at", "{time}"],
    ["how", "much", "is", "a", "ticket", "to", "{dest}"],
    ["i", "need", "to", "cancel", "my", "ticket"],
    ["when", "will", "the", "next", "bus", "arrive"],
    ["please", "tell", "me", "the", "fare", "from", "{origin}", "to", "{dest}"],
    ["does", "this", "train", "stop", "at", "{dest}"],
    ["i", "want", "a", "return", "ticket", "to", "{dest}"],
    ["the", "bus", "stand", "is", "near", "{origin}"],
]
places = ["vellore","chennai","madurai","katpadi","arani","tirupati","kanchipuram",
          "ambur","jolarpettai","salem","coimbatore","trichy","bangalore","arcot"]
times = ["06:30","07:15","08:00","09:45","13:20","18:10","21:00"]
def generate():
    rng = random.Random(SEED)
    rows=[]
    for i in range(N_UTTERANCES):
        t = list(rng.choice(templates))
        origin, dest = rng.sample(places, 2)
        t = [x.replace("{origin}",origin).replace("{dest}",dest).replace("{time}",rng.choice(times)) for x in t]
        # Small natural variation, still deterministic.
        if rng.random() < .18: t.insert(0, rng.choice(["hello","hi","excuse","please"]))
        if rng.random() < .12: t.append(rng.choice(["please","thank","you"]))
        rows.append((f"utt_{i:05d}", t))
    rng.shuffle(rows)
    return rows

def split_rows(rows):
    # Split utterances, not tokens. Deterministic shuffle already applied.
    n=len(rows); a=int(.8*n); b=int(.9*n)
    return rows[:a], rows[a:b], rows[b:]

def count_words(rows):
    c=collections.Counter(w.lower() for _, sent in rows for w in sent)
    return c, sum(c.values())

def vocab_for(counter, threshold):
    # Rare words with count <= threshold become UNK.
    return {w for w,n in counter.items() if n > threshold}

def map_rows(rows, vocab):
    return [(uid,[w if w in vocab else "<UNK>" for w in sent]) for uid,sent in rows]

def ngram_counts(rows, order):
    counts=collections.Counter(); contexts=collections.Counter()
    for _, sent in rows:
        seq=["<s>"]*(order-1)+sent+["</s>"]
        for i in range(order-1,len(seq)):
            gram=tuple(seq[i-order+1:i+1]); counts[gram]+=1
            contexts[gram[:-1]]+=1
    return counts, contexts

def logprob_bigram(w, h, counts, contexts, V, k=0.0):
    num=counts[(h,w)] + k
    den=contexts[(h,)] + k*V
    if den == 0 or num == 0: return float("-inf")
    return math.log(num/den)

def evaluate_bigram(rows, counts, contexts, vocab, k=0.1):
    V=max(1,len(vocab))
    total_log=0.0; n=0; zeros=0
    for _, sent in rows:
        seq=["<s>"]+sent+["</s>"]
        for h,w in zip(seq,seq[1:]):
            lp=logprob_bigram(w,h,counts,contexts,V,k)
            if lp == float("-inf"): zeros+=1
            else: total_log += lp
            n+=1
    if zeros: return {"events":n,"zero_events":zeros,"cross_entropy_bits":None,"perplexity":float("inf")}
    H=-total_log/(n*math.log(2))
    return {"events":n,"zero_events":0,"cross_entropy_bits":H,"perplexity":2**H}

def zipf_rows(counter):
    return sorted(counter.items(), key=lambda x:(-x[1],x[0]))

def main():
    rows=generate(); train,dev,test=split_rows(rows)
    raw_counts, raw_tokens=count_words(train)
    summary={"seed":SEED,"utterances":{"all":len(rows),"train":len(train),"dev":len(dev),"test":len(test)},
             "train_tokens":raw_tokens,"train_types":len(raw_counts)}
    vocab_results={}
    for threshold in [1,2,3,5]:
        vocab=vocab_for(raw_counts,threshold)
        mapped=map_rows(train,vocab)
        unk=sum(w=="<UNK>" for _,s in mapped for w in s)
        vocab_results[str(threshold)]={"vocab_size":len(vocab)+1,
                                       "train_token_unk_percent":100*unk/raw_tokens}
    summary["vocabulary_thresholds_le_count"]=vocab_results
    vocab=vocab_for(raw_counts,1)
    train_m=map_rows(train,vocab); dev_m=map_rows(dev,vocab); test_m=map_rows(test,vocab)
    dev_tokens=sum(len(s) for _,s in dev)
    dev_oov=sum(w not in vocab for _,s in dev for w in s)
    summary["dev_oov_percent"]=100*dev_oov/max(1,dev_tokens)
    # Zipf rank/frequency file.
    with (OUT/"zipf_rank_frequency.csv").open("w",encoding="utf-8") as f:
        f.write("rank,word,frequency\n")
        for rank,(word,freq) in enumerate(zipf_rows(raw_counts),1):
            f.write(f'{rank},"{word}",{freq}\n')
    # Unsmoothed bigram and add-k development scores.
    bc,ctx=ngram_counts(train_m,2)
    summary["bigram_add_k_dev"]=evaluate_bigram(dev_m,bc,ctx,vocab|{"<UNK>"},k=0.1)
    # Zero-probability example: find a dev bigram unseen in train.
    unseen=None
    for _,s in dev_m:
        seq=["<s>"]+s+["</s>"]
        for h,w in zip(seq,seq[1:]):
            if bc[(h,w)]==0:
                unseen=[h,w]; break
        if unseen: break
    summary["first_unseen_dev_bigram"]=unseen
    # Sample deterministic sentences from unigram distribution (simple demonstration).
    rng=random.Random(SEED)
    words=list(raw_counts); weights=[raw_counts[w] for w in words]
    samples=[]
    for _ in range(10):
        samples.append(" ".join(rng.choices(words,weights=weights,k=8)))
    summary["unigram_samples"]=samples
    (OUT/"experiment_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    print(f"Outputs written to: {OUT.resolve()}")
if __name__=="__main__": main()
