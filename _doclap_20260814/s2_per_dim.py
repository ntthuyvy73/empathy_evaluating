# -*- coding: utf-8 -*-
"""BƯỚC 2 — Phân tích sâu từng chiều A, B, C (từ bảng master đã assert ở bước 1)."""
import os, sys, json
import pandas as pd, numpy as np
from scipy import stats

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
dimA = pd.read_csv(os.path.join(OUT, "m_dimA_records.csv"))
dimB = pd.read_csv(os.path.join(OUT, "m_dimB_records.csv"))
dimC_A = pd.read_csv(os.path.join(OUT, "m_dimC_A.csv"))
dimC_B = pd.read_csv(os.path.join(OUT, "m_dimC_B.csv"))
master = pd.read_csv(os.path.join(OUT, "m_master_dialogue.csv"))

DS_ORDER = ["esconv","kokorochat","psy_insight","annomi","psydial",
            "smile","soulchat","cpsycoun","cactus","simpsydial","kmi"]
PROV = {"esconv":"real","kokorochat":"real","psy_insight":"real",
        "annomi":"semi-real","psydial":"semi-real",
        "smile":"semi-synthetic","soulchat":"semi-synthetic","cpsycoun":"semi-synthetic",
        "cactus":"fully-synthetic","simpsydial":"fully-synthetic","kmi":"fully-synthetic"}
SUBS = ["CAC","EPC","AR","TRA","ASCQ"]
QC = [f"Q{i}" for i in range(1,13)]

def icc2k(mat):
    """ICC(2,k) hai chiều random effects, mat: n_targets x k_raters (đủ dữ liệu)."""
    m = mat.dropna()
    n, k = m.shape
    if n < 5: return np.nan, n
    grand = m.values.mean()
    ms_r = k * ((m.mean(axis=1) - grand) ** 2).sum() / (n - 1)          # rows
    ms_c = n * ((m.mean(axis=0) - grand) ** 2).sum() / (k - 1)          # cols
    ss_tot = ((m.values - grand) ** 2).sum()
    ss_e = ss_tot - (n - 1) * ms_r / 1 - (k - 1) * ms_c / 1
    ms_e = ss_e / ((n - 1) * (k - 1))
    icc = (ms_r - ms_e) / (ms_r + (ms_c - ms_e) / n)
    return icc, n

R = {}  # kết quả để in cuối

# ============ DIM A ============
print("=" * 88)
print("PHẦN A — DIM A (MindEval, thang 1–6, S3 full, 3 judge)")
print("=" * 88)

# A1. Descriptives mức hội thoại (TB 3 judge)
a_dlg = dimA.groupby(["dataset","interaction_id"])["overall"].mean().reset_index()
t = a_dlg.groupby("dataset")["overall"].agg(n="size", mean="mean", sd="std", median="median",
    p_lt3=lambda s: (s < 3).mean()*100, p_ge4=lambda s: (s >= 4).mean()*100).round(3)
t = t.reindex(DS_ORDER); t["prov"] = [PROV[d] for d in t.index]
print("\n[A1] Overall mức hội thoại (TB 3 judge):")
print(t.to_string())
t.to_csv(os.path.join(OUT, "r_A1_dataset_overall.csv"))

# A2. Hồ sơ tiểu thang
sub_d = dimA.groupby(["dataset","interaction_id"])[SUBS].mean().reset_index()
sub_t = sub_d.groupby("dataset")[SUBS].mean().reindex(DS_ORDER).round(3)
sub_t["EPC_minus_rest"] = (sub_t["EPC"] - sub_t[["CAC","AR","TRA","ASCQ"]].mean(axis=1)).round(3)
print("\n[A2] Tiểu thang (TB 3 judge) + độ trội EPC so với 4 trục còn lại:")
print(sub_t.to_string())
sub_t.to_csv(os.path.join(OUT, "r_A2_subscale_profile.csv"))

