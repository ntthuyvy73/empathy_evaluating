# -*- coding: utf-8 -*-
"""
BƯỚC 1 — Nạp toàn bộ dữ liệu thô 3 chiều (11 dataset) thành bảng master.
Nguồn: code/mind-eval/data/<DS>/results/{mind_eval,wai}/*_S3_*full*.jsonl  (dim A, dim B)
       experiments/dim_c/dim_c_{A,B}_full_0629/<ds>/<ds>_dimC_pilot.csv     (dim C)
Mọi số lượng được assert; kết quả ghi ra OUT/.
"""
import json, glob, os, re, sys
import pandas as pd
import numpy as np

BASE = r"H:\Vy\Paper\Empathy\Report\_Chuan_bi\_analyst_v7\vy\New folder"
CODE = os.path.join(BASE, "code", "mind-eval", "data")
EXP  = os.path.join(BASE, "experiments")
OUT  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

DATASETS = {  # folder in code/data -> canonical short name (per dim C)
    "AnnoMI": "annomi", "CPsyCoun": "cpsycoun", "ESConv": "esconv", "KMI": "kmi",
    "KokoroChat": "kokorochat", "Psy-Insight": "psy_insight", "PsyDial": "psydial",
    "SoulChat": "soulchat", "cactus": "cactus", "simpsydial": "simpsydial", "smile": "smile",
}
LANG = {"annomi":"en","cactus":"en","esconv":"en","psy_insight":"en",
        "cpsycoun":"zh","psydial":"zh","simpsydial":"zh","smile":"zh","soulchat":"zh",
        "kokorochat":"ja","kmi":"ko"}
# Taxonomy provenance chính thức (BC-DATA §1.3, Bảng 2.1 — theo 00_du_lieu_tho_va_metric.md mục 4.6)
PROV = {"esconv":"real","kokorochat":"real","psy_insight":"real",
        "annomi":"semi-real","psydial":"semi-real",
        "smile":"semi-synthetic","soulchat":"semi-synthetic","cpsycoun":"semi-synthetic",
        "cactus":"fully-synthetic","simpsydial":"fully-synthetic","kmi":"fully-synthetic"}

SUBS_A = ["Clinical Accuracy & Competence","Ethical & Professional Conduct",
          "Assessment & Response","Therapeutic Relationship & Alliance",
          "AI-Specific Communication Quality"]
SUBS_A_SHORT = {"Clinical Accuracy & Competence":"CAC","Ethical & Professional Conduct":"EPC",
                "Assessment & Response":"AR","Therapeutic Relationship & Alliance":"TRA",
                "AI-Specific Communication Quality":"ASCQ"}

def judge_of(fname):
    m = re.search(r"_S3_(claude|gemini|gpt|qwen)", fname)
    return m.group(1) if m else None

# ---------------- DIM A ----------------
rows_a = []
for folder, ds in DATASETS.items():
    fs = sorted(glob.glob(os.path.join(CODE, folder, "results", "mind_eval", "*_S3_*full_judgments.jsonl")))
    fs = [f for f in fs if judge_of(os.path.basename(f))]
    assert len(fs) == 3, (ds, [os.path.basename(f) for f in fs])
    for f in fs:
        j = judge_of(os.path.basename(f))
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                if not line.strip(): continue
                r = json.loads(line)
                pj = r.get("parsed_judgment") or {}
                row = {"interaction_id": r["interaction_id"], "dataset": ds, "judge": j,
                       "judge_model": r.get("judge_model",""),
                       "overall": pj.get("Overall score", pj.get("Average score"))}
                for s in SUBS_A:
                    row[SUBS_A_SHORT[s]] = pj.get(s)
                rows_a.append(row)
dimA = pd.DataFrame(rows_a)
# khử trùng lặp nếu file chứa id lặp (giữ bản ghi cuối)
n_dup_a = dimA.duplicated(["interaction_id","dataset","judge"]).sum()
dimA = dimA.drop_duplicates(["interaction_id","dataset","judge"], keep="last")

