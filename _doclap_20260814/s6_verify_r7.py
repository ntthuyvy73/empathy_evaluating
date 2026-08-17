# -*- coding: utf-8 -*-
"""BƯỚC 6 — Đối chiếu TỪNG claim định lượng của bài báo r7 với dữ liệu thô.
Mỗi mục in [OK]/[LỆCH]/[SAI] + số của bài vs số tính lại."""
import os, sys
import pandas as pd, numpy as np
from scipy import stats
from itertools import combinations

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
dimA = pd.read_csv(os.path.join(OUT, "m_dimA_records.csv"))
dimB = pd.read_csv(os.path.join(OUT, "m_dimB_records.csv"))
dimC_A = pd.read_csv(os.path.join(OUT, "m_dimC_A.csv"))
dimC_B = pd.read_csv(os.path.join(OUT, "m_dimC_B.csv"))
master = pd.read_csv(os.path.join(OUT, "m_master_dialogue.csv"))

DS = ["esconv","kokorochat","psy_insight","annomi","psydial",
      "smile","soulchat","cpsycoun","cactus","simpsydial","kmi"]
SUBS = ["CAC","EPC","AR","TRA","ASCQ"]
QC = [f"Q{i}" for i in range(1,13)]
# Lưỡng phân CHÍNH THỨC của bài báo (5 human / 6 LLM; PsyDial thuộc human)
HUMAN5 = {"esconv","kokorochat","psy_insight","annomi","psydial"}
# Lưỡng phân "văn bản cuối cùng thuần người" (4/7; PsyDial → LLM vì lời counselor được LLM tinh chỉnh trôi chảy)
HUMAN4 = {"esconv","kokorochat","psy_insight","annomi"}

aggA = dimA.groupby(["dataset","interaction_id"])[["overall"]+SUBS].mean().reset_index()

def sec(t): print("\n" + "="*80 + f"\n{t}\n" + "="*80)

# ---------- 1. "EPC là trục cao nhất ở 10/11 bộ" ----------
sec("[V1] Claim 4.2: 'EPC là trục cao nhất ở 10/11 bộ'")
prof = aggA.groupby("dataset")[SUBS].mean()
top_axis = prof.idxmax(axis=1)
n_epc_top = (top_axis == "EPC").sum()
top2 = prof.apply(lambda r: r.nlargest(2).index.tolist(), axis=1)
n_epc_top2 = top2.apply(lambda l: "EPC" in l).sum()
print("Trục cao nhất từng bộ:", top_axis.to_dict())
print(f"→ EPC cao NHẤT ở {n_epc_top}/11 bộ; EPC trong top-2 ở {n_epc_top2}/11 bộ")
print("Bài viết '10/11' — kiểm: ngoại lệ thực tế =", sorted(top_axis[top_axis != 'EPC'].index.tolist()))

# ---------- 2. Cronbach alpha ----------
sec("[V2] Claim 4.2: 'Cronbach α của cụm CAC–AR–TRA = 0,928' (file 01 lại ghi 'α 5 trục = 0.928')")
def cronbach(df, cols):
    d = df[cols].dropna()
    k = len(cols)
    return k/(k-1) * (1 - d.var(ddof=1).sum() / d.sum(axis=1).var(ddof=1))
a3 = cronbach(aggA, ["CAC","AR","TRA"]); a5 = cronbach(aggA, SUBS)
print(f"α(CAC,AR,TRA) = {a3:.3f} | α(5 trục) = {a5:.3f}  (mức hội thoại judge-mean, n={len(aggA)})")

# ---------- 3. CAC↔AR pooled ----------
sec("[V3] Claim 4.2: 'CAC–AR r = 0,936'")
def pooled_z(df, x, y, weighted=True):
    zs, ns = [], []
    for _, g in df.groupby("dataset"):
        gg = g[[x,y]].dropna()
        if len(gg) < 10: continue
        r = stats.pearsonr(gg[x], gg[y])[0]
        zs.append(np.arctanh(min(r,0.999))); ns.append(len(gg))
    if weighted: return np.tanh(sum(z*n for z,n in zip(zs,ns))/sum(ns))
    return np.tanh(np.mean(zs))
