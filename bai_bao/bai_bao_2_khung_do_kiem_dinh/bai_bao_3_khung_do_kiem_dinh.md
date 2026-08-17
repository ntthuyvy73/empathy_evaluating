# [BẢN THẢO 3 — DẠNG ĐỀ XUẤT: NGHIÊN CỨU ĐO LƯỜNG + KIỂM TOÁN CÓ KHUNG KIỂM ĐỊNH, bản viết lại]

# Hạt giống quyết định trần, LLM quyết định vân tay: Kiểm định khung đánh giá ba chiều cho dataset tham vấn tâm lý đa lượt qua kiểm toán chéo ngôn ngữ 11 dataset

**Tóm tắt.** Ba góc nhìn đánh giá vượt-mức-câu — liên minh trị liệu (WAI-O-S), rủi ro đặc thù AI (MindEval), động học cảm xúc (UED) — đang được đề xuất như ba "chiều" chấm chất lượng dataset tham vấn, nhưng chưa từng được kiểm định đồng thời trên cùng đối tượng: chúng có đo ba thứ khác nhau không, thước đo mang hiện vật gì, và điểm số phản ánh chất lượng hay phản ánh cách dữ liệu được sinh ra? Chúng tôi thao tác hóa cả ba chiều thành một giao thức thống nhất và áp lên 11 dataset đại diện (bốn nhóm nguồn gốc; EN/ZH/JA/KO; 2,111 hội thoại; hội đồng ba LLM-judge khác họ; 12,666 lượt chấm; pilot đối chứng 3 cấu hình ngôn ngữ × 2 cấu hình lexicon). Bốn kết quả chính: **(RQ1)** ma trận hội tụ–phân biệt hai cấp xác nhận ba chiều gần trực giao ở cấp phiên (kỹ năng↔cảm xúc −0.031; kỹ năng↔liên minh 0.375) nhưng phát hiện *hội tụ chọn lọc theo cấp phân tích*: liên minh và kết-thúc-dương đồng biến mạnh giữa dataset (ρ = 0.724, p = 0.012) dù gần độc lập trong nội bộ dataset (0.172) — chữ ký thống kê của kịch bản hóa. **(RQ2)** ba hiện vật thước đo đủ lớn để đảo thứ hạng được định lượng: WAI thưởng độ dài (b = +0.305/log-token; rubric kỹ năng miễn nhiễm, −0.019); hào quang 12 câu WAI (r̄ = 0.715; Goal↔Approach = 0.891); nhiễu lexicon thưa (r giữa độ phủ và biến thiên = −0.455, p ≈ 7×10⁻⁷²). **(RQ3)** sau kiểm soát độ dài, hai định luật nguồn gốc tách bạch: *hạt giống quyết định trần* (nhóm viết lại từ hỏi–đáp đại chúng: −0.427 điểm kỹ năng so với real; nhóm mô phỏng giao thức chuyên gia: +0.387) và *LLM quyết định vân tay* (lời counselor LLM: tông cảm xúc 0.185 so với 0.164, kết-vui 75.2% so với 72.0%, phân phối nén 2–3 lần) — kiểm tra nội-ngôn-ngữ ZH lặp lại đúng thứ bậc, loại trừ ảo ảnh ngôn ngữ. **(RQ4)** kết luận dạng thứ hạng bền vững qua judge, cấu hình và cỡ mẫu (Kendall τ 0.81–0.93) trong khi điểm tuyệt đối thì không; cấu hình "giữ bản gốc + prompt tiếng Anh" đạt chất lượng tương đương dịch toàn bộ (~1.08 triệu token) với chi phí bằng không; và độ tin cậy hội đồng judge là thuộc tính của cặp (dataset × judge), dao động α = 0.52–0.95 theo phân phối dữ liệu. Từ đó chúng tôi đề xuất khung vận hành "3 chiều lõi + 2 chiều nền" kèm bộ quy tắc hiệu chỉnh, và lộ trình "đo trước – sinh sau" cho dataset tham vấn đa lượt – đa phiên tiếng Việt đầu tiên. Toàn bộ giao thức, mã và bảng số liệu được công bố.

