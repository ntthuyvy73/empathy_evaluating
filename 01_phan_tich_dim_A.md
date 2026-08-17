# BƯỚC 1 — PHÂN TÍCH SÂU DIM A (MindEval: ĐÁNH GIÁ COUNSELOR)

## THAY ĐỔI SO VỚI BẢN TRƯỚC
(1) Toàn bộ phần lý thuyết (mục 1, 6, 7) viết lại theo 3 file Word có thẩm quyền (BC-DATA, BC-EVAL, BC-3D) — đặc biệt: **AnnoMI được phân loại lại semi-real** (video trình diễn MI, không phải phiên trị liệu tự nhiên) và nhóm provenance dùng taxonomy 4 nhóm chính thức của BC-DATA §1.3. (2) **Số liệu thực nghiệm Dim A giữ nguyên 100%** so với bản trước (không chạy lại). (3) Bổ sung các phân tích mới trên số liệu đã chốt: cấu trúc nhân tố 5 trục, sức phân biệt/hiệu ứng trần, độ ổn định xếp hạng, hồi quy provenance có kiểm soát độ dài, thiên vị độ dài lượt counselor. (4) Kết luận thay đổi lớn nhất: Dim A là "máy dò giao thức chuyên nghiệp", không phải "máy dò tính thật" — xem §6.1.

> Phạm vi dữ liệu: pilot 20 record × S1/S2/S3 × 4 judge tại `experiments/dim_a_mind_eval/20`; full 200 record × S3 × 3 judge tại `experiments/dim_a_mind_eval/full`. Số liệu đã chốt tại file 00 (bảng 5.1–5.2) và `_stats/`, `_agg_*.csv`.

## 1. Tổng quan khung đánh giá và cách 11 dataset được xây dựng (theo BC-EVAL, BC-DATA)

### 1.1. Khung MindEval (BC-EVAL mục 3.2)
Dim A dùng 5 trục MindEval: **CAC, EPC, AR, TRA, ASCQ**, thang Likert **1–6, cao = tốt**; Overall = trung bình không trọng số (bảng metric đầy đủ: file 00 §1). Các đặc điểm quyết định cách đọc kết quả, theo BC-EVAL:
1. **Judge chấm toàn bộ tương tác** ("tín hiệu trị liệu hiện ra ở cấp phiên") — điểm là chất lượng tích lũy, không phải trung bình lượt.
2. **Bản chất là khung đo RỦI RO ĐẶC THÙ AI** (góc nhìn 2 trong 3 góc của BC-EVAL): sycophancy/trấn an quá mức → CAC/AR; tạo phụ thuộc → TRA; xói mòn ranh giới → EPC; ảo giác/giọng máy → ASCQ. Rubric neo hướng dẫn giám sát lâm sàng và khuyến cáo chatbot của APA.
3. **Meta-evaluation đã làm sẵn** (BC-EVAL 3.2.f): judge nằm trong khoảng đồng thuận giữa chuyên gia; đổi judge giữ >0.85 độ chính xác xếp cặp; có self-preference bias (GPT-5 tự nâng 1.58 hạng trong 72% tương tác) → khi dùng phải kiểm tra bias này (đã làm ở §5.5).
4. **Hai bằng chứng nền quan trọng của BC-EVAL** dùng để đối chiếu: (i) mọi LLM hiện đại <4/6, ASCQ là trục khó nhất (1.75–3.11), EPC dễ nhất (2.31–4.58); (ii) xếp hạng ASCQ tách khỏi xếp hạng năng lực (Gemma3 thấp tổng thể nhưng vượt GPT-5 về ASCQ) — bằng chứng trực giao nội bộ của chính khung đo.
5. **Điểm mù khai báo trước** (BC-3D §2.5, giới hạn 4): trục Safety & Crisis bị bỏ vì không tạo được phương sai → Dim A **không đo vùng khủng hoảng**; và judge kéo dài hội thoại 20→40 lượt làm điểm giảm rõ — điểm chịu ảnh hưởng độ dài theo hướng ngược với Dim B (kiểm chứng thực nghiệm ở §5.4).

