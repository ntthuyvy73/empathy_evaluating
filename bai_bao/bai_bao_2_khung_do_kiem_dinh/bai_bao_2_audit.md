# [BẢN THẢO 2 — AUDIT, bản viết lại]

# Kiểm toán chéo ngôn ngữ 11 dataset hội thoại tham vấn tâm lý đa lượt: kỹ năng lâm sàng, liên minh trị liệu, động học cảm xúc, và các hiện vật của chính thước đo

**Tóm tắt.** Các dataset hội thoại tham vấn đang được dùng để huấn luyện LLM trò chuyện với con người ở thời điểm dễ tổn thương nhất của họ, nhưng mỗi dataset chỉ được đánh giá bằng chuẩn tự chọn của nhóm phát hành. Chúng tôi thực hiện cuộc **kiểm toán độc lập, cùng thước đo** đầu tiên trên 11 dataset đại diện (EN/ZH/JA/KO; đủ bốn nhóm nguồn gốc real / semi-real / semi-synthetic / fully-synthetic; 2,111 hội thoại) theo ba chiều: kỹ năng counselor (rubric MindEval, 5 trục × 1–6), liên minh trị liệu (WAI-O-S, 12 câu × 1–5), và động học cảm xúc (UED trên NRC-VAD), chấm bởi hội đồng ba LLM-judge khác họ (6,333 lượt chấm/chiều), kèm pilot đối chứng ba cấu hình ngôn ngữ và hai cấu hình lexicon. **Kết quả kiểm toán:** (1) chất lượng dataset là một *vector* — quán quân ba chiều thuộc ba nhóm nguồn gốc khác nhau, và tương quan hạng giữa chiều kỹ năng với chiều liên minh chỉ 0.182; (2) 6/11 dataset có ≥91% phiên dưới ngưỡng "chấp nhận được" của rubric lâm sàng — phần lớn nguyên liệu SFT hiện hành mô tả mức chăm sóc dưới chuẩn; (3) dữ liệu fully-synthetic được thưởng có hệ thống ở chiều liên minh (+0.237 sau kiểm soát độ dài) với phân phối "không tưởng" (99% phiên ≥4/5, 0% liên minh xấu), trong khi nhóm semi-synthetic viết lại từ hỏi–đáp đại chúng xếp đáy chiều kỹ năng (−0.427 so với real); (4) ba hiện vật của chính thước đo — thưởng độ dài (b = +0.305/log-token), hào quang 12 câu WAI (r̄ = 0.715), nhiễu lexicon thưa (r = −0.455) — đủ lớn để đảo thứ hạng nếu không hiệu chỉnh. Chúng tôi công bố hồ sơ kiểm toán từng dataset, sáu insight tổng hợp, giao thức tái lập được, và bộ khuyến nghị cho người dùng, người xây và người đo dataset.

**Từ khóa:** audit dataset; LLM-as-judge; liên minh trị liệu; động học cảm xúc; dữ liệu tổng hợp; đo lường học; sức khỏe tâm thần.

## 1. Giới thiệu

Một chuỗi sự kiện gần đây phơi bày rủi ro của "đánh giá tự thân": Cactus được lọc bằng thang lâm sàng CTRS (giữ 86.3% hội thoại đạt ≥5/6) và thắng đánh giá người về Helpfulness/Empathy [6], nhưng khi một nhóm độc lập áp bộ chỉ số động học cảm xúc, dữ liệu này lộ khiếm khuyết hệ thống — biến thiên cảm xúc thua dữ liệu thật với effect size r = 0.84, cung cảm xúc tổng hợp gần như không tương quan với cung thật [16]. Nếu một dataset 31,577 hội thoại có thể vượt mọi thước đo tự chọn mà vẫn mang khiếm khuyết cấu trúc, thì câu hỏi không còn là "dataset nào tốt" mà là: **dưới cùng một thước, cảnh quan dataset thực sự trông ra sao, và bao nhiêu phần của 'điểm' là tín hiệu thật?**

