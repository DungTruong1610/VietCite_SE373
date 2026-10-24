# Pháp lý trên website Tallyo

> **Đối chiếu ngày:** 24/10/2026. **Phạm vi:** các văn bản pháp luật thật được nhắc trên website mock Tallyo.
> **Không phải tư vấn pháp lý.** Tallyo là thương hiệu giả lập; phần pháp luật là thông tin tham khảo cho đồ án.
> **Báo cáo nghiên cứu đầy đủ** (trích dẫn nguyên văn, số trang PDF đã đọc, độ tin cậy từng mục): [phap-ly-chi-tiet.md](phap-ly-chi-tiet.md).

## Cách đã kiểm chứng

1. Một agent nghiên cứu tra từng văn bản trên nguồn chính thống: vanban.chinhphu.vn, Công báo, xaydungchinhsach.chinhphu.vn, baochinhphu.vn. Các bản PDF ký số là ảnh quét, agent chuyển từng trang thành ảnh và đọc trực tiếp.
2. Claude mở lại từng trang nguồn sẽ gắn link trên site, đối chiếu số hiệu, ngày ban hành, ngày hiệu lực, người ký. Những quan hệ thay thế mà trang thuộc tính không ghi thì kiểm thêm bằng ít nhất một nguồn độc lập (EY, MISA meInvoice, Thư viện Pháp luật).
3. Riêng hạn thông báo doanh thu 31/01, Claude tự đọc bản ký số của Nghị định 68/2026/NĐ-CP (trang 6, Điều 8 khoản 1 điểm a).
4. Chỉ đưa lên site điều có độ tin cậy cao. Mỗi văn bản nằm trong `facts.legal` với `verified: true`, `source_url`, `verified_on`. `sitegen check --strict` báo lỗi nếu trang nhắc văn bản không có trong danh sách hoặc chưa xác minh.

## Văn bản đang dùng trên site

| Văn bản | Nội dung dùng trên site | Hiệu lực | Trang dùng |
|---|---|---|---|
| Nghị quyết 198/2025/QH15 | Bỏ thuế khoán và lệ phí môn bài từ 01/01/2026 (Điều 10 khoản 6, 7) | 17/05/2025 | Hướng dẫn chuyển sang kê khai, blog 12/2025 |
| Luật Quản lý thuế 108/2025/QH15 | Hiệu lực chung 01/07/2026; phần hộ kinh doanh áp dụng từ 01/01/2026 | 01/07/2026 | Hướng dẫn chuyển sang kê khai |
| Nghị định 68/2026/NĐ-CP (sửa bởi NĐ 141/2026) | Thông báo doanh thu chậm nhất 31/01 năm sau; hạn khai quý, khai tháng; khai thuế bằng phương thức điện tử | 05/03/2026 | Hướng dẫn chuyển sang kê khai |
| Nghị định 141/2026/NĐ-CP | Ngưỡng 1 tỷ đồng/năm (thay 500 triệu), áp dụng từ 01/01/2026; hộ trên 1 tỷ phải dùng hoá đơn điện tử, đăng ký trong 30 ngày | 01/01/2026 (ký 29/04/2026) | Hoá đơn điện tử, hướng dẫn, hỏi đáp |
| Thông tư 18/2026/TT-BTC | Hồ sơ, thủ tục quản lý thuế hộ kinh doanh; thay Thông tư 40/2021 | 05/03/2026 | Hướng dẫn chuyển sang kê khai |
| Thông tư 152/2025/TT-BTC | Mẫu sổ S1a-HKD, S2a đến S2e-HKD; lưu tài liệu kế toán tối thiểu 5 năm; thay Thông tư 88/2021 | 01/01/2026 | Tính năng, hướng dẫn, chính sách bảo mật |
| Nghị định 254/2026/NĐ-CP | Hộ trên 1 tỷ dùng hoá đơn có mã hoặc từ máy tính tiền; dưới mức được tự nguyện; thay NĐ 123/2020 và NĐ 70/2025 | 01/07/2026 | Hoá đơn điện tử, hướng dẫn, hỏi đáp |
| Thông tư 91/2026/TT-BTC | Mẫu số 01/ĐKTĐ-HĐĐT; đăng ký qua tổ chức cung cấp dịch vụ hoá đơn điện tử; đối chiếu với cơ sở dữ liệu dân cư | 01/07/2026 | Hướng dẫn xuất hoá đơn |
| Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 | Căn cứ của chính sách bảo mật | 01/01/2026 | Chính sách bảo mật |
| Nghị định 356/2025/NĐ-CP | Hướng dẫn luật trên; thay Nghị định 13/2023 | 01/01/2026 | Chính sách bảo mật |