# A3. Mức nghiêm khắc judge + tương tác judge×dataset
jt = dimA.pivot_table(index="dataset", columns="judge", values="overall", aggfunc="mean").reindex(DS_ORDER).round(3)
jt["gpt_minus_claude"] = (jt["gpt"] - jt["claude"]).round(3)
print("\n[A3] Điểm TB theo judge (hàng=dataset):")
print(jt.to_string())
print("Chênh lệch judge toàn cục:", dimA.groupby("judge")["overall"].mean().round(3).to_dict())
jt.to_csv(os.path.join(OUT, "r_A3_judge_severity.csv"))

# A4. Đồng thuận judge: Pearson từng cặp per dataset + ICC(2,k)
rows = []
for ds, g in dimA.groupby("dataset"):
    piv = g.pivot_table(index="interaction_id", columns="judge", values="overall")
    pr = {}
    for a, b in [("claude","gemini"),("claude","gpt"),("gemini","gpt")]:
        x = piv[[a,b]].dropna()
        pr[f"r_{a[:2]}_{b[:2]}"] = stats.pearsonr(x[a], x[b])[0] if len(x) > 5 else np.nan
    icc, n = icc2k(piv[["claude","gemini","gpt"]])
    rows.append({"dataset": ds, **pr, "mean_pairwise_r": np.nanmean(list(pr.values())),
                 "ICC2k": icc, "n": n})
agr = pd.DataFrame(rows).set_index("dataset").reindex(DS_ORDER).round(3)
print("\n[A4] Đồng thuận giữa judge (overall, mức record):")
print(agr.to_string())
agr.to_csv(os.path.join(OUT, "r_A4_judge_agreement.csv"))
# pooled: within-dataset z trung bình
print("Trung bình pairwise r (11 ds):", round(agr["mean_pairwise_r"].mean(), 3),
      "| ICC(2,k) trung bình:", round(agr["ICC2k"].mean(), 3))

# A4b. Kendall W đồng thuận xếp hạng dataset giữa 3 judge
rk = jt[["claude","gemini","gpt"]].rank(ascending=False)
kw = 12 * ((rk.sum(axis=1) - rk.sum(axis=1).mean()) ** 2).sum() / (9 * (11**3 - 11))
print(f"[A4b] Kendall W xếp hạng 11 dataset giữa 3 judge (dim A): {kw:.3f}")
sp = [stats.spearmanr(jt[a], jt[b])[0] for a,b in [("claude","gemini"),("claude","gpt"),("gemini","gpt")]]
print("Spearman xếp hạng dataset giữa cặp judge:", [round(x,3) for x in sp])

# A5. Phân tán trong dataset (đồng nhất hóa synthetic?)
print("\n[A5] SD overall nội dataset (record-level TB 3 judge) — thước đo độ đa dạng chất lượng:")
sd_t = a_dlg.groupby("dataset")["overall"].std().reindex(DS_ORDER).round(3)
print(sd_t.to_string())

# A6. Tương quan giữa các tiểu thang (record-level, TB 3 judge, within-dataset pooled)
def pooled_within_corr(df, cols, by="dataset"):
    zs = []
    for _, g in df.groupby(by):
        gg = g[cols].dropna()
        if len(gg) < 10: continue
        c = gg.corr()
        zs.append((np.arctanh(np.clip(c.values, -0.999, 0.999)), len(gg)))
    wsum = sum(n for _, n in zs)
    acc = sum(z * n for z, n in zs) / wsum
    return pd.DataFrame(np.tanh(acc), index=cols, columns=cols)
pc = pooled_within_corr(sub_d, SUBS).round(3)
print("\n[A6] Tương quan tiểu thang dim A (pooled within-dataset, TB 3 judge):")
print(pc.to_string())
pc.to_csv(os.path.join(OUT, "r_A6_subscale_intercorr.csv"))

# ============ DIM B ============
print("\n" + "=" * 88)
print("PHẦN B — DIM B (WAI-O-S, thang 1–5, S3 full, 3 judge)")
print("=" * 88)

b_dlg = dimB.groupby(["dataset","interaction_id"])[["total","goal","approach","bond"]].mean().reset_index()
tb = b_dlg.groupby("dataset").agg(n=("total","size"), total=("total","mean"), sd=("total","std"),
    goal=("goal","mean"), approach=("approach","mean"), bond=("bond","mean"),
    p_ge4=("total", lambda s: (s >= 4).mean()*100)).round(3).reindex(DS_ORDER)
