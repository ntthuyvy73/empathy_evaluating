# -*- coding: utf-8 -*-
"""BƯỚC 3 — Phân tích liên chiều, nhóm provenance, độ dài, sức phân biệt, ca bất đồng."""
import os, sys
import pandas as pd, numpy as np
from scipy import stats
from itertools import combinations

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
master = pd.read_csv(os.path.join(OUT, "m_master_dialogue.csv"))
dimA = pd.read_csv(os.path.join(OUT, "m_dimA_records.csv"))
dimB = pd.read_csv(os.path.join(OUT, "m_dimB_records.csv"))

DS_ORDER = ["esconv","kokorochat","psy_insight","annomi","psydial",
            "smile","soulchat","cpsycoun","cactus","simpsydial","kmi"]
PROV_ORDER = ["real","semi-real","semi-synthetic","fully-synthetic"]
HUMAN_VOICED = {"esconv","kokorochat","psy_insight","annomi"}  # lời counselor do người viết
master["counselor_voice"] = np.where(master["dataset"].isin(HUMAN_VOICED), "human-voiced", "llm-voiced")
master["happy_num"] = master["client_valence_happy_ending"].map({True:1, False:0, "True":1, "False":0})

print("=" * 88)
print("PHẦN D — LIÊN CHIỀU (dataset-level, n=11) VÀ MTMM (record-level)")
print("=" * 88)

# D1. Bảng trung bình dataset 3 chiều + xếp hạng
ds_means = master.groupby("dataset").agg(
    A_overall=("A_overall","mean"), A_TRA=("TRA","mean"), A_ASCQ=("ASCQ","mean"), A_EPC=("EPC","mean"),
    B_total=("B_total","mean"), B_bond=("B_bond","mean"),
    C_nec=("client_valence_nec","mean"), C_happy=("happy_num","mean"),
    C_vstd=("client_valence_emo_std","mean"), C_co_minus_cli=("counselor_valence_emo_mean","mean"),
    tokens=("total_tokens","mean")).reindex(DS_ORDER)
cli_v = master.groupby("dataset")["client_valence_emo_mean"].mean().reindex(DS_ORDER)
ds_means["C_co_minus_cli"] = (ds_means["C_co_minus_cli"] - cli_v)
ds_means["prov"] = [ {"esconv":"real","kokorochat":"real","psy_insight":"real","annomi":"semi-real","psydial":"semi-real","smile":"semi-synthetic","soulchat":"semi-synthetic","cpsycoun":"semi-synthetic","cactus":"fully-synthetic","simpsydial":"fully-synthetic","kmi":"fully-synthetic"}[d] for d in ds_means.index]
print("\n[D1] Trung bình dataset 3 chiều:")
print(ds_means.round(3).to_string())
ds_means.to_csv(os.path.join(OUT, "r_D1_dataset_means.csv"))

rk = ds_means[["A_overall","B_total","C_nec","C_happy"]].rank(ascending=False)
rk.columns = ["hạng_A","hạng_B","hạng_NEC","hạng_happy"]
print("\nXếp hạng (1=tốt nhất):")
print(rk.astype(int).to_string())

# D2. Tương quan hạng dataset-level giữa các chiều (n=11)
pairs = [("A_overall","B_total"),("A_overall","C_nec"),("A_overall","C_happy"),
         ("B_total","C_nec"),("B_total","C_happy"),("A_overall","tokens"),("B_total","tokens"),
         ("A_TRA","B_total"),("A_TRA","B_bond")]
rows = []
for x, y in pairs:
    rho, p = stats.spearmanr(ds_means[x], ds_means[y])
    rows.append({"cặp": f"{x} ↔ {y}", "spearman_rho": round(rho,3), "p": round(p,4)})
d2 = pd.DataFrame(rows)
print("\n[D2] Tương quan hạng giữa các chiều (dataset-level, n=11):")
print(d2.to_string(index=False))
d2.to_csv(os.path.join(OUT, "r_D2_rankcorr.csv"), index=False)