**Từ khóa:** đánh giá dataset; giá trị hội tụ–phân biệt; LLM-as-judge; liên minh trị liệu; động học cảm xúc; dữ liệu tổng hợp; ngôn ngữ ít tài nguyên.

## 1. Giới thiệu

Ba mệnh đề đang được cộng đồng chấp nhận ngầm. *Thứ nhất*: các chiều đánh giá mới đo những thứ khác nhau và đáng tồn tại song song — bằng chứng hiện có chỉ là ba "ca án" rời rạc (Cactus vượt bộ lọc CTRS và thắng đánh giá người nhưng trượt chiều cảm xúc với r = 0.84 [16]; xếp hạng an toàn ASCQ của MindEval tách khỏi xếp hạng năng lực [13]; SimPsyDial đạt WAI cao hơn dữ liệu thật trong khi cấu trúc lệch xa thật [7]). *Thứ hai*: điểm LLM-judge phản ánh chất lượng dữ liệu — dù các meta-evaluation đã cảnh báo judge thổi phồng dữ liệu máy và mang self-preference bias [13]. *Thứ ba*: kết quả đo trên một ngôn ngữ/cấu hình chuyển giao được sang bối cảnh khác — giả định hệ trọng với các ngôn ngữ ít tài nguyên sắp xây dataset đầu tiên. Bài báo này kiểm định cả ba mệnh đề trong một thiết kế duy nhất, với bốn câu hỏi:

**RQ1 (giá trị hội tụ–phân biệt):** ba chiều có đo ba cấu trúc khác nhau trên cùng 11 dataset không? **RQ2 (hiện vật đo lường):** bao nhiêu phần của "điểm" là thuộc tính của thước đo thay vì của dữ liệu? **RQ3 (định luật nguồn gốc):** sau khi khử nhiễu đo được, nguồn gốc dữ liệu để lại khác biệt hệ thống nào? **RQ4 (khả chuyển):** kết luận sống sót qua judge, cấu hình ngôn ngữ, cỡ mẫu và đơn vị phân tích đến đâu — và hàm ý gì cho tiếng Việt?

**Đóng góp.** (C1) Thao tác hóa thống nhất, tái lập được của ba chiều trên hội thoại tĩnh — lần đầu cả ba chạy đồng thời trên cùng đối tượng; (C2) ma trận hội tụ–phân biệt hai cấp đầu tiên cho đánh giá dataset tham vấn, kèm phát hiện "hội tụ chọn lọc theo cấp"; (C3) danh mục hiện vật đo lường được định lượng thành hệ số hiệu chỉnh; (C4) hai định luật nguồn gốc có kiểm soát nhiễu và khử một phần confound ngôn ngữ; (C5) khung vận hành "3 lõi + 2 nền" với dải tham chiếu số học và lộ trình đo-trước-sinh-sau cho tiếng Việt.

## 2. Nền tảng và công trình liên quan

**Ba góc nhìn.** WAI-O-S bắt nguồn từ khái niệm liên minh làm việc của Bordin [19] và bản thang quan sát của Tichenor & Hill [20], được Li et al. [12] thao tác hóa cho tham vấn văn bản bằng LLM-judge với guidelines chi tiết và cơ chế trích-bằng-chứng-trước-điểm (khớp chuyên gia r ≈ 0.50; liên minh ↔ kết cục ORS r ≈ 0.30 trên 859 phiên thật). MindEval [13] vận hành hóa các rủi ro đặc thù AI (nịnh hót, tạo phụ thuộc, xói mòn ranh giới, ảo giác) thành 5 trục × 1–6 neo hướng dẫn APA, chấm toàn tương tác, meta-evaluation với bốn nhà tâm lý và phát hiện self-preference bias. UED [14] đo động học cảm xúc từ lời nói bằng lexicon; điều kiện tin cậy được thẩm định ở [15] (cung cảm xúc >0.9 khi gộp ≥50 mẫu/bin; lexicon dịch cần bin ≥200); [16] áp vào so sánh dataset thật–tổng hợp. **Khoảng trống:** chưa công trình nào chạy cả ba trên cùng tập dataset để kiểm định trực giao bằng số; tách hiện vật thước đo khỏi tín hiệu dữ liệu; kiểm soát độ dài/ngôn ngữ khi so nhóm nguồn gốc; hay đo độ bền của kết luận theo judge/cấu hình/cỡ mẫu.

