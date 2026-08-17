# BƯỚC 5 — GIA CỐ THỐNG KÊ: SUY DIỄN VỮNG CHO CÁC KẾT LUẬN CỦA BƯỚC 00–04

## VỊ TRÍ TÀI LIỆU VÀ PHẠM VI

Tài liệu này bổ sung **suy diễn thống kê đúng cấp phân tích** cho các kết luận đã chốt ở file 00–04, nhằm đạt chuẩn phản biện tạp chí Q1. Nguyên tắc: **không sinh dữ liệu mới, không chấm lại** — chỉ tái phân tích trên đúng 2.111 dialogue × 3 judge (Dim A/B) và 2.031 record hợp lệ (Dim C, cấu hình B) đã kiểm kê ở file 00. Bốn gia cố:

1. **A1 — Hồi quy provenance với suy diễn vững**: vá lỗi pseudo-replication mà file 01 §5.2, 02 §5.1, 04 §2.1 đã tự khai (OLS mức record coi 2.111 quan sát là độc lập trong khi provenance là thuộc tính của 11 dataset).
2. **A2 — Jackknife + bootstrap cho tương quan cấp dataset (n=11)**: kiểm độ bền của các tương quan ở file 04 §1.1 trước ảnh hưởng của từng dataset đơn lẻ.
3. **A3 — Mann–Whitney U + effect size cho lưỡng phân "ai viết lời counselor" (Dim C)**: đúng nghi thức so phân bố của [E7] mà BC-3D Bảng 2.3 yêu cầu, chạy ở CẢ HAI cấp (record và dataset).
4. **A4 — Bootstrap CI 95% cho mean cấp dataset**: định lượng độ bất định của mọi bảng xếp hạng.

Mọi con số sinh bởi 2 script mới: `_notes/gc1_build_records.py` (dựng bảng master độc lập từ dữ liệu thô — không tái dùng bảng trung gian cũ) và `_notes/gc2_robust_analysis.py` (4 phân tích + 16 assert đối chiếu). Seed cố định 20260813. Kết quả: `_gc_*.csv`; nhật ký assert: `_gc_assert_report.txt`.

## 0. KIỂM CHỨNG NỀN: TÁI LẬP ĐỘC LẬP TRƯỚC KHI GIA CỐ

Bảng master (`_gc_records_master.csv`, 2.111 dòng) được dựng lại **trực tiếp từ jsonl/csv thô** (parse mới toàn bộ, không dùng `_stats/crossdim_records*.csv`). Đối chiếu tự động 16 mục — **16/16 PASS**, gồm: n=2.111; 11/11 mean Dim A khớp bảng 00 §5.1 và 11/11 mean Dim B khớp 00 §5.3 (sai số ≤0.0015); bảng lưỡng phân human/llm khớp `_agg_counselor_words_dichotomy.csv`; hệ số OLS và R² tái lập khớp `_agg_provenance_regression_official.csv` (sai số ≤0.005; log = logarit tự nhiên); 6/6 hệ số Spearman khớp `_agg_crossdim_dataset_rankcorr.csv`. → Số liệu của bộ 00–04 **tái lập được từ nguồn bởi mã độc lập**; các gia cố dưới đây đứng trên nền đã kiểm chứng đó.

## 1. A1 — HỒI QUY PROVENANCE: BA MỨC SUY DIỄN CHO CÙNG MỘT HỆ SỐ

**Phương pháp.** Mô hình giữ nguyên như file 04 §2.1: `score ~ ln(total_tokens) + provenance` (ref = real, n=2.111). Ba mức suy diễn: (i) SE thường (như bản cũ — chỉ để đối chiếu, đã biết là lạc quan); (ii) **SE cluster-robust CR1** theo dataset (G=11; kiểm định t với df=G−1=10 theo khuyến nghị cho số cluster nhỏ); (iii) **exact permutation test cấp dataset**: liệt kê **toàn bộ 92.400 cách** gán nhãn 4 nhóm provenance (kích thước 3/2/3/3) cho 11 dataset, refit mỗi lần, p hai phía = tỷ lệ |hệ số hoán vị| ≥ |hệ số quan sát|; kèm kiểm định F cho cả khối provenance (df=3). Với thuộc tính thuần cấp dataset như provenance, permutation exact là chuẩn tham chiếu nghiêm ngặt nhất.

**Kết quả** (`_gc_provenance_regression_robust.csv`):