### 1.2. Cách 11 dataset được xây dựng — taxonomy provenance chính thức (BC-DATA §1.3, Bảng 2.1)
Bảng đầy đủ: file 00 §4.6. Tóm tắt 4 nhóm: **Real** (người thật tạo lời thoại): esconv (crowdworker sát hạch 7.8%), kokorochat (480 counselor/học viên role-play, 91.2 lượt nói, feedback 20 mục), psy_insight (sách/blog chuyên môn, 951 phiên/189 ca — **duy nhất có multi-session**, 12 trường phái); **Semi-real**: annomi (video trình diễn MI + chú giải MINT, 133 hội thoại), psydial (RMRR trên 2,382 hội thoại thật Xinling, giữ lời counselor); **Semi-synthetic** (hạt giống thật + LLM biến đổi): smile (ChatGPT viết lại PsyQA), soulchat (QA người viết → ChatGPT viết lại), cpsycoun (Memo2Demo từ báo cáo ca); **Fully synthetic** (LLM cả hai vai, có neo thật): cactus (GPT-4o + planning CBT, lọc CTRS), simpsydial (GPT-4×GPT-4, role card PsyQA), kmi (LLM–LLM + MI forecaster học từ AnnoMI).

Hệ quả đọc Dim A theo lý thuyết mới: nhóm "real" của BC-DATA đo **ai viết lời thoại**, không đo "độ chuyên nghiệp lâm sàng của người viết". Trong nhóm real có cả peer support không chuyên (esconv); trong nhóm semi-real có trình diễn chuyên gia (annomi). Vì rubric MindEval đo *chuẩn hành nghề lâm sàng*, kỳ vọng lý thuyết đúng là: **điểm Dim A đi theo "độ chuyên nghiệp của hình mẫu counselor + mức khớp giao thức", không đi theo trục real↔synthetic** — được số liệu xác nhận ở §5.

## 2. Tổng hợp kết quả đánh giá (GIỮ NGUYÊN số liệu bản trước)

Xếp hạng Overall full 200 (S3, TB 3 judge; nguồn: `_stats/dimA_full_dataset_summary.csv`): **annomi 3.621 > cactus 3.376 > psy_insight 3.364 > simpsydial 3.188 > kokorochat 2.917 > kmi 2.653 > psydial 2.481 > smile 2.321 > cpsycoun 2.285 > soulchat 2.191 > esconv 1.798**. Bảng 5 trục và bảng theo judge: file 00 §5.1 và bản trước (không đổi). Điểm nhấn: annomi SD 1.079 (46.4% ≥4 VÀ 13.4% <2); cactus/kmi SD hẹp nhất 0.267/0.265; esconv EPC 1.612 thấp nhất toàn bảng; ASCQ cao nhất annomi 3.938, thấp nhất kmi 1.958.

## 3. Đánh giá chéo cấu hình đa ngôn ngữ (GIỮ NGUYÊN + bổ sung độ ổn định hạng)

Số liệu S1/S2/S3 như bản trước (nguồn: `_stats/dimA_pilot_config_pooled.csv`, `dimA_pilot_agreement_by_config.csv`): claude/gpt gần bất biến giữa cấu hình (|Δ| ≤ 0.073); gemini S1−S3 = −0.241 (p<0.001); qwen S2−S3 = +0.420 (p<0.001), S1−S2 = −0.540; đồng thuận judge pooled: S1 0.467, S3 0.423, S2 0.286 — S2 phá đồng thuận.

