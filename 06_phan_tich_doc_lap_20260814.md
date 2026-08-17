# PHÂN TÍCH ĐỘC LẬP KẾT QUẢ ĐÁNH GIÁ 3 CHIỀU — 11 DATASET (14/08/2026)

**Vị trí tài liệu.** Đây là lượt phân tích độc lập, chạy lại **từ dữ liệu JSONL/CSV gốc** (không dùng số trung gian của các vòng trước), nhằm (i) kiểm chứng chéo các kết luận đã có trong 00–05, (ii) bổ sung phát hiện mới. Nguồn dữ liệu: `code/mind-eval/data/<DS>/results/{mind_eval,wai}/*_S3_*full*.jsonl` (dim A, dim B — folder code đầy đủ hơn folder experiments vì chứa cả 4 file claude WAI mà `D:\vy\jsonl\` không còn) và `experiments/dim_c/dim_c_{A,B}_full_0629/` (dim C). Toàn bộ script + bảng số tại `_doclap_20260814/` (chạy `s1→s5`, mọi con số tái lập được; các assert đều PASS).

---

## 0. KIỂM KÊ ĐÃ XÁC NHẬN (assert PASS 100%)

- **Dim A (MindEval, 1–6):** 6.333 record = 3 judge (claude, gemini, gpt) × 2.111 hội thoại (annomi 112, smile 199, 9 dataset còn lại 200). 0 điểm null; `Overall = trung bình 5 tiểu thang` đúng 100%.
- **Dim B (WAI-O-S, 1–5):** 6.333 record đối xứng với dim A; 168 điểm item None **toàn bộ thuộc judge claude** (khớp đúng tổng BT10+BT18 của vòng trước: 24+36+12+72+12+12); `total = trung bình 3 chiều` đúng 99,78% (phần lệch là các record có item None).
- **Dim C (UED/NRC-VAD):** cấu hình A 2.037 record hợp lệ, cấu hình B 2.031 (psy_insight 141, cpsycoun 188/182, annomi 110, smile 198 — khớp kiểm kê 00).
- **Join 3 chiều:** A∩B = 2.111/2.111 (100%); C dư đúng 1 record `smile_74` không có ở A/B.
- Đối chiếu với các bảng vòng trước (`_agg_*`, `_r5_*`): mọi số kiểm tra đều khớp (A↔B ρ=0,182; B↔happy 0,724; B↔NEC 0,655; MTMM A↔B ≈ 0,38; TRA↔WAI ≈ 0,48–0,50 tuỳ cách pooling; η² cùng thứ bậc). **Pipeline cũ tái lập được hoàn toàn.**

---

## 1. BỨC TRANH TỪNG CHIỀU

### 1.1. Dim A — thước đo "giống chuyên gia" có sức phân biệt mạnh nhất, nhưng toàn phổ nằm dưới trần

| Hạng | Dataset | Overall (TB 3 judge) | SD nội DS | %<3 | %≥4 | Provenance |
|---|---|---|---|---|---|---|
| 1 | annomi | 3,621 | 1,079 | 27,7 | 46,4 | semi-real |
| 2 | cactus | 3,376 | 0,267 | 8,5 | 1,0 | fully-synthetic |
| 3 | psy_insight | 3,364 | 0,886 | 30,0 | 27,5 | real |
| 4 | simpsydial | 3,188 | 0,362 | 23,5 | 0,0 | fully-synthetic |
| 5 | kokorochat | 2,917 | 0,497 | 53,5 | 1,0 | real |
| 6 | kmi | 2,653 | 0,265 | 91,0 | 0,0 | fully-synthetic |
| 7 | psydial | 2,481 | 0,392 | 92,0 | 0,0 | semi-real |
| 8 | smile | 2,321 | 0,422 | 95,0 | 0,0 | semi-synthetic |
| 9 | cpsycoun | 2,285 | 0,412 | 95,0 | 0,0 | semi-synthetic |
| 10 | soulchat | 2,191 | 0,332 | 99,0 | 0,0 | semi-synthetic |
| 11 | esconv | 1,798 | 0,359 | 100,0 | 0,0 | real |

- Không dataset nào vượt 3,7/6; 8/11 dataset có ≥91% hội thoại dưới mức "acceptable" (3). Theo anchor MindEval (đa số hội thoại người thật rơi 2–4), phân bố này nhất quán với thiết kế rubric, không phải lỗi chấm.
- **Halo mạnh trong rubric:** CAC↔AR r=0,941 (pooled within-dataset) — hai trục gần như một; ASCQ tách biệt nhất (r 0,56–0,72). Số chiều hữu hiệu của dim A ~2–3, không phải 5.
- **Nén phân phối theo bàn tay LLM:** SD nội dataset của nhóm máy-viết 0,265–0,422; của annomi/psy_insight (người thật, nội dung chuyên gia) 0,886–1,079. Fully-synthetic gần như không có đuôi: chỉ 0,5% record <2 và 0,3% ≥4, trong khi real trải 28,3% <2 và 9,5% ≥4.

### 1.2. Dim B — WAI gần bão hòa trần; đo "bề mặt hợp tác + lượng bằng chứng", nhạy độ dài

| Hạng | Dataset | Total | Goal | Approach | Bond | %≥4 |
|---|---|---|---|---|---|---|
| 1 | simpsydial | 4,335 | 4,333 | 4,435 | 4,238 | 99,0 |
| 2 | cactus | 4,290 | 4,410 | 4,355 | 4,106 | 81,0 |
| 3 | psydial | 4,182 | 4,146 | 4,151 | 4,249 | 83,0 |
| 4 | smile | 4,166 | 4,158 | 4,158 | 4,182 | 80,4 |
| 5 | kmi | 4,088 | 4,241 | 4,084 | 3,938 | 68,0 |
| 6 | kokorochat | 4,046 | 4,053 | 3,989 | 4,095 | 65,0 |
| 7 | esconv | 4,007 | 3,910 | 4,032 | 4,079 | 62,0 |
| 8 | soulchat | 3,992 | 3,937 | 3,942 | 4,096 | 52,5 |
| 9 | annomi | 3,760 | 3,840 | 3,769 | 3,672 | 57,1 |
| 10 | psy_insight | 3,605 | 3,700 | 3,646 | 3,471 | 25,0 |
| 11 | cpsycoun | 3,418 | 3,476 | 3,238 | 3,538 | 6,5 |

- **Trần thang đo:** 80,2% toàn bộ điểm item ≥4; chỉ 2,5% ≤2. simpsydial không có hội thoại nào total <3,95 — sàn thang gần như không được dùng.
- **Item khó nhất là Q10** ("client tin năng lực counselor") — thấp nhất ở 7/11 dataset; **item dễ nhất là Q12** ("tin cậy lẫn nhau", TB 4,236). Nghĩa là: judge *mặc định* có tin cậy, nhưng đòi bằng chứng cho *năng lực* — một bất đối xứng đáng lưu khi diễn giải Bond cao.
- **Goal↔Approach r=0,908** — hai chiều gần trùng; Bond mới là chiều mang thông tin riêng (r 0,77–0,83).
- **Giao thức 3 run gần như thừa:** 81,5% điểm item có SD=0 giữa 3 run (gpt ổn định nhất 0,067) — chi phí ×3 đổi lấy rất ít phương sai thật.
- **Nhạy độ dài:** trong nội dataset, ρ(total, tokens) trung vị 0,327 (pooled 0,298); cấp dataset ρ=0,573 (p=0,066). Nhất quán cơ chế anchor "điểm = lượng bằng chứng" (BT11; vòng 05 đã ước lượng b=+0,303 cluster-robust).

### 1.3. Dim C — tín hiệu mô tả, không phải thước phân hạng; lexicon quyết định kết luận

- Cấu hình B (EN): NEC dương ở 10/11 dataset (trừ psy_insight −0,000); happy ending 49,6% (psy_insight) → 88,0% (simpsydial).
- **η² giữa-dataset chỉ 0,061–0,077** (so 0,26–0,32 của dim B và 0,47–0,57 của dim A): dim C hầu như không phân biệt dataset — đúng vai trò "so phân bố với người thật", không phải xếp hạng.
- **Hội tụ A↔B cực thấp ở cấp record** (7 dataset non-EN): r(emo_mean) 0,071–0,416; đồng thuận nhãn happy_ending 38,5–61,0% (ngang tung đồng xu). Chọn lexicon = chọn kết luận; mọi so sánh phải cố định cấu hình.

---

## 2. LIÊN CHIỀU — BA CHIỀU LÀ BA CẤU TRÚC GẦN TRỰC GIAO

### 2.1. Xếp hạng dataset gần như không chuyển nhượng giữa chiều

A↔B: ρ=0,182 (p=0,593). Các ca đảo hạng cực đoan: **annomi #1 (A) → #9 (B)**; **psy_insight #3 (A) → #10 (B)**; ngược lại **psydial #7 (A) → #3 (B)**, smile #8 → #4. Trong khi đó B↔C đồng pha: B↔happy ρ=0,724 (p=0,012), B↔NEC ρ=0,655 (p=0,029); còn A↔NEC *âm* không ý nghĩa (−0,409, p=0,212).

Ở cấp record (khử khác biệt dataset): A↔B r=0,389 — dương nhưng khiêm tốn; và phần hội tụ "đúng cấu trúc" TRA↔WAI chỉ 0,497, **nhỏ hơn nhiều** TRA↔skill_core nội dim A (0,860). Phương sai *phương pháp* (cùng rubric, cùng lượt chấm) lấn át phương sai *cấu trúc* (cùng khái niệm liên minh) — đúng tinh thần kiểm MTMM, và là lý do không được cộng gộp A+B thành một điểm duy nhất.

### 2.2. Bất đồng có hướng: "liên minh đẹp nhưng lâm sàng kém" phổ biến, chiều ngược gần như không tồn tại

Quadrant B_total ≥4 & A_overall <2,5 chiếm **20,5% toàn bộ mẫu** (433/2.111): esconv 59,5%, smile 48,2%, soulchat 39,5%, psydial 36,5%, kmi 18,0%. Quadrant ngược (A ≥3,5 & B <3,5) gần rỗng: chỉ psy_insight 8,0% và annomi 3,6%. **WAI nhìn thấy "quan hệ tốt" ở nơi MindEval thấy thất bại lâm sàng — nhưng hiếm khi ngược lại.** Hàm ý: bề mặt hợp tác (ấm áp, đồng thuận, không xung đột) là thứ dễ sản xuất — kể cả bởi peer supporter hoặc LLM — trong khi năng lực lâm sàng theo rubric là thứ khan hiếm; hai thứ phải báo cáo tách biệt.

### 2.3. Thang sức phân biệt và vai trò hợp lý của từng chiều

η² giữa-dataset: **A 0,469–0,569 → B 0,258–0,322 → C 0,061–0,077**. Ba chiều nằm ở ba "độ phóng đại" khác nhau: A phân hạng dataset, B phân hạng có điều kiện (sau khử độ dài), C mô tả vân tay phân bố.

---

## 3. PHÁT HIỆN MỚI CỦA LƯỢT NÀY (chưa có trong 00–05)

### 3.1. "Phụ phí EPC" — vân tay guardrail tách hoàn hảo người-viết / máy-viết

Định nghĩa: `EPC_premium = EPC − trung bình(CAC, AR, TRA, ASCQ)` (mức dataset).

| Dataset | EPC_premium | Lời counselor |
|---|---|---|
| esconv | **−0,233** | người viết |
| annomi | +0,060 | người viết |
| kokorochat | +0,332 | người viết |
| psy_insight | +0,341 | người viết |
| smile | +0,442 | LLM viết |
| soulchat | +0,450 | LLM viết |
| cpsycoun | +0,631 | LLM viết |
| psydial | +0,648 | LLM viết (tái tạo) |
| simpsydial | +0,755 | LLM viết |
| cactus | +0,917 | LLM viết |
| kmi | **+1,622** | LLM viết |

Tách **hoàn hảo** (max human 0,341 < min LLM 0,442), Mann–Whitney U=0, p chính xác = 0,0061 — mức ý nghĩa tối đa khả dĩ với n=4/7. Diễn giải: LLM sinh lời thoại mang sẵn guardrail an toàn (không hứa hẹn, không vượt vai, lịch sự chuẩn mực) nên EPC luôn "được điểm nền" cao hơn hẳn năng lực thực chất; người thật thì EPC đi cùng (hoặc thấp hơn) kỹ năng — thậm chí âm ở esconv vì peer supporter tự bộc lộ. **Đề xuất dùng EPC_premium làm chỉ số QC rẻ để phát hiện "chữ ký guardrail" trong dữ liệu sinh** (bên cạnh chỉ số tông counselor ở 3.3).

**ĐÍNH CHÍNH (14/08, sau khi đối chiếu bài báo r7 — xem file 07 mục 5):** bảng trên gán "psydial — LLM viết (tái tạo)" theo lưỡng phân *văn bản cuối cùng có bàn tay LLM* (4/7). Lưỡng phân **chính thức** của bài báo (Bảng 1 r7 + `_agg_counselor_words_dichotomy.csv`) xếp PsyDial vào nhóm **người viết** (counselor thật, LLM chỉ tinh chỉnh trôi chảy; thân chủ GPT-4o) → 5 human / 6 LLM. Dưới lưỡng phân chính thức này, tách không còn hoàn hảo (PsyDial +0,649 nằm trong dải LLM): Mann–Whitney U=3, **p = 0,030** — vẫn ý nghĩa nhưng yếu hơn. Điểm đáng giá nhất là **PsyDial phân ly hai vân tay**: tông counselor ở mức người (0,173) nhưng EPC_premium (+0,65) và ASCQ (2,07, thấp nhì bảng) ở mức máy → vân tay *tông* bám nội dung (giữ lời người), vân tay *EPC-premium/ASCQ* bám bề mặt văn bản (lớp LLM đánh bóng). Khi dùng làm chỉ số QC phải nêu rõ lưỡng phân nào đang áp dụng.

### 3.2. Đồng thuận judge phần lớn là hàm của độ trải điểm (range restriction)

Tương quan giữa mức đồng thuận (mean pairwise r) và SD nội dataset: dim A ρ=0,627 (p=0,039); dim B ρ=0,836 (p=0,001). Các dataset "khó chấm tin cậy" (cactus r̄=0,484; simpsydial 0,555) chính là các dataset bị nén phân phối — judge không bất đồng về chất lượng, họ chỉ không còn phương sai để đồng thuận *trên đó*. Hệ quả phương pháp: (i) không dùng inter-judge r cấp record làm bằng chứng "judge kém tin" khi phân phối nén; (ii) mọi so sánh agreement giữa dataset phải kèm SD.

### 3.3. Bias của judge đổi chiều theo công cụ — nghiêm khắc không phải thuộc tính của judge

Chuẩn hóa về % thang: claude chấm dim A ở 32,3% thang nhưng dim B ở 69,8% (+37,5 điểm); gemini 30,7% → 80,7% (**+50,0 điểm** — nghiêm nhất A, rộng rãi nhất B); gpt 39,6% → 74,4% (+34,8). Xếp hạng dataset vẫn bảo toàn tốt ở dim A (Kendall W=0,980; bỏ bất kỳ judge nào hạng đổi ≤1 bậc) nhưng kém hơn ở dim B (bỏ claude: đổi tới 3 bậc). Hàm ý: (i) tuyệt đối không so điểm thô giữa hai công cụ; (ii) panel ≥3 judge là bắt buộc cho dim B, trong khi dim A một judge đơn lẻ đã gần đủ cho mục đích *xếp hạng*.

### 3.4. Bất đối xứng quadrant (mục 2.2) và bằng chứng motif từ thinking_trace

Đếm từ khóa trong trace của claude+gemini (chỉ dấu, không phải mã hóa nội dung chặt):
- **esconv**: 83,0% record bị nêu lỗi ranh giới/tự bộc lộ; 56,5% bị gắn cờ "hallucination/claim trải nghiệm cá nhân" — đọc trace cho thấy judge đang phạt *hành vi peer-support bình thường* (kể chuyện bản thân, "I am also going through the same") vì rubric ép vai "AI therapist". Điểm A của esconv đo **độ lệch khung vai trò**, không thuần túy đo chất lượng hỗ trợ cảm xúc.
- **kmi**: 98,2% bị nêu "formulaic/máy móc" (phản xạ ~군요/네요 lặp), nhưng chính sự rón rén đó cho EPC 3,950 (hạng 2) bên cạnh ASCQ 1,958 (bét) — chân dung "an toàn nhưng rỗng".
- **soulchat/smile/cpsycoun**: 82,8–89,5% bị nêu "advice-giving/directive" — di sản viết lại từ QA một-lượt (PsyQA): trả lời như *cho lời khuyên*, không như *tham vấn tiến trình*.

---

## 4. KIỂM CHỨNG CHÉO VỚI 00–05: KHỚP, VÀ MỘT GHI CHÚ TRỌNG SỐ

1. Toàn bộ số cấp dataset và liên chiều khớp `_agg_*`/`_r5_*` (sai khác ≤0,02 do cách pooling; ví dụ MTMM A↔B: 0,375 Pearson-pooled cũ vs 0,389 Fisher-z trọng số mới — cùng kết luận).
2. Bảng nhóm provenance cũ (`_agg_group_means_official.csv`) dùng **trọng số record** (semi-real 2,890 vì psydial n=200 lấn annomi n=112); lượt này dùng **đơn vị dataset** (semi-real 3,051). Không mâu thuẫn — nhưng bài báo nên nói rõ đơn vị suy diễn là dataset (như bước 05 đã làm với permutation/jackknife) và dùng nhất quán một cách.
3. Hai "định luật provenance" của 04 (hạt giống quyết định trần; LLM quyết định vân tay) đứng vững qua phân tích độc lập; riêng vân tay LLM nay có thêm chỉ số mới EPC_premium tách hoàn hảo (3.1) bổ sung cho tông counselor (record r=0,275 p≈7e−36 của vòng 05; dataset-level lượt này: human −0,007 vs LLM +0,024, Mann–Whitney p=0,024).

---

## 5. KẾT LUẬN TỔNG VÀ HÀM Ý

**KL1 — Ba chiều là ba cấu trúc gần trực giao, bắt buộc báo cáo thành 3 hồ sơ, không composite.** A↔B ρ=0,182 (n.s.), A↔C âm n.s., B↔C dương (0,655–0,724) nhưng "C" ở đây là *tông kịch bản lạc quan* — B và C cùng bị hút bởi thứ đó, không phải cùng đo chất lượng. Gộp điểm sẽ cộng táo với cam và triệt tiêu tín hiệu ngược chiều.

**KL2 — Mỗi chiều đo một thứ hẹp hơn tên gọi của nó.** A = "độ khớp với rubric AI-therapist chuyên nghiệp" (phạt peer support lệch khung; thưởng guardrail); B = "lượng bằng chứng hợp tác quan sát được" (nhạy độ dài, trần 80% điểm ≥4, mặc-định-tin-cậy); C = "vân tay từ vựng cảm xúc" (nhạy lexicon tới mức đổi dấu kết luận). Không chiều nào là "chất lượng trị liệu" trọn nghĩa — mọi câu chữ trong bài phải thu hẹp claim tương ứng.

**KL3 — Điểm cao của dataset tổng hợp là chiến thắng của khuôn mẫu, không phải bằng chứng trị liệu tốt hơn người thật.** Fully-synthetic đứng đầu B (simpsydial 4,335; 99% ≥4) và top A (cactus #2) nhưng với phân phối nén (SD 0,18–0,27; 0,3% đạt ≥4 ở A), motif formulaic 94–98%, happy ending 88%, tông counselor sáng hơn client +0,032. Real đứng bét A (esconv) *vì sai khung chấm*, không vì vô giá trị. Bảng xếp hạng nào cũng phải đọc kèm cơ chế của thước.

**KL4 — Provenance để lại vân tay định lượng được, và nay có bộ 2 chỉ số QC rẻ:** (i) `EPC_premium` ≥ ~0,44 gợi ý văn bản lời counselor có bàn tay LLM (tách hoàn hảo p=0,0061 theo lưỡng phân "văn bản cuối"; p=0,030 theo lưỡng phân chính thức 5/6 của bài báo — xem đính chính mục 3.1); (ii) chênh tông counselor−client valence >0 hệ thống (p=0,024 cấp dataset; r=0,275 cấp record). Hai vân tay đo hai tầng khác nhau (bề mặt văn bản vs nội dung) — ca PsyDial phân ly chứng minh điều đó. Kèm chỉ dấu phụ: SD nội dataset nén (<~0,45 trên thang 6) và happy-ending >80%. Đây là đóng góp dùng được ngay khi nghiệm thu dataset tiếng Việt sinh bằng LLM.

**KL5 — LLM-as-judge dùng được cho xếp hạng, không dùng được cho điểm tuyệt đối.** Xếp hạng dataset dim A cực bền (W=0,980; leave-one-judge-out Δ≤1). Nhưng: mức điểm lệch giữa judge (gpt +0,36–0,44 so claude ở A), bias đổi chiều theo công cụ (tới +50 điểm % ở gemini), đồng thuận cấp record là hàm của range (ρ tới 0,836), và 3-run lặp lại 81,5% giá trị y hệt (ảo giác tin cậy nếu báo "3 run"). Khuyến nghị: panel 3 judge cho B, có thể 1–2 judge cho A nếu chỉ cần hạng; báo cáo điểm chuẩn hóa nội-judge (z hoặc %thang) thay vì thô khi so công cụ.

**KL6 — WAI bản hiện tại cần chống trần trước khi Việt hóa.** 80,2% item ≥4; Q12 mặc định cao; sức phân biệt một nửa dim A và phụ thuộc độ dài (ρ dataset 0,573). Ba chỉnh sửa khả thi: anchor "4/5" đòi bằng chứng cụ thể hơn (đặc biệt Bond); chấm kèm trích chứng cứ bắt buộc cho mọi điểm ≥4 (như đã bắt buộc cho ≤2); và báo cáo `residual(total | log tokens)` như metric chính thay total thô.

**KL7 — Với dataset tham vấn tiếng Việt (nối 04 §5):** giữ nguyên tắc "chuẩn hóa bộ đo trước, sinh dữ liệu sau", bổ sung cụ thể từ lượt này: (a) nghiệm thu bằng bộ 3 hồ sơ + 2 chỉ số vân tay (KL4) với ngưỡng công bố trước; (b) trộn có chủ đích các nguồn human-voiced để giữ đuôi phân phối (mục tiêu SD dim A ≥ ~0,5, tránh "đồng phục hóa" kiểu kmi/cactus); (c) nếu dùng WAI, áp gói chống trần KL6; (d) dim C tiếng Việt bắt buộc quyết định lexicon *trước* (bài học BT14/C2: r hội tụ 0,07–0,42), ưu tiên một cấu hình chuẩn + một cấu hình đối chứng báo song song.

**Giới hạn của lượt phân tích này.** (1) n=11 ở cấp dataset — mọi p cấp dataset đều thiếu power trừ hiệu ứng cực lớn (hai chỉ số ở KL4 đạt nghĩa *vì* hiệu ứng cực lớn); (2) provenance × ngôn ngữ vẫn đan xen (đã có kiểm chứng nội-ZH ở 04 §2.3 làm chỗ dựa); (3) đếm motif là keyword-matching trên trace — chỉ dấu, không thay được mã hóa nội dung; (4) trộn phiên bản model trong judge (BT1) đã được vòng trước định lượng ~0,04 điểm — nhỏ, không đảo kết luận nào ở trên; (5) điểm pilot tái dùng trong full (BT2) không ảnh hưởng các phân tích cấp full-200.

---

## PHỤ LỤC — TÁI LẬP
Scripts: `_doclap_20260814/s1_load_master.py` (nạp + assert), `s2_per_dim.py` (A/B/C), `s3_crossdim.py` (liên chiều, provenance, độ dài, η², quadrant), `s4_qualitative.py` (motif + trích trace), `s5_new_findings.py` (3 phát hiện mới + đối chiếu cũ). Bảng số: `r_A1..r_H1*.csv`, log đầy đủ `s2_report.txt`…`s5_report.txt`. Dữ liệu vào đọc nguyên trạng từ `code/mind-eval/data/` và `experiments/dim_c/`; không sửa bất kỳ file gốc nào.
