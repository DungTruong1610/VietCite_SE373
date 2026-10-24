---
path: /huong-dan/chuyen-tu-thue-khoan-sang-ke-khai/
parent: /huong-dan/
title: "Chuyển từ thuế khoán sang kê khai: hộ kinh doanh cần làm gì"
description: "Lộ trình bỏ thuế khoán từ năm 2026 và những việc hộ kinh doanh cần làm: chọn hoá đơn điện tử, mở sổ sách, chuẩn bị kê khai. Kèm mốc thời gian."
template: doc
h1: "Chuyển từ thuế khoán sang kê khai: hộ kinh doanh cần làm gì"
eyebrow: Hướng dẫn
summary: Mốc thời gian bỏ thuế khoán, ngưỡng doanh thu 1 tỷ đồng và năm việc cần làm theo thứ tự.
icon: landmark
order: 42
toc: true
laws: [198/2025/QH15, 68/2026/NĐ-CP, 141/2026/NĐ-CP, 18/2026/TT-BTC, 152/2025/TT-BTC, 254/2026/NĐ-CP, 108/2025/QH15]
---

{% set L = facts.legal_facts %}
{% set R = facts.legal_refs %}
Từ ngày 01/01/2026, hộ kinh doanh không còn nộp thuế theo mức khoán. Mỗi hộ tự xác định doanh thu, thông báo hoặc khai thuế với cơ quan thuế. Trang này tóm tắt các quy định đã ban hành và những việc nên làm theo thứ tự, viết cho chủ cửa hàng không chuyên về thuế.

<div class="note">{{ icon("info", 20) }}<div><p><strong>Thông tin tham khảo, đối chiếu nguồn chính thống ngày {{ L.verified_on | date_vi }}.</strong> Trang này không thay cho tư vấn thuế. Với trường hợp cụ thể, hãy hỏi cơ quan thuế quản lý hộ của bạn hoặc người làm dịch vụ kế toán.</p></div></div>

## Vì sao không còn thuế khoán

{{ law(R.khoan_abolish) }} của Quốc hội quy định hộ kinh doanh, cá nhân kinh doanh không áp dụng phương pháp khoán thuế từ ngày 01/01/2026 và nộp thuế theo pháp luật về quản lý thuế. Cũng từ ngày này, lệ phí môn bài không còn thu.

## Các mốc thời gian

| Ngày | Văn bản | Thay đổi |
|---|---|---|
| 17/05/2025 | {{ law(R.khoan_abolish) }} | Quốc hội quyết định bỏ thuế khoán và lệ phí môn bài từ 01/01/2026 |
| 01/01/2026 | {{ law(R.khoan_abolish) }}, {{ law(R.books) }} | Hết thuế khoán và lệ phí môn bài; mẫu sổ kế toán mới cho hộ kinh doanh có hiệu lực |
| 05/03/2026 | {{ law(R.hkd_tax) }}, {{ law(R.hkd_procedures) }} | Quy định cách tính thuế, khai thuế và hồ sơ, thủ tục cho hộ kinh doanh |
| 29/04/2026 | {{ law(R.threshold) }} | Nâng mức doanh thu không chịu thuế từ {{ L.old_threshold_label }} lên {{ L.threshold_label }} mỗi năm, áp dụng ngược từ 01/01/2026 |
| 01/07/2026 | {{ law(R.tax_admin_law) }}, {{ law(R.einvoice) }} | Luật Quản lý thuế mới có hiệu lực chung; quy định mới về hoá đơn điện tử |

## Hộ của bạn thuộc nhóm nào

| Hạng mục | Doanh thu năm từ {{ L.threshold_label }} trở xuống | Doanh thu năm trên {{ L.threshold_label }} |
|---|---|---|
| Thuế GTGT, thuế TNCN | Không chịu thuế GTGT, không phải nộp thuế TNCN | Khai và nộp thuế GTGT, thuế TNCN |
| Việc phải làm với cơ quan thuế | Thông báo doanh thu thực tế trong năm, chậm nhất {{ L.revenue_notice_deadline }} | Nộp hồ sơ khai thuế theo quý hoặc theo tháng |
| Hoá đơn điện tử | Không bắt buộc, được tự nguyện đăng ký | Bắt buộc: có mã của cơ quan thuế hoặc khởi tạo từ máy tính tiền |
| Sổ kế toán theo {{ law(R.books) }} | Mẫu S1a-HKD (sổ doanh thu bán hàng hoá, dịch vụ) | Mẫu S2a-HKD đến S2e-HKD, tuỳ cách tính thuế |