**Bổ sung (lần 2) — độ ổn định xếp hạng giữa cấu hình** (`_agg_rank_stability.csv`): Kendall τ giữa bảng xếp hạng 7 dataset đa ngôn ngữ pilot (3 judge, bỏ qwen): **S1 vs S3 τ = 0.810 (p=0.011); S2 vs S3 τ = 0.905 (p=0.003)**. Nghĩa là dù mức điểm dao động theo cấu hình (nhất là với judge yếu), **thứ hạng dataset gần như không đổi** — kết luận so sánh giữa dataset bền vững với lựa chọn cấu hình; hiệu ứng cấu hình chủ yếu là dịch chuyển hệ số (offset) theo judge, đúng tinh thần "đọc kết quả tương đối" mà BC-3D §2.6 yêu cầu.

## 4. Pilot 20 → kiểm chứng lựa chọn S3 (GIỮ NGUYÊN + định lượng chi phí)

Kết luận bản trước giữ nguyên: pilot ủng hộ chọn S3 (S3 ≈ S1 về chất lượng, S2 bị loại vì phá đồng thuận và thổi phồng qwen; loại qwen khỏi full là đúng — bias +0.766…+1.190, MAE 0.794–1.195). Bổ sung định lượng cho "đường biên chi phí–chất lượng" (góc Q1 bổ sung; số token từ `crossdim_records_v2.csv`): S1 đòi dịch **~1.08 triệu token** hội thoại (7 dataset non-EN × ~200 record) chỉ riêng full-run Dim A/B, trong khi chênh chất lượng đo được S1↔S3 ở hai judge mạnh ≤0.073 điểm và τ hạng 0.810 → **mức tăng chất lượng trên mỗi đơn vị chi phí của S1 ≈ 0**; S3 chiếm ưu thế tuyệt đối trên đường biên chi phí–chất lượng. Điều kiện kèm: S3 chuyển gánh nặng ngôn ngữ sang năng lực đa ngữ của judge (qwen thất bại), và kết luận dựa trên n=20/dataset không có neo chuyên gia người.

Độ ổn định pilot→full (bổ sung, 3 judge): τ = 0.818 (p<0.001, 11 dataset) — mẫu 20 dự báo tốt thứ hạng mẫu 200; sai lệch lớn nhất vẫn là annomi (phương sai nội bộ 1.08).

## 5. Phân tích sâu trên full 200 (số liệu giữ nguyên; diễn giải cập nhật theo taxonomy mới)

### 5.1. Đọc lại xếp hạng theo provenance chính thức
Ba bậc điểm không xếp theo trục real→synthetic mà theo **giao thức chuyên nghiệp của hình mẫu counselor**:
- Bậc trên (3.19–3.62): annomi (semi-real — *trình diễn chuyên gia MI*), cactus (fully-synthetic — *giả lập CBT có planning, lọc CTRS*), psy_insight (real — *ca xuất bản trong sách chuyên môn*), simpsydial (fully-synthetic — *giả lập integrative theo Hill*). Điểm chung: lời counselor mô phỏng/ghi lại **giao thức trị liệu tường minh**.
- Bậc giữa (2.48–2.92): kokorochat (real role-play nghề), kmi (fully-synthetic MI — bị ASCQ 1.958 kéo xuống), psydial (semi-real — counselor thật kênh text TQ, phong cách ngắn-hỗ trợ).
- Bậc đáy (1.80–2.32): toàn bộ nhóm **semi-synthetic** (smile 2.321, cpsycoun 2.285, soulchat 2.191) + esconv (real peer support 1.798).
Trung bình nhóm chính thức (`_agg_group_means_official.csv`): fully-synthetic **3.072** > semi-real 2.890 > real 2.693 > semi-synthetic **2.265**.

### 5.2. Hồi quy provenance có kiểm soát độ dài (góc "synthetic inflation"; `_agg_provenance_regression_official.csv`)
OLS mức record (n=2,111; cảnh báo pseudo-replication vì provenance là thuộc tính dataset): Overall ~ log(tokens) + provenance → R²=0.180; hệ số log-token ≈ **−0.019 (không đáng kể)** — Dim A gần như miễn nhiễm độ dài; so với real: semi-real **+0.218**, fully-synthetic **+0.387**, semi-synthetic **−0.427**. Hai cách đọc buộc phải nêu song song: (a) đọc "thật": dữ liệu fully-synthetic mô phỏng giao thức chuyên nghiệp nên được chấm cao hơn peer-support thật; (b) đọc "bias": judge LLM ưa văn phong giao thức mượt của LLM (BC-3D §2.5 giới hạn 2: "mọi kết quả 'tổng hợp tốt hơn thật' phải bị nghi ngờ trước tiên"; BC-EVAL: self-preference bias có thật). Thiết kế hiện tại **không tách được hai cách đọc** — cần thí nghiệm judge chéo họ (§7).

