# ĐỐI CHIẾU BÀI BÁO `_r7.docx` ↔ PHÂN TÍCH ĐỘC LẬP TỪ DỮ LIỆU THÔ (14/08/2026)

**Phạm vi.** Đối chiếu TỪNG claim định lượng trong `paper_eval_llm_judges_mtmm_v1_vi_r7.docx` (bản hiện hành) với kết quả tính lại độc lập từ JSONL/CSV gốc (bộ script `_doclap_20260814/`, bổ sung `s6_verify_r7.py` + `s7_trace_levels.py` cho lượt này). Mục tiêu: (i) xác nhận khớp, (ii) liệt kê **errata** (số/nhãn sai cần sửa), (iii) đề xuất **bổ sung/loại trừ** nội dung. Mọi con số dưới đây đều in trong `s6_report.txt`/`s7_report.txt`.

**Kết luận tổng quát trước:** KHÔNG có mâu thuẫn nào ở tầng phát hiện chính. Toàn bộ khung kết luận của bài (hiệu ứng độ dài WAI; vân tay tông counselor 2 cấp + 7/7 nội-ngôn-ngữ; trực giao kỹ năng–cảm xúc; liên minh tách kỹ năng; hòa hợp kịch bản B↔kết-vui chỉ ở cấp bộ; phần thưởng provenance chỉ mô tả; nén phương sai đơn điệu; đọc theo hạng không theo điểm) **tái lập chính xác từ dữ liệu thô**. Các vấn đề tìm thấy đều ở tầng số-liệu-phụ hoặc nhãn gọi — nhưng có 1 lỗi đảo chiều claim (E5) cần sửa trước khi nộp.

---

## 1. NHỮNG GÌ ĐÃ KIỂM VÀ KHỚP CHÍNH XÁC (spot-check 20 nhóm, không sai lệch)

| Claim trong r7 | Kết quả tính lại | Phán quyết |
|---|---|---|
| Bảng 3: A/B/NEC/kết-vui/tông counselor 11 bộ | khớp toàn bộ (vd AnnoMI 3,62/3,76/+0,027/64,5%/0,138) | KHỚP |
| 6/11 bộ ≥91% hội thoại dưới mức 3 (danh sách + %) | ESConv 100/SoulChat 99/CPsyCoun 95/SMILE 95/PsyDial 92/KMI 91 | KHỚP |
| AnnoMI 46,4% ≥4 và 13,4% <2; annomi_20 = 4,8/6,0/5,2; annomi_69 = 1,0/1,0/1,3 | đúng từng số theo judge | KHỚP |
| Bảng 5: tiểu thang + %≥4 + %<3 (AnnoMI 17,0; CPsyCoun 11,5; Psy-Insight 9,5…) | khớp 11/11 hàng | KHỚP |
| Giữa-bộ/trong-bộ: A 0,587/0,479 = 1,22; B 0,286/0,415 = 0,69 | 0,587/0,479/1,22 và 0,286/0,415/0,69 | KHỚP tuyệt đối |
| Q10 đáy (AnnoMI 3,48; CPsyCoun 3,20; CACTUS 3,79); SimPsyDial "đồng thuận bước đi" 4,76 | 3,48/3,20/3,79; Q5 = 4,77 (mục cao nhất của bộ) | KHỚP (4,76→4,77 làm tròn) |
| Tông counselor: 0,185 vs 0,164; MW p = 7,3×10⁻³⁶; r = 0,275; Cliff = −0,933 (29/30 cặp); nội-EN 3/3 (0,179 vs 0,155; p 6,6e-13); nội-ZH 4/4 (0,187 vs 0,173; p 4,2e-10); cặp CPsyCoun–PsyDial "chênh không đáng kể" | 0,164/0,185; p 7,30e-36; 29/30; 3/3 p 6,5e-13; 4/4 p 4,2e-10; CPsyCoun 0,1740 vs PsyDial 0,1735 | KHỚP tuyệt đối |
| r(độ phủ, biến thiên) = −0,455, p < 10⁻⁷⁰ | −0,455, p = 7,3×10⁻⁷² | KHỚP (trừ n — xem E7) |
| Kendall τ giữa giám khảo: A 0,891–0,927; B 0,600–0,709 | A {0,927; 0,891; 0,891}; B {0,600; 0,709; 0,600} | KHỚP tuyệt đối |
| SimPsyDial: chênh Claude–GPT 0,154 dù r 0,649 | MAE 0,154; r 0,649 | KHỚP |
| Claude−Gemini trên B: −0,757 (SMILE) → −0,019 (Psy-Insight) | −0,757/−0,019 (theo cặp record đủ điểm — truy nguồn `_agg_dimB_judge_agreement_11ds.csv`) | KHỚP |
| Bảng 7 (toàn bộ 7 hàng: 0,477; 0,309/0,355; 0,375; 0,182/0,593; −0,031; −0,409/0,212; 0,172; 0,655/0,029; 0,724/0,012; 0,291; 0,573/0,066) + TRA↔kỹ-năng-lõi 0,860/0,973 | tái lập trong ±0,02 (khác biệt do cách pooling z, không đổi phán quyết ô nào) | KHỚP |
| Bảng 8 nhóm provenance (gộp mức hội thoại) + SD(A) 0,74/0,58/0,39/0,30 | khớp từng ô (lưu ý: bảng dùng trọng số record — caption đã khai báo đúng) | KHỚP |
| 6 case study 4.8 (cactus_121; kmi_712; simpsydial_463; cactus_19; soulchat_157820; esconv_43) | khớp đúng từng số A/B/NEC cả 6 ca | KHỚP tuyệt đối |
| Psy-Insight 29,5% phiên không dựng được quỹ đạo | 59/200 = 29,5% | KHỚP |