## 3. Phương pháp

**Đối tượng.** 11 dataset theo taxonomy nguồn gốc bốn nhóm: real (ESConv [1], KokoroChat [11], Psy-Insight [10]), semi-real (AnnoMI [2], PsyDial [9]), semi-synthetic (SMILE [3], SoulChat [4], CPsyCoun [5]), fully-synthetic (Cactus [6], SimPsyDial [7], KMI [8]); 200 phiên/dataset (AnnoMI 112; SMILE 199), tổng 2,111 phiên.

**Bảng 1.** Thao tác hóa ba chiều.

| | Chiều A — Kỹ năng | Chiều B — Liên minh | Chiều C — Cảm xúc |
|---|---|---|---|
| Công cụ / thang | MindEval 5 trục × 1–6 [13] | WAI-O-S 12 câu × 1–5, Goal–Approach–Bond [12] | UED [14] + NEC, happy-ending (vận hành, kiểm chứng số học 100%) |
| Đơn vị chấm | toàn phiên | từng câu, 3 lần chạy, trung bình | cửa sổ trượt 10 từ, NRC-VAD |
| Hội đồng | 3 LLM khác họ; trung bình; α theo dataset | như A | không judge |
| Đối chứng | S1/S2/S3 (pilot 20 phiên/dataset) | S1/S3 | lexicon A (bản ngữ) / B (dịch EN) |

**Quyết định giao thức từ pilot (số liệu):** chọn S3 (S2 phá đồng thuận judge: Pearson liên-judge pooled 0.286 so với 0.467/0.423; S1 ≈ S3: |Δ| ≤ 0.073, τ hạng 0.810, nhưng tốn ~1.08 triệu token dịch); loại judge thứ tư vì lệch hệ thống (bias +0.766…+1.190); chiều C lấy cấu hình B làm chính (mục 5.3). **Phân tích:** MTMM hai cấp; hồi quy điểm ~ nguồn gốc + log-token (khai báo pseudo-replication); khử một phần confound bằng so sánh nội-ZH; Kendall τ; phân tích nhân tố nội chiều; kiểm verbosity và self-preference.

## 4. RQ1 — Giá trị hội tụ–phân biệt

![Hình 1. Ma trận hội tụ–phân biệt hai cấp: gần trực giao ở cấp phiên; hội tụ B↔C chọn lọc ở cấp dataset.](figs/fig_mtmm.png)

Cấp phiên (pooled-z nội dataset, n ≈ 2,111): A↔C(NEC) = −0.031; B↔C = 0.172; A↔B = 0.375. Cấp dataset (n = 11): A↔B ρ = 0.182 (p = 0.593); A↔happy = −0.369 (p = 0.264); **B↔happy = 0.724 (p = 0.012); B↔NEC = 0.655 (p = 0.029)**. Ba kết luận: (i) trực giao kỹ-năng↔cảm-xúc là tuyệt đối ở cả hai cấp — "counselor được chấm giỏi" không mang thông tin về chuyển biến cảm xúc của thân chủ; minh họa cấp phiên: `cactus_121` (A = 4.10, NEC = −0.081) và `kmi_712` (A = 3.27, NEC = −0.268) so với `soulchat_157820` (A = 1.80, NEC = +0.511); (ii) A↔B chồng lấn vừa phải, đủ riêng để giữ hai chiều; (iii) phát hiện vượt khung lý thuyết: **hội tụ chọn lọc theo cấp** — liên minh và kết-vui gần độc lập trong từng dataset nhưng đồng biến mạnh giữa dataset, tức phần chung của chúng nằm ở *phong cách sinh dữ liệu*, không ở quan hệ nhân quả trong phiên. Cấu trúc tương quan hai-cấp này tự nó là một thước đo mới: chỉ báo kịch bản hóa cấp dataset.