# D3. MTMM record-level: pooled within-dataset (Fisher z, trọng số n)
def pooled_r(df, x, y):
    zs, ns, per_ds = [], [], {}
    for ds, g in df.groupby("dataset"):
        gg = g[[x,y]].dropna()
        if len(gg) < 10: continue
        r = stats.pearsonr(gg[x], gg[y])[0]
        per_ds[ds] = round(r,3)
        zs.append(np.arctanh(np.clip(r,-0.999,0.999)) * len(gg)); ns.append(len(gg))
    return np.tanh(sum(zs)/sum(ns)), per_ds

mt_pairs = [("A_overall","B_total"),("A_TRA","B_total"),("A_TRA","B_bond"),
            ("A_overall","client_valence_nec"),("B_total","client_valence_nec"),
            ("A_ASCQ","B_total") if "A_ASCQ" in master.columns else ("ASCQ","B_total")]
mt_pairs = [("A_overall","B_total"),("TRA","B_total"),("TRA","B_bond"),
            ("A_overall","client_valence_nec"),("B_total","client_valence_nec"),
            ("ASCQ","B_total"),("EPC","B_total"),
            ("A_overall","total_tokens"),("B_total","total_tokens")]
rows = []
for x, y in mt_pairs:
    r, per = pooled_r(master, x, y)
    rows.append({"cặp": f"{x} ↔ {y}", "pooled_within_r": round(r,3),
                 "min_ds": min(per.values()), "max_ds": max(per.values())})
d3 = pd.DataFrame(rows)
print("\n[D3] Tương quan record-level pooled within-dataset (khử khác biệt giữa dataset):")
print(d3.to_string(index=False))
d3.to_csv(os.path.join(OUT, "r_D3_mtmm_pooled.csv"), index=False)

# D3b. Riêng TRA↔B_total theo dataset (bảng đầy đủ) — đối chiếu 0.477/0.860 của vòng r5
r_pooled, per = pooled_r(master, "TRA", "B_total")
print("\n[D3b] TRA(dim A) ↔ WAI total(dim B): pooled record-level r = %.3f" % r_pooled)
print("   theo dataset:", per)
rho_ds, p_ds = stats.spearmanr(ds_means["A_TRA"], ds_means["B_total"])
r_ds, p_ds2 = stats.pearsonr(ds_means["A_TRA"], ds_means["B_total"])
print("   dataset-level: Pearson r = %.3f (p=%.4f), Spearman rho = %.3f (p=%.4f)" % (r_ds, p_ds2, rho_ds, p_ds))

print("\n" + "=" * 88)
print("PHẦN E — NHÓM PROVENANCE & 'AI VIẾT LỜI COUNSELOR'")
print("=" * 88)

# E1. Trung bình nhóm provenance (đơn vị = dataset mean, tránh giả tăng n)
gp = ds_means.groupby("prov")[["A_overall","B_total","C_nec","C_happy"]].mean().reindex(PROV_ORDER).round(3)
print("\n[E1] Trung bình nhóm provenance (đơn vị dataset, n=3/2/3/3):")
print(gp.to_string())

# Kruskal-Wallis trên dataset means (đơn vị dataset)
for col in ["A_overall","B_total","C_nec"]:
    groups = [ds_means[ds_means["prov"]==p][col].dropna().values for p in PROV_ORDER]
    H, pv = stats.kruskal(*groups)
    print(f"   Kruskal–Wallis {col} theo 4 nhóm (n=11 dataset): H={H:.2f}, p={pv:.3f}")

# E2. Nhị phân human-voiced vs llm-voiced (đơn vị dataset)
dv = ds_means.copy()
dv["voice"] = np.where(dv.index.isin(HUMAN_VOICED), "human-voiced", "llm-voiced")
gv = dv.groupby("voice")[["A_overall","B_total","C_nec","C_happy"]].agg(["mean","count"]).round(3)
print("\n[E2] Human-voiced (n=4 ds) vs LLM-voiced (n=7 ds) — đơn vị dataset:")
print(gv.to_string())
for col in ["A_overall","B_total","C_nec"]:
    a = dv[dv["voice"]=="human-voiced"][col].dropna(); b = dv[dv["voice"]=="llm-voiced"][col].dropna()
    U, pv = stats.mannwhitneyu(a, b, alternative="two-sided")
    print(f"   Mann–Whitney {col}: U={U:.0f}, p={pv:.3f} | human={a.mean():.3f} llm={b.mean():.3f}")