Cuộc kiểm toán này trả lời ba câu hỏi: **A1** — xếp hạng chéo của 11 dataset đại diện trên từng chiều, và mức nhất quán giữa các chiều; **A2** — khác biệt hệ thống theo nguồn gốc dữ liệu sau khi kiểm soát các nhiễu đo được; **A3** — các hiện vật của chính giao thức đo, độ lớn, và quy tắc hiệu chỉnh. Đóng góp: (i) giao thức kiểm toán ba chiều tái lập được, công bố kèm mã và bảng trung gian; (ii) bảng xếp hạng chéo và hồ sơ kiểm toán 11 dataset; (iii) định lượng hiệu ứng nguồn gốc có kiểm soát; (iv) danh mục hiện vật đo lường kèm độ lớn — theo hiểu biết của chúng tôi, đây là lần đầu các cảnh báo định tính về LLM-judge trong lĩnh vực này được chuyển thành hệ số định lượng trên cùng một tập dữ liệu; (v) sáu insight tổng hợp và khuyến nghị vận hành.

## 2. Đối tượng kiểm toán

Bảng 1 (bài khảo sát đồng hành trình bày chi tiết sáu trục taxonomy) tóm tắt 11 dataset: **real** — ESConv [1] (crowdworker sát hạch 7.8%), KokoroChat [11] (480 counselor role-play, 91.2 lượt nói/phiên), Psy-Insight [10] (951 phiên/189 ca từ sách chuyên môn, song ngữ EN+ZH, duy nhất đa phiên); **semi-real** — AnnoMI [2] (video trình diễn MI có chú giải MINT), PsyDial [9] (RMRR: giữ lời counselor thật của 2,382 phiên Xinling, tái tạo lời thân chủ để bảo mật); **semi-synthetic** — SMILE [3], SoulChat [4], CPsyCoun [5] (LLM biến đổi hạt giống thật); **fully-synthetic** — Cactus [6], SimPsyDial [7], KMI [8] (LLM cả hai vai, có neo thật ở hạt giống). Mẫu kiểm toán: 200 phiên/dataset lấy ngẫu nhiên (AnnoMI: toàn bộ 112; smile: 199 sau loại 1 bản ghi lỗi), tổng 2,111 phiên.

## 3. Giao thức kiểm toán

**Bảng 1.** Giao thức ba chiều.

| Thành phần | Chiều A — Kỹ năng | Chiều B — Liên minh | Chiều C — Cảm xúc |
|---|---|---|---|
| Công cụ | Rubric MindEval 5 trục (CAC, EPC, AR, TRA, ASCQ) [13] | WAI-O-S 12 câu, 3 tiểu thang Goal–Approach–Bond [12] | UED: mean, variability, displacement, rise/recovery [14]; NEC & happy-ending (định nghĩa vận hành, kiểm chứng số học 100%) |
| Thang; chiều tốt | 1–6; cao = tốt | 1–5; cao = liên minh mạnh; 3 = chưa có bằng chứng | mô tả; chuẩn = "gần phân bố người thật" [16] |
| Đơn vị chấm | toàn phiên | từng câu hỏi, 3 lần chạy/câu, lấy trung bình | chuỗi từ, cửa sổ trượt 10 từ |
| Người chấm | hội đồng 3 LLM khác họ (Claude-Sonnet-4-6; Gemini-3.1-Pro; GPT-5.x); điểm = trung bình | như chiều A | không cần judge (lexicon NRC-VAD) |
| Kiểm soát | pilot 20 phiên/dataset × 3 cấu hình ngôn ngữ (S1 dịch EN; S2 prompt bản ngữ; S3 gốc + prompt EN) | như A (S2 không khả dụng; S1 một judge) | 2 cấu hình lexicon (A: bản ngữ; B: dịch EN + lexicon EN) |
| Thống kê | hồi quy điểm ~ nguồn gốc + log-token; Kendall τ; Krippendorff α theo dataset; MTMM hai cấp | như A | so phân bố; kiểm chứng độ phủ lexicon |

