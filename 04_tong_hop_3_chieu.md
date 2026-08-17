# BƯỚC 4 — TỔNG HỢP 3 CHIỀU (BẢN ĐẦY ĐỦ 11×3) VÀ ĐỊNH HƯỚNG DATASET THAM VẤN TRỊ LIỆU TIẾNG VIỆT

## THAY ĐỔI SO VỚI BẢN TRƯỚC
(1) Toàn bộ tổng hợp tính lại với **Dim B đầy đủ 11 dataset** — các tương quan chéo đổi trạng thái (B↔happy từ "không ý nghĩa" thành ρ=0.724, p=0.012). (2) Phân tích nhóm chuyển sang **taxonomy provenance 4 nhóm chính thức của BC-DATA** (real / semi-real / semi-synthetic / fully synthetic) — đảo một phần kết luận nhóm của bản trước (nhóm "real" cũ chỉ có annomi nay là semi-real). (3) Khung lý thuyết nền đổi sang BC-3D: kiểm chứng thực nghiệm Điều kiện A/B/C, đối chiếu 5 giới hạn, 5 nguyên tắc, và bám **kiến trúc 5 tầng + 4 công cụ Việt hóa**. (4) Lồng 12 góc phân tích Q1 bổ sung (mỗi góc: có số liệu → kết quả; thiếu → "không đủ bằng chứng"). Chỉ dùng kết luận từ file 00–03 và các bảng `_agg_*.csv` đã chốt ở Bước 0; không tạo số liệu mới.

---

## 1. INSIGHT XUYÊN DIM VÀ KIỂM CHỨNG HỘI TỤ–TRỰC GIAO (convergent–discriminant, góc Q1 #1)

### 1.1. Ma trận MTMM thực nghiệm — Điều kiện B của BC-3D được kiểm chứng trên 11 dataset
BC-3D §2.3 khẳng định tính trực giao của 3 chiều bằng 3 "ca án" đơn lẻ (CACTUS, MindEval, SimPsyDial). Nghiên cứu này cung cấp **kiểm chứng hệ thống đầu tiên trên 11 dataset chung một khung**, ở hai cấp (nguồn: `_agg_crossdim_MTMM_pooled.csv`, `_agg_crossdim_dataset_rankcorr.csv`):

| Cặp chiều | Record-level (pooled-z nội dataset, n≈2,111) | Dataset-level (Spearman, n=11) |
|---|---|---|
| A (kỹ năng) ↔ B (liên minh) | 0.375 | 0.182 (p=0.593) |
| A ↔ C (NEC) | −0.031 | −0.409 (p=0.212) |
| B ↔ C (NEC / happy) | 0.172 | **0.655 (p=0.029) / 0.724 (p=0.012)** |