## 5. RQ2 — Hiện vật đo lường

![Hình 2. Thưởng độ dài bất đối xứng giữa hai chiều: liên minh tăng theo log-độ-dài (b = +0.305), kỹ năng miễn nhiễm (b = −0.019).](figs/fig_length_effect.png)

1. **Thưởng độ dài bất đối xứng** (Hình 2): cơ chế anchor "3 = chưa có bằng chứng" của WAI biến độ dài thành cơ hội tích lũy bằng chứng; hệ quả thực: PsyDial — phiên dài nhất corpus — đạt hạng 3 liên minh; ~1/3 khoảng cách thô giữa dataset ngắn nhất (CPsyCoun, 89 token thân chủ) và nhóm đầu là hiệu ứng độ dài. *Quy tắc:* báo cáo kèm điểm residual độ dài.
2. **Hào quang trong WAI:** tương quan liên-câu trung bình 0.715 (α = 0.968); Goal↔Approach 0.891 — ba tiểu thang của Bordin không tách được khi người chấm là LLM đọc transcript; between-dataset SD chỉ 0.286 → thứ hạng kém bền (τ liên-judge 0.60–0.71 so với 0.89–0.93 của chiều A; τ pilot→full 0.564 so với 0.818). *Quy tắc:* đọc chiều B theo cụm; giữ câu kháng-hào-quang Q10 ("thân chủ tin năng lực counselor" — câu thấp nhất gần như toàn cục, kể cả ở dữ liệu tô hồng) làm chỉ báo đơn.
3. **Nhiễu lexicon thưa:** lexicon bản ngữ dịch tự động phủ 23–31% token; độ phủ tương quan âm mạnh với biến thiên đo được (r = −0.455, p ≈ 7×10⁻⁷², n = 1,398); NEC đổi dấu ở 5/7 dataset; tương quan giữa hai cấu hình ở cấp phiên chỉ 0.07–0.42. *Quy tắc:* công bố độ phủ kèm mọi chỉ số UED; không so chéo ngôn ngữ khi độ phủ <50% — nhất quán tiên đoán lý thuyết của [15].
4. **Rubric kỹ năng gần một nhân tố:** CAC↔AR = 0.936; cụm CAC–AR–TRA α = 0.928; EPC và ASCQ tách riêng và là hai trục phân biệt dataset mạnh nhất (range trung bình dataset 2.50 và 2.24 điểm). *Quy tắc:* rubric ba trục (lâm sàng chung; ranh giới; ASCQ) giảm ~40% chi phí judge gần như không mất thông tin.
5. **Độ tin cậy là thuộc tính (dataset × judge):** trong cùng hội đồng, α = 0.520 (SoulChat) đến 0.949 (AnnoMI); dữ liệu phương sai thật cho đồng thuận cao (Psy-Insight 0.926), dữ liệu nén làm α sụp vì giới hạn biên độ (SimPsyDial 0.526 dù MAE liên-judge chỉ 0.154). Test–retest các trường hợp chấm lại độc lập: r = 0.41–0.80. *Quy tắc:* công bố α theo dataset; chỉ dùng trung bình hội đồng; không kết luận từ điểm một phiên đơn lẻ.
6. **Dấu hiệu self-preference:** GPT chấm hai dataset do họ GPT sinh cao hơn Claude 0.29–0.38 điểm — chưa đủ thiết kế chéo để kết luận; liệt kê làm kiểm định bắt buộc.

## 6. RQ3 — Hai định luật nguồn gốc

![Hình 3. Vân tay nguồn gốc trên bốn đại lượng (trung bình nhóm; trục y cắt).](figs/fig_group_fingerprint.png)

Hồi quy mức phiên có kiểm soát log-độ-dài (n = 2,111; tham chiếu: real): chiều A — semi-real +0.218, semi-synthetic **−0.427**, fully-synthetic **+0.387** (R² = 0.180); chiều B — semi-real −0.186, semi-synthetic −0.038, fully-synthetic **+0.237** (R² = 0.312). Kiểm tra nội-ngôn-ngữ ZH (đủ ba nhóm LLM-tham-gia) lặp lại đúng thứ bậc — hiệu ứng nhóm không phải ảo ảnh ngôn ngữ.