### 5.3. Phương sai, đuôi phân phối và "chữ ký" provenance
SD trung bình nhóm (nguồn: lệnh nhóm lần 2): semi-real 0.736 (annomi 1.079 + psydial 0.392) > real 0.581 > semi-synthetic 0.389 > fully-synthetic 0.298. Nhất quán BC-DATA (§4.3: dữ liệu máy đồng nhất hóa) và BC-EVAL/[E7] (Syn–Syn 0.215 vs Real–Real 0.015): **mức độ LLM chạm vào lời thoại tỉ lệ nghịch với biên độ chất lượng**. Đuôi phân phối: chỉ annomi (46.4%) và psy_insight (27.5%) có tỷ lệ record ≥4 đáng kể — hai nguồn "mẫu đáng học" (một trình diễn chuyên gia, một sách chuyên môn); fully-synthetic hầu như không có record ≥4 (cactus 1.0%, simpsydial 0.0%) dù trung bình cao — "sự tầm thường đồng đều".

### 5.4. Hiệu ứng độ dài và thiên vị verbosity (góc Q1 bổ sung; `_agg_verbosity_bias.csv`)
Trong nội bộ dataset, tương quan Overall × token *counselor*: pooled ≈ **0.044** (gần 0); theo dataset: dương ở nhóm người-viết (kokorochat 0.418, psy_insight 0.302, annomi 0.282), âm/nil ở nhóm LLM-viết (smile −0.234, simpsydial −0.113). → **Judge Dim A không thưởng độ dài lượt counselor một cách máy móc** (khớp BC-EVAL 3.2.f: MindEval ép ≤4 câu/lượt thì điểm TĂNG); tương quan dương ở dữ liệu người phản ánh phiên giàu nội dung hơn, không phải verbosity bias.

### 5.5. Tin cậy giữa judge và độ ổn định hạng (giữ nguyên + bổ sung)
Krippendorff α theo dataset 0.520–0.834; pooled Pearson từng cặp 0.652–0.714; bias cố định gpt +0.35–0.40 (bản trước). Bổ sung: **Kendall τ giữa bảng xếp hạng dataset của từng judge = 0.891–0.927** (`_agg_rank_stability.csv`) — thứ hạng gần như bất biến theo judge; đúng khuyến nghị BC-3D (nhiệm vụ xếp hạng đáng tin hơn nhiệm vụ cho điểm). Kiểm tra "sân nhà": gpt chấm simpsydial (+0.375 so với claude) và cactus (+0.293) cao hơn rõ so với mức bias trung bình của gpt — dấu hiệu nhẹ của self-preference cùng họ generator (simpsydial/cactus sinh bằng GPT-4/4o), chưa kết luận được vì thiếu thiết kế chéo (§7.1).

### 5.6. Cấu trúc nhân tố 5 trục (góc Q1 bổ sung; `_agg_dimA_metric_intercorr.csv`)
Tương quan giữa 5 trục (pooled-z nội dataset, judge-mean, n≈2,111): CAC↔AR **0.936**, AR↔TRA 0.862, CAC↔TRA 0.832; EPC và ASCQ tách hơn (0.540–0.716). Cronbach α (5 trục) = **0.928**. Kết luận đo lường: 5 trục thực tế đo **một nhân tố "chất lượng lâm sàng chung" (CAC–AR–TRA) + hai trục bán độc lập (EPC, ASCQ)**. CAC và AR trùng lặp tới mức có thể gộp mà gần như không mất thông tin. Đề xuất cắt tỉa: rubric 3 thành phần (Lâm sàng chung, Ranh giới đạo đức, LLMness) giảm ~40% chi phí judge — nhưng lưu ý đối trọng: theo BC-EVAL, TRA là trục có validity judge–người thấp nhất (τ=0.172) nên "nhân tố chung" nên neo vào CAC.

