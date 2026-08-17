# BƯỚC 3 — PHÂN TÍCH SÂU DIM C (UED: ĐỘNG HỌC CẢM XÚC) — BẢN CẬP NHẬT LÝ THUYẾT

## THAY ĐỔI SO VỚI BẢN TRƯỚC
(1) Phần lý thuyết (mục 1, 6, 7) viết lại theo BC-EVAL (mục 3.3–3.5: UED là "góc nhìn 3 — động học cảm xúc", với [E6] là "giấy chứng nhận đo lường" và [E7] là bài đánh giá dataset mẫu mực) và BC-3D (điều kiện vận hành của chiều cảm xúc: **chỉ đọc cấp phân bố, bắt buộc có mốc thật cùng kênh cùng ngôn ngữ**). (2) **Số liệu thực nghiệm giữ nguyên 100%** (không chạy lại). (3) Nhãn provenance cập nhật theo BC-DATA — thay đổi diễn giải lớn nhất: psy_insight (real-xuất bản, **đa phiên**) và annomi (semi-real trình diễn). (4) Bổ sung: lưỡng phân "ai viết lời counselor", đối chiếu nhóm chính thức, và lý giải mới cho psy_insight. Kết luận đổi: **§6.0**.

> Phạm vi dữ liệu: `experiments/dim_c/dim_c_A_full_0629/` (cấu hình A: văn bản gốc + lexicon NRC-VAD bản ngữ) và `dim_c_B_full_0629/` (B: bản dịch EN + NRC-VAD v2.1 EN); 200 record/dataset (annomi 112), n_valid theo file 00 §4.4. Trọng tâm valence client. Số liệu: `_stats/dimC_*`, `_agg_*.csv`.

## 1. Tổng quan khung đánh giá và liên hệ cách xây dựng dataset (theo BC-EVAL, BC-3D, BC-DATA)

### 1.1. Vị trí của Dim C trong 3 góc nhìn (BC-EVAL Phần 1, 4)
Dim C đo **tầng cảm xúc** — "nguyên liệu của trị liệu và dấu vân tay của tính chân thực": quỹ đạo (arc), biến thiên, phản ứng (rise), điều hòa (recovery) qua lời nói, tính bằng lexicon NRC-VAD với cửa sổ trượt 10 từ, **không cần nhãn, không cần model** ([E5]). Chuỗi thẩm định 3 bài (BC-EVAL 3.3–3.5): [E5] lập khung và bảng chuẩn trên 2,687 nhân vật phim; [E6] cấp "giấy chứng nhận đo lường" — arc lexicon đạt tương quan >0.9 với arc vàng khi **bin ≥ 50**, lexicon dịch đạt giữa-0.90s từ **bin 200** ở ngôn ngữ ít tài nguyên; [E7] là **bài đánh giá dataset thuần túy đầu tiên** — so RealCBT (76 phiên thật) với CACTUS bằng đúng bộ chỉ số này và phát hiện khiếm khuyết mà lọc CTRS + đánh giá người AMT không thấy (biến thiên arousal r=0.84; arc Real–Syn ≈ 0; Syn–Syn 0.215 vs Real–Real 0.015 — "một khuôn cảm xúc chung").
Điều kiện vận hành bắt buộc (BC-3D §2.4 Bảng 2.3, §2.5 giới hạn 3): (i) **không chấm từng phiên** — chỉ so PHÂN BỐ toàn dataset với mốc thật (Mann–Whitney + effect size); (ii) **mốc thật phải cùng kênh, cùng ngôn ngữ** (76 phiên đủ); (iii) lexicon dịch phải thẩm định người bản ngữ trên mẫu nhỏ; (iv) hạn chế cố hữu: không xét phủ định/mỉa mai.

