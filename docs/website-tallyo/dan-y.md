# Dàn ý nội dung website Tallyo

> **Trạng thái:** đã triển khai ngày 24/10/2026 (xem [README.md](README.md)). Dàn ý giữ làm tài liệu thiết kế; nội dung thật nằm ở `fixtures/brands/tallyo/content/`. Phần pháp luật đã đổi so với bản nháp này, xem [phap-ly.md](phap-ly.md).
> **Dữ kiện:** mọi con số lấy từ [`fixtures/brands/tallyo/content/facts.yaml`](../../fixtures/brands/tallyo/content/facts.yaml). Trong dàn ý, `{...}` là tên trường sẽ được template điền vào.
> **Người duyệt:** TV3 (giọng văn, mức giá giả lập), TV2 (văn bản pháp luật, các bẫy cho D3).

Tallyo là thương hiệu giả lập. Trang nào cũng có dải thông báo giả lập và `noindex`; không trang nào nêu giá hay nhận định về đối thủ thật.

## Cần nhóm chốt ở bước này

1. **Mức giá giả lập** có hợp lý với thị trường hộ kinh doanh không: Khởi đầu 99.000 đ/tháng, Cửa hàng 149.000 đ/tháng (tăng lên 179.000 đ từ 01/11/2026), Chuỗi 399.000 đ/tháng.
2. **Số liệu công ty giả lập:** thành lập 2023, 40 người, hơn 3.200 hộ kinh doanh (01/10/2026).
3. **Giọng văn:** gọi người đọc là "bạn", tự xưng "Tallyo"; danh sách từ cấm và từ bắt buộc trong `voice`.
4. **Văn bản pháp luật:** đã xác minh ngày 24/10/2026 (15 văn bản, xem [phap-ly.md](phap-ly.md)); cần đối chiếu lại trước khi nộp.
5. **Ba bẫy cố ý cho D3:** bài blog 03/2025 còn giá ra mắt 129.000 đ; trang bảng giá bản 24/10 vừa có giá hiện hành vừa có thông báo giá mới; hướng dẫn thuế nhắc Nghị định 70/2025/NĐ-CP và mức 500 triệu đồng đã hết hiệu lực hoặc đã bị sửa.

## Quy ước chung cho mọi trang

- Một `<h1>`; H2/H3 không nhảy cấp; mỗi section tự đứng được (đọc riêng vẫn hiểu).
- Cuối trang nội dung có dòng "Cập nhật ngày {page_dates}" bằng `<time datetime>`.
- Nút CTA chính: "Dùng thử {trial.days} ngày". Vì là demo, nút dẫn tới `/lien-he/#dung-thu`, nơi giải thích đây là sản phẩm giả lập.
- Không dùng emoji, không viết hoa toàn bộ, không dùng từ trong `voice.forbidden_phrases`.

## Danh mục trang

### 1. Trang chủ `/`

- **Title:** Tallyo: bán hàng và hoá đơn điện tử cho hộ kinh doanh
- **Meta description:** Tallyo giúp hộ kinh doanh tính tiền tại quầy, xuất hoá đơn điện tử từ máy tính tiền và tự lập sổ sách. Dùng thử 15 ngày, không cần thẻ.
- **H1:** Tính tiền xong là có hoá đơn điện tử
- **Bố cục (theo thứ tự section của conarum):**
  1. Hero: H1, một câu mô tả từ `brand.tagline`, 2 nút (Dùng thử {trial.days} ngày, Xem bảng giá). Bên phải là mockup tờ hoá đơn in từ máy tính tiền, có mã của cơ quan thuế và mã QR tra cứu.
  2. H2 "Bốn việc Tallyo làm thay bạn": bán tại quầy, hoá đơn điện tử từ máy tính tiền, quản lý kho, sổ sách hộ kinh doanh (từ `features`).
  3. H2 "Ghi sổ tay và dùng Tallyo khác nhau thế nào": bảng 5 dòng, cột trái "Sổ tay hoặc Excel", cột phải "Tallyo". Không nhắc tên phần mềm khác.
  4. H2 "Vài con số về Tallyo": {trial.days} ngày dùng thử; giá từ {plans.start.price_month}/tháng; {brand.customers.wording}.
  5. H2 "Bắt đầu trong 4 bước": tạo tài khoản → nhập mặt hàng → kết nối máy in → bán đơn đầu tiên.
  6. CTA cuối trang: "Thử Tallyo ở cửa hàng của bạn".