**Định luật 1 — hạt giống quyết định trần.** Nhóm semi-synthetic viết lại từ hỏi–đáp đại chúng đứng đáy chiều kỹ năng bất kể kỹ thuật viết lại (SMILE 2.32; CPsyCoun 2.29; SoulChat 2.19); nhóm fully-synthetic nhại giao thức chuyên gia (planning CBT [6]; forecaster MI học từ AnnoMI với R:Q = 1.8:1 chuẩn MITI [8]) đạt 2.65–3.38. Viết lại bằng LLM thêm trôi chảy, không thêm kỹ năng vốn không có trong nguồn.

**Định luật 2 — LLM quyết định vân tay.** Lưỡng phân "ai viết lời counselor": tông cảm xúc 0.185 (LLM) so với 0.164 (người); NEC 0.066 so với 0.047; kết-vui 75.2% so với 72.0%; nén phân phối kỹ năng SD 0.27–0.39 so với 0.58–1.08. Vân tay bám theo *bàn tay trên văn bản*, độc lập với hạt giống thật hay không — bất biến qua bốn ngôn ngữ và ba họ pipeline sinh; tái lập độc lập [16] ở quy mô 11 dataset.

**Hệ quả — ma trận thiết kế 2×2** (hạt giống chuyên gia/đại chúng × người/LLM viết): (chuyên gia × người) chuẩn nhưng đắt; (chuyên gia × LLM) trần cao + vân tay máy → cần cổng QC cảm xúc; (đại chúng × người) "ấm mà non nghề" (ESConv: A = 1.80 nhưng B = 4.01, NEC = 0.082 — trung thực với construct peer-support); (đại chúng × LLM) đáy kép → tránh. Kèm cảnh báo diễn giải: phần thưởng +0.24/+0.39 của fully-synthetic không tách được hoàn toàn khỏi thiên vị văn phong của judge (mục 5.6) — theo nguyên tắc thận trọng, mọi kết quả "dữ liệu máy tốt hơn dữ liệu người" phải bị nghi ngờ trước tiên.

## 7. RQ4 — Khả chuyển và đơn vị phân tích

(1) **Hạng bền, điểm không bền:** Kendall τ liên-judge 0.89–0.93 (A); giữa cấu hình S1/S3 = 0.810, S2/S3 = 0.905; pilot→full 0.818 (A) nhưng 0.564 (B — hệ quả dải nén). (2) **Biên chi phí–chất lượng của cấu hình ngôn ngữ:** S3 (giữ bản gốc + prompt tiếng Anh) đạt chất lượng tương đương S1 với chi phí dịch bằng 0; điều kiện: judge đủ năng lực đa ngữ — judge yếu lệch tới 0.54 điểm chỉ vì đổi ngôn ngữ prompt và bị loại. (3) **Đơn vị phân tích là quyết định đo lường:** Psy-Insight — dataset duy nhất có cấu trúc ca đa phiên (951 phiên/189 ca [10]) — bị mọi thước đo cấp phiên hạ thấp (NEC ≈ −0.000; kết-vui 49.6% ở mức ngẫu nhiên; liên minh 3.605) trong khi hội đồng judge đồng thuận cao nhất nhì bảng trên chính nó (α = 0.926): điểm thấp là tín hiệu thật của *đơn vị đo sai*, không phải nhiễu — bằng chứng định lượng đầu tiên cho điểm mù đa phiên của toàn bộ hệ thước đo hiện hành. (4) **Chuyển giao sang tiếng Việt:** mốc cấu trúc phụ thuộc kênh/văn hóa (C/T 1.35 trên nền tảng text Trung Quốc so với 0.58 trên LINE Nhật [11]); lexicon dịch không dùng được ở granularity nhỏ (mục 5.3); rubric cần neo lại quy điều đạo đức nghề bản địa — bốn công cụ (WAI-VN; lexicon VAD-VN thẩm định bản ngữ; rubric rủi ro AI-VN; thang lâm sàng khớp liệu pháp) phải Việt hóa và meta-evaluate với chuyên gia Việt **trước** khi sinh dữ liệu, mở màn bằng pilot 20 phiên lặp lại thiết kế S1/S2/S3.