**Các quyết định giao thức rút từ pilot (có số):** (i) chọn **S3** cho vòng chính — S2 phá vỡ đồng thuận judge (Pearson liên-judge pooled 0.286 so với 0.467/0.423 của S1/S3) và thổi phồng judge yếu (+0.42 điểm); S1 tương đương S3 về điểm (|Δ| ≤ 0.073 ở hai judge mạnh) và về hạng (τ = 0.810) nhưng đòi dịch ~1.08 triệu token; (ii) **loại judge thứ tư** (Qwen3-235B-thinking) vì lệch hệ thống (bias +0.766…+1.190; MAE 0.794–1.195 so với ba judge còn lại); (iii) chiều C dùng **cấu hình B** làm chính — cấu hình A (lexicon bản ngữ dịch tự động) chỉ phủ 23–31% token và bị chứng minh nhiễu chi phối (mục 5.2).

## 4. Kết quả kiểm toán theo chiều (A1)

### 4.1. Chiều A — kỹ năng lâm sàng

![Hình 1. Xếp hạng chiều kỹ năng (trung bình 3 giám khảo ± SD), tô màu theo nguồn gốc; vạch đứt = ngưỡng "acceptable baseline" của rubric.](figs/fig_dimA_ranking.png)

Ba tầng hiện rõ (Hình 1): tầng trên 3.19–3.62 (AnnoMI 3.62; Cactus 3.38; Psy-Insight 3.36; SimPsyDial 3.19) — điểm chung là lời counselor mô phỏng/ghi lại **giao thức trị liệu tường minh**; tầng giữa 2.48–2.92 (KokoroChat, KMI, PsyDial); tầng đáy 1.80–2.32 (SMILE, CPsyCoun, SoulChat, ESConv). Ba sự kiện kiểm toán: (i) **6/11 dataset có ≥91% phiên dưới mức 3** ("acceptable baseline"): ESConv 100%, SoulChat 99%, CPsyCoun 95%, SMILE 95%, PsyDial 92%, KMI 91%; (ii) hồ sơ 5 trục nhất quán: EPC (đạo đức–ranh giới) cao nhất ở 10/11 dataset trong khi ASCQ ("chất LLM") thấp nhất ở dữ liệu máy — KMI có khoảng cách EPC−ASCQ tới 1.99 điểm (3.95 so với 1.96): *đúng chuẩn mực, giọng máy*; (iii) ESConv đội sổ **theo thiết kế chứ không theo lỗi**: EPC 1.61 vì supporter ngang hàng tự bộc lộ và khuyên trực tiếp — rubric lâm sàng phạt đúng cái mà dataset này không hề tuyên bố có (peer support, không phải trị liệu).

![Hình 2. Phân phối điểm kỹ năng theo phiên: dữ liệu người-viết trải rộng (AnnoMI SD 1.08, có cả đuôi ≥4 lẫn <2), dữ liệu LLM-viết bị nén (Cactus/KMI SD 0.27).](figs/fig_dimA_violin.png)

Hình 2 cho thấy đặc trưng quan trọng hơn cả trung bình: **biên độ chất lượng**. AnnoMI chứa đồng thời 46.4% phiên ≥4 và 13.4% phiên <2 (ví dụ `annomi_20` được ba judge chấm 4.8/6.0/5.2 trong khi `annomi_69` nhận 1.0/1.0/1.3) — nhất quán với thiết kế gốc gồm cả mẫu MI chất lượng cao lẫn thấp [2]. Ngược lại nhóm fully-synthetic gần như không có phiên ≥4 (Cactus 1.0%, SimPsyDial 0.0%) dù trung bình cao.

