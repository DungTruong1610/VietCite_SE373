---
path: /tinh-nang/hoa-don-dien-tu/
parent: /tinh-nang/
title: Hoá đơn điện tử khởi tạo từ máy tính tiền | Tallyo
description: "Tallyo lập hoá đơn điện tử khởi tạo từ máy tính tiền ngay khi bạn tính tiền. Xem ai phải dùng, khách nhận hoá đơn thế nào và số hoá đơn trong từng gói."
template: doc
h1: Hoá đơn điện tử khởi tạo từ máy tính tiền
eyebrow: Tính năng
lede: Tính tiền xong là hoá đơn điện tử đã được lập. Bạn không phải mở phần mềm khác hay nhập lại vào cuối ngày.
icon: receipt
order: 21
toc: true
laws: [254/2026/NĐ-CP, 141/2026/NĐ-CP, 91/2026/TT-BTC]
---

{% set L = facts.legal_facts %}
## Hoá đơn điện tử khởi tạo từ máy tính tiền là gì?

Đây là hoá đơn điện tử được lập ngay tại quầy khi bạn tính tiền cho khách, từ phần mềm bán hàng có kết nối dữ liệu với cơ quan thuế. Theo {{ law(facts.legal_refs.einvoice) }}, loại hoá đơn này có thể có mã hoặc không có mã của cơ quan thuế. Người mua dùng mã tra cứu in trên hoá đơn giấy để xem lại hoá đơn.

## Hộ kinh doanh nào phải dùng hoá đơn điện tử?

Từ ngày {{ lawref(facts.legal_refs.einvoice).effective_date | date_vi }}, quy định về hoá đơn điện tử nằm ở {{ law(facts.legal_refs.einvoice) }}:

- Hộ kinh doanh có **doanh thu năm trên {{ L.threshold_label }}** phải dùng hoá đơn điện tử có mã của cơ quan thuế, hoặc hoá đơn điện tử khởi tạo từ máy tính tiền có kết nối dữ liệu với cơ quan thuế. Bạn được chọn một trong hai loại; hoá đơn từ máy tính tiền hợp với tiệm bán lẻ và quán ăn uống.
- Hộ có **doanh thu năm từ {{ L.threshold_label }} trở xuống** không bắt buộc, nhưng được tự nguyện đăng ký nếu có nhu cầu, ví dụ khi khách hay xin hoá đơn.
- Hộ có doanh thu luỹ kế trong năm vượt {{ L.threshold_label }} phải đăng ký sử dụng hoá đơn điện tử trong **{{ L.einvoice_register_days }} ngày** kể từ ngày cuối cùng của kỳ tính thuế có doanh thu vượt mức ({{ law(facts.legal_refs.threshold) }}).

<div class="note">{{ icon("info", 20) }}<div><p><strong>Cẩn thận với bài viết cũ.</strong> Nhiều trang vẫn dẫn {{ law(facts.legal_refs.old_pos_rule) }} với mức "từ 1 tỷ đồng trở lên phải dùng máy tính tiền". Nghị định này và {{ law(facts.legal_refs.old_einvoice) }} đã hết hiệu lực từ {{ lawref(facts.legal_refs.old_pos_rule).ended_on | date_vi }}.</p></div></div>

## Tallyo lập hoá đơn thế nào khi bạn tính tiền

1. Bạn quét mã vạch hoặc chọn món, bấm thanh toán như mọi ngày.
2. Tallyo lập hoá đơn điện tử ngay lúc thanh toán, gắn với đơn hàng vừa bán.
3. Máy in nhiệt in tờ hoá đơn có mã QR tra cứu cho khách.
4. Hoá đơn được ghi vào sổ doanh thu của ngày, dùng cho lúc kê khai.

Muốn bắt đầu, xem [hướng dẫn xuất hoá đơn từ máy tính tiền](/huong-dan/xuat-hoa-don-tu-may-tinh-tien/).

## Khách nhận hoá đơn bằng cách nào

Khách quét mã QR in trên hoá đơn giấy để xem hoá đơn điện tử. Nếu khách cần hoá đơn ghi tên công ty, nhân viên nhập mã số thuế của khách trước khi thanh toán.

## Khi mất mạng thì sao?

{{ facts.compatibility.offline_mode }}

## Số hoá đơn có trong từng gói

| Gói | Hoá đơn điện tử mỗi năm |
|---|---|
{% for rp in plans.values() %}| {{ rp.name }} ({{ rp.code }}) | {{ rp.einvoice_per_year | number_vi }} |
{% endfor %}

Dùng hết số hoá đơn trong năm, bạn mua thêm gói {{ facts.addons[0].name | lower }} giá {{ facts.addons[0].price | vnd }} ở trang [Bảng giá](/bang-gia/).

<div class="note">{{ icon("info", 20) }}<div><p><strong>Đây là sản phẩm demo.</strong> {{ brand.name }} là thương hiệu giả lập phục vụ đồ án SE373 (UIT), không phải tổ chức cung cấp dịch vụ hoá đơn điện tử thực tế và không kết nối với hệ thống của cơ quan thuế. Phần pháp luật trên trang là thông tin tham khảo, đã đối chiếu nguồn chính thống ngày {{ L.verified_on | date_vi }}.</p></div></div>