print(f"pooled-z có trọng số n: {pooled_z(aggA,'CAC','AR'):.3f} | không trọng số: {pooled_z(aggA,'CAC','AR',False):.3f}")

# ---------- 4. AnnoMI %<2 và 2 ví dụ ----------
sec("[V4] Claim 4.2: AnnoMI '46,4% ≥4, 13,4% <2'; ví dụ annomi_20 (4,8/6,0/5,2), annomi_69 (1,0/1,0/1,3)")
an = aggA[aggA["dataset"]=="annomi"]["overall"]
print(f"annomi: %≥4 = {(an>=4).mean()*100:.1f} | %<2 = {(an<2).mean()*100:.1f}")
for iid in ["annomi_20","annomi_69"]:
    r = dimA[(dimA["dataset"]=="annomi") & (dimA["interaction_id"]==iid)][["judge","overall"]]
    print(iid, ":", dict(zip(r["judge"], r["overall"])))

# ---------- 5. Dim B %<3 theo bộ (Bảng 5) ----------
sec("[V5] Bảng 5: %hội thoại <3 (annomi 17,0; cpsycoun 11,5; psy_insight 9,5; kokorochat/esconv 4,5...)")
aggB = dimB.groupby(["dataset","interaction_id"])[["total","goal","approach","bond"]].mean().reset_index()
p3 = aggB.groupby("dataset")["total"].apply(lambda s: (s<3).mean()*100).round(1)
print(p3.reindex(DS).to_string())

# ---------- 6. Between/within SD & tỷ số ----------
sec("[V6] Claim 4.3: B giữa-bộ 0,286/trong-bộ 0,415 → 0,69; A 0,587/0,479 → 1,22")
for name, agg, col in [("A", aggA, "overall"), ("B", aggB, "total")]:
    between = agg.groupby("dataset")[col].mean().std(ddof=1)
    within = agg.groupby("dataset")[col].std(ddof=1).mean()
    print(f"Chiều {name}: between={between:.3f}, within={within:.3f}, tỷ số={between/within:.2f}")

# ---------- 7. WAI item intercorr, alpha, Goal-Approach ----------
sec("[V7] Claim 4.3: r̄ 12 mục = 0,715; α = 0,968; Goal–Approach r = 0,891")
aggQ = dimB.groupby(["dataset","interaction_id"])[QC].mean().reset_index()
# pooled-z trung bình tương quan giữa 12 mục (66 cặp), within-dataset, judge-mean
zsum, nsum = 0, 0
alpha_item = cronbach(aggQ, QC)
pair_rs = []
for a, b in combinations(QC, 2):
    pair_rs.append(pooled_z(aggQ, a, b))
print(f"r̄ giữa các mục (pooled within-ds, judge-mean) = {np.mean(pair_rs):.3f} | Cronbach α(12 mục) = {alpha_item:.3f}")
print(f"Goal↔Approach pooled: judge-mean {pooled_z(aggB,'goal','approach'):.3f}")
# thử ở mức record per-judge (không gộp 3 judge)
def pooled_z_perjudge(df, x, y):
    zs, ns = [], []
    for _, g in df.groupby(["dataset","judge"]):
        gg = g[[x,y]].dropna()
        if len(gg) < 10: continue
        r = stats.pearsonr(gg[x], gg[y])[0]
        zs.append(np.arctanh(min(r,0.999))*len(gg)); ns.append(len(gg))
    return np.tanh(sum(zs)/sum(ns))
print(f"Goal↔Approach pooled per-judge-record: {pooled_z_perjudge(dimB,'goal','approach'):.3f}")

# ---------- 8. Q10 + Q5 ----------
sec("[V8] Claim 4.3: Q10 AnnoMI 3,48 / CPsyCoun 3,20 / CACTUS 3,79; SimPsyDial Q5 = 4,76")
q10 = dimB.groupby("dataset")["Q10"].mean()
print("Q10:", {d: round(q10[d],2) for d in ["annomi","cpsycoun","cactus"]})
q5 = dimB[dimB["dataset"]=="simpsydial"]["Q5"].mean()
q_all = dimB[dimB["dataset"]=="simpsydial"][QC].mean().sort_values(ascending=False)
print(f"SimPsyDial Q5 = {q5:.2f}; mục cao nhất simpsydial = {q_all.index[0]} ({q_all.iloc[0]:.2f})")