tb["prov"] = [PROV[d] for d in tb.index]
print("\n[B1] WAI total & 3 chiều (TB 3 judge):")
print(tb.to_string())
tb.to_csv(os.path.join(OUT, "r_B1_dataset_wai.csv"))

# B2. Hiệu ứng trần & nén thang đo
allb = dimB.melt(id_vars=["dataset","judge"], value_vars=QC, var_name="item", value_name="score").dropna()
print("\n[B2] Trần thang đo: phân bố điểm item toàn cục (n=%d):" % len(allb))
dist = allb["score"].round().value_counts(normalize=True).sort_index() * 100
print(dist.round(1).to_string())
print("Tỷ lệ điểm item ≥4:", round((allb['score'] >= 4).mean()*100, 1), "% | ≥4.5:",
      round((allb['score'] >= 4.5).mean()*100, 1), "% | ≤2:", round((allb['score'] <= 2).mean()*100, 1), "%")
rng = b_dlg.groupby("dataset")["total"].agg(["min","max"])
print("Khoảng total theo dataset (min–max):")
print(rng.round(2).reindex(DS_ORDER).to_string())

# B3. Item nào kéo xuống / lên
im = allb.groupby("item")["score"].mean().reindex(QC).round(3)
print("\n[B3] Điểm TB từng item (toàn cục):")
print(im.to_string())
im.to_csv(os.path.join(OUT, "r_B3_item_means.csv"))
# item nghèo nhất per dataset
imd = allb.groupby(["dataset","item"])["score"].mean().unstack()[QC].reindex(DS_ORDER)
print("Item thấp nhất từng dataset:", {d: imd.loc[d].idxmin() for d in imd.index})
imd.round(3).to_csv(os.path.join(OUT, "r_B3_item_by_dataset.csv"))

# B4. Ổn định 3 run trong 1 lần chấm (SD giữa individual_scores)
sd_cols = [c + "_sd" for c in QC]
runsd = dimB.melt(id_vars=["dataset","judge"], value_vars=sd_cols, value_name="run_sd").dropna()
print("\n[B4] SD giữa 3 run nội một judge (item-level): mean=%.3f | %% run_sd=0: %.1f%%" % (
    runsd["run_sd"].mean(), (runsd["run_sd"] == 0).mean()*100))
print(runsd.groupby("judge")["run_sd"].mean().round(3).to_string())

# B5. Đồng thuận judge dim B
rows = []
for ds, g in dimB.groupby("dataset"):
    piv = g.pivot_table(index="interaction_id", columns="judge", values="total")
    pr = {}
    for a, b in [("claude","gemini"),("claude","gpt"),("gemini","gpt")]:
        x = piv[[a,b]].dropna()
        pr[f"r_{a[:2]}_{b[:2]}"] = stats.pearsonr(x[a], x[b])[0] if len(x) > 5 else np.nan
    icc, n = icc2k(piv[["claude","gemini","gpt"]])
    rows.append({"dataset": ds, **pr, "mean_pairwise_r": np.nanmean(list(pr.values())), "ICC2k": icc})
agrb = pd.DataFrame(rows).set_index("dataset").reindex(DS_ORDER).round(3)
print("\n[B5] Đồng thuận judge dim B (total):")
print(agrb.to_string())
print("Trung bình pairwise r:", round(agrb["mean_pairwise_r"].mean(), 3),
      "| ICC(2,k) TB:", round(agrb["ICC2k"].mean(), 3))
agrb.to_csv(os.path.join(OUT, "r_B5_judge_agreement.csv"))
jtb = dimB.pivot_table(index="dataset", columns="judge", values="total", aggfunc="mean").reindex(DS_ORDER)
spb = [stats.spearmanr(jtb[a], jtb[b])[0] for a,b in [("claude","gemini"),("claude","gpt"),("gemini","gpt")]]
print("Spearman xếp hạng dataset giữa cặp judge (dim B):", [round(x,3) for x in spb])
print("Điểm TB theo judge (dim B):", dimB.groupby("judge")["total"].mean().round(3).to_dict())

