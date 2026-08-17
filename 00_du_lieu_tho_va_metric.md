# BƯỚC 0 — CHUẨN BỊ & KIỂM CHỨNG DỮ LIỆU (BẢNG METRIC + SỐ LIỆU THÔ + BẤT THƯỜNG)

## THAY ĐỔI SO VỚI BẢN TRƯỚC (cập nhật lần chạy 2)
1. **Nguồn lý thuyết được thay thế toàn bộ**: lý thuyết duy nhất có thẩm quyền nay là 3 file Word — `Tong_hop_11_dataset_tham_van_tri_lieu_multi_turn.docx` (viết tắt **BC-DATA**), `Tong_hop_5_bai_evaluation_3_goc_nhin.docx` (**BC-EVAL**), `Phan_tich_3_chieu_danh_gia_va_thiet_ke_dataset.docx` (**BC-3D**). Đối chiếu: bảng metric 3 dim (mục 1–3) **không đổi giá trị** (BC-EVAL xác nhận đúng thang/chiều đã chốt); phần nguồn gốc 11 dataset (mục 4.6 cũ) được **thay bằng taxonomy provenance 4 nhóm chính thức** của BC-DATA §1.3/Bảng 2.1. BT15 cũ (folder theory lệch mô tả) được đóng — nguyên nhân đúng như ghi nhận: PDF cũ là nhầm lẫn, nay đã thay nguồn.
2. **Dim B đã đủ 11 dataset**: nạp 4 file jsonl mới trong `D:\vy\jsonl\` (claude, S3, full): PsyDial 200, Simpsydial 200, Psy-Insight 200, smile 199 record — gỡ toàn bộ nhãn "N/A"; panel Dim B nay hoàn chỉnh 2.111 dialogue × 3 judge. Số liệu cũ được tái dùng nguyên trạng (không chạy lại; kiểm tra trùng lặp old–new = 0).
3. **Bảng gọn mới** đặt tại `ket_qua_phan_tich/_agg_*.csv` (13 file, sinh bởi `_notes/step0_dimB_moi.py` + lệnh bổ trợ): bảng Dim B 11 dataset, agreement, MTMM, hồi quy provenance (nhãn chính thức), sức phân biệt metric, rank stability, case bất đồng chiều, nhóm provenance/nhóm "ai viết lời counselor".
4. Bất thường mới BT17–BT20 (mục 7); các bảng ở mục 5.3 và mục 6 được cập nhật tương ứng. Mọi nội dung khác giữ nguyên.

Tài liệu này chốt (i) bảng metric của 3 chiều đánh giá (đối chiếu BC-EVAL), (ii) kiểm kê dữ liệu thô thực đọc được từ các thư mục kết quả theo đúng bảng ánh xạ (+ folder `jsonl` mới), (iii) danh mục dữ liệu thiếu, và (iv) toàn bộ bất thường/mâu thuẫn phát hiện. Các file phân tích 01–04 chỉ dùng số liệu đã chốt tại đây. Bảng trung gian: `_stats/` (lần 1, tái dùng) và `_agg_*.csv` (lần 2).

---

## 1. BẢNG METRIC DIM A — MindEval (đánh giá counselor)

**Nguồn:** `theory/evaluation/3.AI-specific Risks (Dependency, Over-reassurance, Boundary erosion, Hallucinated guidance).pdf`. Đối chiếu nội dung: file này chính là paper **MindEval: Benchmarking Language Models on Multi-turn Mental Health Support** (Pombal et al., arXiv:2511.18491v3; venue chính thức: không xác định được từ nguồn). Judge đánh giá **toàn bộ hội thoại như một khối**, không chấm từng lượt (MindEval §2.3, tr.4).

| # | Metric (tên nguyên văn) | Nội dung | Thang điểm | Chiều tốt/xấu |
|---|---|---|---|---|
| 1 | Clinical Accuracy & Competence (CAC) | Vận dụng kiến thức trị liệu đúng, khớp can thiệp với nhu cầu | Likert **1–6** | **Cao = tốt** |
| 2 | Ethical & Professional Conduct (EPC) | Giữ ranh giới nghề nghiệp, tôn trọng, không hứa hẹn/mờ vai trò AI | 1–6 | Cao = tốt |
| 3 | Assessment & Response (AR) | Hiểu input của thân chủ và điều chỉnh phản hồi, attunement | 1–6 | Cao = tốt |
| 4 | Therapeutic Relationship & Alliance (TRA) | Xây dựng/duy trì quan hệ hợp tác, chống dependency | 1–6 | Cao = tốt |
| 5 | AI-Specific Communication Quality (ASCQ, "LLMness") | Tính tự nhiên, không rập khuôn, không hallucination — trục mới của MindEval | 1–6 | Cao = tốt |
| — | Overall/Average score | **Trung bình cộng không trọng số của 5 trục** (MindEval §2.3 tr.4, §4.1 tr.7) | 1–6 | Cao = tốt |

- Anchor thang điểm (judge prompt, MindEval Fig.12 tr.23): 1 = major failures phá hoại giá trị trị liệu/an toàn; 2 = significant problems; 3 = acceptable baseline còn hạn chế đáng kể; 4 = solid, lỗi nhỏ; 5 = strong (RARE); 6 = exceptional (VERY RARE). Judge được calibrate rằng đa số hội thoại rơi vào 2–4.
- 4 rủi ro AI trong tên file (Dependency / Over-reassurance / Boundary erosion / Hallucinated guidance) **không phải taxonomy riêng trong paper**; chúng là hành vi neo điểm thấp phân tán trong rubric: Dependency→TRA; Over-reassurance/sycophancy→CAC+AR; Boundary erosion→EPC; Hallucination→ASCQ (MindEval App.B tr.24–28). Trục "Safety & Crisis Management" đã bị paper loại bỏ (§5 tr.11) → khung này **không đo rủi ro khủng hoảng cấp tính**.
- Validation của paper: Kendall-τ judge–chuyên gia (Average score) = 0.3786, nằm trong khoảng đồng thuận người–người 0.1178–0.3854; per-criterion: ASCQ cao nhất (τ=0.481), TRA thấp nhất (τ=0.1721) (MindEval §3.2 tr.6–7, Tables 12–17 tr.35–36).
- **Kiểm chứng trên dữ liệu:** 6,333/6,333 record full có "Overall score" = "Average score" (chênh ≤0.05: 100%) → pipeline nhất quán với định nghĩa trung bình không trọng số (script `aggregate_stats.py`).

## 2. BẢNG METRIC DIM B — WAI-O-S (liên minh trị liệu counselor–client)

**Nguồn:** `theory/evaluation/1.Therapeutic Alliance (Goal, Approach, Affective Bond).pdf` = paper **Understanding the Therapeutic Relationship between Counselors and Clients in Online Text-based Counseling using LLMs** (Li et al., arXiv:2402.11958v2). Khung: **WAI-O-S** (Observer-rated Short version, Tichenor & Hill 1989) — 12 item, 3 chiều × 4 item (Table 1, tr.4 của paper).

| Chiều (metric) | Item | Nội dung tóm tắt | Thang | Chiều tốt/xấu |
|---|---|---|---|---|
| **Goal** | Q1–Q4 | Đồng thuận về mục tiêu trị liệu, cùng cách hiểu vấn đề thật của client | 1–5 | **Cao = liên minh mạnh = tốt** |
| **Approach** (=Task trong WAI gốc) | Q5–Q8 | Đồng thuận về bước đi/nhiệm vụ, client tin cách làm là đúng | 1–5 | Cao = tốt |
| **Affective Bond** | Q9–Q12 | Thiện cảm, tin tưởng năng lực, được trân trọng, tin cậy lẫn nhau | 1–5 | Cao = tốt |
| Total | — | Trung bình 3 chiều | 1–5 | Cao = tốt |

- Anchor điểm theo **lượng bằng chứng** (paper §5.1 tr.6, Fig.5 tr.20): 1 = substantial evidence AGAINST; 2 = some against; **3 = absence of evidence (trung lập)**; 4 = some for; 5 = substantial evidence FOR. → Điểm không chỉ đo "chất lượng" mà đo *bằng chứng quan sát được* — hội thoại ngắn thiếu bằng chứng sẽ tụ về 3 (hệ quả đo được ở mục 7-BT11).
- Giao thức pipeline khớp setting mạnh nhất của paper (Detailed Guidelines + CoT + 3 runs, tổng hợp bằng mean; paper §5.2 tr.6, App.C.2 tr.19). Validation của paper: Pearson LLM–chuyên gia tốt nhất ≈ 0.50 (GPT-4 overall 0.5018); human ICC(2,k) Goal 0.7581/Approach 0.6587/Bond 0.6498.
- Cảnh báo từ paper: wording Appendix A.3 của Q1, Q3 là bản âm tính đảo chiều; pipeline của nghiên cứu này dùng wording dương tính Table 1 (đã đối chiếu nguyên văn Q1–Q12 trong dữ liệu — khớp Table 1) → **mọi item đồng hướng cao = tốt**, không có reverse-scoring.
- **Kiểm chứng trên dữ liệu:** `dimensions.Goal/Approach/Affective Bond` = trung bình đúng 4 item tương ứng; `total` = trung bình 3 chiều (0/5,528 record lệch >0.02; script `aggregate_stats.py`).

## 3. BẢNG METRIC DIM C — UED (động lực học cảm xúc)

**Nguồn:** `theory/evaluation/5` (Hipson & Mohammad 2021 — nền tảng UED), `6` (Teodorescu & Mohammad 2023 — độ tin cậy arc đa ngôn ngữ), `7` (Wang et al. — "Feel the Difference?", paper chính; so sánh RealCBT vs CACTUS). Pipeline: NRC-VAD, cửa sổ trượt 10 từ, arc riêng cho client/counselor trên 3 chiều Valence/Arousal/Dominance (paper 7 §4 tr.4; thang VAD v2: **−1..1**).

| Metric (cột dữ liệu) | Định nghĩa | Nguồn định nghĩa | Chiều diễn giải |
|---|---|---|---|
| emo_mean | Trung bình điểm V/A/D trên arc | P7 §4; P5 tr.4 | Mô tả; valence cao = tông tích cực. P7: synthetic > real = "elevated tone" thiếu tự nhiên |
| emo_std (variability) | SD của chuỗi điểm | P5 tr.4 Eq.3; P7 §4 | Mô tả ("richness/unpredictability"); P7: real > synthetic (arousal r=0.84) |
| avg_peak_dist | Khoảng cách Euclid từ chu vi home base đến peak | P5 tr.5–6 | Cao = lệch khỏi nền mạnh hơn |
| avg_disp_length | Số từ từ lúc rời home base đến lúc quay lại | P5 tr.5; P7 §4 | Dài = đợt cảm xúc dai dẳng hơn; P7: real > synthetic |
| rise_rate | peak_dist ÷ số từ giai đoạn rise (reactivity) | P5 tr.6; P7 §4 | Cao = phản ứng nhanh/mạnh; P7: synthetic client cao hơn = "exaggerated affect" |
| recovery_rate | peak_dist ÷ số từ giai đoạn recovery (regulation) | P5 tr.6; P7 §4 | Cao = hồi phục nhanh; P7: synthetic client cao hơn = "smoothing", KHÔNG nghĩa là tốt hơn |
| n_displacements (low/high) | Số lần rời home base | P5 tr.5; phân tách low/high: **không xác định được từ nguồn** (chỉ có tên biến trong P7 Bảng 8–10) | Mô tả |
| **nec** | **Không có trong 3 paper nguồn.** Kiểm chứng số học trên dữ liệu: `nec = last_mean − first_mean` đúng 100% (2,031+2,037 record, sai số 0) | Định nghĩa vận hành từ dữ liệu | Dương = kết phiên tích cực hơn mở phiên (net emotional change của arc) |
| first_mean / last_mean | Không có trong nguồn; theo dữ liệu = mean đoạn đầu/cuối arc | Vận hành | — |
| **happy_ending** | Không có trong nguồn. Kiểm chứng: `happy_ending = (nec > 0)` đúng 100% | Vận hành | True = valence cuối > đầu |
| variability_ratio | Không có trong nguồn. Kiểm chứng: = client_emo_std ÷ counselor_emo_std (sai số ≤5e−5) | Vận hành | >1 = client dao động hơn counselor |
| lex_coverage | Không định nghĩa trong nguồn; P5 tr.18 cảnh báo "coverage" của lexicon theo domain | Vận hành: tỷ lệ token khớp lexicon | Thấp → ước lượng cảm xúc dựa trên ít bằng chứng từ vựng → kém tin cậy |
| arc_length, n_tokens | Không định nghĩa trong nguồn; theo dữ liệu: số điểm arc / số token | Vận hành | Proxy độ dài |

- **Quan trọng (P5 tr.18–19):** UED chỉ có ý nghĩa **tương đối so với quần thể**, không metric nào tốt/xấu tuyệt đối; chuẩn chất lượng của P7 là "**gần phân bố người thật**".
- **P6 (nền tảng đa ngôn ngữ):** lexicon dịch tự động cho arc đáng tin khi **aggregate đủ lớn** (bin ≥ vài trăm instance: correlation 0.9x; bin nhỏ: chỉ 0.1–0.5) → trực tiếp liên quan cấu hình A/B của Dim C (cửa sổ 10 từ là aggregation nhỏ).
- Lexicon thực dùng (đọc từ trường `lexicon_used` trong dữ liệu): cấu hình A = bản dịch NRC-VAD tiếng Trung/Hàn/Nhật ("[native col, scale=0_1]"); cấu hình B = NRC-VAD v2.1 EN unigrams; 4 dataset tiếng Anh (annomi, cactus, esconv, psy_insight) dùng chung EN lexicon ở cả A và B (A≡B, đã kiểm chứng byte-level: identical_AB = True).

## 4. KIỂM KÊ DỮ LIỆU THÔ (số record THỰC đọc được)

### 4.1. 11 dataset và ngôn ngữ (theo trường `language` trong dim C và mã ngôn ngữ file)
EN: annomi, cactus, esconv, psy_insight · ZH: cpsycoun, psydial, simpsydial, smile, soulchat · JA: kokorochat · KO: kmi.

### 4.2. Dim A — `experiments/dim_a_mind_eval/`
| Giai đoạn | Cấu hình | Judge (chuẩn hóa theo họ model) | Số record/dataset |
|---|---|---|---|
| Pilot `20/` | S3: đủ 11 dataset; S1+S2: chỉ 7 dataset non-EN (cpsycoun, kmi, kokorochat, psydial, simpsydial, smile, soulchat) | 4 judge: claude (claude-sonnet-4-6), gemini (gemini-3.1-pro-low), gpt (gpt-5.1), qwen (qwen3-235b-a22b-thinking-2507) | 20 (smile: **19**) |
| Full `full/` | S3 | 3 judge: claude, gemini, gpt (**không có qwen**) | 200; AnnoMI **112**; smile **199** |

Tổng record full Dim A đọc được: **6,333** (= 3 judge × 2,111 dialogue), parse_fail = 0.

### 4.3. Dim B — `experiments/dim_b_wai/`
| Giai đoạn | Cấu hình | Judge | Số record |
|---|---|---|---|
| Pilot `20/` | **S3**: 11 dataset × 3 judge (claude, gemini, gpt) | claude, gemini, gpt (KHÔNG có qwen) | 20 (smile 19; **kokorochat×gpt: chỉ 2** — xem BT9) |
| Pilot `20/` | **S1**: 10 dataset (không có ESConv), **chỉ judge gpt** | gpt | 20 (file chứa 20–40 id, xem BT8) |
| Pilot `20/` | **S2**: **KHÔNG TỒN TẠI** file nào | — | — |
| Full `full/` | S3 | gemini + gpt: đủ 11 dataset; claude: 7 dataset | 200; AnnoMI 112; smile 199 |
| **Full bổ sung `D:\vy\jsonl\` (lần 2)** | S3 | **claude cho 4 dataset còn thiếu**: PsyDial (200), Simpsydial (200), Psy-Insight (200), smile (199) | id khớp 100% bộ full cũ; trùng lặp old–new = 0 |

Tổng record full Dim B đọc được (sau bổ sung): **6,333** (claude 2,111 + gemini 2,111 + gpt 2,111) — panel hoàn chỉnh, đối xứng với Dim A. (Nguồn: `_agg_dimB_newfiles_report.csv`, `_stats/dimB_records_full_v2.csv`.)

### 4.4. Dim C — `experiments/dim_c/`
| Cấu hình | Thư mục | Số dòng/dataset | n_valid (client valence không NaN) |
|---|---|---|---|
| A (ngôn ngữ gốc + lexicon gốc) | `dim_c_A_full_0629/` | 200/dataset; annomi 112; **smile 200** | annomi 110, cpsycoun 188, **psy_insight 141**, smile 198, còn lại 200 |
| B (dịch EN + lexicon EN) | `dim_c_B_full_0629/` | như trên | annomi 110, cpsycoun **182**, psy_insight 141, smile 198, còn lại 200 |

### 4.5. Khớp ID giữa các dim (điều kiện cho phân tích liên kết)
Join theo `interaction_id`/`dialogue_id`: Dim A ∩ Dim B = 100%; Dim A ∩ Dim C = 100% (trừ smile: 199/200, thiếu `smile_74` ở Dim A/B). Pilot-20 là **tập con** của full-200 (overlap 20/20, kiểm tra trên CPsyCoun, KMI, smile). → Cho phép phân tích ghép cặp mức record xuyên dim và pilot–full. (`crossdim_join_diagnostics.csv`)

### 4.6. Nguồn gốc 11 dataset theo taxonomy provenance chính thức (BC-DATA §1.3, Bảng 2.1) — THAY THẾ mục cũ
Định nghĩa 4 nhóm (BC-DATA §1.3): **REAL** = người thật tạo lời thoại (role-play có huấn luyện hoặc tư liệu chuyên môn đã xuất bản); **SEMI-REAL** = nửa thật (bản ghi trình diễn chuyên môn; hoặc tái tạo từ hội thoại thật với một phía do LLM sinh lại); **SEMI-SYNTHETIC** = hạt giống thật + LLM biến đổi; **FULLY SYNTHETIC** = LLM đóng cả hai vai (giữ "mỏ neo thật" ở hạt giống).

| Dataset | Ngôn ngữ | Provenance (nguyên văn BC-DATA) | Quy mô gốc; số lượt | Nền tảng lý thuyết |
|---|---|---|---|---|
| esconv | EN | **Real** — crowdworker được huấn luyện + sát hạch, role-play | 1,053 hội thoại; 29.8 lượt nói | Hill Helping Skills; 8 chiến lược |
| kokorochat | JA | **Real** — role-play bởi counselor đã đào tạo (cả 2 vai) | 6,589; 91.2 lượt nói | Feedback 20 mục chuyên gia |
| psy_insight | **EN+ZH** | **Real (xuất bản)** — hội thoại từ sách/blog chuyên môn + chú giải | 951 phiên / **189 ca (multi-session)**; 54–77 lượt nói/ca | 12 trường phái (SFBT 41.9%, CBT 24.3%) |
| annomi | EN | **Semi-real** — video **trình diễn** MI + chuyên gia MINT chú giải | 133 hội thoại; 72.9 lượt nói | MI (MISC/MITI); change talk |
| psydial | ZH | **Semi-real** — RMRR tái tạo từ 2,382 hội thoại thật (Xinling) | 2,382; 37.8 lượt (~75.6 lượt nói) | Client-centered; 8 kỹ năng |
| smile | ZH | **Semi-synthetic** — ChatGPT viết lại PsyQA thành đa lượt | 55,165; 5.7 lượt (33.2 lượt nói) | Không; 60 chủ đề (kèm PsyTest thật) |
| soulchat | ZH | **Semi-synthetic** — QA người viết → ChatGPT viết lại đa lượt | ~258k hội thoại; 5.9 lượt | Ràng buộc thấu cảm trong prompt |
| cpsycoun | ZH | **Semi-synthetic** — tái tạo từ BÁO CÁO tham vấn thật (Memo2Demo) | 3,134; 8.7 lượt | 7 trường phái (CBT 26%); 4 giai đoạn |
| cactus | EN | **Fully synthetic** — GPT-4o script mode + planning CBT | 31,577; 16.6 lượt (31.5 lượt nói) | CBT; lọc CTRS (giữ 86.3%) |
| simpsydial | ZH | **Fully synthetic** — GPT-4 × GPT-4; role card từ PsyQA | 1,000; 13 lượt (25.9 lượt nói) | Hill 3 giai đoạn + integrative |
| kmi | KO | **Fully synthetic** — LLM–LLM + MI forecaster học từ AnnoMI | 1,000; 18.12 lượt nói | MI (MITI 8 nhãn; DARN) |

Ghi chú đối chiếu quan trọng với bản trước: (i) **AnnoMI được BC-DATA xếp semi-real** (video trình diễn chuyên môn, không phải phiên trị liệu tự nhiên) — bản trước xếp "real"; (ii) nhóm **real theo BC-DATA đo "ai viết lời thoại"** (người thật) chứ không phải "phiên trị liệu thật"; (iii) **Psy-Insight có cấu trúc multi-session duy nhất trong 11 dataset** (BC-3D §3.3 xu hướng 7) — bản trước ghi "không dataset nào"; (iv) AnnoMI gốc 133 hội thoại (thí nghiệm lấy 112 — chênh lệch ghi ở BT19). Chi tiết từng dataset: `_notes/theory_word_11dataset_tomtat.md`.

## 5. BẢNG SỐ LIỆU THÔ TỔNG HỢP ĐÃ CHỐT

### 5.1. Dim A full (S3, 200 record, Overall 1–6, trung bình 3 judge; nguồn: `_stats/dimA_full_dataset_summary.csv`, `_stats/dimA_full_metric_profile.csv`)
| Dataset | n | Overall mean±SD | median | %<3 | %≥4 | CAC | EPC | AR | TRA | ASCQ |
|---|---|---|---|---|---|---|---|---|---|---|
| annomi | 112 | **3.621**±1.079 | 3.900 | 27.7 | 46.4 | 3.478 | 3.669 | 3.443 | 3.576 | **3.938** |
| cactus | 200 | 3.376±0.267 | 3.383 | 8.5 | 1.0 | 3.360 | 4.110 | 3.178 | 3.419 | 2.815 |
| psy_insight | 200 | 3.364±0.886 | 3.492 | 30.0 | 27.5 | 3.266 | 3.637 | 3.145 | 3.188 | 3.584 |
| simpsydial | 200 | 3.188±0.362 | 3.250 | 23.5 | 0.0 | 2.949 | 3.792 | 2.962 | 3.336 | 2.901 |
| kokorochat | 200 | 2.917±0.497 | 2.933 | 53.5 | 1.0 | 2.750 | 3.182 | 2.874 | 3.130 | 2.647 |
| kmi | 200 | 2.653±0.265 | 2.675 | 91.0 | 0.0 | 2.364 | **3.950** | 2.369 | 2.622 | **1.958** |
| psydial | 200 | 2.481±0.392 | 2.500 | 92.0 | 0.0 | 2.356 | 3.000 | 2.262 | 2.722 | 2.067 |
| smile | 199 | 2.321±0.422 | 2.317 | 95.0 | 0.0 | 2.170 | 2.674 | 2.138 | 2.407 | 2.215 |
| cpsycoun | 200 | 2.285±0.412 | 2.300 | 95.0 | 0.0 | 2.110 | 2.790 | 1.996 | 2.222 | 2.307 |
| soulchat | 200 | 2.191±0.332 | 2.217 | 99.0 | 0.0 | 2.026 | 2.551 | 1.968 | 2.271 | 2.138 |
| esconv | 200 | **1.798**±0.359 | 1.750 | 100.0 | 0.0 | 1.755 | **1.612** | 1.855 | 2.068 | 1.702 |

### 5.2. Dim A pilot (Overall theo cấu hình, TB 4 judge; nguồn: `_stats/dimA_pilot_dsxconfig.csv`)
| Dataset | S1 | S2 | S3 |
|---|---|---|---|
| cpsycoun | 2.287 | 2.369 | 2.411 |
| kmi | 2.192 | 2.443 | 2.446 |
| kokorochat | 2.426 | 2.909 | 2.469 |
| psydial | 2.322 | 2.422 | 2.336 |
| simpsydial | 2.934 | 2.923 | 3.065 |
| smile (n=19) | 1.844 | 1.830 | 1.779 |
| soulchat | 2.029 | 2.114 | 2.073 |
| annomi / cactus / esconv / psy_insight | — | — | 2.707 / 3.187 / 1.638 / 2.761 |

### 5.3. Dim B full — ĐẦY ĐỦ 11 DATASET (S3, total 1–5, trung bình 3 judge; nguồn: `_agg_dimB_official_11ds.csv`; nhãn N/A đã gỡ)
| Hạng | Dataset | Total 3j ± SD | Goal | Approach | Bond | %≥4 | Total 2j (đối chiếu) | 2j−3j |
|---|---|---|---|---|---|---|---|---|
| 1 | simpsydial | **4.335**±0.181 | 4.333 | 4.435 | 4.238 | **99.0** | 4.433 | +0.097 |
| 2 | cactus | 4.290±0.336 | 4.410 | 4.355 | 4.106 | 81.0 | 4.358 | +0.067 |
| 3 | psydial | 4.182±0.273 | 4.146 | 4.151 | 4.249 | 83.0 | 4.325 | +0.143 |
| 4 | smile | 4.166±0.369 | 4.158 | 4.158 | 4.182 | 80.4 | 4.318 | +0.153 |
| 5 | kmi | 4.088±0.199 | 4.241 | 4.084 | 3.938 | 68.0 | 4.161 | +0.073 |
| 6 | kokorochat | 4.046±0.531 | 4.053 | 3.989 | 4.095 | 65.0 | 4.133 | +0.087 |
| 7 | esconv | 4.007±0.512 | 3.910 | 4.032 | 4.079 | 62.0 | 4.139 | +0.132 |
| 8 | soulchat | 3.992±0.300 | 3.937 | 3.942 | 4.096 | 52.5 | 4.164 | +0.172 |
| 9 | annomi | 3.760±0.934 | 3.840 | 3.769 | 3.672 | 57.1 | 3.803 | +0.043 |
| 10 | psy_insight | 3.605±0.573 | 3.700 | 3.646 | 3.471 | 25.0 | 3.605 | −0.000 |
| 11 | cpsycoun | **3.418**±0.355 | 3.476 | 3.238 | 3.538 | 6.5 | 3.554 | +0.136 |

Kiểm chứng dự đoán bản trước: bản trước dự đoán 3 dataset thiếu (simpsydial/psydial/smile) "vẫn thuộc nhóm đầu" với hiệu chỉnh −0.10 — thực tế đúng: chênh 2j−3j của 4 dataset mới = +0.097/+0.143/+0.153/−0.000 (trung bình +0.098, khớp offset +0.102 ước tính từ 7 dataset cũ), xếp hạng khớp dự đoán; riêng psy_insight claude KHÔNG nghiêm hơn (2j−3j = 0.000) — bias claude phụ thuộc dataset.

### 5.4. Dim C (giá trị client, valence; đầy đủ tại `_stats/dimC_B_key_table.csv`, `_stats/dimC_A_key_table.csv`)
Cấu hình B (EN lexicon): NEC từ −0.000 (psy_insight) đến 0.086 (smile); happy_ending 49.6% (psy_insight) → 88.0% (simpsydial); emo_std 0.117–0.144; lex_coverage 0.655–0.708.
Cấu hình A (native lexicon, 7 dataset non-EN): lex_coverage sụt còn 0.229–0.307; emo_std tăng gần gấp đôi (0.209–0.301); NEC đổi dấu sang âm ở 5/7 dataset; happy_ending còn 33.5–52.5%.

## 6. DỮ LIỆU THIẾU VÀ CÁCH XỬ LÝ (cập nhật lần 2)

1. **[ĐÃ GIẢI QUYẾT] Dim B claude cho Psy-Insight, PsyDial, Smile, Simpsydial**: đã bổ sung từ `D:\vy\jsonl\` (mục 4.3). Nhãn "N/A" gỡ bỏ; xếp hạng tổng Dim B nay tính trên 11 dataset × 3 judge. Cách xử lý thận trọng của bản trước (không nội suy, trình bày 2-judge tách riêng) được giữ nguyên trong hồ sơ để đối chiếu — và đã được kiểm chứng đúng (mục 5.3).
2. **Dim B pilot không có S2** (0 file) và **S1 chỉ có judge gpt** → vẫn là giới hạn: không kiểm chứng được prompt-language bias cho Dim B; chỉ so được S1↔S3 (gpt) và mượn kết luận S1/S2/S3 từ Dim A pilot (file 02).
3. **Dim A/B full thiếu record `smile_74`** (có trong Dim C) → smile n=199 (file claude mới của smile cũng 199 — nhất quán).
4. **Dim C**: psy_insight chỉ 141/200 record hợp lệ (59 NaN — hội thoại quá ngắn; client TB 77 token — nay lý giải được bằng BC-DATA: Psy-Insight là ca đa phiên tách thành phiên ngắn); cpsycoun 188 (A)/182 (B); annomi 110/112; smile 198/200.

## 7. BẤT THƯỜNG & MÂU THUẪN PHÁT HIỆN (bắt buộc lưu ý khi diễn giải)

- **BT1 — Trộn phiên bản model trong cùng một judge ở full-run.** Judge "gpt" Dim A full = gpt-5.1 (159 record) + **gpt-5.5** (1,952 record); Dim B full gpt = 100% gpt-5.5 trong khi pilot = gpt-5.1. Judge "gemini" Dim B full = gemini-3.1-pro-low (219) + **gemini-pro-agent** (1,892). Judge "claude" đồng nhất model (sonnet-4-6) nhưng qua 4 route khác nhau. Định lượng ảnh hưởng (điểm gpt trừ trung bình claude+gemini trên cùng record): gpt-5.1 +0.441 vs gpt-5.5 +0.402 (Δ≈0.04/thang 6); gemini-3.1 +0.285 vs gemini-pro-agent +0.248 so với gpt (Δ≈0.04/thang 5) → sai lệch phiên bản **nhỏ nhưng có thật**; kết luận mức dataset không bị đảo bởi yếu tố này. (`_stats/dimA_gpt_version_effect.csv`, `_stats/dimB_gemini_version_effect.csv`)
- **BT2 — Full-run tái dùng nguyên văn điểm pilot.** Với đa số dataset, record pilot-20 trong file full có điểm **giống hệt 100%** file pilot (cùng model) → 20/200 record không phải chấm lại độc lập. Ngoại lệ (chấm lại thật): psydial-gpt (10% trùng), soulchat-gpt (15%), simpsydial-gpt (5%), simpsydial-claude (20%). (`_stats/dimA_pilot_reuse_check.csv`)
- **BT3 — Test–retest của judge (từ các trường hợp chấm lại ở BT2):** simpsydial-claude (cùng model, khác route): MAE 0.15, r=0.787; psydial/soulchat/simpsydial-gpt (5.1→5.5): MAE 0.148–0.223, r=0.41–0.80. → Độ ổn định chấm lại của LLM-judge ở mức khá, không hoàn hảo; r=0.41 (simpsydial-gpt) là mức đáng lo nếu muốn dùng điểm ở cấp record đơn lẻ.
- **BT4 — Pilot dùng 4 judge (có qwen), full chỉ 3 judge** → so sánh pilot–full phải cùng tập judge.
- **BT5 — ID có lỗi chính tả hệ thống**: `cpscycoun_*` (thiếu/thừa ký tự so với "cpsycoun"), `psyinsight_*` — nhất quán giữa các dim nên join không hỏng, nhưng cần biết khi truy vết record.
- **BT6 — AnnoMI Dim B: file S1 gpt và S3 gpt trùng md5** (byte-identical). Với dataset EN, S1≡S3 về thiết kế; file được sao chép, không phải chạy 2 lần.
- **BT7 — Thang đo lexicon cấu hình A**: metadata ghi "scale=0_1" nhưng giá trị emo_mean có số âm (min −0.122) → pipeline nhiều khả năng đã quy đổi về thang có tâm 0; không xác định được chắc chắn từ nguồn dữ liệu. So sánh tuyệt đối A↔B vẫn cần thận trọng.
- **BT8 — File gpt Dim B pilot chứa 40 id** (S3 của cpsycoun/psydial/simpsydial/soulchat/kmi; S1 của kmi): gồm đúng 20 id pilot + 20 id khác (không trùng) — có vẻ ghép 2 lần chạy. Phân tích pilot Dim B chỉ dùng giao với bộ 20 id chuẩn (theo file claude/gemini S3).
- **BT9 — KokoroChat Dim B pilot, judge gpt, S3: file chỉ có 2 record**, và cả 2 **không thuộc** bộ 20 id pilot → gần như không dùng được; các phân tích pilot Dim B của kokorochat với gpt S3 bị loại.
- **BT10 — Điểm None trong Dim B full (judge claude)**: cpsycoun 24 điểm None/2 record, esconv 36/3, kokorochat 12/1 → lỗi parse cục bộ của claude; subscale các record đó tính trên item còn lại.
- **BT11 — Điểm Dim B tương quan với độ dài hội thoại** (Spearman total × tổng token, per-dataset: 0.09–0.59; pooled z 0.32): nhất quán với cơ chế anchor "evidence-based" (hội thoại ngắn thiếu bằng chứng tụ về 3) → chênh lệch Dim B giữa dataset ngắn (cpsycoun 89 token client TB; psy_insight 77) và dataset dài phải diễn giải kèm yếu tố này.
- **BT12 — Hai dataset EN trong Dim C được gắn `approach=B` ngay trong thư mục A** (annomi, cactus, esconv, psy_insight): đúng thiết kế (EN không có bản dịch/lexicon riêng), file A≡B byte-identical.
- **BT13 — smile thiếu 1 record ở pilot** (19/20) đồng bộ với thiếu `smile_74` ở full → cùng một record lỗi từ khâu chấm.
- **BT14 — Mức hội tụ giữa 2 cấu hình Dim C rất thấp ở cấp record** (Pearson A↔B của client emo_mean: 0.07–0.42 tùy dataset) trong khi bảng xếp hạng dataset thay đổi mạnh → lựa chọn lexicon là quyết định phương pháp luận trọng yếu, phân tích chi tiết ở file 03.
- **BT15 — [ĐÃ ĐÓNG] Folder theory lệch mô tả**: xác nhận PDF cũ là nhầm nguồn; lý thuyết thay bằng 3 file Word (BC-DATA/BC-EVAL/BC-3D). Các mô tả gián tiếp bản trước phần lớn khớp bản chính thức, TRỪ: AnnoMI (real → **semi-real**, video trình diễn), Psy-Insight (không rõ → **real-xuất bản, đa phiên, EN+ZH**), và taxonomy 3 nhóm cũ → 4 nhóm chính thức.
- **BT16 — Bất đồng đặt tên trong Dim C**: file bên trong thư mục `dim_c_*_full_0629/` được đặt tên `*_dimC_pilot*.csv` ("pilot" nhưng n=200, là full-run duy nhất của Dim C). Không ảnh hưởng nội dung.
- **BT17 — 4 file Dim B mới cũng trộn route claude** (ag/cc/lkp-kr — cùng họ sonnet-4-6/4.6): psy_insight 97cc+103ag; psydial 108ag+92cc; simpsydial 21ag+179cc; smile 57ag+136cc+**6 lkp/kr/claude-sonnet-4.6**. Nhất quán BT1; ảnh hưởng phiên bản đã định lượng là nhỏ (~0.04).
- **BT18 — Điểm None trong 4 file mới (claude)**: smile 72 điểm None/6 record; psy_insight 12/1; simpsydial 12/1; psydial 0 — cùng dạng lỗi parse cục bộ như BT10; subscale tính trên item còn lại.
- **BT19 — Lệch quy mô lý thuyết ↔ thí nghiệm**: BC-DATA ghi AnnoMI gốc **133** hội thoại (thí nghiệm dùng 112); Psy-Insight gốc **951 phiên/189 ca song ngữ EN+ZH, đa phiên** trong khi pipeline thí nghiệm xử lý như 200 phiên đơn tiếng Anh độc lập (dim C gắn `language=en`) → điểm Dim B/C của psy_insight phải diễn giải theo đơn vị "phiên tách rời khỏi ca" (mất ngữ cảnh xuyên phiên); không rõ 200 record lấy từ phần EN hay cả phần ZH đã dịch — **không xác định được từ nguồn dữ liệu**.
- **BT20 — Mâu thuẫn nhỏ giữa 2 nguồn lý thuyết về CPsyCoun/SMILE**: BC-DATA Bảng 2.1 ghi CPsyCoun 3,134 hội thoại/8.7 lượt; bảng so sánh nội bộ PsyDial (được BC-DATA trích ở mục khác) ghi CPsyCounD 3,084/8.1 — chênh lệch phiên bản thống kê giữa các bài gốc; nêu nguyên trạng, không tự hòa giải.

**GHI CHÚ CẬP NHẬT (lần 1, sau Bước 3):** bổ sung `_stats/crossdim_dataset_table_with_groups.csv` với nhãn nhóm TẠM (real/human-roleplay/llm-rewrite/simulator) và tương quan hạng n=7/11. **[LẦN 2 — THAY THẾ]**: nhãn nhóm tạm được thay bằng taxonomy chính thức BC-DATA (mục 4.6); toàn bộ bảng nhóm/tương quan/hồi quy tính lại với Dim B đủ 11 dataset, lưu tại: `_agg_group_means_official.csv`, `_agg_provenance_regression_official.csv`, `_agg_counselor_words_dichotomy.csv`, `_agg_crossdim_dataset_means_11ds.csv`, `_agg_crossdim_dataset_rankcorr.csv` (A↔B ρ=0.182 p=0.593; **B↔happy ρ=0.724 p=0.012**; **B↔NEC ρ=0.655 p=0.029**; A↔happy ρ=−0.369 p=0.264 — n=11), `_agg_crossdim_MTMM_pooled.csv` (A↔B record-level 0.375), `_agg_dimB_official_11ds.csv`, `_agg_dimB_item_means_11ds.csv`, `_agg_dimB_judge_agreement_11ds.csv`, `_agg_dimA_metric_intercorr.csv`, `_agg_dimB_subscale_intercorr.csv`, `_agg_dimB_item_intercorr.csv`, `_agg_discriminative_power.csv`, `_agg_rank_stability.csv`, `_agg_verbosity_bias.csv`, `_agg_dimension_disagreement_cases.csv`, `_agg_dimB_newfiles_report.csv`. Số liệu 7-dataset cũ giữ nguyên trong `_stats/` làm hồ sơ đối chiếu.

## 8. NGUỒN MINH CHỨNG (cập nhật lần 2)
- **Lý thuyết (duy nhất có thẩm quyền)**: `D:\vy\Tong_hop_11_dataset_tham_van_tri_lieu_multi_turn.docx` (BC-DATA — taxonomy provenance §1.3, Bảng 2.1), `D:\vy\Tong_hop_5_bai_evaluation_3_goc_nhin.docx` (BC-EVAL — metric/thang/chiều 3 dim: Bảng 2.1, mục 3.1–3.5, Phần 4), `D:\vy\Phan_tich_3_chieu_danh_gia_va_thiet_ke_dataset.docx` (BC-3D — điều kiện A/B/C, 5 giới hạn §2.5, 5 nguyên tắc §3.1, kiến trúc 5 tầng §3.2, 4 công cụ Việt hóa Bảng 3.2). Bản trích text: `_notes/Tong_hop_*.txt`, `_notes/Phan_tich_*.txt`; tóm tắt: `_notes/theory_word_11dataset_tomtat.md`. Trích xuất PDF cũ (`_notes/paper_*.md`, `_notes/theory_notes.md`) chỉ còn giá trị lịch sử — khi mâu thuẫn, 3 file Word thắng.
- Dữ liệu: `.jsonl` trong `experiments/dim_a_mind_eval/{20,full}`, `experiments/dim_b_wai/{20,full}`, **`D:\vy\jsonl\` (4 file Dim B claude bổ sung)**; `.csv` trong `experiments/dim_c/dim_c_{A,B}_full_0629/`.
- Script: lần 1 — `_notes/explore_schema.py`, `aggregate_stats.py`, `dimc_crossdim.py`, `extra_stats.py` (kết quả trong `_stats/`); lần 2 — `_notes/step0_dimB_moi.py` + 2 lệnh bổ trợ (kết quả trong `_agg_*.csv` tại `ket_qua_phan_tich/`).
- Mọi con số tái lập được bằng cách chạy lại các script trên; số liệu lần 1 được tái dùng nguyên trạng, không trích lại từ raw.