# E2b. record-level cho co_minus_cli valence (tông counselor trội)
mm = master.dropna(subset=["counselor_valence_emo_mean","client_valence_emo_mean"]).copy()
mm["co_minus_cli"] = mm["counselor_valence_emo_mean"] - mm["client_valence_emo_mean"]
per_ds_gap = mm.groupby("dataset")["co_minus_cli"].mean().reindex(DS_ORDER)
gap_h = per_ds_gap[per_ds_gap.index.isin(HUMAN_VOICED)]
gap_l = per_ds_gap[~per_ds_gap.index.isin(HUMAN_VOICED)]
U, pv = stats.mannwhitneyu(gap_h, gap_l, alternative="two-sided")
print("\n[E2b] Chênh tông counselor−client (valence, cấu hình B), đơn vị dataset:")
print(per_ds_gap.round(4).to_string())
print(f"   human-voiced mean={gap_h.mean():.4f} vs llm-voiced={gap_l.mean():.4f}; Mann–Whitney U={U:.0f}, p={pv:.3f}")

print("\n" + "=" * 88)
print("PHẦN F — YẾU TỐ GÂY NHIỄU: ĐỘ DÀI, NGÔN NGỮ, NÉN PHƯƠNG SAI")
print("=" * 88)

# F1. Độ dài ↔ điểm (record-level, per dataset Spearman)
rows = []
for ds, g in master.groupby("dataset"):
    gg = g.dropna(subset=["total_tokens"])
    rows.append({"dataset": ds,
        "rho_B_tokens": stats.spearmanr(gg["B_total"], gg["total_tokens"])[0],
        "rho_A_tokens": stats.spearmanr(gg["A_overall"], gg["total_tokens"])[0],
        "median_tokens": gg["total_tokens"].median()})
f1 = pd.DataFrame(rows).set_index("dataset").reindex(DS_ORDER).round(3)
print("\n[F1] Spearman điểm ↔ tổng token (record-level, từng dataset):")
print(f1.to_string())
f1.to_csv(os.path.join(OUT, "r_F1_length_effect.csv"))
print("Trung vị rho_B_tokens:", round(f1["rho_B_tokens"].median(),3),
      "| rho_A_tokens:", round(f1["rho_A_tokens"].median(),3))
# dataset-level: token mean vs B_total
rho, p = stats.spearmanr(ds_means["tokens"], ds_means["B_total"])
print(f"Dataset-level: tokens ↔ B_total Spearman rho={rho:.3f} (p={p:.3f})")
rho, p = stats.spearmanr(ds_means["tokens"], ds_means["A_overall"])
print(f"Dataset-level: tokens ↔ A_overall Spearman rho={rho:.3f} (p={p:.3f})")

# F2. Sức phân biệt: eta² (giữa dataset / tổng) cho từng metric chính
def eta2(df, col):
    d = df.dropna(subset=[col])
    grand = d[col].mean()
    ss_b = d.groupby("dataset")[col].apply(lambda s: len(s)*(s.mean()-grand)**2).sum()
    ss_t = ((d[col]-grand)**2).sum()
    return ss_b/ss_t
rows = []
for col, nice in [("A_overall","A_overall"),("CAC","A_CAC"),("EPC","A_EPC"),("AR","A_AR"),
                  ("TRA","A_TRA"),("ASCQ","A_ASCQ"),("B_total","B_total"),("B_goal","B_goal"),
                  ("B_approach","B_approach"),("B_bond","B_bond"),
                  ("client_valence_nec","C_nec"),("client_valence_emo_std","C_vstd"),
                  ("client_valence_emo_mean","C_vmean")]:
    rows.append({"metric": nice, "eta2_between_dataset": round(eta2(master, col),3)})
f2 = pd.DataFrame(rows).sort_values("eta2_between_dataset", ascending=False)
print("\n[F2] η² giữa-dataset (tỷ lệ phương sai do khác dataset) — sức phân biệt của metric:")
print(f2.to_string(index=False))
f2.to_csv(os.path.join(OUT, "r_F2_eta2.csv"), index=False)

# F3. Rank stability: bỏ 1 judge (dim A/B) — hạng dataset thay đổi tối đa bao nhiêu?
def ranks_with_judges(dim, val, judges):
    d = dim[dim["judge"].isin(judges)]
    m = d.groupby(["dataset","interaction_id"])[val].mean().reset_index()
    return m.groupby("dataset")[val].mean().rank(ascending=False)