### 1.2. Trạng thái định nghĩa metric (giữ nguyên + đối chiếu nguồn mới)
Bộ chỉ số có nguồn lý thuyết: emo_mean, variability (emo_std), displacement (count/length), peak_dist, rise_rate, recovery_rate ([E5]; [E7] §4 — bảng chi tiết: file 00 §3). **`nec`, `first/last_mean`, `happy_ending`, `variability_ratio`, `lex_coverage`, `arc_length`, phân tách low/high: KHÔNG có trong cả BC-EVAL lẫn 3 paper nguồn** — vẫn là phần mở rộng vận hành của pipeline, đã kiểm chứng số học 100% trên dữ liệu (NEC = last−first; happy = NEC>0; var_ratio = std client/counselor). Khi công bố: trình bày như đóng góp riêng có kiểm chứng, không gán cho nguồn.

### 1.3. Liên hệ provenance chính thức (BC-DATA §1.3) và kỳ vọng lý thuyết
Kỳ vọng từ [E7] + BC-DATA §4.3: dữ liệu càng nhiều LLM viết lời → tông cảm xúc cao hơn ("bốc" để trông thấu cảm), biến thiên thấp hơn, client "ngoan" (rise/recovery mượt), kết cục lạc quan hóa. Hai cơ chế định hình từ khâu xây dựng cần nhớ khi đọc: ESConv **lọc đầu ra theo thành công cảm xúc** (auto-approval yêu cầu intensity giảm — BC-DATA mục ESConv) → NEC dương là thuộc tính thiết kế; nhóm semi-synthetic ép giọng "an ủi, công nhận" trong prompt (SoulChat). Điểm mới từ BC-DATA cho Dim C: **psy_insight là ca đa phiên** (951 phiên/189 ca) bị pipeline cắt thành phiên rời → kỳ vọng arc phẳng ở đơn vị phiên (kiểm chứng §5.2).

## 2. Tổng hợp kết quả đánh giá (GIỮ NGUYÊN số liệu — cấu hình B)

Bảng đầy đủ: bản trước / `_stats/dimC_B_key_table.csv`. Các mốc chính (client, valence): NEC từ −0.000 (psy_insight) đến 0.086 (smile); happy_ending 49.6% (psy_insight) → **88.0% (simpsydial)**; emo_std 0.117–0.144; lex_coverage 0.655–0.708; n_high_displacements > n_low ở 11/11; variability_ratio >1 ở 10/11 (ngoại lệ soulchat 0.991); counselor emo_mean: annomi thấp nhất 0.138, simpsydial cao nhất 0.198.

## 3. Đánh giá chéo cấu hình A vs B (GIỮ NGUYÊN số liệu; đối chiếu [E6] qua BC-EVAL)

Số liệu không đổi (`_stats/dimC_AB_paired_diffs.csv`, `extra_checks.txt`): 4 dataset EN identical A≡B; 7 dataset non-EN: lex_coverage sụt 0.66–0.71 → **0.23–0.31**; emo_std ≈ ×2; NEC đổi dấu âm ở 5/7; happy_ending giảm 17.6–54.5 điểm %; tương quan A↔B mức record chỉ 0.071–0.416; bằng chứng cơ chế: r(coverage, emo_std) = **−0.455** (p≈7×10⁻⁷², n=1,398).
Đối chiếu lý thuyết (BC-EVAL 3.4): [E6] chứng minh lexicon dịch chỉ đáng tin từ bin lớn (≥200 instance cho ngôn ngữ xa) — cửa sổ 10 từ với coverage 26% (≈2.6 từ khớp/cửa sổ) nằm rất sâu trong vùng không tin cậy → **các metric động của cấu hình A là nhiễu lấy mẫu thưa, không phải tâm lý**; cấu hình B là nền so sánh hợp lệ duy nhất, với thiên lệch riêng đã khai báo (dịch máy "làm phẳng" — bài học KMI trong BC-DATA). Kết luận phương pháp giữ nguyên: **B chính, A làm phân tích độ nhạy** — và là minh chứng thực nghiệm quy mô 11-dataset cho khuyến nghị của [E6]/BC-3D về lexicon tiếng Việt (mục 7.5, file 04 §5).

