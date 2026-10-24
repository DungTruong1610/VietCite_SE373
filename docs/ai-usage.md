# Minh bạch việc dùng công cụ AI

Quy tắc của môn: dùng AI phải **minh bạch** (ghi công cụ và phần việc), **kiểm chứng** (đối chiếu output, mở nguồn trích dẫn) và **giải thích được** (mỗi thành viên giải thích được mọi dòng code mình nộp).

Mỗi lần dùng AI cho phần việc đáng kể, thêm một dòng vào bảng. Ghi ngắn, đúng sự thật.

| Ngày | Người | Công cụ | Phần việc | Cách đã kiểm chứng |
|---|---|---|---|---|
| 24/10/2026 | TV1 | Claude Code | Tóm tắt slide Buổi 1–7 vào tài liệu tổng quan; soạn kế hoạch đồ án; tích hợp kiến thức Buổi 7 vào kế hoạch | Đối chiếu với slide gốc trong `slide/`; nhóm đọc lại và chỉnh sửa |
| 24/10/2026 | TV1 | Claude Code | Dựng khung Phase 0: `.gitignore`, `.env.example`, pre-commit + gitleaks, README, AGENTS.md, khung scorecard UC1–UC8, ADR 0001 | Chạy `pre-commit`; thử commit một key giả `sk-…` và xác nhận bị chặn |
| 24/10/2026 | TV1 | Claude Code | Đánh giá cách dùng thư viện UI `@cnma/react-ui`, viết `packages/README.md`, `scripts/check-ui-package.mjs`, ADR 0002 | Cài thử gói với React 19 trong thư mục tạm, import được 349 export; phát hiện 3 phụ thuộc gói thiếu khai báo; chạy script kiểm SHA-256 |