### 4.2. Chiều B — liên minh trị liệu
Xếp hạng (trung bình 3 judge): SimPsyDial 4.335 > Cactus 4.290 > PsyDial 4.182 > SMILE 4.166 > KMI 4.088 > KokoroChat 4.046 > ESConv 4.007 > SoulChat 3.992 > AnnoMI 3.760 > Psy-Insight 3.605 > CPsyCoun 3.418. Bốn vị trí đầu đều là dữ liệu LLM-tham-gia và **vượt dải người thật 3.5–4.0** (mốc 859 phiên tham vấn văn bản thật [12]). Cờ đỏ phân phối: SimPsyDial 99% phiên ≥4 và **0% phiên <3**; mức câu hỏi: "đồng thuận về các bước" (Q5) của SimPsyDial đạt 4.76/5 — sát trần. Ngược lại AnnoMI có 17% phiên liên minh <3 — nguồn mẫu "liên minh gãy" đáng kể duy nhất. Hai câu hỏi WAI mang nhiều thông tin nhất: Q10 ("thân chủ tin năng lực counselor") là câu **thấp nhất gần như toàn cục** (AnnoMI 3.48; CPsyCoun 3.20; Cactus 3.79) — chiều khó "diễn" nhất; Q12 ("tin cậy lẫn nhau") cao nhất toàn cục — đúng pattern dữ liệu người thật trong [12].

### 4.3. Chiều C — động học cảm xúc (cấu hình B)
Tỷ lệ kết-thúc-dương (happy-ending): SimPsyDial 88.0% > PsyDial 84.0% > SMILE 79.3% > ESConv 77.5% > SoulChat 76.0% > KMI = KokoroChat 74.5% > Cactus 72.5% > AnnoMI 64.6% > CPsyCoun 59.3% > Psy-Insight 49.6%. Ba chú giải: (i) ESConv cao **theo thiết kế** — quy trình phê duyệt gốc yêu cầu cường độ cảm xúc của seeker giảm sau phiên [1]; (ii) tông cảm xúc counselor tách hai khối: lời LLM 0.179–0.198 (đỉnh SimPsyDial 0.198, SoulChat 0.194) so với lời người 0.138–0.175 (đáy AnnoMI 0.138) — tái lập độc lập "elevated tone" của [16]; (iii) Psy-Insight có cung phẳng (NEC ≈ −0.000, kết-thúc-dương ở mức ngẫu nhiên 49.6%) — hệ quả đơn vị phân tích: các phiên bị tách khỏi ca đa phiên (mục 6, I5).

### 4.4. Bảng so sánh chéo và cấu trúc tương quan giữa các chiều

**Bảng 2.** Bảng chéo 11 dataset × 3 chiều (đậm: cực trị mỗi cột; α: Krippendorff của hội đồng judge trên dataset đó).

| Dataset (nguồn gốc) | A: Overall (1–6) | SD(A) | B: WAI (1–5) | %B≥4 | C: NEC | C: Happy% | Tông counselor | α(A) | α(B) |
|---|---|---|---|---|---|---|---|---|---|
| AnnoMI (semi-real) | **3.62** | **1.08** | 3.76 | 57.1 | 0.027 | 64.6 | **0.138** | **0.834** | **0.949** |
| Cactus (fully-syn) | 3.38 | 0.27 | 4.29 | 81.0 | 0.049 | 72.5 | 0.179 | 0.629 | 0.861 |
| Psy-Insight (real) | 3.36 | 0.89 | 3.61 | 25.0 | **−0.000** | **49.6** | 0.142 | 0.739 | 0.926 |
| SimPsyDial (fully-syn) | 3.19 | 0.36 | **4.34** | **99.0** | 0.085 | **88.0** | **0.198** | 0.712 | **0.526** |
| KokoroChat (real) | 2.92 | 0.50 | 4.05 | 65.0 | 0.048 | 74.5 | 0.173 | 0.732 | 0.849 |
| KMI (fully-syn) | 2.65 | **0.27** | 4.09 | 68.0 | 0.076 | 74.5 | 0.182 | 0.594 | 0.563 |
| PsyDial (semi-real) | 2.48 | 0.39 | 4.18 | 83.0 | 0.056 | 84.0 | 0.174 | 0.622 | 0.565 |
| SMILE (semi-syn) | 2.32 | 0.42 | 4.17 | 80.4 | **0.086** | 79.3 | 0.182 | 0.602 | 0.618 |
| CPsyCoun (semi-syn) | 2.29 | 0.41 | **3.42** | 6.5 | 0.017 | 59.3 | 0.174 | 0.607 | 0.689 |
| SoulChat (semi-syn) | 2.19 | 0.33 | 3.99 | 52.5 | 0.076 | 76.0 | 0.194 | 0.520 | 0.566 |
| ESConv (real) | **1.80** | 0.36 | 4.01 | 62.0 | 0.082 | 77.5 | 0.175 | 0.540 | 0.784 |