| y | Hệ số | b | SE thường | p thường | SE cluster | p cluster (df=10) | p permutation (exact) |
|---|---|---|---|---|---|---|---|
| Dim A | semi-real vs real | +0.219 | 0.051 | 1.9e-05 | 0.545 | 0.697 | 0.709 |
| Dim A | semi-synthetic vs real | −0.427 | 0.039 | 1.7e-27 | 0.396 | 0.306 | 0.414 |
| Dim A | fully-synthetic vs real | +0.387 | 0.039 | 2.7e-22 | 0.441 | 0.402 | 0.463 |
| Dim A | ln_tokens | −0.019 | 0.019 | 0.299 | 0.121 | 0.876 | — |
| Dim A | KHỐI provenance (F, df=3) | F=148.4 | — | 3.0e-87 | — | — | **0.443** |
| Dim B | semi-real vs real | −0.186 | 0.032 | 1.0e-08 | 0.111 | 0.126 | 0.366 |
| Dim B | semi-synthetic vs real | −0.039 | 0.024 | 0.114 | 0.128 | 0.768 | 0.836 |
| Dim B | fully-synthetic vs real | +0.237 | 0.025 | 5.1e-21 | 0.083 | **0.017** | 0.179 |
| Dim B | ln_tokens | **+0.303** | 0.012 | 5.1e-126 | 0.039 | **<0.001** | — |
| Dim B | KHỐI provenance (F, df=3) | F=79.8 | — | 6.9e-49 | — | — | **0.124** |

**Ba kết luận đo lường:**

1. **Hiệu ứng độ dài của Dim B là phát hiện vững nhất toàn bộ hồi quy**: b=+0.303 giữ p<0.001 ngay cả với SE cluster-robust — vì đây là quan hệ BÊN TRONG dataset (within), không bị pseudo-replication chạm tới. Kết luận "cơ chế anchor-bằng-chứng thưởng độ dài" (file 02 §5.1, BT11) được **nâng cấp thành phát hiện có suy diễn vững**, đủ chuẩn làm claim chính của bài báo.
2. **"Phần thưởng provenance" chuyển từ suy diễn xuống mô tả**: khi kiểm định đúng cấp dataset, cả khối provenance KHÔNG đạt ngưỡng ý nghĩa thông thường (p permutation: Dim A 0.443; Dim B 0.124; từng hệ số 0.18–0.84). Riêng fully-synthetic ở Dim B có p cluster = 0.017 nhưng p permutation = 0.179 — hai phương pháp bất đồng; với G=11 cluster nhỏ, kiểm định cluster-t được biết là lạc quan, nên **lấy permutation làm chuẩn báo cáo**. Cách viết đúng cho bài báo: hiệu ứng +0.39/+0.24 là **effect size mô tả với hướng nhất quán** (và nhất quán nội-ngôn-ngữ ZH, file 04 §2.3), nhưng với 11 dataset chia 4 nhóm thì **không đủ sức mạnh thống kê để loại trừ may rủi cấp dataset** — cần nhiều dataset hơn, không phải nhiều record hơn.
3. Dim A tiếp tục **miễn nhiễm độ dài** ở mọi mức suy diễn (b=−0.019, p≥0.30 cả ba mức) — giữ nguyên kết luận file 01 §5.4.

Lưu ý diễn giải: "không đạt ý nghĩa" ≠ "không có hiệu ứng" — đây là giới hạn sức mạnh (power) cố hữu của thiết kế 11 dataset, cần nêu nguyên trạng thay vì im lặng.

## 2. A2 — TƯƠNG QUAN CẤP DATASET (n=11): JACKKNIFE + BOOTSTRAP

**Phương pháp.** Với 6 cặp tương quan Spearman của file 04 §1.1 (`_agg_crossdim_dataset_rankcorr.csv`): (i) jackknife bỏ-từng-dataset (11 lần) — báo khoảng [min, max] và dataset gây dao động mạnh nhất; (ii) bootstrap cấp dataset (lấy mẫu lại 11 dataset có hoàn lại, B=10.000, seed 20260813) — CI 95% percentile và tỷ lệ mẫu bootstrap cùng dấu.

**Kết quả** (`_gc_rankcorr_jackknife_bootstrap.csv`):

