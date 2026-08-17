# BƯỚC 2 — PHÂN TÍCH SÂU DIM B (WAI-O-S: LIÊN MINH TRỊ LIỆU) — BẢN ĐẦY ĐỦ 11 DATASET

## THAY ĐỔI SO VỚI BẢN TRƯỚC
(1) **Dim B nay đủ 11 dataset × 3 judge**: bổ sung 4 file claude (`D:\vy\jsonl\`) cho PsyDial, Simpsydial, Psy-Insight, smile — mọi nhãn "N/A" được gỡ, xếp hạng tổng tính lại trên 11 dataset; tương quan chéo liên quan Dim B tính lại toàn bộ. (2) Lý thuyết viết lại theo BC-EVAL (mục 3.1) và taxonomy provenance BC-DATA. (3) Bổ sung phân tích mới: cấu trúc nhân tố/halo 12 item, sức phân biệt–hiệu ứng trần, độ ổn định hạng, hồi quy provenance kiểm soát độ dài. (4) Danh sách kết luận thay đổi so với bản trước: **§6.0**.

> Phạm vi dữ liệu: pilot tại `experiments/dim_b_wai/20` (S3 × 3 judge; S1 chỉ gpt; không có S2); full = `experiments/dim_b_wai/full` (7 dataset × 3 judge + 4 dataset gemini/gpt) **+ 4 file claude mới tại `D:\vy\jsonl\`**. Panel hoàn chỉnh: 2,111 dialogue × 3 judge = 6,333 lượt chấm. Số liệu cũ tái dùng nguyên trạng; số mới chỉ trích từ 4 file bổ sung (`_agg_dimB_newfiles_report.csv`: 200/200/200/199 record; trùng lặp với dữ liệu cũ = 0).

## 1. Tổng quan khung đánh giá và liên hệ cách xây dựng dataset (theo BC-EVAL, BC-DATA)

### 1.1. Khung WAI-O-S (BC-EVAL mục 3.1)
12 item × thang 1–5 (anchor theo lượng bằng chứng, 3 = trung tính "không có bằng chứng"), 3 chiều × 4 item: **Goal (Q1–4), Approach (Q5–8), Affective Bond (Q9–12)**, cao = liên minh mạnh (bảng chi tiết: file 00 §2). Các điểm lý thuyết quyết định cách đọc, theo BC-EVAL:
1. Liên minh là "biến quá trình kinh điển" đo **quan hệ hai chiều tích lũy qua nhiều lượt** — thứ mà metric mức câu (empathy/fluency) không chạm tới; bằng chứng giá trị: liên minh tương quan kết cục tự báo cáo ORS r ≈ 0.30 trên 859 phiên thật (BC-EVAL 3.1.f).
2. Pipeline hiện tại tái tạo đúng setting mạnh nhất của [E1]: guidelines chi tiết + CoT bằng-chứng-trước-điểm + 3 run/câu — nơi GPT-4 khớp chuyên gia r ≈ 0.50; **đây cũng là trần độ tin cậy tuyệt đối của Dim B** (BC-3D §2.5 giới hạn 1 → chỉ đọc so sánh tương đối).
3. Mốc người thật để đối chiếu (BC-EVAL 3.1.e): các chiều 3.5–4 trên dữ liệu tham vấn text thật; Bond cao nhất (~4 ở câu tin cậy lẫn nhau), thấp nhất là "ích lợi của hoạt động hiện tại" (3.32); và **giao tiếp dài hạn không tự làm liên minh sâu thêm** (gần 50% cặp giảm/không đổi).
4. Cảnh báo định sẵn của BC-3D (§2.3 minh chứng 3, §2.5 giới hạn 2): **SimPsyDial từng đạt WAI cao hơn cả dữ liệu thật** (goal 6.045 vs 5.505, thang 1–7) trong khi cấu trúc lệch xa thật → "điểm liên minh cao của dữ liệu tổng hợp phải bị nghi ngờ trước tiên". Kỳ vọng lý thuyết này được kiểm chứng trực tiếp ở §5.

### 1.2. Liên hệ provenance (BC-DATA §1.3)
Nhóm fully-synthetic (cactus, simpsydial, kmi) có client LLM "quá dễ hợp tác" (BC-EVAL 3.2.g; BC-DATA: "RLHF làm ngoan hóa"); nhóm semi-synthetic (smile, soulchat, cpsycoun) viết lại từ QA nên **quan hệ hai chiều là sản phẩm dựng lại**, không phải tương tác tích lũy; nhóm real/semi-real chứa ma sát quan hệ thật (annomi có cả mẫu MI chất lượng thấp chủ ý; kokorochat role-play có kịch bản khó). → Kỳ vọng: Dim B thiên vị dương cho dữ liệu càng nhiều LLM trong lời thoại, và phân phối càng nén.

## 2. Tổng hợp kết quả đánh giá — BẢNG CHÍNH THỨC 11 DATASET

Nguồn: `_agg_dimB_official_11ds.csv` (total 1–5, TB 3 judge; SD của judge-mean theo record):

| Hạng | Dataset (provenance) | Total ± SD | Goal | Approach | Bond | %≥4 | %<3 |
|---|---|---|---|---|---|---|---|
| 1 | simpsydial (fully-syn) | **4.335**±0.181 | 4.333 | 4.435 | 4.238 | **99.0** | 0.0 |
| 2 | cactus (fully-syn) | 4.290±0.336 | 4.410 | 4.355 | 4.106 | 81.0 | 0.0 |
| 3 | psydial (semi-real) | 4.182±0.273 | 4.146 | 4.151 | 4.249 | 83.0 | 0.5 |
| 4 | smile (semi-syn) | 4.166±0.369 | 4.158 | 4.158 | 4.182 | 80.4 | 2.0 |
| 5 | kmi (fully-syn) | 4.088±0.199 | 4.241 | 4.084 | 3.938 | 68.0 | 0.0 |
| 6 | kokorochat (real) | 4.046±0.531 | 4.053 | 3.989 | 4.095 | 65.0 | 4.5 |
| 7 | esconv (real) | 4.007±0.512 | 3.910 | 4.032 | 4.079 | 62.0 | 4.5 |
| 8 | soulchat (semi-syn) | 3.992±0.300 | 3.937 | 3.942 | 4.096 | 52.5 | 0.5 |
| 9 | annomi (semi-real) | 3.760±0.934 | 3.840 | 3.769 | 3.672 | 57.1 | 17.0 |
| 10 | psy_insight (real) | 3.605±0.573 | 3.700 | 3.646 | 3.471 | 25.0 | 9.5 |
| 11 | cpsycoun (semi-syn) | **3.418**±0.355 | 3.476 | 3.238 | 3.538 | 6.5 | 11.5 |

Mức item (`_agg_dimB_item_means_11ds.csv`): **Q10** ("client tin năng lực counselor") vẫn là item thấp nhất gần như toàn cục (psy_insight 3.29, annomi 3.48, smile 4.09); **Q12** (tin cậy lẫn nhau) cao nhất (simpsydial 4.58, psydial 4.51); cận trần: **simpsydial Q5 = 4.76/5** ("đồng thuận về các bước"). Lỗi parse cục bộ claude ở 4 file mới: smile 72 điểm None/6 record, psy_insight 12/1, simpsydial 12/1 (BT18) — subscale tính trên item còn lại.

## 3. Đánh giá chéo cấu hình đa ngôn ngữ (GIỮ NGUYÊN bản trước)

Chỉ so được **S1↔S3 với judge gpt** (không tồn tại S2; S1 không có claude/gemini — file 00 §6.2). Kết quả không đổi: pooled Δ(S1−S3) = **+0.006**, |Δ| = 0.064 (n=219), không dataset nào có ý nghĩa (bảng chi tiết: bản trước / `_stats/dimB_pilot_config_diffs.csv`). WAI gần như bất biến với việc dịch hội thoại — tín hiệu quan hệ vĩ mô (đồng thuận mục tiêu, tin cậy) sống sót qua dịch máy tốt hơn tín hiệu vi mô của Dim A. **Prompt-language bias (S2): không đo được — giới hạn giữ nguyên.**

## 4. Pilot → kiểm chứng lựa chọn cấu hình (GIỮ NGUYÊN + một bổ sung)

Kết luận bản trước giữ nguyên: S1 ≈ S3 với gpt → S3 hợp lý về chi phí–chất lượng (đỡ dịch ~1.08 triệu token cho 7 dataset non-EN); mức kiểm chứng của Dim B yếu hơn Dim A (1 judge, không S2, kokorochat gpt S3 pilot hỏng — BT9). Bổ sung độ ổn định mẫu (`_agg_rank_stability.csv`): **pilot-20 vs full-200 trên 11 dataset: Kendall τ = 0.564 (p=0.017)** — thấp hơn hẳn Dim A (0.818). Nguyên nhân ở §5.6: dải điểm Dim B giữa dataset quá hẹp nên hạng nhạy với nhiễu mẫu nhỏ. Hàm ý thiết kế pilot: với thước đo nén như WAI, **20 record/dataset không đủ để chốt thứ hạng** — chỉ đủ để kiểm tra pipeline.

## 5. Phân tích sâu trên full 200 × 11 dataset

### 5.1. Kiểm chứng dự đoán bản trước và "lạm phát liên minh" dạng đầy đủ
Dự đoán bản trước (dựa trên offset 2-judge → 3-judge trung bình +0.102) **đúng**: 2j−3j của 4 dataset mới = +0.097/+0.143/+0.153/−0.000 (TB +0.098); simpsydial/psydial/smile vào thẳng top-4. Bức tranh đầy đủ: **4 vị trí đầu bảng đều là dữ liệu LLM-viết-lời hoặc client-LLM** (simpsydial, cactus, psydial, smile); toàn bộ nhóm này vượt mốc người thật của [E1] (3.5–4.0) và vượt xa dữ liệu real (kokorochat 4.046, esconv 4.007, psy_insight 3.605). Riêng **psy_insight là ngoại lệ kép**: claude không nghiêm hơn ở dataset này (2j−3j = −0.000) và điểm thấp thứ 10 — hội thoại sách chuyên môn (ca đa phiên bị cắt rời — BT19) không "diễn" liên minh như dữ liệu sinh.
Hồi quy kiểm soát độ dài (`_agg_provenance_regression_official.csv`): total ~ log(tokens) + provenance → R²=0.312; **b_log(tokens) = +0.305** (mạnh); so với real: **fully-synthetic +0.237**, semi-synthetic −0.038, semi-real −0.186. → Sau khi trừ hiệu ứng độ dài, chỉ nhóm fully-synthetic còn "phần thưởng liên minh" rõ (+0.24/thang 5). Vị trí cao của psydial (semi-real, hạng 3) chủ yếu do **độ dài** (dialogue dài nhất corpus, ~1,620 token TB): dài → nhiều bằng chứng → điểm cao theo cơ chế anchor; sau kiểm soát độ dài nhóm semi-real KHÔNG được thưởng. Đây là dạng tách "chất lượng thật" khỏi "cơ chế đo" mà BC-3D §2.5 yêu cầu.

### 5.2. Phân phối nén và ceiling — chữ ký của "hòa hợp kịch bản"
SD nội bộ: simpsydial 0.181, kmi 0.199 (nén nhất — fully-synthetic) so với annomi 0.934, psy_insight 0.573, kokorochat 0.531 (dữ liệu người có ma sát). simpsydial 99% record ≥4 và **0% record <3** — một thế giới không có liên minh xấu; annomi có 17% record <3 (ca liên minh gãy đổ thật — nguồn mẫu âm tính quý). Mức item: Q5 simpsydial 4.76 sát trần. Khớp tiên đoán BC-3D: "điểm liên minh của dữ liệu tổng hợp có thể cao ảo"; và khớp cơ chế BC-DATA ("client AI quá ngoan").

### 5.3. Nghịch đảo với Dim A và hội tụ với Dim C — cập nhật đầy đủ
- Với Dim A (dataset-level, n=11): ρ = **0.182** (p=0.593; `_agg_crossdim_dataset_rankcorr.csv`) — gần trực giao. Record-level pooled: 0.375 (`_agg_crossdim_MTMM_pooled.csv`).
- Với Dim C: **B↔happy_ending ρ = 0.724 (p=0.012); B↔NEC ρ = 0.655 (p=0.029)** — có ý nghĩa thống kê dù n=11. Đây là phát hiện mới quan trọng: ở cấp dataset, **chiều liên minh đồng biến với "độ lạc quan cảm xúc"** (kết phiên vui, NEC dương) trong khi chiều kỹ năng lâm sàng thì không (A↔happy ρ=−0.369 ns). Cách đọc thận trọng (không tự hòa giải hai khả năng): (a) liên minh tốt thật sự đi kèm cải thiện cảm xúc — đúng lý thuyết Bordin; (b) judge WAI và chỉ số NEC cùng bị hút bởi một nguồn chung là "kịch bản hòa hợp–kết đẹp" của dữ liệu LLM. Bằng chứng nghiêng về (b) ở cấp dataset: cặp record-level trong nội bộ dataset chỉ 0.172 (yếu), nghĩa là sự đồng biến chủ yếu xuất hiện GIỮA dataset (theo phong cách sinh) chứ không GIỮA các phiên trong cùng dataset.

### 5.4. Chữ ký khung trị liệu trên 3 subscale (cập nhật với 4 dataset mới)
Pattern bản trước giữ nguyên và rõ hơn: nhóm kỹ thuật (MI/CBT): Goal/Approach > Bond (kmi 4.241/4.084/3.938; cactus 4.410/4.355/4.106; simpsydial Approach 4.435 cao nhất bảng); nhóm đồng cảm/viết lại: Bond ≥ Goal (soulchat 4.096 vs 3.937; psydial 4.249 vs 4.146; smile cân bằng); annomi cân bằng thấp; psy_insight Bond thấp nhất (3.471) — ca sách nặng kỹ thuật, nhẹ "diễn" quan hệ.

### 5.5. Độ tin cậy giữa judge — hai thái cực mới (`_agg_dimB_judge_agreement_11ds.csv`)
Krippendorff α: **psy_insight 0.926** (cao nhì toàn bảng, sau annomi 0.949) — dữ liệu có phương sai thật thì judge đồng thuận; **simpsydial 0.526, psydial 0.565** (thấp nhất) — dải điểm nén làm α sụp dù MAE nhỏ (range restriction: simpsydial claude↔gpt MAE chỉ 0.154 nhưng Pearson 0.649). Bias claude−gemini dao động mạnh theo dataset (−0.757 ở smile, −0.019 ở psy_insight) → **bias judge không phải hằng số, phụ thuộc phong cách dữ liệu**; pooled 11 dataset: claude thấp hơn gemini 0.425, thấp hơn gpt 0.182.

### 5.6. Sức phân biệt & hiệu ứng trần — Dim B yếu hơn Dim A rõ rệt (`_agg_discriminative_power.csv`, `_agg_rank_stability.csv`)
Between-dataset SD của Dim B total chỉ **0.286** (range 0.917/thang 5) so với within-dataset SD 0.415; Dim A: between 0.587 (range 1.822/thang 6) > within 0.479. Chuẩn hóa theo bề rộng thang: sức phân tách giữa dataset của B ≈ 0.23 vs A ≈ 0.36. Hệ quả đo được: τ giữa judge của bảng xếp hạng B chỉ 0.600–0.709 (A: 0.891–0.927); τ pilot–full 0.564 (A: 0.818). Ceiling cục bộ: 2.1–6.2% record đạt ≥4.75; grand mean ~4.0/5. **Bond là subscale kém phân biệt nhất** (range 0.779). → Đề xuất đo lường ở §7.

### 5.7. Cấu trúc nhân tố: halo được định lượng (`_agg_dimB_subscale_intercorr.csv`, `_agg_dimB_item_intercorr.csv`)
Tương quan subscale (pooled-z nội dataset): **goal↔approach 0.891**, approach↔bond 0.810, goal↔bond 0.740; 12 item: trung bình inter-item r = **0.715** (min 0.531, max 0.924), Cronbach α = **0.968**. Kết luận: LLM-judge chấm 12 item gần như MỘT ấn tượng chung + offset cố định theo item (Q12 luôn đỉnh, Q10 luôn đáy) — nghi vấn halo của bản trước nay **được xác nhận định lượng**. Goal và Approach trên thực tế không tách được (0.891). Trớ trêu về đo lường: α=0.968 là "độ tin cậy nội tại tuyệt vời" theo tâm trắc học, nhưng ở đây nó tố cáo **thiếu độ phân giải giữa các thành phần lý thuyết của Bordin** khi người chấm là LLM đọc transcript.

## 6. Kết luận & insight của Dim B

### §6.0. KẾT LUẬN NÀO THAY ĐỔI SO VỚI BẢN TRƯỚC (yêu cầu bắt buộc)
1. **Xếp hạng #1 đổi: cactus → simpsydial** (4.335); top-4 nay toàn dữ liệu LLM-tham-gia; kokorochat/esconv (real) rơi xuống giữa bảng; kết luận "cactus đứng đầu 7 dataset" hết hiệu lực.
2. **"Lạm phát liên minh" được nâng cấp từ mô tả thành ước lượng có kiểm soát**: bản trước chỉ so trung bình thô; nay hồi quy kiểm soát log-độ-dài cho thấy phần thưởng fully-synthetic +0.237 so với real; đồng thời phát hiện MỚI rằng ~1/3 khoảng cách thô giữa các dataset là **hiệu ứng độ dài** (b=+0.305) — bản trước mới chỉ ra tương quan, chưa tách phần thưởng provenance khỏi độ dài.
3. **Tương quan B↔C đổi trạng thái**: bản trước (7 dataset) B↔happy ρ=0.342 không ý nghĩa; nay (11 dataset) **ρ=0.724, p=0.012** — hội tụ liên minh–lạc quan cảm xúc ở cấp dataset trở thành phát hiện chính thức.
4. **Độ tin cậy xếp hạng Dim B bị hạ cấp**: có đủ 11 dataset mới lộ rõ τ judge 0.60–0.71 và τ pilot–full 0.564 — bản trước chưa đánh giá được vì thiếu 4 dataset; khuyến nghị đọc hạng Dim B theo cụm (top/giữa/đáy), không đọc từng bậc.
5. **psy_insight**: bản trước chỉ có số 2-judge tham khảo (3.605) — nay chính thức 3.605 (trùng), nhưng có thêm hai sự kiện mới: α=0.926 (judge cực kỳ đồng thuận) và claude không nghiêm hơn — điểm thấp của nó là tín hiệu thật của dữ liệu, không phải nhiễu judge; kết hợp BT19 (ca đa phiên bị cắt rời) → điểm B thấp phần lớn vì đơn vị phân tích sai (phiên tách khỏi ca), một giới hạn của chính thí nghiệm.
6. Các kết luận giữ nguyên: S3 hợp lệ; Q10 là item khó "fake" nhất; cơ chế anchor-bằng-chứng gây confound độ dài; halo 12 item (nay có số).

### §6.1–6.5. Insight chính (bản đầy đủ)
1. **Dim B đo "mức độ hội thoại TRÔNG hợp tác", và dữ liệu sinh tự động tối ưu đúng cái đó**: top-4 LLM-involved, vượt mốc người thật 0.2–0.8 điểm; phân phối nén (simpsydial 0% record <3); phần thưởng +0.24 sau kiểm soát độ dài. Đọc kèm BC-3D: đây chính là ca SimPsyDial-vs-RealPsyDial được tái lập độc lập trên 11 dataset với panel judge khác.
2. **Liên minh không suy ra kỹ năng**: A↔B dataset-level 0.182 — một dataset có thể dạy model "diễn quan hệ tốt" mà không dạy nghề (simpsydial: B #1, A #4; esconv: B #7, A #11 — nhưng chiều lệch ngược nhau).
3. **Dim B + NEC/happy hội tụ ở cấp dataset (ρ≈0.65–0.72)**: khi xây bộ đánh giá nên coi "liên minh cao + kết vui dày đặc + phân phối nén" là **một cụm triệu chứng của kịch bản hóa**, không phải ba thành tích độc lập.
4. **Trần đo lường của WAI-LLM**: halo (r̄=0.715), nén dải (between-SD 0.286), τ judge thấp — WAI 12 item bản LLM-judge hiện cho ~1 bit thông tin/dataset (top/giữa/đáy). Giá trị chính nằm ở mức record trong nội bộ dataset (lọc mẫu liên minh gãy: annomi 17% <3) và ở item khó Q10.
5. **Giới hạn còn lại**: không S2; S1 chỉ gpt; r≈0.50 với chuyên gia là trần kế thừa từ [E1]; chưa có neo chuyên gia người cho panel này (điều kiện vận hành 2 của BC-3D chưa thỏa cho tiếng Việt — phải làm khi áp sang VN).

## 7. Luận điểm bổ sung & góc phân tích chưa khai thác

1. **Rút gọn công cụ theo bằng chứng nhân tố**: với r̄ item 0.715 và goal↔approach 0.891, một bản **WAI-rút-gọn 4 item** (Q10 + Q6 + Q12 + 1 item goal) có thể giữ ~90% thông tin với 1/3 chi phí; kiểm chứng đề xuất: chấm lại 2 dataset bằng bản rút gọn, so τ với bản 12 item. (Nối tiếp logic "đã loại S2, loại qwen" — cắt tỉa dựa trên số liệu.)
2. **Điểm liên minh theo đoạn phiên** (giữ từ bản trước, nay có thêm động cơ): BC-EVAL 3.1.f — liên minh không tự sâu thêm theo thời gian ở người thật; giả thuyết "synthetic flat-high, real tăng/võng" kiểm được ngay bằng chấm 3 đoạn.
3. **Judge-as-client**: WAI-O-S là observer; CUEMPATHY (bản trước) và chính [E1] gợi ý góc nhìn client khác hẳn observer — thêm một cấu hình judge đóng vai client chấm WAI bản client-rated làm chiều đối chứng rẻ.
4. **Dùng độ dài như biến thiết kế, không phải nhiễu**: b_log(tokens)=0.305 nghĩa là mọi so sánh WAI giữa dataset khác độ dài đều phải kèm hiệu chỉnh (báo cáo cả điểm thô lẫn residual sau hồi quy độ dài) — đề xuất đưa thành quy ước trong bộ QC "3+2 chiều" của BC-3D Tầng 3.
5. **Khai thác mẫu âm tính**: trích toàn bộ record total <3 (annomi 19 record, cpsycoun 23, psy_insight 19, kokorochat 9, esconv 9...) thành "bộ sưu tập liên minh gãy đổ" — tài nguyên huấn luyện contrastive/safety mà không dataset synthetic nào cung cấp (simpsydial/cactus/kmi: 0–1 record).

## 8. Nguồn minh chứng
- Dữ liệu: 43 file pilot + 29 file full cũ (`experiments/dim_b_wai/`) — tái dùng qua `_stats/dimB_records_full.csv`; **4 file mới**: `D:\vy\jsonl\{PsyDial,simpsydial,Psy-Insight,smile}_S3_claude_9router_full_wai_judgments.jsonl` (200/200/200/199 record; kiểm kê `_agg_dimB_newfiles_report.csv`); hợp nhất: `_stats/dimB_records_full_v2.csv`. Record minh chứng: `simpsydial_463` (B=4.769, A=2.750), `cactus_19` (B=4.870, A=2.867) — `_agg_dimension_disagreement_cases.csv`.
- Bảng dẫn xuất lần 2: `_agg_dimB_official_11ds.csv`, `_agg_dimB_item_means_11ds.csv`, `_agg_dimB_judge_agreement_11ds.csv`, `_agg_crossdim_MTMM_pooled.csv`, `_agg_crossdim_dataset_rankcorr.csv`, `_agg_provenance_regression_official.csv`, `_agg_group_means_official.csv`, `_agg_discriminative_power.csv`, `_agg_rank_stability.csv`, `_agg_dimB_subscale_intercorr.csv`, `_agg_dimB_item_intercorr.csv`, `_agg_verbosity_bias.csv`; bảng cũ tái dùng: `_stats/dimB_pilot_config_diffs.csv`, `dimB_pilot_summary.csv`.
- Lý thuyết: BC-EVAL mục 3.1 (WAI-O-S, mốc người thật, r≈0.50, ORS r≈0.30), Phần 4 (3 tầng); BC-DATA §1.3/Bảng 2.1 (provenance), §4.3 (client AI ngoan); BC-3D §2.3 minh chứng 3 (SimPsyDial), §2.5 giới hạn 1–2, §2.6 (đọc tương đối). Tóm tắt: `_notes/theory_word_11dataset_tomtat.md`.
- Giới hạn khai báo: BT6, BT8–BT11, BT17–BT19 (file 00 §7); hồi quy provenance mang pseudo-replication; halo có thể do judge hoặc do bản chất dữ liệu — không tách được trong thiết kế hiện tại (nêu nguyên trạng).
