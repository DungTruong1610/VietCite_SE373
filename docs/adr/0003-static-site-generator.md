# ADR 0003: Website mock Tallyo là HTML tĩnh, build bằng Python + Jinja2

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 24/10/2026
- **Người quyết định:** TV1, theo kế hoạch `docs/website-tallyo/plan.html`

## Bối cảnh

Website mock của thương hiệu giả lập Tallyo là dữ liệu đầu vào chung của UC1 (Brand Analyst đọc sitemap và trang), Phase 2 RAG và golden D3, profile vàng D1, kịch bản memory D10, UC6 (đo phần đóng góp của schema) và UC7 (SGE-vi). Vì vậy site phải đọc được bằng crawler và trafilatura khi không có JavaScript, tái lập được từng byte để eval chạy offline, và mọi con số phải có một nguồn sự thật để đáp án D1 không lệch với nội dung trang.

## Quyết định

1. Site là **HTML tĩnh**, sinh bởi `tools/sitegen` (Python 3.13, Jinja2, markdown-it-py, Pydantic). Nội dung là Markdown có frontmatter ở `fixtures/brands/tallyo/content/`, dữ kiện nằm trong một file `facts.yaml`.
2. Mọi số liệu (giá, giới hạn gói, ngày, số hiệu văn bản pháp luật) được render từ `facts.yaml`. `sitegen check` báo lỗi nếu trang có số tiền không có trong `facts.yaml` hoặc nhắc văn bản pháp luật không có trong `facts.legal`.
3. Output đã build được **commit** ở `fixtures/brands/tallyo/site/<as_of>/`, gồm hai bản: `2026-10-20` (giá v1) và `2026-11-10` (sau đợt tăng giá). Test so sánh output đã commit với bản build mới.
4. Giao diện theo **conarum-brand-guidelines** và **conarum-html-page-design**, không dùng logo conarum. Font và icon tự host, không gọi CDN.
5. Site gốc cố ý **không có** `llms.txt`, FAQPage, HowTo, SoftwareApplication JSON-LD; đó là output của UC6.

## Hệ quả

- **Tốt:** cùng ngôn ngữ với backend (Python); build tất định nên eval tái lập; crawler đọc được không cần JS; đổi giá chỉ sửa một dòng YAML; dùng lại cho Lâm Viên Coffee bằng cách thêm thư mục `fixtures/brands/lamvien/`.
- **Đổi lại:** không có CMS, sửa nội dung phải sửa Markdown và build lại; output HTML commit vào repo làm diff PR dài hơn.
- **Ràng buộc:** không sửa tay file trong `site/`; luôn chạy `python -m sitegen build --all` rồi commit cả nguồn lẫn output.

## Phương án đã cân nhắc

- **React SPA (Vite):** cùng stack frontend nhưng nội dung render bằng JS, trafilatura dự phòng của Phase 2 không đọc được. Loại.
- **Astro:** site tĩnh đẹp, nhưng thêm một toolchain Node chỉ để làm fixture. Loại.
- **Dựng site trong WordPress:** một chỗ cho cả site và blog, nhưng ingest và eval phụ thuộc WordPress đang chạy, khó tái lập và khó chạy CI offline. WordPress chỉ dùng cho bài GEO do agent xuất bản (UC8). Loại.