# ---------- 9. dim C: coverage↔std r=−0,455 n=1398; NEC đổi dấu 5/7 ----------
sec("[V9] Claim 4.4: r(độ phủ, biến thiên)=−0,455, n=1.398; NEC đổi dấu 5/7 bộ ở cấu hình A")
non_en = [d for d in DS if d not in ("esconv","annomi","cactus","psy_insight")]
ca = dimC_A[dimC_A["dataset"].isin(non_en)][["dataset","client_lex_coverage","client_valence_emo_std","client_valence_nec"]].dropna(subset=["client_lex_coverage","client_valence_emo_std"])
r, p = stats.pearsonr(ca["client_lex_coverage"], ca["client_valence_emo_std"])
print(f"r = {r:.3f}, p = {p:.2e}, n = {len(ca)}")
necA = dimC_A[dimC_A["dataset"].isin(non_en)].groupby("dataset")["client_valence_nec"].mean()
necB = dimC_B[dimC_B["dataset"].isin(non_en)].groupby("dataset")["client_valence_nec"].mean()
flip = [(d, round(necA[d],4), round(necB[d],4)) for d in non_en if np.sign(necA[d]) != np.sign(necB[d])]
print(f"NEC đổi dấu A↔B ở {len(flip)}/7 bộ:", flip)

# ---------- 10. variability ratio >1 ở 10/11; soulchat 0,991 ----------
sec("[V10] Claim 4.4: tỷ số biến thiên client/counselor >1 ở 10/11 bộ; SoulChat 0,991")
vr = dimC_B.groupby("dataset")["valence_variability_ratio"].mean().reindex(DS)
print(vr.round(3).to_string()); print("Số bộ >1:", (vr>1).sum())

# ---------- 11. Tông counselor: lưỡng phân 5/6 chính thức ----------
sec("[V11] Claim 4.4: tông counselor LLM 0,185 vs người 0,164; Cliff=−0,933 (29/30 cặp); MW record p=7,3e-36")
mm = master.dropna(subset=["counselor_valence_emo_mean"]).copy()
mm["voice5"] = np.where(mm["dataset"].isin(HUMAN5), "human", "llm")
lv = mm.groupby("voice5")["counselor_valence_emo_mean"].mean()
print(f"record-pooled: human={lv['human']:.3f}, llm={lv['llm']:.3f}")
U, p = stats.mannwhitneyu(mm[mm.voice5=="human"]["counselor_valence_emo_mean"],
                          mm[mm.voice5=="llm"]["counselor_valence_emo_mean"])
print(f"MW record-level p = {p:.2e}")
tone_ds = mm.groupby("dataset")["counselor_valence_emo_mean"].mean()
h5 = [tone_ds[d] for d in HUMAN5]; l6 = [tone_ds[d] for d in DS if d not in HUMAN5]
wins = sum(1 for a in l6 for b in h5 if a > b)
print(f"Cặp LLM>human: {wins}/30 → Cliff's delta = {(wins-(30-wins))/30:.3f}")

# ---------- 12. EPC premium dưới 2 lưỡng phân ----------
sec("[V12] EPC premium (phát hiện mới của tôi) dưới lưỡng phân 4/7 và 5/6 chính thức")
prem = (prof["EPC"] - prof[["CAC","AR","TRA","ASCQ"]].mean(axis=1))
print(prem.round(3).reindex(DS).to_string())
for name, hum in [("4/7 (psydial→LLM vì lời counselor có LLM tinh chỉnh)", HUMAN4),
                  ("5/6 CHÍNH THỨC của bài (psydial→người)", HUMAN5)]:
    h = prem[prem.index.isin(hum)]; l = prem[~prem.index.isin(hum)]
    U, p = stats.mannwhitneyu(h, l, alternative="two-sided")
    print(f"  {name}: human max={h.max():.3f} vs llm min={l.min():.3f} | tách hoàn hảo={h.max()<l.min()} | MW U={U:.0f}, p={p:.4f}")