# ---------------- DIM B ----------------
rows_b, rows_b_items = [], []
for folder, ds in DATASETS.items():
    fs = sorted(glob.glob(os.path.join(CODE, folder, "results", "wai", "*_S3_*full_wai_judgments.jsonl")))
    fs = [f for f in fs if judge_of(os.path.basename(f))]
    assert len(fs) == 3, (ds, [os.path.basename(f) for f in fs])
    for f in fs:
        j = judge_of(os.path.basename(f))
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                if not line.strip(): continue
                r = json.loads(line)
                dims = r.get("dimensions") or {}
                row = {"interaction_id": r["interaction_id"], "dataset": ds, "judge": j,
                       "judge_model": r.get("judge_model",""), "n_runs": r.get("n_runs"),
                       "goal": dims.get("Goal"), "approach": dims.get("Approach"),
                       "bond": dims.get("Affective Bond"), "total": r.get("total")}
                qs = r.get("questions") or {}
                n_none = 0
                for qid in [f"Q{i}" for i in range(1,13)]:
                    q = qs.get(qid) or {}
                    sc = q.get("score")
                    row[qid] = sc
                    if sc is None: n_none += 1
                    ind = q.get("individual_scores") or []
                    ind = [x for x in ind if x is not None]
                    row[qid+"_sd"] = float(np.std(ind, ddof=0)) if len(ind) >= 2 else np.nan
                row["n_item_none"] = n_none
                rows_b.append(row)
dimB = pd.DataFrame(rows_b)
n_dup_b = dimB.duplicated(["interaction_id","dataset","judge"]).sum()
dimB = dimB.drop_duplicates(["interaction_id","dataset","judge"], keep="last")

# ---------------- DIM C ----------------
def load_dimc(cfg):
    sub = {"A": "dim_c_A_full_0629", "B": "dim_c_B_full_0629"}[cfg]
    # tên thư mục con trong A có hậu tố ngôn ngữ (vd cpsycoun_zh), trong B thì không
    frames = []
    for d in sorted(glob.glob(os.path.join(EXP, "dim_c", sub, "*"))):
        if not os.path.isdir(d): continue
        fs = glob.glob(os.path.join(d, "*_dimC_pilot.csv"))
        assert len(fs) == 1, d
        df = pd.read_csv(fs[0])
        frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    out["dataset"] = out["dataset"].str.lower().str.replace("-", "_")
    return out

dimC_A = load_dimc("A")
dimC_B = load_dimc("B")
for df in (dimC_A, dimC_B):
    df.rename(columns={"dialogue_id": "interaction_id"}, inplace=True)

# ---------------- ASSERT KIỂM KÊ ----------------
rep = []
def log(s):
    rep.append(s); print(s)

EXPECT_N = {ds: 200 for ds in DATASETS.values()}
EXPECT_N["annomi"] = 112; EXPECT_N["smile"] = 199

log("== DIM A ==")
ca = dimA.groupby(["dataset","judge"]).size().unstack()
log(ca.to_string())
for ds, n in EXPECT_N.items():
    for j in ["claude","gemini","gpt"]:
        assert ca.loc[ds, j] == n, (ds, j, ca.loc[ds, j])
assert len(dimA) == 6333, len(dimA)
log(f"dup dimA bị loại: {n_dup_a}; tổng record dim A = {len(dimA)} (khớp 6.333)")
# overall == mean 5 subscale?
sub_mean = dimA[["CAC","EPC","AR","TRA","ASCQ"]].mean(axis=1)
ok = (dimA["overall"] - sub_mean).abs() <= 0.05
log(f"overall==mean(5 tiểu thang) trong ±0.05: {ok.mean()*100:.2f}% ({ok.sum()}/{len(ok)})")
n_null_a = dimA[["CAC","EPC","AR","TRA","ASCQ","overall"]].isna().sum().sum()
log(f"Số ô điểm null dim A: {n_null_a}")

log("\n== DIM B ==")
cb = dimB.groupby(["dataset","judge"]).size().unstack()
log(cb.to_string())
for ds, n in EXPECT_N.items():
    for j in ["claude","gemini","gpt"]:
        assert cb.loc[ds, j] == n, (ds, j, cb.loc[ds, j])