- **Dùng cho eval:** UC1 lấy USP, đối tượng, giọng văn.

### 2. Tính năng `/tinh-nang/`

- **Title:** Tính năng Tallyo cho hộ kinh doanh và cửa hàng nhỏ
- **Meta description:** Xem các tính năng của Tallyo: bán tại quầy, hoá đơn điện tử từ máy tính tiền, quản lý kho, sổ sách hộ kinh doanh, đơn online và phân quyền.
- **H1:** Tính năng của Tallyo
- **Sections:** mỗi mục trong `features` là một H2, gồm `summary`, gói nào có (từ `plans`), link tới trang chi tiết nếu có. Cuối trang có bảng "Tính năng theo gói" và link sang `/bang-gia/`.

### 3. Hoá đơn điện tử `/tinh-nang/hoa-don-dien-tu/`

- **Title:** Hoá đơn điện tử khởi tạo từ máy tính tiền | Tallyo
- **Meta description:** Tallyo tạo hoá đơn điện tử có mã của cơ quan thuế ngay khi bạn tính tiền. Xem ai phải dùng, khách nhận hoá đơn thế nào và số hoá đơn trong từng gói.
- **H1:** Hoá đơn điện tử khởi tạo từ máy tính tiền
- **Sections:**
  - H2 "Hoá đơn điện tử khởi tạo từ máy tính tiền là gì?" (đoạn mở 40–60 từ, trả lời thẳng).
  - H2 "Ai phải dùng loại hoá đơn này?": theo `legal[70/2025/NĐ-CP]`, ghi số hiệu và ngày hiệu lực.
  - H2 "Tallyo tạo hoá đơn thế nào khi bạn tính tiền": 4 bước.
  - H2 "Khách nhận hoá đơn bằng cách nào": mã QR in trên hoá đơn giấy.
  - H2 "Khi mất mạng thì sao?": từ `compatibility.offline_mode`.
  - H2 "Số hoá đơn có trong từng gói": bảng `einvoice_per_year` và `addons.einvoice_pack`.
- **Dùng cho eval:** D3 câu định danh (số hiệu nghị định, ngưỡng doanh thu).

### 4. Bán hàng tại quầy `/tinh-nang/ban-hang-tai-quay/`

- **Title:** Bán hàng tại quầy và quản lý kho với Tallyo
- **Meta description:** Tính tiền bằng mã vạch, nhận tiền qua mã VietQR, in hoá đơn ra máy in nhiệt và theo dõi tồn kho trên điện thoại. Tallyo vẫn bán được khi mất mạng.
- **H1:** Bán hàng tại quầy và quản lý kho
- **Sections:** H2 tính tiền nhanh; H2 nhận tiền qua mã VietQR; H2 máy in và máy quét dùng được (`compatibility`); H2 quản lý kho (gói Cửa hàng trở lên); H2 bán khi mất mạng; H2 "Tallyo có bán máy in không?" (không, `sells_hardware: false`).

### 5. Bảng giá `/bang-gia/`