# ---------- 13. Tông trong-ngôn-ngữ 7/7 ----------
sec("[V13] Claim 4.4: nội-EN 3/3 cặp (0,179 vs 0,155; p=6,6e-13); nội-ZH 4/4 cặp (0,187 vs 0,173; p=4,2e-10)")
en_h = ["esconv","psy_insight","annomi"]; en_l = ["cactus"]
zh_h = ["psydial"]; zh_l = ["smile","soulchat","cpsycoun","simpsydial"]
en = mm[mm["dataset"].isin(en_h+en_l)]
enp = stats.mannwhitneyu(en[en.dataset.isin(en_l)]["counselor_valence_emo_mean"],
                         en[en.dataset.isin(en_h)]["counselor_valence_emo_mean"])[1]
print(f"EN: cactus {tone_ds['cactus']:.3f} vs human-EN pooled {en[en.dataset.isin(en_h)]['counselor_valence_emo_mean'].mean():.3f}; cặp thắng {sum(1 for b in en_h if tone_ds['cactus']>tone_ds[b])}/3; MW p={enp:.1e}")
zh = mm[mm["dataset"].isin(zh_h+zh_l)]
zhp = stats.mannwhitneyu(zh[zh.dataset.isin(zh_l)]["counselor_valence_emo_mean"],
                         zh[zh.dataset.isin(zh_h)]["counselor_valence_emo_mean"])[1]
print(f"ZH: LLM-4 pooled {zh[zh.dataset.isin(zh_l)]['counselor_valence_emo_mean'].mean():.3f} vs psydial {tone_ds['psydial']:.3f}; cặp thắng {sum(1 for a in zh_l if tone_ds[a]>tone_ds['psydial'])}/4; MW p={zhp:.1e}")

# ---------- 14. Claude−Gemini B; GPT bias A ----------
sec("[V14] Claim 4.5: Claude−Gemini trên B từ −0,757 (SMILE) đến −0,019 (Psy-Insight); GPT +0,35–0,40 trên A")
jb = dimB.pivot_table(index="dataset", columns="judge", values="total", aggfunc="mean")
cg = (jb["claude"] - jb["gemini"]).round(3)
print("claude−gemini B:", cg.reindex(DS).to_dict())
print(f"  min = {cg.min():.3f} ({cg.idxmin()}), max = {cg.max():.3f} ({cg.idxmax()})")
ja = dimA.pivot_table(index="dataset", columns="judge", values="overall", aggfunc="mean")
gpt_vs_council = (ja["gpt"] - ja.mean(axis=1)).mean()
gpt_vs_others = (ja["gpt"] - (ja["claude"]+ja["gemini"])/2)
gpt_vs_claude = (ja["gpt"] - ja["claude"])
print(f"GPT−TB hội đồng (A): {gpt_vs_council:.3f} | GPT−TB(2 judge kia): TB={gpt_vs_others.mean():.3f} | GPT−Claude: TB={gpt_vs_claude.mean():.3f}")

# ---------- 15. Kendall tau xếp hạng giữa judge ----------
sec("[V15] Claim 4.5: Kendall τ trật tự 11 bộ — A: 0,891–0,927; B: 0,600–0,709")
for name, piv in [("A", ja), ("B", jb)]:
    taus = []
    for x, y in combinations(["claude","gemini","gpt"], 2):
        taus.append(stats.kendalltau(piv[x], piv[y])[0])
    print(f"Chiều {name}: τ = {[round(t,3) for t in taus]} (min {min(taus):.3f}, max {max(taus):.3f})")

# ---------- 16. SimPsyDial: MAE claude-gpt = 0,154, r = 0,649 ----------
sec("[V16] Claim 4.5: SimPsyDial chênh tuyệt đối Claude–GPT 0,154 dù r 0,649")
sp = dimB[dimB["dataset"]=="simpsydial"].pivot_table(index="interaction_id", columns="judge", values="total")[["claude","gpt"]].dropna()
mae = (sp["claude"] - sp["gpt"]).abs().mean(); r = stats.pearsonr(sp["claude"], sp["gpt"])[0]
print(f"MAE = {mae:.3f}, r = {r:.3f}")