![Hình 3. Ma trận hội tụ–phân biệt hai cấp: ba chiều gần trực giao ở cấp phiên; ở cấp dataset, liên minh hội tụ với kết-thúc-dương (ρ = 0.724).](figs/fig_mtmm.png)

![Hình 4. Liên minh (B) ↔ kết-thúc-dương (C): cụm góc trên-phải toàn dữ liệu LLM-tham-gia; nhóm real/semi-real nằm trong hoặc sát dải người thật.](figs/fig_B_vs_happy.png)

Cấu trúc tương quan (Hình 3–4) là phát hiện trung tâm của A1: **các chiều gần trực giao ở cấp phiên** (A↔C −0.031; A↔B 0.375; B↔C 0.172, pooled-z, n≈2,111) nhưng **B↔C hội tụ mạnh ở cấp dataset** (happy: ρ = 0.724, p = 0.012; NEC: ρ = 0.655, p = 0.029) trong khi A↔B chỉ 0.182 (p = 0.593). Nghĩa là: liên minh "diễn" và kết-vui không đi cùng nhau trong từng phiên, nhưng đi cùng nhau như **phong cách của cả dataset** — một chữ ký của kịch bản hóa, không phải của hiệu quả trị liệu.

## 5. Phân tích cắt ngang (A2, A3)

### 5.1. Hiệu ứng nguồn gốc có kiểm soát

![Hình 5. Vân tay nguồn gốc trên bốn đại lượng (trung bình nhóm, trục y cắt): kỹ năng cao nhất ở fully-synthetic và thấp nhất ở semi-synthetic; liên minh, kết-vui và tông counselor tăng dần theo mức LLM tham gia.](figs/fig_group_fingerprint.png)

**Bảng 3.** Hồi quy mức phiên có kiểm soát log-độ-dài (n = 2,111; nhóm tham chiếu: real; khai báo pseudo-replication vì nguồn gốc là thuộc tính dataset).

| Biến | Chiều A (kỹ năng) | Chiều B (liên minh) |
|---|---|---|
| log(token) | −0.019 (không đáng kể) | **+0.305** |
| semi-real so với real | +0.218 | −0.186 |
| semi-synthetic so với real | **−0.427** | −0.038 |
| fully-synthetic so với real | **+0.387** | **+0.237** |
| R² | 0.180 | 0.312 |

Hai kiểm tra vững: (i) so sánh **nội ngôn ngữ ZH** (5 dataset, đủ 3 nhóm LLM-tham-gia) lặp lại đúng thứ bậc — SimPsyDial 3.19 > PsyDial 2.48 > SMILE/CPsyCoun/SoulChat 2.19–2.32 ở chiều A — loại trừ khả năng hiệu ứng nhóm là ảo ảnh ngôn ngữ; (ii) lưỡng phân "ai viết lời counselor" cho tách biệt sạch trên chiều C: tông 0.185 (LLM) so với 0.164 (người), NEC 0.066 so với 0.047, kết-vui 75.2% so với 72.0%.

### 5.2. Hiện vật của chính thước đo

![Hình 6. Thưởng độ dài bất đối xứng: chiều liên minh tăng theo độ dài hội thoại (b = +0.305/log-token) trong khi chiều kỹ năng miễn nhiễm (b = −0.019).](figs/fig_length_effect.png)

**Bảng 4.** Danh mục hiện vật đo lường, độ lớn, và quy tắc hiệu chỉnh.