## 8. Khung vận hành "3 lõi + 2 nền" và lộ trình tiếng Việt

**Khung kèm quy tắc hiệu chỉnh** (thứ tự theo chi phí): (nền 1) cấu trúc — số lượt, tỷ lệ token thân chủ/counselor, phân bố độ dài; (lõi C) UED cấp phân bố + độ phủ lexicon + NEC cắt nghi thức chào–kết; (nền 2) thang lâm sàng khớp liệu pháp; (lõi B) WAI + residual độ dài + đọc theo cụm; (lõi A) rubric ba trục + kiểm self-preference. Mỗi vòng đo dùng để *sửa pipeline sinh*, không chỉ loại mẫu. **Dải tham chiếu người thật** (rút từ nhóm người-viết của kiểm toán): tông counselor ≤ 0.17; kết-vui 60–75%; SD kỹ năng nội bộ ≥ 0.4; ≥10% phiên không cải thiện; ≥5% phiên liên minh <3; thân chủ nói ≥ counselor. **Lộ trình năm tầng "đo trước – sinh sau":** (0) mốc thật tiếng Việt 50–100 phiên (đủ theo hai tiền lệ: 76 phiên RealCBT [16]; 112 phiên AnnoMI trong kiểm toán này); (1) lõi role-play counselor Việt kèm phản hồi cấu trúc ~20 mục, chủ động phủ ca khủng hoảng trong môi trường kiểm soát (con đường duy nhất có tiền lệ [11], vì cả benchmark tự động [13] lẫn sinh tự động [8] đều mù/tự kiểm duyệt vùng này); (2) nhân rộng máy-có-neo (planning trị liệu, thân chủ có kháng cự, role card thật, few-shot giáo trình tiếng Việt); (3) cổng QC 3+2 chạy vòng lặp; (4) chuẩn cuối chuyên gia + benchmark động + phát hành kèm tài nguyên đánh giá. Multi-session thiết kế từ tầng 0: client-ID 3–10 phiên, quỹ đạo WAI theo phiên, NEC xuyên phiên, thang kết cục đầu phiên — trực tiếp lấp điểm mù ở mục 7(3).

## 9. Hạn chế

Không có neo chuyên gia người cho hội đồng judge (kế thừa trần r ≈ 0.50 [12]); nguồn gốc đan xen ngôn ngữ, chỉ khử được một phần; hồi quy mang pseudo-replication; n = 11 cho tương quan cấp dataset; NEC/happy-ending là định nghĩa vận hành; chưa khép vòng downstream (điểm mô tả dữ liệu ≠ giá trị huấn luyện; bằng chứng gián tiếp cùng hướng từ ba nghiên cứu gốc: bản dữ liệu nhỏ-chất-lượng thắng bản lớn ở [11], [6], [9]); mẫu 200 phiên/dataset có thể không phủ đuôi phân phối gốc.

## 10. Kết luận

Ba chiều đánh giá vượt qua kiểm định hội tụ–phân biệt và xứng đáng thành chuẩn báo cáo cho dataset tham vấn — nhưng chỉ khi đi kèm bộ hiệu chỉnh hiện vật mà nghiên cứu này định lượng, vì với thước đo hiện tại, một phần của "chất lượng" là tiếng vọng của cách dữ liệu được sinh ra. Hai định luật nguồn gốc cho người xây dataset một la bàn: *chọn hạt giống là chọn trần; chọn ai viết lời là chọn vân tay*. Với các ngôn ngữ chưa có dataset như tiếng Việt, lợi thế người đi sau nằm ở một chỗ duy nhất: dựng thước đo đã kiểm định trước khi viết dòng hội thoại đầu tiên.