### 5.7. Sức phân biệt và hiệu ứng trần (`_agg_discriminative_power.csv`)
Between-dataset SD / range của trung bình dataset: EPC 0.747/2.498 và ASCQ 0.695/2.235 là hai trục **phân biệt dataset mạnh nhất**; CAC/AR/TRA 0.536–0.593/1.508–1.723. Không có hiệu ứng trần ở Dim A (0–0.05% record đạt ≥5.5/6; grand mean 2.5–3.2 nằm giữa thang). → Khác hẳn Dim B (xem file 02 §5.6): Dim A còn nhiều "khoảng đo" phía trên — phù hợp phát hiện của BC-EVAL rằng thang này được calibrate "đa số 2–4, hiếm 5–6".

## 6. Kết luận & insight của Dim A (viết lại theo lý thuyết mới)

1. **Dim A là máy dò "giao thức chuyên nghiệp", không phải máy dò "tính thật"**: xếp hạng đi theo mức độ lời counselor tuân theo giao thức trị liệu tường minh (MI trình diễn, CBT có planning, ca sách chuyên môn) chứ không theo trục real↔synthetic của BC-DATA; nhóm semi-synthetic (viết lại từ QA — hạt giống là lời khuyên đại chúng) đội sổ bất kể kỹ thuật viết lại. Đây là dạng bằng chứng trực giao mới bổ sung cho BC-3D §2.3: chiều lâm sàng và chiều provenance không đo cùng một thứ.
2. **"Hạt giống quyết định trần"**: semi-synthetic thấp hơn real 0.427 điểm sau kiểm soát độ dài — viết lại bằng LLM thêm trôi chảy nhưng không thêm kỹ năng lâm sàng vốn không có trong nguồn; ngược lại fully-synthetic mô phỏng thẳng giao thức chuyên gia nên vượt real +0.387. Bài học thiết kế cho tiếng Việt: **nếu dùng đường viết lại, nguồn phải là chuyên gia; nếu nguồn đại chúng, thà mô phỏng có planning còn hơn** (nhất quán nguyên tắc 2 và 3 của BC-3D §3.1).
3. **Biên độ chất lượng là tài sản riêng của dữ liệu người-viết**: chỉ annomi/psy_insight có đuôi ≥4 đáng kể; mọi pipeline LLM nén phân phối (SD nhóm 0.298–0.389). Dataset huấn luyện cần cả mẫu xuất sắc lẫn mẫu thất bại — điều fully-synthetic hiện không cung cấp.
4. **ASCQ hoạt động đúng như thiết kế** (trục "LLMness" của BC-EVAL): cao nhất ở lời người trình diễn (annomi 3.938), thấp nhất ở LLM sinh có khuôn (kmi 1.958). ASCQ + EPC là hai trục phân biệt dataset mạnh nhất; cụm CAC–AR–TRA có thể gộp (α=0.928, CAC↔AR=0.936).
5. **Điểm tuyệt đối phải đọc dè dặt, thứ hạng thì tin được**: τ giữa judge 0.891–0.927, giữa cấu hình 0.810–0.905, pilot–full 0.818; trong khi mức điểm lệch theo judge (gpt +0.35–0.40) và có dấu hiệu self-preference nhẹ với dataset cùng họ GPT. Đúng khuyến nghị "đọc tương đối, cấp phân bố" của BC-3D §2.6.
6. **Ba vùng mù khai báo**: không đo khủng hoảng (Safety bị loại từ gốc — BC-3D giới hạn 4); TRA validity thấp; rubric neo chuẩn APA Bắc Mỹ — dùng cho tiếng Việt phải neo lại quy điều đạo đức nghề trong nước (BC-3D Bảng 3.2, công cụ 3).