full_rank_A = ranks_with_judges(dimA, "overall", ["claude","gemini","gpt"])
full_rank_B = ranks_with_judges(dimB, "total", ["claude","gemini","gpt"])
rows = []
for drop in ["claude","gemini","gpt"]:
    keep = [j for j in ["claude","gemini","gpt"] if j != drop]
    ra = ranks_with_judges(dimA, "overall", keep); rb = ranks_with_judges(dimB, "total", keep)
    rows.append({"bỏ_judge": drop,
                 "maxΔhạng_A": int((ra - full_rank_A).abs().max()),
                 "spearman_A_vs_full": round(stats.spearmanr(ra, full_rank_A)[0],3),
                 "maxΔhạng_B": int((rb - full_rank_B).abs().max()),
                 "spearman_B_vs_full": round(stats.spearmanr(rb, full_rank_B)[0],3)})
f3 = pd.DataFrame(rows)
print("\n[F3] Ổn định xếp hạng khi bỏ 1 judge:")
print(f3.to_string(index=False))

print("\n" + "=" * 88)
print("PHẦN G — CA BẤT ĐỒNG GIỮA CHIỀU (quadrant) & PHỔ ĐIỂM THEO NHÓM")
print("=" * 88)

# G1. Quadrant: B cao (>=4) nhưng A thấp (<2.5) và ngược lại
m = master.copy()
m["quad_B_cao_A_thap"] = (m["B_total"] >= 4) & (m["A_overall"] < 2.5)
m["quad_A_cao_B_thap"] = (m["A_overall"] >= 3.5) & (m["B_total"] < 3.5)
q = m.groupby("dataset")[["quad_B_cao_A_thap","quad_A_cao_B_thap"]].mean().mul(100).round(1).reindex(DS_ORDER)
q["n"] = m.groupby("dataset").size().reindex(DS_ORDER)
print("\n[G1] %% hội thoại 'liên minh đẹp nhưng lâm sàng kém' (B≥4 & A<2.5) và ngược lại (A≥3.5 & B<3.5):")
print(q.to_string())
q.to_csv(os.path.join(OUT, "r_G1_quadrant.csv"))
tot = m["quad_B_cao_A_thap"].mean()*100
print(f"Toàn cục: B≥4 & A<2.5 = {tot:.1f}% ({int(m['quad_B_cao_A_thap'].sum())}/{len(m)})")

# G2. ESConv mổ xẻ: vì sao real bét bảng dim A? — phân bố EPC theo judge, và ví dụ percentile
es = master[master["dataset"]=="esconv"]
print("\n[G2] ESConv: A_overall=%.3f (EPC=%.3f thấp nhất trong 5 trục) nhưng B_total=%.3f (hạng %d)" % (
    es["A_overall"].mean(), es["EPC"].mean(), es["B_total"].mean(),
    int(rk.loc["esconv","hạng_B"])))
esA = dimA[dimA["dataset"]=="esconv"].groupby("judge")[["overall","EPC","CAC","ASCQ"]].mean().round(3)
print(esA.to_string())

# G3. KMI mổ xẻ: EPC 3.95 (hạng 2) nhưng ASCQ 1.958 (bét) — 'an toàn nhưng máy móc'
km = dimA[dimA["dataset"]=="kmi"][["EPC","ASCQ","CAC"]].describe().round(3)
print("\n[G3] KMI phân bố EPC vs ASCQ (record × judge):")
print(km.loc[["mean","std","25%","50%","75%"]].to_string())

# G4. Hai phổ điểm A theo nhóm provenance — mật độ vùng
bins = [1,2,2.5,3,3.5,4,6.01]
m["A_bin"] = pd.cut(m["A_overall"], bins, right=False)
gb = m.groupby(["provenance","A_bin"], observed=True).size().unstack(fill_value=0)
gb = gb.div(gb.sum(axis=1), axis=0).mul(100).round(1).reindex(PROV_ORDER)
print("\n[G4] Phân bố A_overall theo nhóm provenance (% hàng):")
print(gb.to_string())

print("\nDONE BƯỚC 3")