# B6. Cấu trúc 3 chiều WAI: tương quan Goal–Approach–Bond
pcb = pooled_within_corr(b_dlg, ["goal","approach","bond"]).round(3)
print("\n[B6] Tương quan 3 chiều WAI (pooled within-dataset):")
print(pcb.to_string())

# ============ DIM C ============
print("\n" + "=" * 88)
print("PHẦN C — DIM C (UED/NRC-VAD; client & counselor)")
print("=" * 88)

key = ["client_valence_emo_mean","client_valence_emo_std","client_valence_nec",
       "client_valence_happy_ending","client_valence_emo_rise_rate","client_valence_emo_recovery_rate",
       "counselor_valence_emo_mean","client_lex_coverage","client_n_tokens","counselor_n_tokens"]
cb = dimC_B.groupby("dataset").agg(
    n_valid=("client_valence_emo_mean", lambda s: s.notna().sum()),
    v_mean=("client_valence_emo_mean","mean"), v_std=("client_valence_emo_std","mean"),
    nec=("client_valence_nec","mean"),
    happy=("client_valence_happy_ending", lambda s: s.mean()*100),
    rise=("client_valence_emo_rise_rate","mean"), recov=("client_valence_emo_recovery_rate","mean"),
    co_v_mean=("counselor_valence_emo_mean","mean"),
    lexcov=("client_lex_coverage","mean"), cli_tok=("client_n_tokens","mean"),
    co_tok=("counselor_n_tokens","mean")).round(4).reindex(DS_ORDER)
cb["prov"] = [PROV[d] for d in cb.index]
cb["co_minus_cli_v"] = (cb["co_v_mean"] - cb["v_mean"]).round(4)
print("\n[C1] Cấu hình B (EN lexicon) — chỉ số valence client + tông counselor:")
print(cb.to_string())
cb.to_csv(os.path.join(OUT, "r_C1_dimC_B_summary.csv"))

# C2. A vs B cho 7 dataset non-EN
non_en = [d for d in DS_ORDER if d not in ("esconv","annomi","cactus","psy_insight")]
rows = []
for ds in non_en:
    a = dimC_A[dimC_A["dataset"] == ds][["interaction_id","client_valence_emo_mean","client_valence_nec","client_valence_happy_ending","client_lex_coverage"]]
    b = dimC_B[dimC_B["dataset"] == ds][["interaction_id","client_valence_emo_mean","client_valence_nec","client_valence_happy_ending","client_lex_coverage"]]
    m = a.merge(b, on="interaction_id", suffixes=("_A","_B")).dropna(subset=["client_valence_emo_mean_A","client_valence_emo_mean_B"])
    r_mean = stats.pearsonr(m["client_valence_emo_mean_A"], m["client_valence_emo_mean_B"])[0]
    r_nec = stats.pearsonr(m["client_valence_nec_A"], m["client_valence_nec_B"])[0]
    agree_happy = (m["client_valence_happy_ending_A"] == m["client_valence_happy_ending_B"]).mean()*100
    rows.append({"dataset": ds, "n": len(m), "r_emo_mean_AB": r_mean, "r_nec_AB": r_nec,
                 "happy_agree_%": agree_happy,
                 "lexcov_A": m["client_lex_coverage_A"].mean(), "lexcov_B": m["client_lex_coverage_B"].mean()})
ab = pd.DataFrame(rows).set_index("dataset").round(3)
print("\n[C2] Hội tụ cấu hình A↔B (record-level, 7 dataset non-EN):")
print(ab.to_string())
ab.to_csv(os.path.join(OUT, "r_C2_dimC_AB_convergence.csv"))

# C3. Tông counselor vs client theo nhóm provenance (elevated tone?)
mm = master.dropna(subset=["client_valence_emo_mean"])
g3 = mm.groupby("provenance")[["client_valence_emo_mean","counselor_valence_emo_mean","client_valence_nec","client_valence_emo_std"]].mean().round(4)
g3 = g3.reindex(["real","semi-real","semi-synthetic","fully-synthetic"])
g3["co_minus_cli"] = (g3["counselor_valence_emo_mean"] - g3["client_valence_emo_mean"]).round(4)
print("\n[C3] Valence theo nhóm provenance (cấu hình B):")
print(g3.to_string())

print("\nDONE BƯỚC 2")
