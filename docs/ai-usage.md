# Minh bạch việc dùng công cụ AI

Quy tắc của môn: dùng AI phải **minh bạch** (ghi công cụ và phần việc), **kiểm chứng** (đối chiếu output, mở nguồn trích dẫn) và **giải thích được** (mỗi thành viên giải thích được mọi dòng code mình nộp).

Mỗi lần dùng AI cho phần việc đáng kể, thêm một dòng vào bảng. Ghi ngắn, đúng sự thật.

| Ngày | Người | Công cụ | Phần việc | Cách đã kiểm chứng |
|---|---|---|---|---|
| 24/10/2026 | TV1 | Claude Code | Tóm tắt slide Buổi 1–7 vào tài liệu tổng quan; soạn kế hoạch đồ án; tích hợp kiến thức Buổi 7 vào kế hoạch | Đối chiếu với slide gốc trong `slide/`; nhóm đọc lại và chỉnh sửa |
| 24/10/2026 | TV1 | Claude Code | Dựng khung Phase 0: `.gitignore`, `.env.example`, pre-commit + gitleaks, README, AGENTS.md, khung scorecard UC1–UC8, ADR 0001 | Chạy `pre-commit`; thử commit một key giả `sk-…` và xác nhận bị chặn |
| 24/10/2026 | TV1 | Claude Code | Đánh giá cách dùng thư viện UI `@cnma/react-ui`, viết `packages/README.md`, `scripts/check-ui-package.mjs`, ADR 0002 | Cài thử gói với React 19 trong thư mục tạm, import được 349 export; phát hiện 3 phụ thuộc gói thiếu khai báo; chạy script kiểm SHA-256 |
| 24/10/2026 | TV1 | Claude Code | Lập kế hoạch website demo Tallyo (`docs/website-tallyo/plan.html`), viết nháp dữ kiện giả lập `facts.yaml` và dàn ý 16 trang | Script kiểm YAML hợp lệ, title ≤ 60 ký tự, meta description 120–160 ký tự. **Chưa kiểm chứng:** 6 văn bản pháp luật trong `facts.yaml` do Claude viết từ trí nhớ (`verified: false`), TV2 cần đối chiếu nguồn chính thống; mức giá và số liệu công ty là giả lập, TV3 cần duyệt |
| 24/10/2026 | TV1 | Claude Code (kèm một agent nghiên cứu) | Dựng toàn bộ website demo Tallyo: generator `tools/sitegen`, theme theo brand conarum, nội dung 16 trang, bộ test; tra cứu và đối chiếu 15 văn bản pháp luật về hộ kinh doanh, hoá đơn điện tử, kế toán, dữ liệu cá nhân | `sitegen check --strict` 0 lỗi; 46 test pass (build tất định, trafilatura, Playwright 390/1440 px, axe-core WCAG AA). Pháp luật: agent đọc bản PDF ký số trên cổng Chính phủ; Claude mở lại từng trang nguồn để đối chiếu số hiệu, ngày ban hành, ngày hiệu lực, và tự đọc Điều 8 Nghị định 68/2026. **Chưa kiểm chứng:** nhóm chưa duyệt mức giá, số liệu công ty giả lập và giọng văn (TV3); cần đối chiếu lại pháp luật trước khi nộp |