# ---------- 17. Krippendorff alpha (interval) spot-check ----------
sec("[V17] Bảng 3 α(A)/α(B) — kiểm 5 giá trị: annomi A 0,834/B 0,949; soulchat A 0,520; simpsydial B 0,526; cactus A 0,629")
def kripp_interval(piv):
    m = piv.dropna(); vals = m.values
    pooled = vals.flatten()
    De = 2 * np.var(pooled, ddof=1)
    pairs = [(0,1),(0,2),(1,2)]
    Do = np.mean([np.mean([(row[i]-row[j])**2 for i,j in pairs]) for row in vals])
    return 1 - Do/De
for ds, dim, piv_src, val in [("annomi","A",ja,None),("soulchat","A",None,None)]:
    pass
pivA = {ds: dimA[dimA["dataset"]==ds].pivot_table(index="interaction_id", columns="judge", values="overall") for ds in DS}
pivB = {ds: dimB[dimB["dataset"]==ds].pivot_table(index="interaction_id", columns="judge", values="total") for ds in DS}
checks = [("annomi","A",0.834),("soulchat","A",0.520),("cactus","A",0.629),
          ("annomi","B",0.949),("simpsydial","B",0.526),("psy_insight","B",0.926)]
for ds, d, ref in checks:
    a = kripp_interval(pivA[ds] if d=="A" else pivB[ds])
    print(f"  {ds} α({d}): bài={ref} | tính lại={a:.3f}")

# ---------- 18. 6 case study 4.8 ----------
sec("[V18] 6 case study 4.8")
cases = [("cactus","cactus_121"),("kmi","kmi_712"),("simpsydial","simpsydial_463"),
         ("cactus","cactus_19"),("soulchat","soulchat_157820"),("esconv","esconv_43")]
for ds, iid in cases:
    row = master[(master["dataset"]==ds) & (master["interaction_id"]==iid)]
    if len(row)==0:
        print(f"  {iid}: KHÔNG TÌM THẤY"); continue
    r = row.iloc[0]
    print(f"  {iid}: A={r['A_overall']:.2f}, B={r['B_total']:.2f}, NEC={r['client_valence_nec'] if pd.notna(r['client_valence_nec']) else float('nan'):+.3f}")

# ---------- 19. Self-preference ----------
sec("[V19] Bảng 9: 'GPT chấm SimPsyDial/CACTUS cao hơn Claude 0,29–0,38 so với thiên lệch nền'")
gc = (ja["gpt"] - ja["claude"]).round(3)
print("gpt−claude (A) từng bộ:", gc.reindex(DS).to_dict())
base_all = gc.mean(); base_excl = gc.drop(["simpsydial","cactus"]).mean(); base_med = gc.median()
print(f"cactus={gc['cactus']:.3f}, simpsydial={gc['simpsydial']:.3f} | nền: TB 11 bộ={base_all:.3f}, TB 9 bộ khác={base_excl:.3f}, trung vị={base_med:.3f}")
print(f"→ Vượt nền? cactus {gc['cactus']-base_excl:+.3f}, simpsydial {gc['simpsydial']-base_excl:+.3f} so nền-9-bộ")
# thử cả dim B
gcB = (jb["gpt"] - jb["claude"]).round(3)
print("gpt−claude (B): cactus=%.3f, simpsydial=%.3f, TB 9 bộ khác=%.3f" % (gcB["cactus"], gcB["simpsydial"], gcB.drop(["simpsydial","cactus"]).mean()))

# ---------- 20. Tương quan A với token counselor (4.2) ----------
sec("[V20] Claim 4.2: KokoroChat 0,42; Psy-Insight 0,30; AnnoMI 0,28; SMILE −0,23 — 'lượng lời counselor'")
for ds in ["kokorochat","psy_insight","annomi","smile"]:
    g = master[master["dataset"]==ds].dropna(subset=["counselor_n_tokens"])
    rco = stats.spearmanr(g["A_overall"], g["counselor_n_tokens"])[0]
    rtot = stats.spearmanr(g["A_overall"], g["total_tokens"])[0]
    print(f"  {ds}: rho(A, counselor_tokens)={rco:.3f} | rho(A, total_tokens)={rtot:.3f}")

print("\nDONE BƯỚC 6")