Ngoài ra: 4.1 (pilot |Δ|≤0,073; S2 sập 0,286; τ 0,810/0,905; loại Qwen; τ pilot→full 0,818/0,564) **kế thừa từ vòng r5 — không kiểm lại lượt này** (dữ liệu pilot không thuộc phạm vi chạy lại); τ pilot→full 0,564/0,818 có trong `_agg_rank_stability.csv` nhất quán nội bộ.

---

## 2. ERRATA — SỐ/NHÃN CẦN SỬA TRONG r7 (9 mục, xếp theo mức hệ trọng)

**E5 (HỆ TRỌNG NHẤT — claim bị đảo chiều). Bảng 9 hàng "Dấu hiệu tự ưu ái" + câu tương ứng trong 5.3.**
Bài viết: *"GPT chấm hai bộ sinh bằng họ GPT (SimPsyDial, CACTUS) cao hơn Claude 0,29–0,38 so với thiên lệch nền"*. Kiểm lại trên full-run: gpt−claude từng bộ (Chiều A) = CACTUS **+0,293**, SimPsyDial **+0,375**; trong khi **nền** (trung bình 9 bộ còn lại) = **+0,357**, trung vị 11 bộ = +0,375. Nghĩa là: CACTUS **thấp hơn nền 0,064**, SimPsyDial ngang nền (+0,018). Trên Chiều B còn rõ hơn: gpt−claude CACTUS +0,129, SimPsyDial +0,115 so nền +0,195 — **dưới nền**. → Không có tín hiệu tự ưu ái vượt thiên lệch nền trong dữ liệu này. Nguồn gốc lỗi: file 01 §5.5 so 0,293/0,375 với "mức bias trung bình của gpt" nhưng mức nền thật (0,35–0,40, chính bài cũng dẫn) đã bao trùm hai giá trị đó.
**Đề nghị sửa:** đảo hàng Bảng 9 thành phát hiện âm tính — "Kiểm tra phần thưởng cùng họ: gpt−claude trên hai bộ sinh bằng họ GPT (+0,29/+0,38 Chiều A) không vượt thiên lệch nền của GPT (+0,36); Chiều B thấp hơn nền — chưa phát hiện self-preference vượt nền; thiết kế chéo generator×giám khảo vẫn cần để loại trừ triệt để." Sửa câu 5.3 tương ứng. **Lợi ích phụ:** phần thưởng fully-synthetic (+0,39 A) không thể bị quy cho self-preference của GPT — claim RQ4 của bài *mạnh lên*.

