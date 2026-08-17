# 08 — Tái phân tích pilot từ kho chính tắc `data/<dataset>/results/`

**Ngày:** 15/08/2026 · **Nguồn duy nhất:** `code/mind-eval/data/<DS>/results/{mind_eval,wai}/` (KHÔNG dùng `experiments/` — folder đó sót lô pilot WAI gpt_9router).

## 1. Quy tắc chọn file (chốt theo xác nhận của Vy)

- File **không** hậu tố `_full` = **pilot** (20 hội thoại/bộ; SMILE 19). File `_full` = **lượt chạy chính** (200/bộ; AnnoMI 112; smile 199).
- **S1 chỉ có nghĩa với 7 bộ phi tiếng Anh** (CPsyCoun, KMI, KokoroChat, PsyDial, SoulChat, simpsydial, smile). File nhãn S1 của 4 bộ tiếng Anh (AnnoMI, ESConv, Psy-Insight, cactus) là bản copy nhãn của S3 (`copy_en_results()`), **loại khỏi mọi so sánh S1/S2**.
- Giám khảo pilot Chiều A: gpt (= GPT-5.1), claude (gộp hai tên file `claude` + `claude_batch`, cùng model claude-sonnet-4-6), gemini, qwen (= file `qwen_thinking`, đúng Qwen3-235B-Thinking). File `qwen` thường (không thinking) là thí nghiệm phụ, loại.
- Điểm Chiều A = `parsed_judgment["Average score"]`; điểm Chiều B = `total`.
- Pilot Chiều B có **4 bộ điểm S3**: gpt (GPT-5.1; KokoroChat hỏng còn 2), **gpt_9router (GPT-5.5-route — đúng phiên bản hội đồng chính, phủ đủ 11 bộ)**, claude_9router, gemini; S1 chỉ gpt (GPT-5.1).
- File lạc loại khỏi phân tích và khỏi gói công bố: `KMI_S1_ko_translated_gpt`, `KMI/simpsydial *claude_haiku*` (mind_eval); `AnnoMI…claude_9router__…` (34 dòng), `PsyDial…claude_9router_f_…` (wai).

## 2. Số TÁI LẬP ĐƯỢC — giữ trong bài (kèm định nghĩa metric nay đã tường minh)

| Số trong bài (5.2/Bảng 4) | Tái tính từ kho chính tắc | Định nghĩa metric |
|---|---|---|
| \|Δ(S1−S3)\| ≤ 0,073 (Claude, GPT) | GPT −0,028; Claude +0,073 (n = 139 cặp) | Ghép cặp theo hội thoại, 7 bộ phi-EN, mean Δ theo giám khảo |
| Đồng thuận 0,467 / 0,286 / 0,423 | **0,467 / 0,288 / 0,424** | Trung bình tương quan Pearson từng cặp trong 4 giám khảo, tính trong từng bộ rồi trung bình không trọng số (42 hệ số r/phương án) |
| Qwen swing S2−S3 = +0,420; S1−S2 = −0,540 | +0,421 / −0,540 (n = 139) | Điểm Qwen thô, ghép cặp id giữa cấu hình |
| Kendall τ 0,810 (S1↔S3); 0,905 (S2↔S3) | 0,810 / 0,905 — **trên 7 bộ phi-EN**, xếp hạng theo trung bình hội đồng 3 giám khảo (không Qwen) | Bài đang viết "11 bộ" — SAI PHẠM VI, cần sửa thành "bảy bộ phi tiếng Anh" |
| Chiều B: S1−S3 +0,007 (\|Δ\| 0,084, n=139); gộp +0,006 (0,064, n=219) | +0,0066 / 0,084 / 139 và +0,0061 / 0,064 / 219 | Ghép cặp id, giám khảo GPT-5.1 |
| τ pilot→full Chiều A = 0,818 | 0,818 | Hạng trung bình hội đồng, pilot S3 vs full |

## 3. Số PHẢI SỬA trong bài

| Nội dung | Bài đang ghi | Số đúng từ kho chính tắc |
|---|---|---|
| **Thiên lệch Qwen** | "+0,77 đến +1,19 so với trung bình hội đồng; MAE 0,79–1,20" (**SAI DẤU**) | Qwen chấm **THẤP hơn** hội đồng: bias gộp −0,79 (S1) / −0,25 (S2) / −0,88 (S3); MAE 0,81 / 0,49 / 0,89; theo từng bộ (S3) từ −0,44 (cactus) tới **−1,87 (Psy-Insight)**, âm ở **11/11 bộ** |
| τ pilot→full Chiều B | 0,564 (tính với lô GPT-5.1 cũ) | **0,600** (bộ pilot đúng phiên bản hội đồng gpt_9router + claude_9router + gemini) |
| Phạm vi τ | "thứ hạng 11 bộ dữ liệu" | "thứ hạng **bảy bộ phi tiếng Anh**" |
| Đồng thuận S2/S3 (làm tròn) | 0,286 / 0,423 | 0,288 / 0,424 |

## 4. Số MỚI đưa vào bài (đã vá các vòng 15/08)

- Pilot Chiều B S3, bộ ba **đúng phiên bản hội đồng chính** (gpt_9router × claude_9router × gemini): **216 hội thoại đủ bộ ba**; đồng thuận từng cặp pooled-z nội-bộ-dữ-liệu **r = 0,825 / 0,835 / 0,810** (n hiệu dụng 183–186) → ghi bài "r = 0,81–0,84".
- Coverage đầy đủ: A full = 3 × 2.111 = 6.333 ✓; B full = 3 × 2.111 = 6.333 ✓; A pilot đủ S1/S2/S3 × 4 giám khảo × 7 bộ phi-EN; B pilot S3 × 4 bộ điểm × 11 bộ + S1 GPT-5.1 × 10 bộ (7 phi-EN dùng được); B S2 = 0 file (đúng thiết kế sàng lọc).

## 5. Ghi chú tái lập

Script tính nằm trong phiên làm việc 15/08 (chạy trực tiếp từ jsonl, không phụ thuộc CSV trung gian). Nếu cần đóng gói: chuyển các khối python trong log phiên thành `_notes/s8_pilot_canonical.py`.