assert len(dimB) == 6333, len(dimB)
log(f"dup dimB bị loại: {n_dup_b}; tổng record dim B = {len(dimB)} (khớp 6.333)")
qcols = [f"Q{i}" for i in range(1,13)]
none_by_judge = dimB.groupby("judge")["n_item_none"].sum()
log("Số điểm item None theo judge: " + str(none_by_judge.to_dict()))
# total == mean(goal, approach, bond)?
dmean = dimB[["goal","approach","bond"]].mean(axis=1)
ok_b = (dimB["total"] - dmean).abs() <= 0.02
log(f"total==mean(3 chiều) trong ±0.02: {ok_b.mean()*100:.2f}%")

log("\n== DIM C ==")
for cfg, df in [("A", dimC_A), ("B", dimC_B)]:
    cnt = df.groupby("dataset").size()
    nv = df.groupby("dataset")["client_valence_emo_mean"].apply(lambda s: s.notna().sum())
    log(f"dim C cấu hình {cfg}: n dòng = {cnt.to_dict()}")
    log(f"   n hợp lệ (client valence không NaN) = {nv.to_dict()}")
    assert set(df["dataset"]) == set(DATASETS.values())

log("\n== JOIN ==")
a_ids = set(zip(dimA["dataset"], dimA["interaction_id"]))
b_ids = set(zip(dimB["dataset"], dimB["interaction_id"]))
log(f"A∩B (cặp dataset-id): {len(a_ids & b_ids)} / A={len(a_ids)} / B={len(b_ids)}")
c_ids = set(zip(dimC_B["dataset"], dimC_B["interaction_id"]))
log(f"A∩C_B: {len(a_ids & c_ids)}; chỉ có trong C: {sorted(list(c_ids - a_ids))[:5]}")

# ---------------- GHI FILE ----------------
dimA.to_csv(os.path.join(OUT, "m_dimA_records.csv"), index=False)
dimB.to_csv(os.path.join(OUT, "m_dimB_records.csv"), index=False)
dimC_A.to_csv(os.path.join(OUT, "m_dimC_A.csv"), index=False)
dimC_B.to_csv(os.path.join(OUT, "m_dimC_B.csv"), index=False)

# bảng mức hội thoại (trung bình 3 judge) + ghép C (cấu hình B làm chuẩn so sánh chéo)
aggA = dimA.groupby(["dataset","interaction_id"]).agg(
    A_overall=("overall","mean"), CAC=("CAC","mean"), EPC=("EPC","mean"),
    AR=("AR","mean"), TRA=("TRA","mean"), ASCQ=("ASCQ","mean")).reset_index()
aggB = dimB.groupby(["dataset","interaction_id"]).agg(
    B_total=("total","mean"), B_goal=("goal","mean"),
    B_approach=("approach","mean"), B_bond=("bond","mean")).reset_index()
ccols = ["interaction_id","dataset","client_n_tokens","counselor_n_tokens",
         "client_valence_emo_mean","client_valence_emo_std","client_valence_nec",
         "client_valence_happy_ending","client_arousal_emo_std","client_valence_first_mean",
         "client_valence_last_mean","counselor_valence_emo_mean","counselor_valence_emo_std",
         "counselor_valence_nec","client_lex_coverage","counselor_lex_coverage",
         "client_valence_emo_rise_rate","client_valence_emo_recovery_rate",
         "client_valence_n_displacements","valence_variability_ratio"]
master = aggA.merge(aggB, on=["dataset","interaction_id"], how="outer")
master = master.merge(dimC_B[ccols], on=["dataset","interaction_id"], how="left")
master["language"] = master["dataset"].map(LANG)
master["provenance"] = master["dataset"].map(PROV)
master["total_tokens"] = master["client_n_tokens"] + master["counselor_n_tokens"]
assert len(master) == 2111, len(master)  # 2.111 hội thoại có điểm A/B; smile_74 chỉ có ở C nên không vào master
log(f"\nmaster: {len(master)} dòng; thiếu A_overall: {master['A_overall'].isna().sum()}; thiếu B_total: {master['B_total'].isna().sum()}; thiếu C: {master['client_valence_emo_mean'].isna().sum()}")
master.to_csv(os.path.join(OUT, "m_master_dialogue.csv"), index=False)

with open(os.path.join(OUT, "s1_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(rep))
print("\nDONE BƯỚC 1")