| Cặp | ρ (p) | Jackknife [min, max] | Nhạy nhất khi bỏ | Bootstrap CI 95% | % cùng dấu | Phán quyết |
|---|---|---|---|---|---|---|
| B ↔ happy | +0.724 (0.012) | [+0.632, +0.888] | cactus (→ +0.888) | [+0.089, +0.991] | 98.3% | **BỀN** — dấu không đổi ở mọi jackknife, CI không chứa 0 |
| B ↔ NEC | +0.655 (0.029) | [+0.539, +0.758] | annomi (→ +0.539) | [−0.009, +0.944] | 97.4% | **RANH GIỚI** — jackknife luôn dương nhưng CI chạm 0 |
| B ↔ tokens | +0.573 (0.066) | [+0.455, +0.685] | psy_insight (→ +0.455) | [−0.005, +0.891] | 97.4% | Ranh giới (đã có bằng chứng within mạnh hơn ở A1) |
| A ↔ B | +0.182 (0.593) | [−0.006, +0.455] | annomi (→ +0.455) | [−0.523, +0.815] | 68.3% | Không kết luận được tương quan — nhất quán "gần trực giao" |
| A ↔ NEC | −0.409 (0.212) | [−0.636, −0.285] | cpsycoun (→ −0.636) | [−0.857, +0.249] | 89.6% | CI chứa 0 — không kết luận |
| A ↔ happy | −0.369 (0.264) | [−0.596, −0.219] | cpsycoun (→ −0.596) | [−0.867, +0.351] | 85.0% | CI chứa 0 — không kết luận |

**Kết luận:** (1) Phát hiện chính của file 04 — **hội tụ B↔happy ở cấp dataset** — sống sót qua cả jackknife lẫn bootstrap: không dataset đơn lẻ nào tạo ra nó, và CI 95% không chứa 0 (dù rộng, đúng bản chất n=11). (2) **B↔NEC hạ một bậc** thành "nhất quán dương, ranh giới ý nghĩa" — khi viết bài nên gộp về một claim "liên minh cao đi cùng kết phiên lạc quan" lấy happy làm chỉ số chính, NEC làm phụ. (3) Các cặp với Dim A đều có CI chứa 0 → khẳng định thận trọng đúng như file 04: không đủ bằng chứng cho tương quan, tức **tính trực giao A↔B, A↔C không bị bác bỏ** (lưu ý logic: đây là "không bác bỏ được trực giao", không phải "chứng minh trực giao" — n=11 không đủ sức mạnh cho khẳng định mạnh hơn).

## 3. A3 — DIM C, HUMAN-VIẾT vs LLM-VIẾT: SO PHÂN BỐ HAI CẤP