- **Title:** Bảng giá Tallyo: gói Khởi đầu, Cửa hàng, Chuỗi
- **Meta description:** Bảng giá Tallyo cho hộ kinh doanh: gói Khởi đầu, Cửa hàng và Chuỗi, trả theo tháng hoặc năm. Dùng thử 15 ngày, không cần thẻ thanh toán.
- **H1:** Bảng giá Tallyo
- **Sections:**
  - Ba thẻ gói: mã gói (`TL-START`…), tên, dành cho ai, giá tháng, giá năm, nút. Gói Cửa hàng được làm nổi bật.
  - Dòng "Giá áp dụng từ {effective_from}" bằng `<time>`.
  - **Thông báo điều chỉnh giá:** tự hiện khi `price_history` có bản có hiệu lực sau ngày build. Bản 2026-10-20 sẽ hiện "Từ 01/11/2026, gói Cửa hàng có giá 179.000 đ/tháng"; bản 2026-11-10 thì không.
  - H2 "So sánh chi tiết các gói": bảng có `<thead>`, cuộn ngang trên mobile.
  - H2 "Dùng thử {trial.days} ngày".
  - H2 "Mua thêm hoá đơn điện tử".
  - H2 "Thanh toán và hoàn tiền": phương thức, ưu đãi trả năm, link điều khoản.
- **Dùng cho eval:** D3 mã gói, D10 đổi giá.

### 6. Giới thiệu `/gioi-thieu/`

- **Title:** Về Tallyo
- **Meta description:** Tallyo được thành lập năm 2023 tại TP. Hồ Chí Minh để giúp hộ kinh doanh bán hàng và kê khai đúng quy định mà không cần biết kế toán.
- **H1:** Về Tallyo
- **Sections:** H2 "Tallyo bắt đầu từ một tiệm tạp hoá" (câu chuyện giả lập, không có tên người thật); H2 "Điều Tallyo tin" (`brand.mission`); H2 "Tallyo hôm nay" ({brand.customers.wording} tính đến {brand.customers.as_of}, {brand.team_size} người); H2 "Thông tin công ty" (`legal_name`, `city`, email, ghi rõ giả lập).
- **Dùng cho eval:** nguồn chính thức cho Organization trong D1.

### 7. Hướng dẫn `/huong-dan/`

- **Title:** Hướng dẫn sử dụng Tallyo
- **Meta description:** Hướng dẫn từng bước dùng Tallyo: xuất hoá đơn điện tử từ máy tính tiền và chuẩn bị cho việc chuyển từ thuế khoán sang kê khai.
- **H1:** Hướng dẫn sử dụng Tallyo
- **Sections:** danh sách hướng dẫn (tiêu đề, một câu tóm tắt, thời gian đọc); H2 "Cần hỗ trợ thêm?".

### 8. Hướng dẫn xuất hoá đơn `/huong-dan/xuat-hoa-don-tu-may-tinh-tien/`

- **Title:** Cách xuất hoá đơn điện tử từ máy tính tiền trên Tallyo
- **Meta description:** Các bước đăng ký và xuất hoá đơn điện tử khởi tạo từ máy tính tiền trên Tallyo, từ khai báo với cơ quan thuế đến in hoá đơn đầu tiên.
- **H1:** Cách xuất hoá đơn điện tử từ máy tính tiền trên Tallyo
- **Sections:**
  - Đoạn mở: mất khoảng {guides.einvoice_setup_minutes} phút.
  - H2 "Bạn cần chuẩn bị gì".
  - H2 "Các bước": danh sách có thứ tự (đăng ký sử dụng theo mẫu {guides.einvoice_registration_form} → khai báo thông tin trong Tallyo → kết nối máy in → bán thử một đơn → kiểm tra hoá đơn đã có mã).
  - H2 "Lỗi thường gặp và cách sửa".
- **Dùng cho eval:** về sau UC6 sinh HowTo JSON-LD cho trang này.

### 9. Hướng dẫn chuyển sang kê khai `/huong-dan/chuyen-tu-thue-khoan-sang-ke-khai/`