**Đạo đức.** Dữ liệu công khai/được cấp, đã ẩn danh; phát hiện tiêu cực ở mức dataset; kết quả không phải chứng nhận lâm sàng; vùng khủng hoảng thuộc về chuyên gia người trong mọi khâu. **Tính tái lập:** giao thức, mã, bảng trung gian và hồ sơ kiểm toán phát hành kèm.

## Tài liệu tham khảo
[1] S. Liu, C. Zheng, O. Demasi, S. Sabour, Y. Li, Z. Yu, Y. Jiang, M. Huang. Towards Emotional Support Dialog Systems. ACL-IJCNLP 2021.
[2] Z. Wu, S. Balloccu, V. Kumar, R. Helaoui, E. Reiter, D. Reforgiato Recupero, D. Riboni. AnnoMI: A Dataset of Expert-Annotated Counselling Dialogues. ICASSP 2022.
[3] H. Qiu, H. He, S. Zhang, A. Li, Z. Lan. SMILE: Single-turn to Multi-turn Inclusive Language Expansion via ChatGPT for Mental Health Support. 2023/Findings EMNLP 2024.
[4] Y. Chen, X. Xing, J. Lin, H. Zheng, Z. Wang, Q. Liu, X. Xu. SoulChat. Findings EMNLP 2023.
[5] C. Zhang, R. Li, M. Tan, M. Yang, J. Zhu, D. Yang, J. Zhao, G. Ye, C. Li, X. Hu. CPsyCoun. Findings ACL 2024.
[6] S. Lee, S. Kim, M. Kim, et al., K.-M. Chung, Y. Yu, D. Lee, J. Yeo. Cactus: Towards Psychological Counseling Conversations using Cognitive Behavioral Theory. Findings EMNLP 2024.
[7] H. Qiu, Z. Lan. Interactive Agents (SimPsyDial). arXiv:2408.15787, 2024.
[8] H. Kim, S. Lee, Y. Cho, E. Ryu, Y. Jo, S. Seong, S. Cho. KMI: A Dataset of Korean Motivational Interviewing Dialogues for Psychotherapy. NAACL 2025.
[9] H. Qiu, Z. Lan. PsyDial: A Large-scale Long-term Conversational Dataset for Mental Health Support. ACL 2025.
[10] K. Chen, Z. Sun, Y. Wen, H. Lian, Y. Gao, Y. Li. Psy-Insight: Explainable Multi-turn Bilingual Dataset for Mental Health Counseling. arXiv, 2025.
[11] Z. Qi, T. Kaneko, K. Takamizo, M. Ukiyo, M. Inaba. KokoroChat. arXiv:2506.01357, 2025.
[12] A. Li, Y. Lu, N. Song, S. Zhang, L. Ma, Z. Lan. Understanding the Therapeutic Relationship between Counselors and Clients in Online Text-based Counseling using LLMs. arXiv:2402.11958, 2024.
[13] J. Pombal, M. D'Eon, N.M. Guerreiro, P.H. Martins, A. Farinhas, R. Rei. MindEval. arXiv:2511.18491, 2025.
[14] W.E. Hipson, S.M. Mohammad. Emotion Dynamics in Movie Dialogues. PLOS ONE 16(9), 2021.
[15] D. Teodorescu, S.M. Mohammad. Evaluating Emotion Arcs Across Languages. Findings EMNLP 2023.
[16] X. Wang, J. Zhang, G. Zhang, H. Guo. Feel the Difference? arXiv:2508.20764, 2025.
[17] H. Sun, Z. Lin, C. Zheng, S. Liu, M. Huang. PsyQA. Findings ACL-IJCNLP 2021.
[18] H. Rashkin, E.M. Smith, M. Li, Y.-L. Boureau. Towards Empathetic Open-domain Conversation Models. ACL 2019.
[19]–[25] Nguồn lý thuyết kinh điển (Bordin 1979; Tichenor & Hill 1989; Hill 2009; Rogers 1946; Miller & Rollnick 2012; Beck 1979; Horvath & Symonds 1991) — trích dẫn thứ cấp qua kho lõi, chi tiết như bài khảo sát đồng hành.