**Phương pháp.** Lưỡng phân "ai viết lời counselor" (5 dataset human: esconv, kokorochat, psy_insight, annomi, psydial; 6 dataset LLM: smile, soulchat, cpsycoun, cactus, simpsydial, kmi). Cấp record (nghi thức [E7]): Mann–Whitney U hai phía, effect size r=|Z|/√N (hiệu chỉnh ties) và rank-biserial (≡ Cliff's delta; âm = LLM cao hơn). Cấp dataset (chống pseudo-replication): Mann–Whitney exact trên 11 giá trị mean (5 vs 6), Cliff's delta, và exact permutation toàn bộ C(11,5)=462 cách chia nhóm cho hiệu trung bình.

**Kết quả** (`_gc_dimC_group_tests.csv`; cấu hình B, giá trị = mean human / mean LLM):

| Chỉ số | human | LLM | Record-level: p; r; rank-biserial | Dataset-level: p MW exact; Cliff; p perm (462) |
|---|---|---|---|---|
| **Tông counselor (valence mean)** | 0.164 | 0.185 | **7.3e-36; r=0.275; −0.322** | **0.0087; −0.933; 0.0043** |
| NEC client | 0.047 | 0.066 | 3.9e-05; r=0.091; −0.107 | 0.247; −0.467; 0.236 |
| emo_std client | 0.135 | 0.137 | 0.33; r=0.022; −0.025 | 0.79; −0.133; 0.55 |
| Variability ratio | 1.131 | 1.138 | 0.098; r=0.037; −0.043 | 0.66; −0.200; 0.97 |
| Happy ending | 72.0% | 75.2% | 0.12; r=0.035; −0.031 | 0.79; −0.167; 0.50 |

**Kết luận:** Bộ "vân tay LLM" của file 03 §5.1/04 §2.2 được **phân tầng lại theo độ vững**:

1. **Tông counselor là vân tay vững duy nhất ở cả hai cấp**: LLM-viết cao hơn human-viết với Cliff's delta cấp dataset = −0.933 — tức trong 30 cặp (dataset human × dataset LLM) chỉ 1 cặp có human cao hơn; p exact 0.0087, p permutation 0.0043 — **sống sót kiểm định nghiêm ngặt nhất dù chỉ có 11 dataset**. Đây là bản tái lập độc lập, đa ngôn ngữ, và giờ có suy diễn đúng cấp, của phát hiện "elevated tone" trong [E7]. Đủ chuẩn làm claim chính.
2. **NEC hạ cấp thành mô tả**: khác biệt rõ ở record-level (p=3.9e-05) nhưng effect size nhỏ (r=0.091) và KHÔNG giữ được ở cấp dataset (p≈0.24) — gradient NEC giữa hai nhóm có thể do vài dataset chi phối.
3. emo_std, variability ratio, happy ending: không khác biệt có ý nghĩa ở cả hai cấp trong so sánh chéo-dataset này — nhất quán với ghi nhận của file 03 §5.3 rằng tín hiệu biến thiên của [E7] chỉ hiện khi so **cùng kênh, khớp chủ đề** (thiết kế mà nghiên cứu này không có, do thiếu mốc thật cùng kênh — đúng điều kiện BC-3D).

## 4. A4 — BOOTSTRAP CI 95% CHO MEAN CẤP DATASET

**Phương pháp.** Lấy mẫu lại record trong từng dataset (B=10.000), CI percentile cho mean của Dim A, Dim B, NEC, tông counselor, happy (`_gc_dataset_means_bootstrapCI.csv` — bảng đầy đủ; dưới đây trích 3 cột chính).

| Dataset | Dim A [CI 95%] | Dim B [CI 95%] | Happy [CI 95%] |
|---|---|---|---|
| annomi | 3.621 [3.420, 3.818] | 3.760 [3.582, 3.926] | 0.645 [0.554, 0.736] |
| cactus | 3.376 [3.339, 3.413] | 4.290 [4.244, 4.336] | 0.725 [0.665, 0.785] |
| psy_insight | 3.364 [3.240, 3.486] | 3.605 [3.525, 3.684] | 0.496 [0.411, 0.582] |
| simpsydial | 3.188 [3.137, 3.237] | 4.335 [4.311, 4.361] | 0.880 [0.835, 0.925] |
| kokorochat | 2.917 [2.849, 2.988] | 4.046 [3.971, 4.118] | 0.745 [0.685, 0.805] |
| kmi | 2.653 [2.616, 2.688] | 4.088 [4.060, 4.115] | 0.745 [0.685, 0.805] |
| psydial | 2.481 [2.428, 2.536] | 4.182 [4.142, 4.218] | 0.840 [0.790, 0.890] |
| smile | 2.321 [2.261, 2.380] | 4.166 [4.113, 4.216] | 0.792 [0.731, 0.848] |
| cpsycoun | 2.285 [2.228, 2.342] | 3.418 [3.370, 3.466] | 0.593 [0.522, 0.665] |
| soulchat | 2.191 [2.144, 2.237] | 3.992 [3.950, 4.032] | 0.760 [0.700, 0.820] |
| esconv | 1.798 [1.750, 1.848] | 4.007 [3.935, 4.076] | 0.775 [0.720, 0.830] |

**Kết luận:** (1) Ở Dim A, CI của **top-3 (annomi, cactus, psy_insight) chồng lấn nhau** — không được viết "annomi đứng đầu" như khẳng định điểm; ngược lại **esconv tách đáy tuyệt đối** (CI [1.750, 1.848] không chạm dataset nào khác). (2) Ở Dim B, simpsydial–cactus chồng nhẹ ở đỉnh; cpsycoun tách đáy rõ. (3) Các CI này định lượng chính xác khuyến nghị "đọc hạng theo cụm" của file 02 §6.0-4 — nay có ngưỡng số để vẽ cụm (các CI không chồng lấn = khác cụm).

## 5. HỆ QUẢ CHO BÀI BÁO Q1 — BẢNG PHÂN TẦNG CLAIM THEO ĐỘ VỮNG

| Tầng | Claim | Bằng chứng sau gia cố | Cách viết khuyến nghị |
|---|---|---|---|
| **Tầng 1 — suy diễn vững, làm claim chính** | Cơ chế anchor của WAI thưởng độ dài hội thoại | b=+0.303, p<0.001 với cluster-robust SE (within-dataset) | Khẳng định trực tiếp, kèm hệ quả phương pháp (báo residual độ dài) |
| Tầng 1 | Tông cảm xúc counselor: LLM-viết > human-viết | Cả hai cấp: record r=0.275, p=7e-36; dataset Cliff=−0.933, p_perm=0.0043 | Khẳng định trực tiếp — "vân tay LLM" bản kiểm định đúng cấp |
| Tầng 1 | Liên minh (B) đồng biến "kết phiên lạc quan" (happy) giữa dataset | ρ=0.724; jackknife luôn dương; bootstrap CI [0.089, 0.991] | Khẳng định kèm CI; diễn giải "cụm kịch bản hóa" giữ nguyên |
| **Tầng 2 — mô tả có hướng nhất quán, không đủ power cấp dataset** | Phần thưởng fully-synthetic (+0.39 Dim A; +0.24 Dim B sau khử độ dài) | p permutation 0.18–0.46; nhất quán nội-ZH | Trình bày như effect size mô tả + "not statistically separable at the dataset level (exact permutation)"; tránh chữ significant |
| Tầng 2 | NEC: LLM-viết > human-viết | Chỉ record-level (r=0.091 nhỏ); dataset-level p≈0.24 | Gradient mô tả, đặt sau claim tông counselor |
| Tầng 2 | B↔NEC cấp dataset (ρ=0.655) | Jackknife luôn dương; CI chạm 0 | Gộp vào claim B↔happy làm chỉ số phụ |
| **Tầng 3 — không kết luận** | A↔B, A↔C tương quan cấp dataset | CI đều chứa 0 | Viết đúng logic: "không bác bỏ được tính trực giao"; nhấn record-level MTMM (n≈2.111) làm bằng chứng chính cho trực giao |
| Tầng 3 | emo_std/var_ratio/happy khác nhau giữa human/LLM (chéo dataset) | Không ý nghĩa cả hai cấp | Nêu như giới hạn của so sánh chéo-dataset không khớp kênh/chủ đề — dẫn lại điều kiện mốc-thật của BC-3D |

Hai câu phương pháp nên đưa vào bài (phần Statistical analysis): (i) "Vì provenance là thuộc tính cấp dataset, mọi so sánh nhóm được kiểm định bằng exact permutation trên toàn bộ 92.400 (hoặc 462) cách gán nhãn ở cấp dataset, bên cạnh SE cluster-robust CR1 (df=G−1); suy diễn record-level chỉ dùng cho hiệu ứng within-dataset (độ dài)." (ii) "Mọi tương quan cấp dataset (n=11) được báo cáo kèm jackknife bỏ-từng-dataset và bootstrap CI 95% (B=10.000)."

## 6. GIỚI HẠN CỦA CHÍNH BƯỚC GIA CỐ

1. n=11 dataset là trần sức mạnh tuyệt đối cho mọi suy diễn cấp dataset; "không ý nghĩa" ở Tầng 2 là thiếu power, không phải bằng chứng vô hiệu.
2. Cluster-robust với G=11 nhỏ có thể lạc quan — đã dùng t(df=10) và đặt permutation làm chuẩn; hai phương pháp bất đồng ở đúng một ô (fully-syn Dim B) và đã xử lý bằng cách lấy kết quả bảo thủ hơn.
3. Confound provenance × ngôn ngữ (file 04 §2.3) không giải quyết được bằng thống kê trên dữ liệu này — giữ nguyên như giới hạn thiết kế.
4. Bootstrap/jackknife không thay được neo chuyên gia người (điều kiện vận hành 2 của BC-3D) — vẫn là việc bắt buộc khi áp khung sang tiếng Việt.

## NGUỒN MINH CHỨNG

- Script: `_notes/gc1_build_records.py` (dựng `_gc_records_master.csv` từ `experiments/dim_a_mind_eval/full/`, `experiments/dim_b_wai/full/` + 4 file claude tại `vy/jsonl/`, `experiments/dim_c/dim_c_B_full_0629/all_dimC_pilot_n200.csv`); `_notes/gc2_robust_analysis.py` (4 phân tích + 16 assert; seed 20260813; tự cài đặt OLS/CR1 bằng numpy—scipy, không phụ thuộc statsmodels).
- Kết quả: `_gc_provenance_regression_robust.csv`, `_gc_rankcorr_jackknife_bootstrap.csv`, `_gc_dimC_group_tests.csv`, `_gc_dataset_means_bootstrapCI.csv`, `_gc_assert_report.txt` (16/16 PASS).
- Đối chiếu số cũ: `_agg_provenance_regression_official.csv`, `_agg_crossdim_dataset_rankcorr.csv`, `_agg_counselor_words_dichotomy.csv`, bảng 00 §5.1/§5.3.
- Lý thuyết: BC-3D §2.5 (giới hạn 1–2: đọc tương đối; nghi ngờ "syn>real"), §2.6 (4 điều kiện vận hành), Bảng 2.3 (nghi thức Mann–Whitney + effect size của chiều cảm xúc); BC-EVAL 3.5 ([E7]).