- **Title:** Chuyển từ thuế khoán sang kê khai: hộ kinh doanh cần làm gì
- **Meta description:** Lộ trình bỏ thuế khoán từ năm 2026 và những việc hộ kinh doanh cần làm: chọn hoá đơn điện tử, mở sổ sách, chuẩn bị kê khai. Kèm mốc thời gian.
- **H1:** Chuyển từ thuế khoán sang kê khai: hộ kinh doanh cần làm gì
- **Sections:**
  - H2 "Vì sao thuế khoán bị bỏ" (`legal[198/2025/QH15]`).
  - H2 "Các mốc thời gian": bảng ngày, văn bản, nội dung.
  - H2 "Việc cần làm theo thứ tự".
  - H2 "Sổ sách cần giữ" (`legal[88/2021/TT-BTC]`).
  - H2 "Tallyo giúp ở bước nào".
  - H2 "Trước đây hoá đơn điện tử theo quy định nào?": nhắc Thông tư 32/2011/TT-BTC đã hết hiệu lực, thay bằng Nghị định 123/2020/NĐ-CP (bẫy "quy định cũ").
  - Ghi chú cuối: nội dung chỉ để tham khảo, không thay cho tư vấn thuế.
- **Dùng cho eval:** D3 câu pháp luật và câu bẫy văn bản đã bị thay thế.

### 10. Blog `/blog/`

- **Title:** Blog Tallyo
- **Meta description:** Bài viết của Tallyo về bán hàng, hoá đơn điện tử và thuế cho hộ kinh doanh. Bài mới về GEO được đăng trên Tallyo Blog chạy WordPress.
- **H1:** Blog Tallyo
- **Sections:** danh sách bài tĩnh (tiêu đề, ngày, tóm tắt); H2 "Bài mới trên Tallyo Blog": một link tới {brand.site.blog_url_default}.

### 11. Bài 09/2026 `/blog/5-viec-truoc-khi-bo-thue-khoan/`

- **Title:** 5 việc hộ kinh doanh nên làm trước khi bỏ thuế khoán
- **Meta description:** Năm việc hộ kinh doanh nên làm trước khi bỏ thuế khoán: ước doanh thu năm, chọn loại hoá đơn, mở sổ sách, tách tài khoản, tập kê khai thử.
- **H1:** 5 việc hộ kinh doanh nên làm trước khi bỏ thuế khoán
- **Sections:** 5 H2 có số thứ tự (thứ tự ở đây là thật: làm việc trước rồi mới làm việc sau). Ngày đăng {page_dates.blog.5-viec-truoc-khi-bo-thue-khoan}.

### 12. Bài 03/2025 `/blog/ra-mat-goi-cua-hang/`

- **Title:** Tallyo ra mắt gói Cửa hàng cho tiệm có nhân viên
- **Meta description:** Tallyo ra mắt gói Cửa hàng dành cho tiệm có nhân viên và cần quản lý kho, với giá ra mắt cho hộ kinh doanh đăng ký trong năm 2025.
- **H1:** Tallyo ra mắt gói Cửa hàng cho tiệm có nhân viên
- **Sections:** giới thiệu gói, giá ra mắt (bản `price_history` ngày 2025-03-01: 129.000 đ/tháng, 1.290.000 đ/năm), tính năng chính. Ghi chú nhỏ: "Giá trong bài là giá tại thời điểm đăng." **Không** cập nhật giá mới. Đây là bẫy cố ý.
- **Dùng cho eval:** D3 câu "giá gói Cửa hàng là bao nhiêu" phải chọn nguồn mới nhất; failure mode "nguồn mâu thuẫn".

### 13. Hỏi đáp `/hoi-dap/`

