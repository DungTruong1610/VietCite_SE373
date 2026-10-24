# UC7: Đo AI Visibility trước và sau (SGE-vi)

> **Ưu tiên:** P0 · **Phụ trách:** TV5 · **Phase:** 3 (baseline), 7 (trước/sau) · **Trạng thái:** Chưa bắt đầu

## 1. Mục tiêu, input, output
- **Mục tiêu:** trả lời bằng số liệu: *có bài rồi thì AI có nhắc tới thương hiệu nhiều hơn không?*
- **Input:** tập truy vấn đo **D7** (40 câu phân tầng theo intent), alias thương hiệu và đối thủ, snapshot nguồn web của từng truy vấn, bài cần đo.
- **Output:** báo cáo thí nghiệm gồm metric theo từng truy vấn, tổng hợp kèm khoảng tin cậy 95%, và drill-down câu trả lời giả lập có tô sáng chỗ nhắc thương hiệu.

## 2. Phân loại
| Câu hỏi | Trả lời |
|---|---|
| Ai quyết bước tiếp? | **Code**: thí nghiệm tất định |
| Ai giữ state? | Hệ thống: cache theo seed và ngày |
| Ai dừng? | Code: hết truy vấn × điều kiện × seed |

**Kết luận:** workflow (thiết kế thí nghiệm) + LLM judge.

## 3. Bốn lớp đo
1. **Closed-book probe:** hỏi DeepSeek và Gemini không cho truy xuất. Đây là đối chứng, cho thấy bài tác động qua lớp truy xuất chứ không qua trọng số model.
2. **Gemini + Google Search grounding:** AI thật trên web thật, đọc `groundingMetadata`. Đây là **baseline thật**.
3. **SGE-vi:** engine giả lập. Hybrid retrieval chọn nguồn từ pool có hoặc không có bài, DeepSeek trả lời kèm trích dẫn; xáo thứ tự nguồn, 3 seed mỗi truy vấn. Hiệu chỉnh bằng Spearman ρ với Gemini grounded.
4. **Probe thủ công ChatGPT, Perplexity:** thành viên hỏi bản miễn phí rồi nhập kết quả.

**Giới hạn (ghi rõ trong báo cáo):** bài chỉ đăng trên WordPress local nên AI thật không đọc được. Phần "sau" đo bằng SGE-vi.

## 4. Chức năng (0,5đ)
- [ ] Chạy một lệnh ra báo cáo.
- [ ] Dashboard so sánh trước và sau.
- **Thí nghiệm:** A0 (không có bài) / A1 (bài viết thường, không có skill GEO) / A2 (bài VietCite). Báo cáo lift A2−A0 và A2−A1 bằng paired bootstrap CI 95% và Wilcoxon.
- **Lệnh demo:** *(bổ sung khi có code, dự kiến `geo visibility run --exp <id>`)*

## 5. Thiết kế harness (0,5đ)
| Lớp | Dùng thế nào | Vì sao | File |
|---|---|---|---|
| retrieval | SGE-vi là một RAG pipeline; bài không được cưỡng ép vào pool | Đo công bằng | `geo/measurement/sge_simulator.py` |
| verification | Metric tính bằng code; judge Gemini temperature 0, rubric cố định | Tái lập được | `geo/measurement/metrics.py` |
| logging | Cache theo seed và ngày; ghi cost của cả thí nghiệm | Tái lập, kiểm soát chi phí | `geo/tracing/` |

**Metric:** mention rate, citation rate, share of voice, vị trí lần nhắc đầu, Position-Adjusted Word Count, Subjective Impression.

## 6. Kiểm chứng (0,5đ)
- Unit test metric trên câu trả lời tổng hợp có đáp án biết trước: 100%.
- Độ chính xác phát hiện mention so với 100 câu trả lời gán nhãn tay ≥ 0,95.
- Tái lập: cùng seed và cache cho cùng kết quả.
- Spearman ρ giữa SGE-vi và Gemini grounded (báo cáo trung thực, kỳ vọng ρ ≥ 0,5).
- **Kết quả thực đo:** *(chưa có)*
- **Trace mẫu:** *(chưa có)*
- **Ca thất bại (debug 4 bước):** *(chưa có)*

## 7. Kiến thức phủ
K1 ○ · K3 ○ · K5 ● · K7 ● · K8 ○