**E1. 4.2: "EPC là trục cao nhất ở 10/11 bộ"** → thực tế **9/11**: AnnoMI cao nhất là ASCQ (3,94 > EPC 3,67 — chính câu sau của bài cũng nói vậy, tự mâu thuẫn), ESConv cao nhất là TRA (2,07; EPC 1,61 là trục **thấp nhất**). Sửa: "9/11" hoặc "cao nhất hoặc nhì ở 10/11 bộ; ngoại lệ đảo ngược duy nhất là ESConv, nơi EPC là trục thấp nhất".

**E2. 4.2: "Cronbach's α của cụm CAC–AR–TRA = 0,928"** → 0,928 là **α chuẩn hóa của CẢ 5 TRỤC** (từ r̄ off-diagonal = 0,720 của `_agg_dimA_metric_intercorr.csv`: 5·0,720/(1+4·0,720) = 0,928 — khớp tuyệt đối; file 01 §5.6 ghi đúng "α (5 trục) = 0,928"). α của riêng cụm CAC–AR–TRA ≈ 0,955 (chuẩn hóa từ r̄ = 0,877) hoặc 0,973–0,980 (thô). Sửa nhãn về "α năm trục = 0,928" hoặc thay số 0,955.

**E4. 4.4: "Tỷ số biến thiên thân chủ/counselor vượt 1 ở 10/11 bộ… ngoại lệ duy nhất là SoulChat (0,991)"** đặt trong đoạn "Trên cấu hình B" → số 0,991 là của **cấu hình A** (đã truy đúng: config A soulchat = 0,991, 10/11 >1). Ở cấu hình B (chính của bài): **11/11 bộ >1**, SoulChat = 1,138 (min = ESConv 1,087). Sửa: "11/11" và bỏ câu ngoại lệ SoulChat, hoặc chuyển câu này thành nhận xét cấu hình A có ghi nhãn rõ. (Câu "giọng cảm thán của counselor máy" nếu muốn giữ phải dựa bằng chứng khác.)

**E3. 4.4: "NEC đổi dấu ở 5/7 bộ"** → tính theo trung bình từng cấu hình: đổi dấu ở **6/7 bộ** (KokoroChat −0,012→+0,048; PsyDial −0,011→+0,056; SMILE −0,071→+0,087; SoulChat −0,048→+0,076; CPsyCoun −0,058→+0,017; SimPsyDial −0,055→+0,085; chỉ KMI giữ dấu dương). Sửa 5/7 → 6/7 (theo hướng làm mạnh thêm luận điểm độ nhạy cấu hình).

**E6. 4.5: "GPT chấm cao hơn trung bình hội đồng +0,35–0,40 trên Chiều A"** → so **trung bình hội đồng** (gồm cả GPT) chỉ +0,25; các giá trị 0,35–0,40 đúng khi so **Claude** (+0,35) hoặc **trung bình hai giám khảo còn lại** (+0,38). Sửa mốc so sánh cho khớp số.

**E7 (nhỏ). 4.4: "n = 1.398"** cho r(độ phủ, biến thiên) → số record cấu hình A có đủ cả hai biến = **1.386** (1.400 dòng 7 bộ, 14 thiếu std). Sửa n.

**E8 (nhỏ, câu chữ). 4.2: "tương quan điểm với lượng lời counselor (KokoroChat 0,42; Psy-Insight 0,30; AnnoMI 0,28; SMILE −0,23)"** → bốn số này khớp với **tổng token hội thoại** (0,427/0,308/0,282/−0,217); nếu đúng nghĩa "lượng lời counselor" thì là 0,41/0,30/0,26/−0,19. Chọn một cách và ghi nhất quán (kết luận không đổi).