## 7. Luận điểm bổ sung & góc phân tích chưa khai thác

1. **Ma trận chéo generator × judge** (giữ từ bản trước, nay cấp thiết hơn): dấu hiệu self-preference ở §5.5 cần thí nghiệm chấm lại mẫu simpsydial/cactus bằng judge ngoài họ GPT/Claude (vd. Gemini làm chuẩn) để tách "chất lượng thật" khỏi "thiên vị văn phong cùng họ" — đúng khuôn kiểm tra bias của BC-EVAL 3.2.
2. **Thí nghiệm "cùng nội dung, khác ngôn ngữ"**: dịch 50 record annomi sang Việt/Trung rồi chấm S3 để tách language bias khỏi dataset effect — thiết kế tách một phần confound provenance×ngôn ngữ (góc Q1 #4; hiện **không đủ bằng chứng** để tách bằng dữ liệu sẵn có vì mọi dataset ZH đều thuộc nhóm semi-synthetic/fully-synthetic và toàn bộ nhóm real là EN/JA — cần dữ liệu bổ sung như đề xuất).
3. **Chấm mức giai đoạn phiên**: rubric hiện chấm cả phiên; chấm theo 3 đoạn (mở–giữa–kết) sẽ định vị lỗi giao thức nằm ở đâu (vd. thiếu khám phá ở đoạn mở hay thiếu kế hoạch ở đoạn kết) — chi phí thấp, tái dùng pipeline.
4. **Đã thực hiện từ đề xuất bản trước**: phân tích nhân tố 5 trục (→ §5.6, có kết quả); kiểm tra verbosity (→ §5.4, không có bias); đuôi phân phối làm tiêu chí chọn dữ liệu SFT (giữ nguyên đề xuất: lấy top-quartile theo judge-mean; với 11 dataset hiện tại, nguồn mẫu ≥4 gần như chỉ có annomi + psy_insight).
5. **Nối Dim A với downstream** (BC-3D giới hạn 5): điểm Dim A mô tả dữ liệu, chưa chứng minh giá trị huấn luyện; đề xuất thử nghiệm SFT nhỏ trên top-quartile vs full của 1–2 dataset để kiểm "chiều mô tả → giá trị huấn luyện" — hiện **không đủ bằng chứng** trong phạm vi dữ liệu này.

## 8. Nguồn minh chứng
- Số liệu (không đổi so bản trước): 99 file `.jsonl` pilot + 33 file full trong `experiments/dim_a_mind_eval/`; bảng chốt `_stats/dimA_*.csv`; record trích dẫn: `annomi_20`, `annomi_69`, `esconv_90` (file `*_S3_*_full_judgments.jsonl` tương ứng).
- Bảng mới lần 2 (tính từ số liệu đã chốt): `_agg_dimA_metric_intercorr.csv`, `_agg_discriminative_power.csv`, `_agg_rank_stability.csv`, `_agg_verbosity_bias.csv`, `_agg_provenance_regression_official.csv`, `_agg_group_means_official.csv`.
- Lý thuyết: BC-EVAL mục 3.2 (MindEval: 5 trục, thang, meta-evaluation, self-preference, độ dài), Phần 4 (3 tầng, trực giao); BC-DATA §1.3 + Bảng 2.1 (provenance 4 nhóm), §4.3 (chữ ký cấu trúc); BC-3D §2.5 (5 giới hạn), §2.6 (4 điều kiện vận hành), §3.1 (5 nguyên tắc), Bảng 3.2 (Việt hóa rubric). Tóm tắt: `_notes/theory_word_11dataset_tomtat.md`.
- Giới hạn khai báo: BT1–BT5, BT13, BT19 (file 00 §7); hồi quy provenance mang pseudo-replication; không có neo chuyên gia người cho chính thí nghiệm này.