- **Title:** Câu hỏi thường gặp về Tallyo
- **Meta description:** Giải đáp về dùng thử, bảng giá, hoá đơn điện tử, máy in, dữ liệu và hoàn tiền khi dùng Tallyo cho hộ kinh doanh và cửa hàng nhỏ.
- **H1:** Câu hỏi thường gặp về Tallyo
- **Câu hỏi (15, chia nhóm H2, mỗi câu là H3):**
  - *Dùng thử và giá:* Dùng thử có mất phí không? · Hết dùng thử thì dữ liệu còn không? · Trả theo năm được ưu đãi gì? · Tallyo có thông báo trước khi đổi giá không?
  - *Hoá đơn điện tử:* Hộ kinh doanh nào phải dùng hoá đơn điện tử từ máy tính tiền? · Hết số hoá đơn trong gói thì sao? · Khách muốn lấy hoá đơn ghi tên công ty thì làm thế nào? · Mất mạng có xuất hoá đơn được không?
  - *Thiết bị:* Tallyo có bán máy in không? · Dùng được máy in khổ nào? · Có chạy trên iPhone không?
  - *Tài khoản và dữ liệu:* Một tài khoản dùng cho mấy nhân viên? · Dữ liệu của tôi lưu ở đâu?
  - *Hoàn tiền:* Gói tháng có được hoàn tiền không? · Gói năm hoàn tiền trong bao lâu?
- **Dùng cho eval:** về sau UC6 sinh FAQPage cho trang này; D3 có câu phủ định (gói tháng không được hoàn).

### 14. Chính sách bảo mật `/chinh-sach/bao-mat/`

- **Title:** Chính sách bảo mật của Tallyo
- **Meta description:** Tallyo thu thập dữ liệu gì, dùng vào việc gì, lưu ở đâu và bạn có quyền gì với dữ liệu bán hàng và thông tin khách hàng của cửa hàng mình.
- **H1:** Chính sách bảo mật
- **Sections:** dữ liệu thu thập; mục đích sử dụng; lưu trữ và thời hạn (nói chung theo yêu cầu lưu trữ hoá đơn của pháp luật, không nêu số năm khi chưa xác minh); chia sẻ với bên thứ ba (tổ chức cung cấp dịch vụ hoá đơn điện tử); quyền của bạn; liên hệ.

### 15. Điều khoản sử dụng `/chinh-sach/dieu-khoan-su-dung/`

- **Title:** Điều khoản sử dụng Tallyo
- **Meta description:** Điều khoản sử dụng Tallyo: phạm vi dịch vụ, thanh toán và gia hạn, chính sách hoàn tiền, trách nhiệm kê khai thuế và thông báo khi thay đổi giá.
- **H1:** Điều khoản sử dụng
- **Sections:** phạm vi dịch vụ; thanh toán và gia hạn; hoàn tiền (gói năm lần đầu: {billing.refund.annual_first_payment_days} ngày; gói tháng không hoàn; phần hoá đơn đã phát hành không hoàn); trách nhiệm kê khai thuế thuộc về hộ kinh doanh; thay đổi giá (báo trước {billing.price_change_notice_days} ngày); chấm dứt dịch vụ.
- **Dùng cho eval:** D3 câu phủ định.

### 16. Liên hệ `/lien-he/`

- **Title:** Liên hệ Tallyo
- **Meta description:** Liên hệ đội hỗ trợ Tallyo qua email từ 8:00 đến 21:00 mỗi ngày, hoặc tìm hiểu cách dùng thử Tallyo cho cửa hàng của bạn.
- **H1:** Liên hệ Tallyo
- **Sections:** H2 "Hỗ trợ khách hàng" (`support_email`, `support_hours`); H2 "Tư vấn bán hàng" (`sales_email`); H2 "Dùng thử" (`id="dung-thu"`): giải thích Tallyo là thương hiệu giả lập phục vụ đồ án SE373 nên không có tài khoản thật. Không có form.

### Trang tiện ích

- `/404.html`: "Không tìm thấy trang", link về trang chủ, bảng giá, hướng dẫn.
- `/sitemap.xml`: 16 URL kể trên (trừ 404), mỗi URL có `lastmod`.
- `/robots.txt`: cho phép tất cả, trỏ tới sitemap.