## 4. Vai trò "pilot"/kiểm chứng cấu hình (GIỮ NGUYÊN)

Dim C không có pha pilot riêng (BT16: file bên trong đặt tên `*_pilot*` nhưng là full-run duy nhất); cặp A/B đóng vai trò phân tích độ nhạy và cho kết quả **phân kỳ mạnh** → buộc chọn cấu hình chính có biện luận (mục 3). Bài học phương pháp giữ nguyên: lựa chọn ngôn ngữ tối ưu phụ thuộc **loại công cụ đo** — LLM-judge đa ngữ thì giữ bản gốc (S3); công cụ lexicon thưa thì dịch sang ngôn ngữ giàu tài nguyên (B) — không có lựa chọn đúng phổ quát. Đây chính là dạng "meta-evaluation từng công cụ cho đúng chiều đó" mà BC-3D §2.6 (điều kiện 2) yêu cầu.

## 5. Phân tích sâu trên full (số liệu giữ nguyên; diễn giải theo taxonomy mới)

### 5.1. Gradient "kịch bản hóa kết thúc có hậu" — đọc lại theo nhóm chính thức
Trung bình nhóm (`_agg_group_means_official.csv`): happy_ending — fully-synthetic **78.3%** > semi-real 77.1% > semi-synthetic 71.9% > real **69.1%**; NEC — fully-synthetic 0.070 > semi-synthetic 0.061 > real 0.048 ≈ semi-real 0.046; counselor tone — fully-synthetic 0.187 ≈ semi-synthetic 0.183 > real 0.165 ≈ semi-real 0.161. Lát cắt sạch hơn là **lưỡng phân "ai viết lời counselor"** (`_agg_counselor_words_dichotomy.csv`): nhóm LLM-viết (6 dataset) vs người-viết (5 dataset): counselor tone **0.185 vs 0.164**; client NEC **0.066 vs 0.047**; happy 75.2% vs 72.0%. → Tái lập độc lập, trên 11 dataset đa ngôn ngữ, phát hiện "elevated tone" của [E7] (counselor synthetic 0.3067 vs real 0.2302 trên RealCBT/CACTUS): **vân tay cảm xúc đi theo bàn tay LLM trên lời thoại, không đi theo nhãn real/synthetic trừu tượng**. Lưu ý trung thực: khoảng cách tuyệt đối ở đây (~0.02) nhỏ hơn nhiều so với [E7] (~0.08) — so sánh chéo dataset đa chủ đề/ngôn ngữ pha loãng tín hiệu so với thiết kế khớp phân bố của [E7].

### 5.2. psy_insight — arc phẳng nay ĐÃ CÓ lời giải lý thuyết
Bản trước ghi nhận chuỗi bất thường (NEC ≈ −0.000; happy 49.6% ≈ ngẫu nhiên; 59/200 NaN; client TB 77 token) và nghi "dataset bị cắt cụt — không xác định được từ nguồn". BC-DATA nay xác nhận: **Psy-Insight gồm 189 CA đa phiên tách thành 951 phiên** — pipeline lấy mẫu phiên rời khỏi ca. Hệ quả: (i) đơn vị "phiên giữa liệu trình" không có cấu trúc mở–kết cảm xúc trọn vẹn → NEC ≈ 0 là **thuộc tính đơn vị phân tích**, không phải khuyết tật dữ liệu; (ii) đây là bằng chứng thực nghiệm đầu tiên trong nghiên cứu này rằng **UED cấp phiên không đọc được tiến triển xuyên phiên** — đúng khoảng trống "đa phiên + kết cục" mà BC-3D §3.3 (xu hướng 7) nêu; (iii) muốn đo Psy-Insight đúng, phải nối phiên theo ca và tính NEC xuyên ca — đề xuất ở §7.

