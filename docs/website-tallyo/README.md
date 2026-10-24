# Website demo Tallyo

Website mock chính thức của **Tallyo**, thương hiệu giả lập bán phần mềm bán hàng và hoá đơn điện tử cho hộ kinh doanh. Đây là dữ liệu đầu vào chung của đồ án VietCite Studio (SE373, UIT): UC1 đọc site để dựng profile thương hiệu, Phase 2 RAG ingest site, D1/D3/D10 lấy đáp án từ site, UC6 và UC7 đo trước/sau trên site.

> Tallyo, công ty, giá và số liệu trên site đều là **giả lập**. Phần pháp luật nhắc tới văn bản **thật**, đã được đối chiếu nguồn chính thống, xem [phap-ly.md](phap-ly.md).

## Chạy nhanh

```bash
cd tools/sitegen
python -m venv .venv                     # hoặc: uv sync
.venv/Scripts/python -m pip install jinja2 pyyaml markdown-it-py pydantic segno pytest trafilatura playwright==1.63.0
.venv/Scripts/python -m sitegen build --all          # build cả hai bản 2026-10-24 và 2026-11-10
.venv/Scripts/python -m sitegen check --all --strict # kiểm tra chất lượng, pháp luật chưa xác minh là lỗi
.venv/Scripts/python -m sitegen serve --port 8081    # mở http://localhost:8081
.venv/Scripts/python -m pytest -q                    # unit, build, trích xuất, trình duyệt + axe
```

Trên Linux/macOS thay `.venv/Scripts/python` bằng `.venv/bin/python`. Test trình duyệt cần Chromium của Playwright (`python -m playwright install chromium`); nếu máy có sẵn Chromium khác bản, đặt `PLAYWRIGHT_CHROMIUM_EXECUTABLE`.

## Cấu trúc

| Đường dẫn | Nội dung |
|---|---|
| `fixtures/brands/tallyo/content/facts.yaml` | Nguồn sự thật duy nhất: công ty, giọng văn, gói giá có lịch sử, tính năng, văn bản pháp luật |
| `fixtures/brands/tallyo/content/pages/*.md`, `blog/*.md` | 16 trang, Markdown + frontmatter; số liệu viết bằng Jinja (`{{ plans.shop.price.price_month \| vnd }}`) |
| `fixtures/brands/tallyo/theme/` | Template Jinja, `site.css`, font, icon, favicon |
| `fixtures/brands/tallyo/site/<as_of>/` | Output đã build, **có commit**, không sửa tay |
| `tools/sitegen/` | Generator: `models.py`, `content.py`, `render.py`, `seo.py`, `build.py`, `checks.py`, CLI |
| `docs/website-tallyo/` | Kế hoạch (`plan.html`), dàn ý (`dan-y.md`), báo cáo pháp lý (`phap-ly.md`, phụ lục `phap-ly-chi-tiet.md`) |

## Danh mục trang

| URL | Vai trò trong eval |
|---|---|
| `/` | UC1: USP, đối tượng, giọng văn |
| `/tinh-nang/`, `/tinh-nang/hoa-don-dien-tu/`, `/tinh-nang/ban-hang-tai-quay/` | UC1, D3 câu định danh |
| `/bang-gia/` | D3 mã gói, D10 đổi giá |
| `/gioi-thieu/` | Organization cho D1 |
| `/huong-dan/` và 2 hướng dẫn | D3 câu pháp luật, về sau UC6 sinh HowTo |
| `/blog/` và 2 bài | Bài 03/2025 giữ giá cũ (bẫy D3) |
| `/hoi-dap/` | Về sau UC6 sinh FAQPage; D3 câu phủ định |
| `/chinh-sach/bao-mat/`, `/chinh-sach/dieu-khoan-su-dung/` | D3 câu phủ định (hoàn tiền) |
| `/lien-he/` | Giải thích đây là demo |

Kèm `404.html`, `sitemap.xml` (16 URL, có `lastmod`), `robots.txt`, `facts.json` (dữ kiện đã giải theo ngày build, seed cho D1).

## Bẫy cố ý cho D3 và D10