## Văn bản đã hết hiệu lực (chỉ nhắc để cảnh báo thông tin cũ)

| Văn bản | Hết hiệu lực | Thay bằng |
|---|---|---|
| Nghị định 123/2020/NĐ-CP (hoá đơn, chứng từ) | 01/07/2026 | Nghị định 254/2026/NĐ-CP |
| Nghị định 70/2025/NĐ-CP (sửa NĐ 123, hoá đơn từ máy tính tiền cho hộ từ 1 tỷ) | 01/07/2026 | Nghị định 254/2026/NĐ-CP |
| Thông tư 88/2021/TT-BTC (kế toán hộ kinh doanh) | 01/01/2026 | Thông tư 152/2025/TT-BTC |
| Thông tư 40/2021/TT-BTC (thuế hộ kinh doanh) | 05/03/2026 | Thông tư 18/2026/TT-BTC |
| Nghị định 13/2023/NĐ-CP (dữ liệu cá nhân) | 01/01/2026 | Nghị định 356/2025/NĐ-CP |

## Những sửa đổi so với bản nháp ban đầu

Bản nháp ở Bước 1 (viết từ trí nhớ) có nhiều điểm đã lỗi thời. Cả sáu điểm dưới đây đã được sửa trước khi đưa lên site:

1. Ngưỡng doanh thu là **1 tỷ đồng/năm** theo NĐ 141/2026, không phải 100, 200 hay 500 triệu.
2. NĐ 123/2020 và NĐ 70/2025 **hết hiệu lực từ 01/07/2026**; quy định hiện hành là NĐ 254/2026 và TT 91/2026.
3. Hộ trên 1 tỷ được **chọn** hoá đơn có mã của cơ quan thuế **hoặc** hoá đơn từ máy tính tiền; máy tính tiền không phải lựa chọn duy nhất.
4. TT 88/2021 đã bị TT 152/2025 thay; TT 40/2021 đã bị TT 18/2026 thay.
5. NQ 198/2025 ghi "từ ngày 01 tháng 01 năm 2026", không có chữ "chậm nhất" (cụm đó là của Nghị quyết 68-NQ/TW).
6. Bỏ Thông tư 32/2011 khỏi site. Bẫy "quy định cũ" cho D3 nay dùng NĐ 70/2025 và mức 500 triệu, sát thực tế hơn.

## Cố ý không đưa lên site

| Nội dung | Lý do |
|---|---|
| Nghị quyết 43/2026/QH16 (giảm 30% thuế TNCN 2026–2027) | Chưa xác minh được nghị định hướng dẫn và thủ tục |
| Bậc thuế suất TNCN theo thu nhập (15%, 17%, 20%) | Chưa đọc được văn bản hợp nhất sau khi Luật 09/2026/QH16 sửa |
| Tiêu chí khai theo quý hay theo tháng | Chỉ có nguồn thứ cấp |
| Thời hạn lưu hoá đơn "10 năm" | Mốc 10 năm của Luật Kế toán áp dụng cho đơn vị kế toán, không áp chung cho hộ kinh doanh |
| Chi tiết các quyền của chủ thể dữ liệu theo điều luật | Chưa đọc nguyên văn các điều của Luật 91/2025; site chỉ nêu quyền theo chính sách của Tallyo |
| Định dạng mã của cơ quan thuế trên hoá đơn | Không cần cho demo; hình minh hoạ ghi rõ "mã tra cứu minh hoạ, không có thật" |
| Tallyo là tổ chức cung cấp dịch vụ hoá đơn điện tử | Sai sự thật; mọi trang về hoá đơn ghi rõ Tallyo là sản phẩm demo, không kết nối với hệ thống của cơ quan thuế |

## Bảo trì

- Văn bản mới hoặc văn bản bị thay: sửa `fixtures/brands/tallyo/content/facts.yaml` (mục `legal`, `legal_refs`, `legal_facts`), build lại, chạy `check --strict`.
- Nội dung trang gọi văn bản theo **vai trò** (`legal_refs.einvoice`, `legal_refs.books`…), nên đổi văn bản chỉ sửa một chỗ.
- Trước khi nộp đồ án (khoảng 24–30/11/2026), đối chiếu lại các văn bản trên vì quy định về hộ kinh doanh thay đổi nhanh trong năm 2026.
