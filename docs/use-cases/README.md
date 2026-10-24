# Scorecard các use case

Mỗi use case được chấm **1,5 điểm** theo 3 tiêu chí, mỗi tiêu chí 0,5: **Chức năng** (chạy đúng tiêu chí) · **Thiết kế harness** (đúng kỹ thuật) · **Kiểm chứng** (có eval và trace). Năm use case trọn điểm là đủ 7,5.

Mỗi file UC giữ đúng cấu trúc giám khảo cần đọc:
1. Mục tiêu, input, output
2. Phân loại theo 3 câu hỏi của Buổi 1
3. Sơ đồ luồng
4. Chức năng: tiêu chí chấp nhận và lệnh demo
5. Thiết kế harness: lớp nào, vì sao, ở file nào
6. Kiểm chứng: dataset, metric, ngưỡng, kết quả thực đo, trace mẫu, một ca thất bại
7. Kiến thức phủ (K1–K8)

| UC | Tên | Ưu tiên | Phụ trách | Phase | Trạng thái |
|---|---|---|---|---|---|
| [UC1](UC1-brand-analysis.md) | Phân tích thương hiệu, sinh Brand-Voice Skill | P0 | TV3 | 3 | Chưa bắt đầu |
| [UC2](UC2-query-universe.md) | Bản đồ câu hỏi người dùng hỏi AI | P1 | TV3 / TV5 | 3 | Chưa bắt đầu |
| [UC3](UC3-research-evidence.md) | Nghiên cứu nguồn và Evidence Ledger | P0 | TV2 | 2, 4 | Chưa bắt đầu |
| [UC4](UC4-geo-writer.md) | Viết bài GEO theo giọng thương hiệu | P0 | TV3 | 4 | Chưa bắt đầu |
| [UC5](UC5-factcheck-editor.md) | Kiểm chứng số liệu và biên tập | P0 | TV4 | 5 | Chưa bắt đầu |
| [UC6](UC6-schema-markup.md) | Schema markup và GEO kỹ thuật | P1 | TV4 | 5 | Chưa bắt đầu |
| [UC7](UC7-ai-visibility.md) | Đo AI Visibility trước và sau | P0 | TV5 | 3, 7 | Chưa bắt đầu |
| [UC8](UC8-approve-publish.md) | Duyệt và xuất bản WordPress | P0 | TV1 | 6 | Chưa bắt đầu |

Đặc tả gốc: [KE_HOACH_DO_AN.md](../KE_HOACH_DO_AN.md) mục 5.