### 5.3–5.5. Các phát hiện giữ nguyên (tóm tắt, số liệu như bản trước)
- **Biến thiên không tách real/synthetic ở so sánh chéo dataset** (annomi emo_std 0.133 nằm giữa dải): tín hiệu "real biến thiên hơn" của [E7] chỉ hiện khi kiểm soát chủ đề — giới hạn khả chuyển của finding, đồng thời củng cố nguyên tắc "so phân bố với mốc CÙNG KÊNH" (BC-3D).
- **esconv NEC cao (0.082) do lọc thành công từ thiết kế** (BC-DATA); **variability_ratio >1** ở 10/11 (client dao động hơn counselor — đúng phân vai); **soulchat 0.991** — counselor dao động ngang client, dấu semi-synthetic giọng cảm thán.
- **Ghép nối client–counselor**: record-level client NEC × counselor tone ≈ 0.024 (nil) nhưng dataset-level đồng biến → tương quan cấp dataset là **phong cách sinh**, không phải hiệu quả trị liệu (ecological fallacy nếu đọc nhầm cấp).

## 6. Kết luận & insight của Dim C

### §6.0. KẾT LUẬN NÀO THAY ĐỔI SO VỚI BẢN TRƯỚC
1. **psy_insight được "minh oan"**: arc phẳng là hệ quả của đơn vị phân tích (phiên tách khỏi ca đa phiên — BC-DATA), không còn là "nghi ngờ dataset cắt cụt"; đây trở thành phát hiện về GIỚI HẠN KHUNG ĐO thay vì về dataset.
2. **Trục diễn giải chính đổi từ "real→simulator" sang "ai viết lời thoại"**: gradient tông/NEC/happy đi theo lưỡng phân human-viết vs LLM-viết (0.164/0.047 vs 0.185/0.066) — nhóm semi-real (annomi + psydial, lời counselor người) đứng về phía human dù chứa LLM ở phía client.
3. Kết luận giữ nguyên: cấu hình B làm chính; lexicon thưa gây nhiễu (r=−0.455); NEC/happy là mở rộng vận hành; UED gần trực giao với Dim A (−0.03) và chỉ chạm nhẹ Dim B record-level (0.172) — NHƯNG bổ sung mới từ Dim B đầy đủ: **ở cấp dataset, B↔happy ρ=0.724 (p=0.012)** → Dim C không còn "độc lập tuyệt đối" với Dim B ở cấp dataset; cụm "liên minh cao + kết vui" là một triệu chứng chung của kịch bản hóa (phân tích ở file 02 §5.3 và file 04 §1).

### Insight chính
1. **UED là chiều rẻ nhất và khó "diễn" nhất trong bộ 3**: không judge, không nhãn ([E5]); dữ liệu LLM lộ vân tay ngay cả khi qua mặt CTRS/AMT ([E7]) và WAI (file 02). Trong khung "3+2" của BC-3D, đây là chiều nên chạy SỚM (sau chiều cấu trúc) trong cổng QC.
2. **Điều kiện tiên quyết không thể bỏ: mốc thật cùng kênh cùng ngôn ngữ** — hiện nghiên cứu này chưa có mốc như vậy cho từng ngôn ngữ (annomi là trình diễn EN; kokorochat là role-play JA) → mọi kết luận Dim C ở đây là SO SÁNH NỘI BỘ giữa 11 dataset, chưa phải "đối chiếu với trị liệu thật" đúng nghĩa [E7]. Với tiếng Việt: Tầng 0 (PsyTest-VN) phải có trước khi Dim C-VN có nghĩa.
3. **Coverage là biến số phải công bố kèm mọi kết quả UED** (bằng chứng r=−0.455); và UED cần độ dài tối thiểu (psy_insight 29.5% NaN khi client <~100 token).

## 7. Luận điểm bổ sung & góc phân tích chưa khai thác