Theo {{ law(R.hkd_tax) }}, hộ kinh doanh nộp hồ sơ khai thuế bằng phương thức điện tử. Hạn nộp hồ sơ khai thuế theo quý là {{ L.quarterly_deadline }}; theo tháng là {{ L.monthly_deadline }}. Cách tính thuế TNCN cụ thể phụ thuộc mức doanh thu và lựa chọn của hộ, được quy định trong {{ law(R.hkd_tax) }}.

## Việc cần làm theo thứ tự

1. **Ước doanh thu cả năm.** Cộng doanh thu từ đầu năm và ước cho các tháng còn lại để biết hộ ở dưới hay trên {{ L.threshold_label }}.
2. **Nếu doanh thu vượt {{ L.threshold_label }}: đăng ký hoá đơn điện tử.** Hạn là {{ L.einvoice_register_days }} ngày kể từ ngày cuối cùng của kỳ tính thuế có doanh thu luỹ kế vượt mức ({{ law(R.threshold) }}). Xem [cách xuất hoá đơn từ máy tính tiền](/huong-dan/xuat-hoa-don-tu-may-tinh-tien/).
3. **Mở sổ kế toán đúng mẫu.** Chọn mẫu sổ theo nhóm của hộ ở bảng trên và ghi đều đặn. Tài liệu kế toán lưu tối thiểu {{ L.books_retention_years }} năm.
4. **Tách tiền kinh doanh khỏi tiền gia đình.** Dùng một tài khoản riêng cho cửa hàng giúp đối chiếu doanh thu dễ hơn khi khai thuế.
5. **Nộp đúng hạn.** Hộ dưới mức chịu thuế thông báo doanh thu chậm nhất {{ L.revenue_notice_deadline }}; hộ trên mức nộp hồ sơ khai thuế theo kỳ.

## Sổ sách cần giữ

{{ law(R.books) }} thay cho {{ law(R.old_books) }} từ ngày 01/01/2026. Hộ không chịu thuế GTGT và không phải nộp thuế TNCN dùng mẫu **S1a-HKD**. Hộ nộp thuế dùng các mẫu từ **S2a-HKD** đến **S2e-HKD** tuỳ cách tính thuế. Tài liệu kế toán của hộ lưu tối thiểu {{ L.books_retention_years }} năm; thời hạn lưu hoá đơn theo pháp luật về thuế.

## Tallyo giúp ở bước nào

- **Bước 1:** báo cáo doanh thu luỹ kế theo năm, có cảnh báo khi gần {{ L.threshold_label }}.
- **Bước 2:** hoá đơn điện tử khởi tạo từ máy tính tiền lập ngay khi tính tiền.
- **Bước 3:** sổ doanh thu và chi phí tự lập từ dữ liệu bán hàng, xuất Excel.

{{ brand.name }} không nộp thuế thay bạn và không phải đại lý thuế.

## Những văn bản cũ không còn áp dụng

Khi tìm hiểu trên mạng, bạn sẽ gặp nhiều bài viết dẫn văn bản đã hết hiệu lực:

- {{ law(R.old_hkd_tax) }} về thuế hộ kinh doanh: bị thay bằng {{ law(R.hkd_procedures) }} từ {{ lawref(R.old_hkd_tax).ended_on | date_vi }}.
- {{ law(R.old_books) }} về sổ kế toán: bị thay bằng {{ law(R.books) }} từ {{ lawref(R.old_books).ended_on | date_vi }}.
- {{ law(R.old_einvoice) }} và {{ law(R.old_pos_rule) }} về hoá đơn: hết hiệu lực từ {{ lawref(R.old_einvoice).ended_on | date_vi }}, thay bằng {{ law(R.einvoice) }}.
- Mức doanh thu không chịu thuế {{ L.old_threshold_label }}: đã được nâng lên {{ L.threshold_label }} từ 01/01/2026.