| Hiện vật | Bằng chứng định lượng | Hệ quả nếu bỏ qua | Quy tắc hiệu chỉnh |
|---|---|---|---|
| Thưởng độ dài của WAI | b = +0.305/log-token (Hình 6); PsyDial (phiên dài nhất corpus) đạt hạng 3 liên minh | ~1/3 khoảng cách thô giữa dataset ngắn nhất và nhóm đầu là độ dài | báo cáo kèm điểm residual sau hồi quy độ dài |
| Hào quang 12 câu WAI | r̄ liên-câu 0.715 (α = 0.968); Goal↔Approach 0.891 | ba tiểu thang không tách được; hạng nhạy nhiễu | đọc theo cụm cao/giữa/thấp; giữ Q10 làm chỉ báo đơn |
| Dải nén của chiều B | between-dataset SD 0.286 (so với 0.587 của chiều A); τ liên-judge 0.60–0.71 (A: 0.89–0.93); τ pilot→full 0.564 (A: 0.818) | thứ hạng B kém bền theo judge và cỡ mẫu | không đọc từng bậc hạng B; pilot 20 phiên không đủ chốt hạng B |
| Nhiễu lexicon thưa (chiều C, cấu hình A) | độ phủ 23–31%; r(độ phủ, biến thiên) = −0.455, p ≈ 7×10⁻⁷²; NEC đổi dấu ở 5/7 dataset; tương quan A↔B cấu hình chỉ 0.07–0.42 | mọi chỉ số động phồng ×2; so chéo ngôn ngữ vô nghĩa | chỉ dùng lexicon phủ cao; công bố độ phủ kèm kết quả |
| Độ tin cậy phụ thuộc dữ liệu | α 0.520→0.949 trong cùng hội đồng (Bảng 2): cao ở dữ liệu phương sai thật (AnnoMI, Psy-Insight), sụp ở dữ liệu nén (SimPsyDial 0.526) | "judge đáng tin" là mệnh đề vô nghĩa nếu tách khỏi phân phối | công bố α theo dataset; chỉ dùng trung bình hội đồng |
| Tính không tái lập cấp phiên | test–retest các trường hợp chấm lại độc lập: r 0.41–0.80; MAE 0.15–0.22 | điểm một phiên đơn lẻ không đáng tin | mọi kết luận cấp phiên dùng ≥3 judge |
| Dấu hiệu self-preference | GPT chấm hai dataset họ-GPT-sinh cao hơn Claude 0.29–0.38 | có thể nâng nhóm fully-synthetic | panel chéo họ generator; thiết kế chéo để kết luận |

### 5.3. Các phiên "bất đồng chiều" — đơn vị thông tin giàu nhất
Trích từ bảng case (z-score nội dataset): **kỹ năng cao, cảm xúc đi xuống** — `cactus_121` (A = 4.10, NEC = −0.081), `kmi_712` (A = 3.27, NEC = −0.268): đúng giao thức nhưng thân chủ không khá lên; **liên minh cao, kỹ năng thấp** — `simpsydial_463` (B = 4.77, A = 2.75), `cactus_19` (B = 4.87, A = 2.87): hòa hợp "diễn" được điểm gần trần với kỹ năng dưới baseline; **kỹ năng thấp, cảm xúc cải thiện** — `soulchat_157820` (A = 1.80, NEC = +0.511), `esconv_43` (A = 1.33, NEC = +0.359): hỗ trợ tay ngang vẫn tạo chuyển biến valence. Các phiên này minh họa vì sao kiểm toán một chiều dẫn tới kết luận sai một cách hệ thống.

## 6. Sáu insight tổng hợp

**I1 — Chất lượng dataset là vector; mọi bảng xếp hạng một-cột đều gây nhầm.** Minh chứng: quán quân ba chiều thuộc ba nhóm nguồn gốc khác nhau (A: AnnoMI semi-real; B: SimPsyDial fully-synthetic; C-gần-chuẩn-thật: chính AnnoMI ở phía "trung thực cảm xúc" với happy 64.6%); A↔B cấp dataset 0.182.

**I2 — "Hòa hợp kịch bản" là một hội chứng đo được, không phải một ấn tượng.** Bộ ba đồng xuất hiện ở dữ liệu máy: liên minh vượt dải người thật (4.09–4.34 so với 3.5–4.0), kết-vui dày (72.5–88.0%), phân phối nén (SD 0.181–0.369; 0% liên minh xấu) — và B↔happy ρ = 0.724 ở cấp dataset trong khi chỉ 0.172 ở cấp phiên. Diễn giải lý thuyết: đây là hình chiếu thống kê của "thân chủ AI quá ngoan" [7, 13] lên các thước đo quan hệ – cảm xúc.

