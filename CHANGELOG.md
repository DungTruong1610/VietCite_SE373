# Changelog

Định dạng theo [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), đánh phiên bản theo [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Phase 0: khung repo gồm `.gitignore`, `.env.example`, pre-commit (gitleaks có rule cho key DeepSeek `sk-…` và Jina `jina_…`, ruff, các kiểm tra cơ bản), `README.md`, `AGENTS.md`.
- Tài liệu: tổng quan môn học và yêu cầu đồ án, kế hoạch đồ án, ma trận K1–K8, khung scorecard UC1–UC8, ADR 0001 về tech stack, file minh bạch dùng AI.

- Hướng dẫn dùng thư viện UI nội bộ `@cnma/react-ui` 1.1.4 (`packages/README.md`), script `scripts/check-ui-package.mjs` kiểm tra gói có mặt và đúng SHA-256, ADR 0002.
- Website demo Tallyo (16 trang, HTML tĩnh) ở `fixtures/brands/tallyo/`: nội dung Markdown, dữ kiện `facts.yaml` làm nguồn sự thật duy nhất, theme theo brand conarum (không dùng logo conarum), hai bản build `site/2026-10-24/` và `site/2026-11-10/` (đổi giá gói Cửa hàng, phục vụ D10), `sitemap.xml`, `robots.txt`, `facts.json` làm seed cho D1.
- Generator `tools/sitegen` (Python, Jinja2, Pydantic): lệnh `build`, `check` (link, heading, meta, số tiền ⊂ facts, văn bản pháp luật đã xác minh, không có JSON-LD dành cho UC6), `serve` (có trang 404); 46 test gồm build tất định, trích xuất bằng trafilatura, kiểm tra trình duyệt ở 390/1440 px và axe-core WCAG 2.1 AA.
- Pháp lý: 15 văn bản đã đối chiếu nguồn chính thống ngày 24/10/2026 (`docs/website-tallyo/phap-ly.md`, phụ lục `phap-ly-chi-tiet.md`).
- Tài liệu: kế hoạch `docs/website-tallyo/plan.html`, dàn ý `dan-y.md`, `README.md` của website, ADR 0003 (site tĩnh bằng Python + Jinja2).

- Phase 1, nền móng kỹ thuật (`backend/`, `frontend/`, `docs/architecture.md`):
  - Gateway LLM (DeepSeek hoặc mock theo vai trò; timeout, retry, rate limit), đếm token, token trúng prompt cache và chi phí; response cache SQLite có chuẩn hoá khoá để agent nhiều lượt cũng trúng cache.
  - Harness port từ Buổi 3 và tổng quát hoá: policy quyền dạng YAML theo từng agent, phát hiện lặp, ngân sách, envelope `status`, grounding số liệu kiểu Việt (`2.400.000`, `1,5`), tiêu chí hoàn thành bằng code, gói bàn giao 4 trường, middleware cho `create_agent`.
  - Trace JSONL theo run/span có che secret, lệnh tìm bước hỏng đầu tiên; audit log chuỗi hash phát hiện sửa xoá.
  - Provider Jina (embed, rerank, reader, search; retry khi 429/5xx) và probe Gemini có Google Search grounding; bản mock cho test.
  - Agent hello (`create_agent` + `HarnessMiddleware` + tool `calculate`), CLI `geo hello | trace | smoke`.
  - FastAPI: `/api/health`, đăng nhập JWT 2 vai trò (tài khoản seed từ env), luồng SSE `/api/runs/demo/stream`.
  - Frontend React 19 + `@cnma/react-ui`: đăng nhập, layout 8 màn hình, trang Tổng quan (trạng thái tích hợp), trang Traces chạy agent demo trực tiếp.
  - `docker-compose.yml` (WordPress + MariaDB, API, web), `Makefile`, GitHub Actions CI (ruff, pyright, pytest offline, gitleaks toàn lịch sử; frontend bỏ qua khi thiếu gói UI).

### Security
- Ẩn giá trị key khỏi `repr` của `Settings` và `JinaClient` (`field(repr=False)`): trước đó một test thất bại có thể in key ra màn hình.

### Changed
- Ghim ruff 0.17.2 ở cả pre-commit và dev dependency để format thống nhất.
- Đổi tên thương hiệu demo từ "SổBán" sang "Tallyo".
- Frontend đổi từ shadcn/ui sang `@cnma/react-ui`. File `.tgz` của gói không commit (`packages/*.tgz` trong `.gitignore`); CI bỏ qua build frontend khi thiếu gói. Backend giữ Python FastAPI, không dùng SAP CAP.