Ba kết luận đo lường: (i) **A↔C trực giao hoàn toàn** ở cả hai cấp — "counselor được chấm giỏi" không đồng nghĩa "client khá lên về cảm xúc" (trả lời trực tiếp góc Q1 #9, xem 1.3); (ii) **A↔B chỉ chồng lấn vừa phải ở mức record và gần trực giao ở mức dataset** — hai chiều xứng đáng tồn tại riêng; (iii) **B↔C hội tụ CÓ CHỌN LỌC**: yếu trong nội bộ dataset (0.17) nhưng mạnh giữa dataset (0.65–0.72) → phần hội tụ nằm ở *phong cách sinh dữ liệu* (kịch bản hòa hợp + kết vui), không nằm ở *quan hệ nhân quả trong từng phiên*. Đây là dạng bằng chứng mà từng "ca án" đơn lẻ của BC-3D không cho được: trực giao là bất biến cấp phiên, còn "đồng phạm kịch bản hóa" là hiện tượng cấp dataset.

### 1.2. Bảng chân dung hợp nhất 11 dataset (nguồn: `_agg_crossdim_dataset_means_11ds.csv`, nhóm theo BC-DATA)
| Dataset (nhóm) | Dim A (1–6) | SD A | Dim B 3j (1–5) | NEC | Happy% | Tông counselor |
|---|---|---|---|---|---|---|
| annomi (semi-real) | **3.62** | **1.08** | 3.76 | 0.027 | 64.6 | **0.138** |
| cactus (fully-syn) | 3.38 | 0.27 | 4.29 | 0.049 | 72.5 | 0.179 |
| psy_insight (real) | 3.36 | 0.89 | 3.61 | −0.000 | **49.6** | 0.142 |
| simpsydial (fully-syn) | 3.19 | 0.36 | **4.34** | 0.085 | **88.0** | **0.198** |
| kokorochat (real) | 2.92 | 0.50 | 4.05 | 0.048 | 74.5 | 0.173 |
| kmi (fully-syn) | 2.65 | 0.27 | 4.09 | 0.076 | 74.5 | 0.182 |
| psydial (semi-real) | 2.48 | 0.39 | 4.18 | 0.056 | 84.0 | 0.174 |
| smile (semi-syn) | 2.32 | 0.42 | 4.17 | 0.086 | 79.3 | 0.182 |
| cpsycoun (semi-syn) | 2.29 | 0.41 | **3.42** | 0.017 | 59.3 | 0.174 |
| soulchat (semi-syn) | 2.19 | 0.33 | 3.99 | 0.076 | 76.0 | 0.194 |
| esconv (real) | **1.80** | 0.36 | 4.01 | 0.082 | 77.5 | 0.175 |

### 1.3. Case study "chiều bất đồng" (góc Q1 #7) và liên kết với kết cục (góc Q1 #9)
Record cụ thể (nguồn: `_agg_dimension_disagreement_cases.csv`; z-score nội dataset):
- **"Trôi chảy mà không chuyển hóa"** (A cao, C thấp): `cactus_121` (A=4.100, NEC=−0.081), `kmi_712` (A=3.267, NEC=−0.268), `psydial_196` (A=3.433, NEC=−0.072) — counselor đúng giao thức nhưng valence client đi xuống. Nhóm này là minh chứng vi mô cho A↔C ≈ 0: **khung chấm counselor hiện hành không chứa thông tin về chuyển biến cảm xúc của client** — câu hỏi biên giới "counselor điểm cao có làm client tốt lên?" nhận câu trả lời thực nghiệm: *không đo được bằng Dim A/B hiện tại, phải đo trực tiếp bằng chiều C* (và xa hơn: outcome thật, BC-3D §3.5).
- **"Được lòng mà non nghề"** (B cao, A thấp): `simpsydial_463` (B=4.769, A=2.750), `cactus_19` (B=4.870, A=2.867) — liên minh "diễn" được điểm gần trần trong khi kỹ năng dưới baseline. `cactus_19` đồng thời có NEC +0.239 → một record "đẹp toàn diện trừ kỹ năng" — đúng chân dung rủi ro over-reassurance của MindEval/BC-EVAL.
- **"Vụng mà chữa lành"** (A thấp, C cao): `soulchat_157820` (A=1.800, NEC=+0.511), `esconv_43` (A=1.333, NEC=+0.359) — hỗ trợ cảm xúc "tay ngang" vẫn tạo cải thiện valence; nhắc rằng thang lâm sàng không phải thước đo duy nhất của "có ích".

## 2. KHÁC BIỆT HỆ THỐNG THEO PROVENANCE (real / semi-real / semi-synthetic / fully synthetic)

### 2.1. Bảng nhóm chính thức (nguồn: `_agg_group_means_official.csv`; diễn giải bằng lý thuyết provenance BC-DATA §1.3, §4.2–4.3)
| Nhóm (BC-DATA) | Dim A | SD(A) nội bộ | Dim B | NEC | Happy% | Tông counselor |
|---|---|---|---|---|---|---|
| real (esconv, kokorochat, psy_insight) | 2.69 | 0.58 | 3.89 | 0.048 | 69.1 | 0.165 |
| semi-real (annomi, psydial) | 2.89 | 0.74 | 4.03 | 0.046 | 77.1 | 0.161 |
| semi-synthetic (smile, soulchat, cpsycoun) | **2.27** | 0.39 | 3.86 | 0.061 | 71.9 | 0.183 |
| fully-synthetic (cactus, simpsydial, kmi) | **3.07** | **0.30** | **4.24** | **0.070** | **78.3** | **0.187** |

Hồi quy kiểm soát log-độ-dài (record-level; `_agg_provenance_regression_official.csv`; cảnh báo pseudo-replication): so với real — Dim A: fully-syn **+0.387**, semi-real +0.218, semi-syn **−0.427** (độ dài không tác động: b=−0.019); Dim B: fully-syn **+0.237**, semi-syn −0.038, semi-real −0.186 (độ dài tác động mạnh: b=+0.305). → Định lượng "phần thưởng dữ liệu tổng hợp" (góc Q1 #2): sau khi khử độ dài, dữ liệu fully-synthetic vẫn được thưởng +0.24 (liên minh) và +0.39 (kỹ năng) so với real. Thiết kế hiện tại **không tách được** "chất lượng giao thức thật" khỏi "judge LLM ưa văn phong LLM" — BC-3D §2.5 (giới hạn 2) yêu cầu nghi ngờ mặc định; dấu hiệu self-preference nhẹ đã ghi nhận (gpt chấm simpsydial/cactus cao hơn claude 0.29–0.38; file 01 §5.5).

### 2.2. Hai định luật thực nghiệm về provenance
1. **"Hạt giống quyết định trần"** (giải thích bằng BC-DATA): semi-synthetic viết lại từ QA đại chúng → trần kỹ năng thấp bất kể kỹ thuật viết lại (−0.43 so real); fully-synthetic nhại giao thức chuyên gia (planning CBT, MI forecaster, Hill 3 giai đoạn) → điểm kỹ năng cao. Khớp làn sóng 4 của BC-DATA §4.1 và nguyên tắc 2–3 của BC-3D §3.1 (chuyên môn trong pipeline; lý thuyết nhúng đo được: planning CBT nâng Strategy 4.62 vs 4.07; KMI R:Q=1.8:1 chuẩn MITI).
2. **"LLM quyết định vân tay"** (lưỡng phân "ai viết lời counselor", `_agg_counselor_words_dichotomy.csv`): nhóm LLM-viết vs người-viết — tông counselor 0.185/0.164, NEC 0.066/0.047, happy 75.2%/72.0%, nén phân phối SD(A) 0.30–0.39/0.58–0.74. Vân tay cảm xúc + độ nén đi theo **bàn tay LLM trên văn bản**, độc lập với việc hạt giống thật hay không. Tái lập độc lập phát hiện [E7] và "chữ ký cấu trúc" BC-DATA §4.3.

### 2.3. Confound provenance × ngôn ngữ (góc Q1 #4) — cảnh báo và cách tách một phần
Thiết kế hiện tại đan xen: toàn bộ semi-synthetic là ZH; real là EN/JA; KO chỉ có fully-synthetic → **không thể tách sạch hiệu ứng ngôn ngữ khỏi provenance**. Tách một phần bằng so sánh NỘI NGÔN NGỮ ZH (5 dataset, đủ 3 nhóm): Dim A — simpsydial (fully-syn) 3.19 > psydial (semi-real) 2.48 > smile/cpsycoun/soulchat (semi-syn) 2.19–2.32; Dim B — simpsydial 4.34 > psydial 4.18 > smile 4.17 > soulchat 3.99 > cpsycoun 3.42. Thứ bậc nhóm trong-ZH lặp lại đúng thứ bậc toàn cục → hiệu ứng provenance **không phải ảo ảnh của ngôn ngữ**. Phần dư không tách được (vd. real-EN vs real-JA) cần thí nghiệm "cùng nội dung, khác ngôn ngữ" (file 01 §7.2) — hiện **không đủ bằng chứng**.

## 3. THẤT BẠI/HẠN CHẾ CỦA KHUNG ĐÁNH GIÁ — ĐỐI CHIẾU 5 GIỚI HẠN CỦA BC-3D §2.5, KÈM ĐỀ XUẤT METRIC

| Giới hạn (BC-3D) | Bằng chứng trong thí nghiệm này | Hệ quả & đề xuất |
|---|---|---|
| 1. Judge–chuyên gia chỉ ~0.50 | Chưa có neo người cho panel này (giới hạn tự nhận); giữa judge: τ hạng A 0.89–0.93, B chỉ 0.60–0.71 | Đọc XẾP HẠNG, không đọc điểm; Dim B chỉ tin ở mức cụm (top/giữa/đáy); bắt buộc neo chuyên gia Việt khi áp sang VN |
| 2. Điểm cao "ảo" của dữ liệu tổng hợp + bias judge | Định lượng được: +0.24 (B), +0.39 (A) sau kiểm soát độ dài; simpsydial 99% record B≥4, 0% <3; dấu self-preference gpt | Mặc định nghi ngờ "syn > real"; panel judge chéo họ generator; báo cáo kèm vân tay cảm xúc/cấu trúc làm đối chứng |
| 3. Chiều cảm xúc chỉ tin ở mức gộp, cần mốc thật | r(coverage, std)=−0.455 (cấu hình A nhiễu); psy_insight 29.5% NaN; chưa có mốc thật cùng kênh cho từng ngôn ngữ | Dim C chỉ so phân bố; công bố lex_coverage kèm mọi kết quả; Tầng 0 (mốc thật) là tiên quyết cho VN |
| 4. Điểm mù vùng khủng hoảng | Không dataset nào trong 11 được đo về xử lý khủng hoảng (Dim A không có trục Safety từ gốc); duy nhất kokorochat CHỦ ĐỘNG phủ kịch bản tự sát bằng role-play kiểm soát (BC-DATA) | Bản đồ khoảng trống (góc Q1 #8): khủng hoảng = vùng trắng của cả khung đo lẫn 10/11 dataset; giải pháp duy nhất có tiền lệ: role-play chuyên gia + người thẩm định 100% (không giao máy) |
| 5. "Qua 3 chiều" ≠ huấn luyện tốt | Chưa chạy downstream — **không đủ bằng chứng** trong phạm vi này; bằng chứng gián tiếp từ BC-DATA: Kokoro-High(2,601)>Full(6,471); Psych8k(8K)>SmileChat(55K); PsyDial π0 > bản tinh chỉnh | Khép vòng bằng SFT nhỏ + benchmark động (MindEval-VN) — điều kiện vận hành 4 của BC-3D |

**Đề xuất bổ sung/loại bỏ metric từ bằng chứng nội bộ** (góc Q1 #3, #6 — sức phân biệt & cấu trúc nhân tố; nguồn: `_agg_discriminative_power.csv`, `_agg_dimA_metric_intercorr.csv`, `_agg_dimB_*intercorr.csv`):
1. **Dim A**: CAC↔AR = 0.936, cụm CAC–AR–TRA α=0.928 → gộp thành 1 trục "lâm sàng chung" (neo CAC vì TRA có validity judge–người thấp nhất theo BC-EVAL); GIỮ EPC và ASCQ như trục riêng (phân biệt dataset mạnh nhất: range 2.50/2.24; ASCQ là trục "LLMness" — đúng đóng góp gốc của MindEval). Rubric 3 trục tiết kiệm ~40% chi phí judge.
2. **Dim B**: 12 item halo nặng (r̄=0.715, α=0.968; goal↔approach=0.891) và between-dataset SD chỉ 0.286 → đề xuất bản **WAI-rút-gọn 4 item** quanh Q10 (item khó "fake" nhất) + báo cáo điểm residual sau hồi quy log-độ-dài (b=+0.305); Bond là subscale kém phân biệt nhất (range 0.779) — không dùng đơn lẻ.
3. **Dim C**: giữ nguyên bộ [E5] + bổ sung bắt buộc lex_coverage; NEC/happy dùng bản trimmed (cắt nghi thức kết phiên); thêm chỉ số Syn–Syn (đồng nhất hóa) khi pipeline xuất chuỗi arc — hiện **không đủ dữ liệu** (file 03 §7.2).
4. **Thêm "2 chiều nền" theo BC-3D**: cấu trúc (số lượt, tỷ lệ token counselor/client, entropy chủ đề) — nghiên cứu này đã dùng không chính thức (token ratio tách psydial 0.85 khỏi mọi dataset LLM-viết ≥1.05) → chính thức hóa thành chiều nền A trong bộ QC.

## 4. INSIGHT MỚI TỪ GHÉP LÝ THUYẾT PROVENANCE × KẾT QUẢ THỰC NGHIỆM (ưu tiên mức contribution)

1. **[Đóng góp chính] Kiểm chứng thực nghiệm khung "3 chiều" trên 11 dataset**: trực giao A↔C tuyệt đối, A↔B yếu, B↔C hội tụ chọn lọc theo cấp phân tích (§1.1) — vượt khỏi 3 "ca án" đơn lẻ của lý thuyết; đồng thời phát hiện **cụm triệu chứng kịch bản hóa** (B cao + happy dày + phân phối nén + tông counselor cao) như một cấu trúc tiềm ẩn cấp dataset. Với bài báo Q1: đây là bảng MTMM đầu tiên cho đánh giá dataset tham vấn.
2. **[Đóng góp] Định lượng synthetic inflation có kiểm soát độ dài**: +0.24 (liên minh) / +0.39 (kỹ năng) cho fully-synthetic so với real; và phân rã "độ dài" như một kênh thưởng riêng của Dim B (b=+0.305) mà Dim A miễn nhiễm (−0.019). Hàm ý phương pháp: mọi so sánh dataset bằng LLM-judge phải báo cáo (điểm thô, điểm residual độ dài, vân tay cảm xúc) như một bộ ba.
3. **[Đóng góp] "Hạt giống quyết định trần, LLM quyết định vân tay"** (§2.2): hai định luật độc lập nhau — trần chất lượng đi theo nguồn chuyên môn của HẠT GIỐNG; vân tay thống kê đi theo AI VIẾT LỜI. Suy ra ma trận thiết kế 2×2 cho người xây dataset: (hạt giống chuyên gia, người viết) = lý tưởng đắt; (hạt giống chuyên gia, LLM viết) = trần cao + vân tay máy — cần cổng QC cảm xúc; (hạt giống đại chúng, người viết) = ấm mà non nghề (esconv); (hạt giống đại chúng, LLM viết) = đáy kép (smile/soulchat) — **tránh**.
4. **Đơn vị phân tích là một quyết định đo lường** (psy_insight): dataset đa phiên duy nhất bị chấm thấp ở B (3.605) và phẳng ở C (NEC≈0) vì bị cắt thành phiên rời — khung đo cấp phiên **mù trước giá trị xuyên phiên**; đây là bằng chứng thực nghiệm đầu tiên cho khoảng trống "đa phiên + kết cục" (BC-3D xu hướng 7) và là lời cảnh báo trực tiếp cho thiết kế multi-session tiếng Việt: phải thiết kế cả **thước đo cấp ca** trước khi thu dữ liệu cấp ca.
5. **Độ tin cậy là thuộc tính của (dataset × judge), không phải của judge**: α dao động 0.520→0.949 theo dataset trong cùng panel; dữ liệu nén phân phối làm sụp α (simpsydial 0.526) trong khi dữ liệu phương sai thật cho α cao (annomi 0.949, psy_insight 0.926). Hàm ý: báo cáo "LLM-judge đáng tin cậy" mà không nêu phân phối dữ liệu là vô nghĩa — một tinh chỉnh đáng công bố cho thực hành meta-evaluation của BC-3D điều kiện 2.
6. **Case study 3 chân dung** (từ §1.2–1.3, làm ví dụ minh họa bài báo): annomi — "chuẩn nghề nhiều ma sát" (A cao, B vừa, happy thấp, phân phối rộng, 17% liên minh gãy); simpsydial — "hòa hợp kịch bản" (B #1, 99% ≥4, happy 88%, SD nén, tông cao); esconv — "ấm mà non nghề" (A đáy, B khá, NEC cao — và trung thực với mục tiêu peer-support của nó). Ba chân dung = ba đích thiết kế khác nhau, không có "tốt nhất" đơn chiều.

## 5. TRỌNG TÂM — XU HƯỚNG VÀ HƯỚNG ĐI CHO DATASET THAM VẤN TRỊ LIỆU MULTI-TURN/MULTI-SESSION TIẾNG VIỆT

### 5.1. Nguyên tắc chỉ đạo: ĐẢO THỨ TỰ — Việt hóa và thẩm định BỘ ĐO trước, sinh dữ liệu sau (BC-3D §3.4a)
Bài học CACTUS (khiếm khuyết chỉ lộ SAU phát hành, bởi nhóm khác, bằng thước đo lúc xây không ai áp — [E7]) + bài học nội bộ của chính nghiên cứu này (lý thuyết sai làm lệch diễn giải cả một vòng phân tích; Dim B thiếu 4 dataset làm kết luận tạm treo) → người đi sau dựng thước đo trước. **4 công cụ Việt hóa theo BC-3D Bảng 3.2**, bổ sung kinh nghiệm thực nghiệm của nghiên cứu này:
1. **WAI-VN**: dịch 12 item + guidelines chi tiết + CoT (khuôn [E1]: 4 người xây, tinh chỉnh 3 vòng trên ~15 hội thoại Việt, ICC mục tiêu ≥0.66); *bổ sung từ số liệu*: cân nhắc bản rút gọn 4 item quanh Q10; luôn báo cáo residual độ dài; đọc theo cụm hạng.
2. **Lexicon cảm xúc VN**: khởi đầu từ bản dịch NRC-VAD tiếng Việt (có sẵn, miễn phí) NHƯNG số liệu của chúng ta cho thấy coverage bản dịch ZH/JA/KO chỉ 23–31% và nhiễu chi phối metric động → lộ trình 3 bậc: (i) baseline cấu hình B (dịch máy→EN); (ii) **ViVAD người gán** 5–8k mục từ miền tham vấn (best–worst scaling; thẩm định theo khuôn [E6]: đo correlation arc theo bin, chỉ dùng vùng bin đạt ≥0.9); (iii) mô hình valence câu tiếng Việt; kèm quy tắc: word-segmentation trước khi match, trim nghi thức chào–kết trước khi tính NEC.
3. **Rubric rủi ro AI-VN (kiểu MindEval)**: giữ ASCQ nguyên trạng (trục phân biệt mạnh nhất), gộp CAC–AR–TRA thành trục lâm sàng chung, neo lại EPC vào quy điều đạo đức nghề tâm lý trong nước; meta-evaluate theo khuôn [E3] (3–4 chuyên gia × ~20 tương tác; kiểm self-preference + độ dài).
4. **Thang lâm sàng VN (chiều nền B)**: chọn theo liệu pháp đã chọn (MITI nếu MI; CTRS nếu CBT; ESC 8 chiến lược cho peer-support); kỳ vọng đồng thuận LLM–chuyên gia 0.4–0.65 (tiền lệ) — đủ mở rộng, không đủ thay người.
Kèm **pilot ngôn ngữ 20 phiên tiếng Việt lặp lại thiết kế S1/S2/S3** trước khi scale: dự đoán từ số liệu (S3 ổn với judge mạnh, τ hạng bền 0.81–0.91) nhưng tiếng Việt phải tự kiểm — bài học S2 (judge yếu lệch tới 0.54) không được ngoại suy.

### 5.2. Kiến trúc 5 tầng (BC-3D §3.2) — ánh xạ với bằng chứng thực nghiệm của nghiên cứu này
- **Tầng 0 — Mốc thật tiếng Việt (làm TRƯỚC TIÊN)**: 50–100 phiên đối chứng không dùng huấn luyện (role-play counselor Việt kiểu KokoroChat + tư liệu chuyên môn xin phép kiểu AnnoMI/RealCBT/D101). Bằng chứng cần thiết từ chính chúng ta: mọi phép đọc Dim B/C ở trên đều phải neo vào "mốc người thật" mượn từ [E1]/[E7] — tiếng Việt chưa có mốc nào; và 76–112 phiên là đủ tạo mốc (annomi 112 phiên đã làm chuẩn cho cả bảng).
- **Tầng 1 — Lõi người tạo (KokoroChat-VN)**: hợp tác khoa tâm lý/trung tâm đào tạo; role-play như bài tập có phản hồi cấu trúc ~20 mục (win-win đào tạo); **chủ động phủ ca khủng hoảng trong kịch bản kiểm soát** (duy nhất kokorochat làm — và là dataset real có B/C cân bằng nhất trong bảng của chúng ta); phản hồi cấu trúc đồng thời là dữ liệu huấn luyện máy-đánh-giá tiếng Việt (tiền lệ: evaluator KokoroChat vượt GPT-4o).
- **Tầng 2 — Nhân rộng bằng máy có neo**: theo trình tự Cactus/BC-3D: ĐO khiếm khuyết LLM mô phỏng tham vấn TIẾNG VIỆT trước (client có "ngoan" quá? — đo bằng chính bộ vân tay §2.2), rồi thiết kế bù: two-agent + planning; client đa thái độ có kháng cự; role card từ tâm sự thật Việt; few-shot từ giáo trình tham vấn tiếng Việt (bài học KMI: ví dụ bản địa thay vì dịch máy); ràng buộc cấu trúc khi sinh (lượt counselor ngắn, token ratio counselor/client <1.2 — mốc từ psydial/Xinling; số lượt ≥16).
- **Tầng 3 — Cổng QC "3+2 chiều" chạy vòng lặp** theo thứ tự chi phí: cấu trúc (miễn phí) → Dim C (lexicon, cấp phân bố; đối chiếu **dải tham chiếu human-viết từ nghiên cứu này**: tông ≤0.17, NEC 0.03–0.05, happy 60–75%, var_ratio >1) → chiều nền lâm sàng → WAI-VN → rubric AI-risk (soi kỹ nhất dữ liệu Tầng 2). Kết quả mỗi vòng dùng để SỬA pipeline (prompt/planning/lọc), không chỉ loại bỏ.
- **Tầng 4 — Chuẩn cuối & vòng đời**: chuyên gia người là chuẩn cuối (3–5 người/mẫu, đo đồng thuận); máy đánh giá tiếng Việt học từ phản hồi Tầng 1; benchmark động MindEval-VN cho kiểm downstream (giới hạn 5); phát hành có trách nhiệm: IRB, thỏa thuận sử dụng, bản che kiểu D0m, tuyên bố không thay thế trị liệu, **phát hành kèm tài nguyên đánh giá** (mốc Tầng 0 + bộ công cụ VN + bảng "3+2 chiều") — theo BC-3D, tài nguyên đánh giá đi kèm tự thân là đóng góp khoa học.

### 5.3. Multi-session và outcome — biên giới có lợi thế định vị rõ nhất
Hiện trạng từ lý thuyết + thực nghiệm: chỉ Psy-Insight có cấu trúc đa phiên trong 11 dataset, và chính nó bị mọi thước đo cấp phiên chấm "oan" (§4.4); dữ liệu [E1] (10.48 phiên/thân chủ, liên minh↔ORS r≈0.30) là hình mẫu multi-session + outcome nhưng không mở hoàn toàn. → Dataset tiếng Việt nên thiết kế **multi-session từ Tầng 0–1**: client-ID xuyên phiên (3–10 phiên/client), goal tracking giữa phiên, và **bộ thước đo cấp ca thiết kế đồng thời**: WAI-trajectory theo phiên (đo "liên minh có được xây dần"), NEC xuyên phiên (chuyển hóa cảm xúc theo liệu trình), một thang outcome tự báo cáo đơn giản kiểu ORS mỗi đầu phiên (khép chuỗi mô tả→kết cục). Đây là đóng góp quốc tế (chưa dataset công khai nào có đủ bộ này), không chỉ đóng góp tiếng Việt.

### 5.4. Cân bằng danh mục provenance cho phiên bản 1 (cập nhật theo taxonomy chính thức)
Từ ma trận 2×2 (§4.3) và bảng nhóm (§2.1): ưu tiên **(hạt giống chuyên gia × người viết)** cho lõi (Tầng 0–1, 15–25%: role-play chuyên gia + tư liệu chuyên môn xin phép); **(hạt giống chuyên gia × LLM viết có neo)** cho quy mô (Tầng 2, 55–65%: RMRR-VN trên chất liệu chuyên gia + two-agent có planning/kháng cự, qua cổng vân tay); **tránh (đại chúng × LLM)** — không lặp lại smile/soulchat; giữ một lát **(đại chúng × người)** kiểu ESConv (10–20%) NẾU đích sản phẩm gồm peer-support, và khai báo construct riêng để không bị chấm "oan" bởi rubric lâm sàng (bài học esconv). Chỉ tiêu phân phối khi nghiệm thu (dải tham chiếu thực nghiệm): happy 60–75%; ≥10% phiên kết không cải thiện + ≥5% record liên minh <3 (mẫu âm tính); SD Dim A nội bộ ≥0.4; tông counselor ≤0.18; token ratio <1.2; 1,000–2,000 phiên chất lượng (chất thắng lượng — 3 bằng chứng BC-DATA + annomi 112 phiên làm chuẩn cả bảng này).

### 5.5. Bảy xu hướng (BC-3D §3.3) — đối chiếu nhanh với số liệu của nghiên cứu này
(1) Neo người thay chạy quy mô — đúng với dữ liệu: 112 phiên annomi giá trị hơn 31.5k cactus về biên độ học; (2) hybrid mặc định — nhóm điểm cao nhất mỗi chiều đều hybrid theo nghĩa nào đó; (3) đánh giá dịch lên mức quan hệ/toàn phân bố — chính là Dim B/C; (4) benchmark động — đề xuất MindEval-VN Tầng 4; (5) giám khảo chuyên biệt học từ phản hồi người — Tầng 1 tạo nguyên liệu; (6) động học cảm xúc + chống đồng nhất hóa thành tiêu chí chuẩn — bộ vân tay §2.2 là bản vận hành; (7) đa phiên + kết cục — §5.3. Lợi thế người đi sau (BC-3D §3.4b): hạ tầng đo gần miễn phí (lexicon dịch sẵn, rubric công khai, RealCBT + dữ liệu người [E3] mở) — nhóm tiếng Việt có thể tái lập phương pháp trên dữ liệu quốc tế (như nghiên cứu này đã làm) trước khi áp lên dữ liệu Việt.

## NGUỒN MINH CHỨNG
- Kết luận nền: file `00` (bảng metric, provenance chính thức §4.6, BT1–BT20, ghi chú cập nhật), `01` (§3–5: cấu hình, hồi quy, nhân tố, verbosity), `02` (§5–6: Dim B 11 dataset, halo, sức phân biệt, thay đổi kết luận), `03` (§3–6: A/B lexicon, vân tay, psy_insight).
- Bảng hợp nhất: `_agg_crossdim_MTMM_pooled.csv`, `_agg_crossdim_dataset_means_11ds.csv`, `_agg_crossdim_dataset_rankcorr.csv`, `_agg_group_means_official.csv`, `_agg_counselor_words_dichotomy.csv`, `_agg_provenance_regression_official.csv`, `_agg_discriminative_power.csv`, `_agg_rank_stability.csv`, `_agg_dimension_disagreement_cases.csv`, `_agg_dimA_metric_intercorr.csv`, `_agg_dimB_subscale_intercorr.csv`, `_agg_dimB_item_intercorr.csv`, `_agg_verbosity_bias.csv`.
- Lý thuyết: BC-3D (điều kiện A/B/C §2.2–2.4; 5 giới hạn §2.5; 4 điều kiện vận hành §2.6; 5 nguyên tắc §3.1; kiến trúc 5 tầng §3.2; 7 xu hướng §3.3; 4 công cụ Việt hóa Bảng 3.2; rủi ro Goodhart §3.5); BC-EVAL (3 tầng đo, mốc [E1], meta-evaluation [E3], thẩm định [E6], khuôn so sánh [E7]); BC-DATA (§1.3 taxonomy; §4.1 bốn làn sóng; §4.2–4.3 ưu–khuyết provenance + chữ ký cấu trúc; mục 5 hàm ý tiếng Việt). Tóm tắt: `_notes/theory_word_11dataset_tomtat.md`.
- Giới hạn tổng: hồi quy provenance mang pseudo-replication (provenance là thuộc tính dataset); n=11 cho tương quan hạng; chưa có neo chuyên gia người và chưa chạy downstream (khai báo "không đủ bằng chứng" tại các mục tương ứng); confound provenance×ngôn ngữ chỉ tách được một phần (§2.3).
