# -*- coding: utf-8 -*-
"""BƯỚC 4 — Bằng chứng định tính: trích thinking_trace các ca cực đoan + đếm motif lỗi."""
import os, sys, json, glob, re
from collections import Counter
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
BASE = r"H:\Vy\Paper\Empathy\Report\_Chuan_bi\_analyst_v7\vy\New folder"
CODE = os.path.join(BASE, "code", "mind-eval", "data")

def load_traces(folder, pattern):
    recs = []
    for f in glob.glob(os.path.join(CODE, folder, "results", "mind_eval", pattern)):
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    r = json.loads(line)
                    recs.append(r)
    return recs

# Motif lỗi cần đếm trong thinking_trace (tiếng Anh, khớp từ khoá phổ biến của judge)
MOTIFS = {
    "advice/directive": r"\badvice|advice-giving|directive|prescriptive|tells? the (client|user) to\b",
    "boundary/self-disclosure": r"boundary|self-disclosur|anthropomorph|pretend|human identity|claims? to (be|have)",
    "no risk assessment": r"risk assessment|safety assessment|suicid|crisis|no (safety|risk)",
    "premature/superficial": r"premature|superficial|surface-level|rushed|too quickly",
    "formulaic/templated": r"formulaic|templated|robotic|repetitive|rigid|scripted|mechanical",
    "over-reassurance/sycophancy": r"over-?reassur|sycophan|excessive praise|toxic positiv|cheerlead",
    "hallucination/fabrication": r"hallucinat|fabricat|invent(ed|s)? detail",
    "good attunement": r"attun|well-calibrated|responsive to|tracks? the client",
}

def motif_counts(recs, judge_label):
    cnt = Counter(); n = 0
    for r in recs:
        t = (r.get("thinking_trace") or "") + " " + (r.get("unparsed_judgment") or "")
        if not t.strip(): continue
        n += 1
        for k, pat in MOTIFS.items():
            if re.search(pat, t, re.I):
                cnt[k] += 1
    return {k: round(100*v/n,1) for k, v in cnt.items()}, n

print("=" * 88)
print("[H1] TẦN SUẤT MOTIF LỖI trong thinking_trace (%% record có nhắc, judge claude+gemini, full S3)")
print("=" * 88)
rows = {}
for folder, ds in [("ESConv","esconv"), ("KMI","kmi"), ("cactus","cactus"),
                   ("SoulChat","soulchat"), ("smile","smile"), ("AnnoMI","annomi"),
                   ("KokoroChat","kokorochat"), ("Psy-Insight","psy_insight"),
                   ("PsyDial","psydial"), ("CPsyCoun","cpsycoun"), ("simpsydial","simpsydial")]:
    recs = load_traces(folder, "*_S3_claude*full_judgments.jsonl") + load_traces(folder, "*_S3_gemini*full_judgments.jsonl")
    pct, n = motif_counts(recs, "cl+ge")
    rows[ds] = pct
mt = pd.DataFrame(rows).T.fillna(0)
mt = mt[["advice/directive","boundary/self-disclosure","no risk assessment","premature/superficial",
         "formulaic/templated","over-reassurance/sycophancy","hallucination/fabrication","good attunement"]]
print(mt.to_string())
mt.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "r_H1_motifs.csv"))

# H2. Trích 2 trace ESConv EPC thấp nhất (claude)
print("\n" + "=" * 88)
print("[H2] ESConv — 2 trích đoạn judge (EPC thấp nhất, claude):")
recs = load_traces("ESConv", "*_S3_claude*full_judgments.jsonl")
recs = [r for r in recs if (r.get("parsed_judgment") or {}).get("Ethical & Professional Conduct") is not None]
recs.sort(key=lambda r: r["parsed_judgment"]["Ethical & Professional Conduct"])
for r in recs[:2]:
    print(f"\n--- {r['interaction_id']} (EPC={r['parsed_judgment']['Ethical & Professional Conduct']}, overall={r['parsed_judgment'].get('Overall score')}):")
    print((r.get("thinking_trace") or "")[:600].replace("\n", " "))

# H3. KMI — trace điển hình (EPC cao nhưng ASCQ thấp, claude)
print("\n" + "=" * 88)
print("[H3] KMI — 2 trích đoạn judge (EPC≥4 & ASCQ≤2, claude):")
recs = load_traces("KMI", "*_S3_claude*full_judgments.jsonl")
sel = [r for r in recs if (r.get("parsed_judgment") or {}).get("Ethical & Professional Conduct", 0) >= 4
       and (r.get("parsed_judgment") or {}).get("AI-Specific Communication Quality", 9) <= 2]
for r in sel[:2]:
    pj = r["parsed_judgment"]
    print(f"\n--- {r['interaction_id']} (EPC={pj['Ethical & Professional Conduct']}, ASCQ={pj['AI-Specific Communication Quality']}):")
    print((r.get("thinking_trace") or "")[:600].replace("\n", " "))

# H4. cactus — trace điển hình EPC>=4.5 (claude): guardrail được khen?
print("\n" + "=" * 88)
print("[H4] cactus — 1 trích đoạn (EPC≥4.5, claude):")
recs = load_traces("cactus", "*_S3_claude*full_judgments.jsonl")
sel = [r for r in recs if (r.get("parsed_judgment") or {}).get("Ethical & Professional Conduct", 0) >= 4.5]
for r in sel[:1]:
    pj = r["parsed_judgment"]
    print(f"\n--- {r['interaction_id']} (EPC={pj['Ethical & Professional Conduct']}, overall={pj.get('Overall score')}):")
    print((r.get("thinking_trace") or "")[:700].replace("\n", " "))

print("\nDONE BƯỚC 4")