**I3 — Hạt giống quyết định trần.** Nhóm semi-synthetic viết lại từ hỏi–đáp đại chúng đứng đáy chiều kỹ năng (−0.427 so với real, đã kiểm soát độ dài) *bất kể* kỹ thuật viết lại; nhóm fully-synthetic nhại giao thức chuyên gia (planning CBT [6], forecaster MI học từ AnnoMI [8]) vượt real +0.387. Viết lại thêm trôi chảy, không thêm kỹ năng vốn không có trong nguồn. Hệ quả thiết kế: chọn nguồn hạt giống là quyết định trần chất lượng, trước cả chọn model sinh.

**I4 — LLM quyết định vân tay, độc lập với hạt giống.** Lời counselor do LLM viết mang chữ ký thống kê nhất quán (tông +0.021; NEC +0.019; kết-vui +3.2 điểm %; nén phân phối ×2–3) ngay cả khi hạt giống là báo cáo ca thật (CPsyCoun) hay lời counselor thật được "làm mượt" (PsyDial ở phía trung gian). Cùng chiều với [16]; đóng góp của kiểm toán là chứng minh vân tay này **bất biến qua bốn ngôn ngữ và ba họ pipeline sinh**.

**I5 — Đơn vị phân tích là một quyết định đo lường có giá.** Psy-Insight — dataset duy nhất có cấu trúc ca đa phiên — bị chấm thấp ở B (3.605) và "phẳng" ở C (NEC ≈ 0; happy 49.6%) không phải vì kém, mà vì phiên bị tách khỏi ca: phiên giữa liệu trình không có mở–kết cảm xúc trọn vẹn, và bằng chứng liên minh phân tán qua nhiều phiên. Đối chứng: hội đồng judge đồng thuận *cao nhất nhì bảng* trên chính dataset này (α = 0.926) — điểm thấp là tín hiệu thật của đơn vị đo sai, không phải nhiễu. Đây là bằng chứng thực nghiệm đầu tiên định lượng "điểm mù đa phiên" của toàn bộ hệ thước đo hiện hành.

**I6 — Thứ hạng đáng tin hơn điểm số, và độ tin cậy thuộc về cặp (dataset × judge).** Kendall τ liên-judge 0.89–0.93 (A), giữa cấu hình ngôn ngữ 0.81–0.905, pilot→full 0.818 (A) — kết luận so sánh bền vững; trong khi điểm tuyệt đối lệch theo judge (GPT hào phóng hơn +0.35–0.40) và α dao động 0.52–0.95 theo phân phối dữ liệu. Hệ quả cho cộng đồng: công bố kết quả LLM-judge phải ở dạng (hạng, α-theo-dataset, panel), không phải một con số.

## 7. Hồ sơ kiểm toán rút gọn (audit card)

AnnoMI — *chuẩn hiệu chuẩn*: A #1 với biên độ đầy đủ (46.4% ≥4; 13.4% <2), B sát dải người thật; hạn chế: 112 phiên, trình diễn. · Cactus — *giao thức tốt, cảm xúc kịch bản*: A #2 nhưng SD 0.27, đã có tiền lệ trượt chiều cảm xúc [16]. · Psy-Insight — *bị đơn vị đo xử ép*: A #3, α cao nhất nhì; cần chấm cấp ca. · SimPsyDial — *hòa hợp kịch bản điển hình*: B #1, 99% ≥4, 0% <3, tông đỉnh 0.198. · KokoroChat — *real cân bằng nhất*: duy nhất chủ động phủ ca khủng hoảng; C/T 0.58 nhắc mốc phụ thuộc kênh. · KMI — *đúng nghề, giọng máy*: Goal 4.24 nhưng ASCQ 1.96. · PsyDial — *giữ cấu trúc thật duy nhất* (thân chủ nói dài hơn counselor), hạng B hưởng lợi độ dài. · SMILE/SoulChat — *đáy kép của viết-lại-đại-chúng*: A 2.32/2.19 dù B 4.17/3.99. · CPsyCoun — *chịu thiệt kép độ dài* (phiên ngắn nhất, thấp nhất B); giá trị ở khung 7 trường phái. · ESConv — *trung thực với construct peer-support*: A đội sổ theo thiết kế, B/C lành mạnh.