1. **NEC xuyên phiên cho dữ liệu đa phiên** (mới, từ §5.2): nối 951 phiên psy_insight theo 189 ca (nếu metadata ca có trong dataset gốc) và tính NEC cấp CA — biến giới hạn thành thí nghiệm đầu tiên về "đo tiến triển cảm xúc xuyên phiên", đúng biên giới BC-3D xu hướng 7. **Không đủ dữ liệu trong bản trích hiện tại** (200 record không kèm mã ca) — cần bổ sung trường case-id khi trích lại.
2. **Chỉ số Syn–Syn chống đồng nhất hóa** ([E7]; BC-3D "còi báo mode-collapse"): cần chuỗi arc từng phiên để tính tương quan cặp arc — pipeline hiện chỉ xuất thống kê tổng hợp. Đề xuất: xuất thêm chuỗi arc (mảng giá trị cửa sổ) → tính Real–Real/Syn–Syn/Real–Syn cho 11 dataset; hiện **không đủ dữ liệu**.
3. **Trim nghi thức chào–kết trước khi tính NEC** (giữ từ bản trước, nay thêm căn cứ văn hóa: nghi thức lịch sự dày ở ZH/JA/KO/VN): tính lại NEC sau khi cắt k token cuối (k=10–30); nếu thứ hạng happy% đảo → hạ cấp kết luận §5.1.
4. **Khai thác dominance như chỉ số empowerment** (giữ nguyên): client dominance-NEC là ứng viên đo "làm chủ" — mục tiêu trị liệu đích thực.
5. **Hồ sơ "vân tay người-viết" làm dải tham chiếu khi xây dataset VN**: bộ (counselor tone ≤0.17; NEC 0.03–0.05; happy 60–75%; var_ratio >1; std client ≥ counselor) từ nhóm human-viết của nghiên cứu này — dùng làm ngưỡng sàng cho lớp dữ liệu sinh tự động (Tầng 2/3 kiến trúc BC-3D).

## 8. Nguồn minh chứng
- Dữ liệu (không đổi): 22 file CSV trong `experiments/dim_c/dim_c_{A,B}_full_0629/`; bảng chốt `_stats/dimC_*.csv`; record NaN minh họa: `annomi_59`, `smile_15`, `psyinsight_000820` (`_stats/dimC_nan_diagnostics.csv`); kiểm chứng NEC/happy/var_ratio + r(coverage,std): `_stats/extra_checks.txt` và lệnh in phiên trước (r=−0.455, p=7.3×10⁻⁷²).
- Bảng mới lần 2: `_agg_group_means_official.csv`, `_agg_counselor_words_dichotomy.csv`, `_agg_crossdim_dataset_rankcorr.csv`, `_agg_crossdim_MTMM_pooled.csv`.
- Lý thuyết: BC-EVAL mục 3.3 ([E5] UED + bảng chuẩn), 3.4 ([E6] bin/lexicon dịch; "giới hạn granularity nhỏ"), 3.5 ([E7] RealCBT vs CACTUS: r=0.84, Syn–Syn 0.215, elevated tone), Phần 4 (3 tầng, cách bù giới hạn); BC-DATA §1.3/Bảng 2.1 (provenance; **Psy-Insight 951 phiên/189 ca**), mục ESConv (lọc thành công), §4.3 (chữ ký cấu trúc); BC-3D Bảng 2.3 (điều kiện chiều 3), §2.5 giới hạn 3, §3.3 xu hướng 6–7, Bảng 3.2 (lexicon VN). Tóm tắt: `_notes/theory_word_11dataset_tomtat.md`.
- Giới hạn khai báo: BT7, BT12, BT14, BT16, BT19 (file 00 §7); NEC/happy không có nguồn lý thuyết; thiếu mốc thật cùng kênh; thiếu chuỗi arc và mã ca để chạy góc 7.1–7.2.
