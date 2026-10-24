# VietCite Studio

Hệ thống đa tác tử viết nội dung tiếng Việt chuẩn GEO (Generative Engine Optimization): đo xem các AI có nhắc tới thương hiệu không, viết bài có kiểm chứng để AI dễ trích dẫn, chỉ xuất bản khi người duyệt, rồi đo lại để so sánh trước và sau.

Đồ án cuối kỳ môn **SE373 – Kỹ thuật xây dựng hệ thống Agentic AI** (UIT), nhóm đề tài #4 *GEO content writer Agent*.

> **Trạng thái:** Phase 0 (khởi động). Chưa có code chạy được. Xem lịch ở [docs/KE_HOACH_DO_AN.md](docs/KE_HOACH_DO_AN.md#7-lịch-tuần-và-mốc).

## Thương hiệu demo

| Vai trò | Thương hiệu | Ghi chú |
|---|---|---|
| Chính | **Tallyo** | Phần mềm bán hàng và hoá đơn điện tử cho hộ kinh doanh. **Thương hiệu giả lập**, cạnh tranh với đối thủ thật (KiotViet, Sapo, MISA eShop…) |
| Phụ | **Lâm Viên Coffee** | Cà phê đặc sản Đà Lạt, **giả lập**, dùng để kiểm tra khả năng tổng quát hoá |

Bài viết chỉ xuất bản lên WordPress **local**, gắn nhãn "demo học thuật".

## Kiến trúc tóm tắt

- **Web:** React 19 + Vite + TypeScript + Tailwind v4 + thư viện UI `@cnma/react-ui` (`frontend/`), FastAPI (`backend/app/`).
- **Agent:** Python 3.13, LangChain 1.x `create_agent`, LangGraph (checkpoint SQLite, interrupt chờ người duyệt).
- **API ngoài:** DeepSeek (LLM chính), Jina (embedding, rerank, reader, search), Gemini (tuỳ chọn: probe có Google Search, judge).
- **Xuất bản:** WordPress local qua MCP server tự viết, chỉ nhận lệnh publish kèm approval token.

Chi tiết: [docs/KE_HOACH_DO_AN.md](docs/KE_HOACH_DO_AN.md) mục 4.

## Bắt đầu (Phase 0)

```bash
git clone https://github.com/DungTruong1610/VietCite_SE373.git
cd VietCite_SE373
git checkout develop

cp .env.example .env          # điền key thật vào .env, KHÔNG commit
pip install pre-commit
pre-commit install            # bắt buộc: chặn commit có API key

# Frontend cần gói UI nội bộ (không có trong repo): xin TV1 file cnma-react-ui-1.1.4.tgz,
# đặt vào packages/ rồi kiểm tra:
node scripts/check-ui-package.mjs
```

Chi tiết về gói UI: [packages/README.md](packages/README.md) và [ADR 0002](docs/adr/0002-company-ui-library.md).

Lệnh chạy hệ thống (`make up`, `make test`…) sẽ có từ Phase 1.

### Website demo Tallyo

Website mock của thương hiệu giả lập Tallyo (16 trang, HTML tĩnh) nằm ở `fixtures/brands/tallyo/site/`, sinh bởi `tools/sitegen`:

```bash
cd tools/sitegen
python -m venv .venv && .venv/Scripts/python -m pip install jinja2 pyyaml markdown-it-py pydantic segno pytest trafilatura playwright==1.63.0
.venv/Scripts/python -m sitegen build --all && .venv/Scripts/python -m sitegen check --all --strict
.venv/Scripts/python -m sitegen serve --port 8081      # http://localhost:8081
```

Chi tiết: [docs/website-tallyo/README.md](docs/website-tallyo/README.md), [ADR 0003](docs/adr/0003-static-site-generator.md).

## Tài liệu

| Tài liệu | Nội dung |
|---|---|
| [docs/TONG_QUAN_MON_HOC_VA_YEU_CAU_DO_AN.md](docs/TONG_QUAN_MON_HOC_VA_YEU_CAU_DO_AN.md) | Tóm tắt môn học, barem, yêu cầu đề tài |
| [docs/KE_HOACH_DO_AN.md](docs/KE_HOACH_DO_AN.md) | Kế hoạch đầy đủ: use case, kiến trúc, phase, lịch, phân công |
| [docs/k-matrix.md](docs/k-matrix.md) | Ma trận phủ 8 mảng kiến thức K1–K8 |
| [docs/use-cases/](docs/use-cases/) | Scorecard từng use case UC1–UC8 |
| [docs/adr/](docs/adr/) | Các quyết định kiến trúc |
| [docs/website-tallyo/](docs/website-tallyo/) | Website demo Tallyo: kế hoạch, dàn ý, báo cáo pháp lý |
| [docs/ai-usage.md](docs/ai-usage.md) | Minh bạch việc dùng công cụ AI |
| [AGENTS.md](AGENTS.md) | Hướng dẫn cho AI coding agent làm việc trong repo |

## Quy ước làm việc

- **GitFlow:** `main` (bản nộp) ← `develop` ← `feature/*`, `bugfix/*`.
- **Conventional Commits:** `feat(rag): ...`, `fix(ui): ...`, `docs: ...`.
- Mỗi PR dưới 400 dòng, có ít nhất 1 người khác review.
- **Không bao giờ commit `.env` hay API key.** Pre-commit chạy gitleaks để chặn.
- **Không commit `packages/*.tgz`** (thư viện UI nội bộ, chỉ chia sẻ trong nhóm).

## Nhóm

| Thành viên | Vai trò |
|---|---|
| TV1 | Tech lead, orchestration |
| TV2 | Knowledge / RAG |
| TV3 | Content agents |
| TV4 | Verification & eval |
| TV5 | Frontend & đo lường |

*(Điền tên thật khi nhóm chốt phân công.)*