**E9 (đặc tả, không hẳn lỗi). Krippendorff α trong Bảng 3/4.5:** giá trị của pipeline không tái lập được bằng interval-α chuẩn trên điểm tổng (vd AnnoMI B: 0,949 vs 0,898; SoulChat A: 0,520 vs 0,040 — lệch rất lớn ở các bộ có bias giữa giám khảo cao vì interval-α phạt lệch tuyệt đối). Giá trị của bài bám sát ICC(2,k) (AnnoMI B 0,964; SoulChat A 0,484) hơn là interval-α. → Bài cần **ghi rõ metric và implementation** (interval/ordinal/gói phần mềm) trong 3.5 hoặc chú thích Bảng 3, và công bố hàm tính kèm mã; nếu ý định là interval chuẩn thì bảng phải tính lại.

*(Ghi chú trọng số, không phải lỗi: Bảng 8 dùng gộp record — caption đã khai báo; nếu muốn đối xứng với triết lý "đơn vị suy diễn là bộ dữ liệu" có thể thêm cột trung bình-của-trung-bình: semi-real 3,05 thay 2,89 — khác biệt do AnnoMI n=112 bị PsyDial n=200 lấn.)*

---

## 3. BỔ SUNG ĐỀ XUẤT (từ phân tích độc lập — chưa có trong bài, chi phí thấp)

**B1 — Vân tay thứ hai: "phụ phí EPC", kèm ca phân ly PsyDial (đề xuất giá trị nhất).**
`EPC_premium = EPC − trung bình(CAC, AR, TRA, ASCQ)`: ESConv −0,23 < AnnoMI +0,06 < KokoroChat +0,33 < Psy-Insight +0,34 **‖** SMILE +0,44 < SoulChat +0,45 < CPsyCoun +0,63 < **PsyDial +0,65** < SimPsyDial +0,76 < CACTUS +0,92 < KMI +1,62. Dưới lưỡng phân "văn bản lời counselor cuối cùng có qua tay LLM" (4 thuần người vs 7 có bàn tay LLM — PsyDial thuộc nhóm sau vì lời counselor được LLM tinh chỉnh trôi chảy, đúng như Bảng 1 của bài ghi): tách **hoàn hảo**, hoán vị chính xác p = 0,0061. Dưới lưỡng phân chính thức 5/6 (PsyDial→người): U = 3, p = 0,030 — vẫn ý nghĩa.
Điểm đắt nhất là **PsyDial phân ly hai vân tay**: tông counselor = mức người (0,173 — nhờ đó 29/30 cặp tông mới đúng) nhưng EPC_premium (+0,65) và ASCQ (2,07 — thấp nhì bảng) = mức máy. Diễn giải: vân tay **tông** bám vào *nội dung* (nội dung người giữ lại), vân tay **EPC-premium/ASCQ** bám vào *bề mặt văn bản* (lớp LLM đánh bóng) — hai tầng can dự LLM khác nhau để lại hai dấu khác nhau. Điều này làm sâu thêm đúng "quy luật 2" của bài (bàn tay LLM trên câu chữ quyết định vân tay) và cho người kiểm toán thêm một chỉ số miễn phí (tính từ chính điểm Chiều A, không cần chấm thêm). Đề xuất: ~120 từ ở 4.7 (sau hai quy luật) hoặc một hàng mới trong Bảng 9.

**B2 — Số hóa cơ chế "thu hẹp dải đo" ở 4.5.** Bài đã nêu cơ chế đúng; bổ sung một câu định lượng: tương quan giữa mức đồng thuận (trung bình r từng cặp) và SD nội bộ = **ρ = 0,63 (A) / 0,84 (B)** trên 11 bộ — đồng thuận giám khảo gần như là hàm của độ trải điểm.

