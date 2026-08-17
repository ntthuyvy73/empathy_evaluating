# -*- coding: utf-8 -*-
"""BƯỚC 7 — Truy vết mức tính của các số chưa khớp trong r7 (0.928, 0.715/0.968, 0.891, variability 0.991, n=1398)."""
import os, sys, glob
import pandas as pd, numpy as np
from scipy import stats
from itertools import combinations

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
KQ = r"H:\Vy\Paper\Empathy\Report\_Chuan_bi\_analyst_v7\vy\New folder\ket_qua_phan_tich"
dimA = pd.read_csv(os.path.join(OUT, "m_dimA_records.csv"))
dimB = pd.read_csv(os.path.join(OUT, "m_dimB_records.csv"))
dimC_B = pd.read_csv(os.path.join(OUT, "m_dimC_B.csv"))
dimC_A = pd.read_csv(os.path.join(OUT, "m_dimC_A.csv"))

DS = ["esconv","kokorochat","psy_insight","annomi","psydial",
      "smile","soulchat","cpsycoun","cactus","simpsydial","kmi"]
SUBS = ["CAC","EPC","AR","TRA","ASCQ"]
QC = [f"Q{i}" for i in range(1,13)]

def cronbach(df, cols):
    d = df[cols].dropna()
    k = len(cols)
    return k/(k-1) * (1 - d.var(ddof=1).sum() / d.sum(axis=1).var(ddof=1))

print("[T1] Cronbach α dim A theo mức tính:")
print(f"  per-judge record (n=6333): α(5)={cronbach(dimA, SUBS):.3f} | α(CAC,AR,TRA)={cronbach(dimA, ['CAC','AR','TRA']):.3f}")
# within-dataset: trung bình α tính riêng từng dataset (per-judge)
a5_ds = [cronbach(g, SUBS) for _, g in dimA.groupby("dataset")]
a3_ds = [cronbach(g, ["CAC","AR","TRA"]) for _, g in dimA.groupby("dataset")]
print(f"  TB α theo dataset (per-judge): α(5)={np.mean(a5_ds):.3f} | α(3)={np.mean(a3_ds):.3f}")

print("\n[T2] WAI: r̄ 12 mục & α & Goal↔Approach theo mức tính:")
print(f"  per-judge record: α(12)={cronbach(dimB, QC):.3f}")
rs = []
for a, b in combinations(QC, 2):
    d = dimB[[a,b]].dropna()
    rs.append(stats.pearsonr(d[a], d[b])[0])
print(f"  r̄ 12 mục per-judge KHÔNG khử dataset (toàn cục): {np.mean(rs):.3f}")
# pooled within-dataset per-judge
def pooled_pj(x, y):
    zs, ns = [], []
    for _, g in dimB.groupby(["dataset","judge"]):
        gg = g[[x,y]].dropna()
        if len(gg) < 10: continue
        r = stats.pearsonr(gg[x], gg[y])[0]
        zs.append(np.arctanh(min(r,0.999))*len(gg)); ns.append(len(gg))
    return np.tanh(sum(zs)/sum(ns))
rs_w = [pooled_pj(a,b) for a,b in combinations(QC,2)]
print(f"  r̄ 12 mục pooled within-(dataset×judge): {np.mean(rs_w):.3f}")
ga_glob = stats.pearsonr(dimB.dropna(subset=['goal','approach'])['goal'], dimB.dropna(subset=['goal','approach'])['approach'])[0]
print(f"  Goal↔Approach per-judge TOÀN CỤC (không khử dataset): {ga_glob:.3f}")

print("\n[T3] Variability ratio: 2 cách tính")
mor = dimC_B.groupby("dataset")["valence_variability_ratio"].mean()          # mean of ratios
rom = dimC_B.groupby("dataset").apply(lambda g: g["client_valence_emo_std"].mean()/g["counselor_valence_emo_std"].mean())  # ratio of means
t3 = pd.DataFrame({"mean_of_ratios": mor, "ratio_of_means": rom}).reindex(DS).round(3)
print(t3.to_string())
print("ratio_of_means > 1:", (rom > 1).sum(), "/11; soulchat =", round(rom["soulchat"], 3))

print("\n[T4] n của r(coverage, std) cấu hình A:")
non_en = [d for d in DS if d not in ("esconv","annomi","cactus","psy_insight")]
ca = dimC_A[dimC_A["dataset"].isin(non_en)]
n_both = ca[["client_lex_coverage","client_valence_emo_std"]].dropna().shape[0]
n_cov = ca["client_lex_coverage"].notna().sum()
print(f"  n đủ cả 2 biến = {n_both}; n có coverage = {n_cov}; tổng dòng 7 bộ = {len(ca)}")
# thử thêm cả 4 bộ EN? (họ không có config A riêng nhưng file A chứa bản B copy)
ca_all = dimC_A[["client_lex_coverage","client_valence_emo_std"]].dropna()
r_all = stats.pearsonr(ca_all["client_lex_coverage"], ca_all["client_valence_emo_std"])
print(f"  nếu gộp cả 11 bộ trong thư mục A: n={len(ca_all)}, r={r_all[0]:.3f}")

print("\n[T5] Truy các file _agg cũ tìm 0.936 / 0.891 / 0.715 / 0.968:")
for f in ["_agg_dimA_metric_intercorr.csv","_agg_dimB_subscale_intercorr.csv","_agg_dimB_item_intercorr.csv"]:
    p = os.path.join(KQ, f)
    df = pd.read_csv(p, index_col=0)
    print(f"--- {f}")
    print(df.round(3).to_string()[:600])

print("\n[T6] _agg_dimB_judge_agreement_11ds.csv (nguồn α Bảng 3?):")
df = pd.read_csv(os.path.join(KQ, "_agg_dimB_judge_agreement_11ds.csv"))
print(df.round(3).to_string())
print("\n[T7] _agg_rank_stability.csv:")
df = pd.read_csv(os.path.join(KQ, "_agg_rank_stability.csv"))
print(df.round(3).to_string()[:900])