1. **Giá cũ trong bài blog:** `/blog/ra-mat-goi-cua-hang/` (đăng 01/03/2025) ghi giá ra mắt gói Cửa hàng 129.000 đ/tháng. Giá đúng ở bản 2026-10-24 là 149.000 đ.
2. **Giá hiện hành và giá sắp áp dụng cùng một trang:** `/bang-gia/` bản 2026-10-24 có thông báo tăng giá gói Cửa hàng lên 179.000 đ từ 01/11/2026. Bản 2026-11-10 chỉ còn giá mới.
3. **Quy định cũ:** nhiều nguồn trên mạng còn dẫn Nghị định 70/2025/NĐ-CP ("từ 1 tỷ đồng trở lên phải dùng máy tính tiền") và mức 500 triệu đồng. Site nêu rõ các văn bản này đã hết hiệu lực hoặc đã bị sửa, và quy định hiện hành là Nghị định 254/2026/NĐ-CP (trên 1 tỷ đồng, hoá đơn có mã hoặc từ máy tính tiền).

Giữa hai bản build, chỉ `bang-gia/index.html` và `facts.json` khác nhau (có test bảo đảm).

## Thiết kế

- Theo **conarum-brand-guidelines** và **conarum-html-page-design**, không dùng logo conarum. Logo Tallyo là bốn vạch đếm và một vạch chéo.
- Màu: đỏ `#C00000` cho CTA, icon, số liệu; nền trắng; chiều sâu bằng shadow; nút dạng pill; CTA là section cuối mỗi trang.
- Font: tiêu đề **Montserrat 600/700**. Thân bài theo brand là Poppins, nhưng Poppins thiếu 88/96 ký tự tiếng Việt (đã đo bằng fontTools), nên dùng **Inter**, là font dự phòng chính thức trong brand guidelines.
- Chỉ một theme sáng, vì brand chỉ cho nền trắng hoặc trắng chuyển đỏ nhạt.
- Font (SIL OFL) và icon Lucide (ISC) tự host; không gọi CDN; không cần JavaScript (menu mobile dùng `<details>`).
- Khi hai skill conarum khác nhau (nút viết hoa, độ đậm H1), theo `conarum-html-page-design` vì skill này viết riêng cho trang HTML.
- Màu xám chú thích `#999999` của brand không đạt tương phản WCAG AA trên nền trắng, nên chữ phụ dùng `#666666` (có trong `conarum-html-page-design`).
- Không làm `wireframe.html` và `mockup.html` riêng: bố cục đã được `conarum-html-page-design` quy định sẵn, người dùng yêu cầu làm thẳng site.

## Chuẩn nghiệm thu đã có test

| Chuẩn | Kiểm bằng |
|---|---|
| Mọi số tiền có trong `facts.yaml`; không placeholder | `sitegen check` |
| Một `<h1>`, heading không nhảy cấp, bảng có `<thead>/<th>`, `<time datetime>` | `sitegen check` |
| Title ≤ 60 ký tự, description 120–160, canonical, `noindex`, dải thông báo giả lập | `sitegen check` |
| Link nội bộ không hỏng, link ngoài chỉ tới nguồn pháp luật và blog | `sitegen check` |
| Không có JSON-LD dành cho UC6, không có `llms.txt` | `sitegen check` |
| Văn bản pháp luật nhắc trên site đều có trong `facts.legal` và đã xác minh | `sitegen check --strict` |
| Không nêu tên đối thủ thật, không dùng cụm từ cấm của giọng văn | `sitegen check` |
| Build tất định, output commit khớp bản build mới | `tests/test_build.py` |
| Trafilatura trích được nội dung chính, không lẫn footer và hình minh hoạ | `tests/test_extraction.py` |
| Không tràn ngang ở 390px và 1440px, không lỗi console, font tải đủ, axe-core WCAG 2.1 AA không vi phạm | `tests/test_visual.py` |

## Thêm thương hiệu mới (ví dụ Lâm Viên Coffee)

1. Tạo `fixtures/brands/lamvien/content/facts.yaml` theo cùng schema (`tools/sitegen/sitegen/models.py`).
2. Thêm trang ở `content/pages/` và `content/blog/`, theme riêng ở `theme/`.
3. `python -m sitegen build --brand lamvien --all` rồi `check --strict`.

## Lưu ý cho Phase 2

Jina Reader (`r.jina.ai`) chạy trên máy chủ của Jina nên **không đọc được `localhost`**. Ingest site mock ở máy local phải dùng fetch local + trafilatura, hoặc đọc thẳng file trong `site/<as_of>/`.
