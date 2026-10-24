# ADR 0001: Tech stack của VietCite Studio

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 24/10/2026
- **Người quyết định:** cả nhóm

## Bối cảnh

Đồ án cần một web app có tích hợp agent thật, làm trong khoảng 5 tuần bởi 5 sinh viên. Các bài lab của môn SE373 (LangChain 1.x, LangGraph, RAG với Chroma) đều viết bằng Python. Nhóm có sẵn key DeepSeek, Jina và (tuỳ chọn) Gemini; không có API của ChatGPT và Perplexity.

Thư mục cha của repo có bộ rule viết cho SAP CAP/TypeScript. Bộ rule đó không khớp với một đồ án agent Python.

## Quyết định

| Tầng | Chọn |
|---|---|
| Backend, agent | Python 3.13, LangChain 1.x `create_agent` + middleware, LangGraph 1.x (checkpoint SQLite), FastAPI |
| LLM | DeepSeek (chính), Gemini (judge và probe có Google Search, tuỳ chọn) |
| Retrieval | Jina embeddings v3, Jina reranker v2 multilingual, Chroma, BM25 + underthesea |
| Frontend | React 19, Vite, TypeScript strict, Tailwind v4, ~~shadcn/ui~~ `@cnma/react-ui` (thay đổi theo [ADR 0002](0002-company-ui-library.md)) |
| CMS | WordPress local (Docker) + MCP server tự viết (FastMCP) |
| Chất lượng | pytest (mock model, chạy offline), ruff, pyright, Playwright, GitHub Actions, pre-commit + gitleaks |

Mọi API ngoài nằm sau một interface có bản dự phòng (local hoặc miễn phí) và bản mock, nên thiếu một key thì hệ thống vẫn chạy.

## Hệ quả

- **Tốt:** dùng lại trực tiếp code harness của Buổi 3 và skill catalog của Buổi 4; đúng API chuẩn mà môn dạy; cả nhóm đã quen Python từ các lab.
- **Đổi lại:** backend không theo rule SAP CAP/TypeScript ở thư mục cha. Frontend vẫn theo đúng rule (React 19, TS strict, Tailwind v4). Các rule về CHANGELOG, tài liệu, Conventional Commits và GitFlow vẫn áp dụng.
- **Rủi ro:** phụ thuộc ba nhà cung cấp API. Giảm bằng retry, timeout, cache, bản dự phòng và mock (xem mục 10 của kế hoạch).

## Phương án đã cân nhắc

- **Backend TypeScript (Node, LangGraph.js):** đồng bộ ngôn ngữ với frontend, nhưng lệch với toàn bộ lab của môn và không dùng lại được code Buổi 3, 4. Loại.
- **Chỉ CLI, không làm web:** ít việc hơn nhưng mất điểm phần mềm (độ hoàn thiện, khối lượng). Loại.
