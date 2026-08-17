# -*- coding: utf-8 -*-
"""BƯỚC 5 — Kiểm định 3 phát hiện mới: (1) 'phụ phí EPC' như vân tay guardrail;
(2) đồng thuận judge ~ hàm của SD nội dataset (range restriction);
(3) judge bias đổi chiều theo công cụ. + đối chiếu eta2 với file cũ."""
import os, sys
import pandas as pd, numpy as np
from scipy import stats
from itertools import combinations

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
KQ = r"H:\Vy\Paper\Empathy\Report\_Chuan_bi\_analyst_v7\vy\New folder\ket_qua_phan_tich"

DS_ORDER = ["esconv","kokorochat","psy_insight","annomi","psydial",
            "smile","soulchat","cpsycoun","cactus","simpsydial","kmi"]
HUMAN_VOICED = {"esconv","kokorochat","psy_insight","annomi"}

sub = pd.read_csv(os.path.join(OUT, "r_A2_subscale_profile.csv"), index_col=0)
prem = sub["EPC_minus_rest"]
voice = pd.Series({d: ("human" if d in HUMAN_VOICED else "llm") for d in prem.index})

print("[N1] 'Phụ phí EPC' (EPC − TB 4 trục còn lại) như vân tay guardrail:")
t = pd.DataFrame({"EPC_premium": prem, "voice": voice}).sort_values("EPC_premium")
print(t.to_string())
h = prem[voice == "human"]; l = prem[voice == "llm"]
U, p = stats.mannwhitneyu(h, l, alternative="two-sided")
sep = h.max() < l.min()
print(f"human-voiced: max={h.max():.3f} | llm-voiced: min={l.min():.3f} | tách hoàn hảo: {sep}")
print(f"Mann–Whitney U={U:.0f}, p={p:.4f} (n=4 vs 7)")
# exact permutation p cho tách hoàn hảo
from math import comb
print(f"p hoán vị chính xác 2 phía cho tách hoàn hảo (U=0): {2/comb(11,4):.4f}")

print("\n[N2] Đồng thuận judge ~ SD nội dataset (range restriction):")
agrA = pd.read_csv(os.path.join(OUT, "r_A4_judge_agreement.csv"), index_col=0)["mean_pairwise_r"]
agrB = pd.read_csv(os.path.join(OUT, "r_B5_judge_agreement.csv"), index_col=0)["mean_pairwise_r"]
sdA = pd.read_csv(os.path.join(OUT, "r_A1_dataset_overall.csv"), index_col=0)["sd"]
sdB = pd.read_csv(os.path.join(OUT, "r_B1_dataset_wai.csv"), index_col=0)["sd"]
rA, pA = stats.spearmanr(agrA.reindex(DS_ORDER), sdA.reindex(DS_ORDER))
rB, pB = stats.spearmanr(agrB.reindex(DS_ORDER), sdB.reindex(DS_ORDER))
print(f"dim A: Spearman(agreement, SD) = {rA:.3f} (p={pA:.4f})")
print(f"dim B: Spearman(agreement, SD) = {rB:.3f} (p={pB:.4f})")

print("\n[N3] Judge bias đổi chiều theo công cụ (điểm TB chuẩn hóa % thang):")
# dim A thang 1-6 → % = (x-1)/5; dim B thang 1-5 → % = (x-1)/4
jA = {"claude": 2.613, "gemini": 2.535, "gpt": 2.978}   # từ s2 [A3]
jB = {"claude": 3.792, "gemini": 4.228, "gpt": 3.976}   # từ s2 [B5]
for j in ["claude","gemini","gpt"]:
    a_pct = (jA[j]-1)/5*100; b_pct = (jB[j]-1)/4*100
    print(f"  {j:7s}: dim A {jA[j]:.3f} ({a_pct:.1f}% thang) | dim B {jB[j]:.3f} ({b_pct:.1f}% thang) | lệch B−A = {b_pct-a_pct:+.1f} điểm %")

print("\n[N4] Đối chiếu eta2 với file cũ _agg_discriminative_power.csv:")
old = pd.read_csv(os.path.join(KQ, "_agg_discriminative_power.csv"))
print(old.to_string(index=False))
mine = pd.read_csv(os.path.join(OUT, "r_F2_eta2.csv"))
print("\n(của tôi)"); print(mine.to_string(index=False))

print("\n[N5] Đối chiếu nhóm provenance với _agg_group_means_official.csv:")
oldg = pd.read_csv(os.path.join(KQ, "_agg_group_means_official.csv"))
print(oldg.to_string(index=False))
