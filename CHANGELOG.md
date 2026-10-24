# Changelog

Định dạng theo [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), đánh phiên bản theo [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Phase 0: khung repo gồm `.gitignore`, `.env.example`, pre-commit (gitleaks có rule cho key DeepSeek `sk-…` và Jina `jina_…`, ruff, các kiểm tra cơ bản), `README.md`, `AGENTS.md`.
- Tài liệu: tổng quan môn học và yêu cầu đồ án, kế hoạch đồ án, ma trận K1–K8, khung scorecard UC1–UC8, ADR 0001 về tech stack, file minh bạch dùng AI.

- Hướng dẫn dùng thư viện UI nội bộ `@cnma/react-ui` 1.1.4 (`packages/README.md`), script `scripts/check-ui-package.mjs` kiểm tra gói có mặt và đúng SHA-256, ADR 0002.

### Changed
- Đổi tên thương hiệu demo từ "SổBán" sang "Tallyo".
- Frontend đổi từ shadcn/ui sang `@cnma/react-ui`. File `.tgz` của gói không commit (`packages/*.tgz` trong `.gitignore`); CI bỏ qua build frontend khi thiếu gói. Backend giữ Python FastAPI, không dùng SAP CAP.