## 8. Threats to validity

(i) Không có neo chuyên gia người cho hội đồng judge của chính chúng tôi — kế thừa trần đồng thuận LLM–chuyên gia r ≈ 0.50 [12]; mọi kết quả chỉ có giá trị so sánh tương đối. (ii) Nguồn gốc đan xen ngôn ngữ; đã khử một phần bằng so sánh nội-ZH, phần dư (ví dụ real-EN so với real-JA) không tách được. (iii) Hồi quy mang pseudo-replication. (iv) Judge trộn phiên bản/route trong cùng họ model (ảnh hưởng đo được ≈ 0.04 điểm). (v) NEC/happy-ending là định nghĩa vận hành (kiểm chứng số học, chưa có nguồn lý thuyết độc lập). (vi) Mẫu 200 phiên/dataset có thể không phủ đuôi của dataset trăm-nghìn-mẫu. (vii) Kết quả mô tả dữ liệu, không suy ra trực tiếp giá trị huấn luyện (downstream nằm ngoài phạm vi).

## 9. Khuyến nghị và kết luận

**Người dùng dataset:** đối chiếu vector ba chiều với đích huấn luyện; mặc định nghi ngờ liên minh cao + kết-vui dày + phân phối nén (I2); khai thác mẫu âm tính từ AnnoMI/KokoroChat (nguồn duy nhất). **Người xây dataset:** chọn hạt giống chuyên gia trước khi chọn kỹ thuật sinh (I3); kiểm soát phân phối đầu ra (kết-vui ≤75%; ≥10% phiên không cải thiện; giữ thân chủ nói ≥ counselor); công bố datasheet gồm C/T, phân bố kết thúc, độ phủ chủ đề. **Người đo:** áp bộ hiệu chỉnh Bảng 4; công bố hạng + α theo dataset + panel judge; không dùng UED trên lexicon phủ <50%; thiết kế chéo generator × judge trước khi tin điểm tuyệt đối của dữ liệu máy.

Cuộc kiểm toán chéo đầu tiên trên 11 dataset tham vấn đa lượt cho thấy phần lớn "điểm chất lượng" đang lưu hành trong lĩnh vực là đại lượng ba lớp: tín hiệu thật của dữ liệu, vân tay của cách sinh dữ liệu, và hiện vật của thước đo. Tách ba lớp đó — như giao thức này minh họa — là điều kiện để các quyết định huấn luyện và các tuyên bố "an toàn cho sức khỏe tâm thần" đứng trên nền có thể kiểm chứng.

**Đạo đức.** Chỉ dùng dữ liệu công khai/được cấp; phát hiện tiêu cực trình bày ở mức dataset, không quy trách nhiệm cá nhân; kết quả không phải chứng nhận lâm sàng cho bất kỳ dataset hay hệ thống nào. **Tính tái lập:** mã trích xuất – tổng hợp – thống kê, bảng trung gian và hồ sơ kiểm toán phát hành kèm.

## Tài liệu tham khảo
[1]–[25]: danh mục đầy đủ trùng bài khảo sát đồng hành (ESConv; AnnoMI; SMILE; SoulChat; CPsyCoun; Cactus; SimPsyDial; KMI; PsyDial; Psy-Insight; KokoroChat; Li et al. 2024; MindEval 2025; Hipson & Mohammad 2021; Teodorescu & Mohammad 2023; Wang et al. 2025; PsyQA; EmpatheticDialogues; và các nguồn lý thuyết kinh điển Bordin 1979, Tichenor & Hill 1989, Hill 2009, Rogers 1946, Miller & Rollnick 2012, Beck 1979, Horvath & Symonds 1991 — trích dẫn thứ cấp qua kho lõi).