**B3 — Bias giám khảo đổi chiều theo công cụ (1 câu ở 4.5).** Chuẩn hóa % thang: Gemini nghiêm nhất Chiều A (30,7% thang) nhưng hào phóng nhất Chiều B (80,7% thang; chênh +50 điểm phần trăm); Claude +37,5; GPT +34,8. → "Thiên lệch không phải hằng số của giám khảo mà của cặp giám khảo×công cụ; hiệu chuẩn độ nghiêm không chuyển giao được giữa các thang."

**B4 — Nâng case-study 4.8 thành thống kê toàn cục (1 câu).** Vùng "liên minh đẹp, lâm sàng kém" (B≥4 & A<2,5) chiếm **20,5%** toàn mẫu (433/2.111; ESConv 59,5%, SMILE 48,2%, SoulChat 39,5%, PsyDial 36,5%); vùng ngược (A≥3,5 & B<3,5) gần rỗng (chỉ Psy-Insight 8,0%, AnnoMI 3,6%). Bất đối xứng này là bản toàn cục của các ca 4.8: bề mặt hợp tác dễ sản xuất, năng lực lâm sàng khan hiếm.

**B5 — Ghi chú chi phí giao thức 3 lần chạy (1 câu ở 5.2 hoặc Bảng 9).** 81,5% điểm mục có SD = 0 giữa 3 lần chạy trong cùng giám khảo (GPT ổn định nhất 0,067) — mức lặp gần trần khiến trung bình 3 lần chạy chủ yếu mang tính bảo hiểm; ngân sách nên ưu tiên thêm *giám khảo* hơn thêm *lần chạy*.

**B6 (tùy chọn) — Con số minh họa cho đoạn ESConv 4.2.** Đếm từ khóa trên trace claude+gemini: 83% record ESConv bị nêu lỗi ranh giới/tự bộc lộ (cao nhất tập mẫu) — đúng câu "rubric phạt đúng cái kho này không tuyên bố có" (nêu rõ đây là keyword-matching, chỉ dấu).

---

## 4. LOẠI TRỪ / HẠ GIỌNG

1. **Bảng 9 hàng self-preference + câu 5.3** — sửa theo E5 (đảo thành phát hiện âm tính). Đây là mục duy nhất mang tính *loại trừ nội dung*.
2. **Câu SoulChat 0,991** trong 4.4 — bỏ hoặc gắn đúng nhãn cấu hình A (E4).
3. Không có nội dung nào khác cần loại: các claim Tầng 1/2/3 đều đứng vững dưới kiểm định độc lập.

---

## 5. ĐÍNH CHÍNH CHO CHÍNH FILE 06 (phân tích độc lập 14/08)

File `06_phan_tich_doc_lap_20260814.md` mục 3.1/KL4 ban đầu dùng lưỡng phân 4/7 với nhãn "PsyDial — LLM viết (tái tạo)". Theo taxonomy chính thức của bài (Bảng 1: counselor người, LLM tinh chỉnh trôi chảy; thân chủ GPT-4o), PsyDial thuộc nhóm **người viết** trong lưỡng phân 5/6. Đã bổ sung phần đính chính trong file 06: kết quả "tách hoàn hảo p=0,0061" chỉ đúng cho lưỡng phân "văn bản cuối có bàn tay LLM" (4/7); dưới lưỡng phân chính thức 5/6, kiểm định còn p = 0,030 và PsyDial là ca phân ly hai vân tay (chi tiết ở B1 trên).

## PHỤ LỤC — TÁI LẬP
`_doclap_20260814/s6_verify_r7.py` (20 nhóm kiểm claim), `s7_trace_levels.py` (truy mức tính 0,928 / 0,715–0,968 / 0,991 / n=1.398), log `s6_report.txt`, `s7_report.txt`. Text bài r7 trích bằng python-zipfile (bản sao, không đụng file gốc).
