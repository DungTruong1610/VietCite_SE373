---
path: /huong-dan/xuat-hoa-don-tu-may-tinh-tien/
parent: /huong-dan/
title: Cách xuất hoá đơn điện tử từ máy tính tiền trên Tallyo
description: "Các bước đăng ký và xuất hoá đơn điện tử khởi tạo từ máy tính tiền trên Tallyo, từ khai báo với cơ quan thuế đến in hoá đơn đầu tiên."
template: doc
h1: Cách xuất hoá đơn điện tử từ máy tính tiền trên Tallyo
eyebrow: Hướng dẫn
summary: Đăng ký sử dụng hoá đơn điện tử, khai báo trong Tallyo và in hoá đơn đầu tiên.
icon: receipt
order: 41
toc: true
laws: [91/2026/TT-BTC, 254/2026/NĐ-CP]
---

{% set L = facts.legal_facts %}
Sau khi việc đăng ký với cơ quan thuế đã xong, phần cài đặt trong {{ brand.name }} mất khoảng {{ facts.guides.einvoice_setup_minutes }} phút. Hướng dẫn này đi theo thứ tự, mỗi bước xong mới sang bước sau.

## Bạn cần chuẩn bị gì

- Mã số thuế của hộ kinh doanh.
- Thông tin định danh của chủ hộ khớp với cơ sở dữ liệu quốc gia về dân cư. Theo {{ law(facts.legal_refs.einvoice_guide) }}, hệ thống của cơ quan thuế tự động đối chiếu thông tin đăng ký với cơ sở dữ liệu này.
- Email hoặc số điện thoại đã đăng ký với cơ quan thuế, để xác nhận khi có kết quả.
- Máy in nhiệt khổ 58 mm hoặc 80 mm, kết nối được với điện thoại hoặc máy tính chạy {{ brand.name }}.

## Các bước

1. **Đăng ký sử dụng hoá đơn điện tử.** Hộ kinh doanh đăng ký theo {{ L.registration_form }} ban hành kèm {{ law(facts.legal_refs.einvoice_guide) }}, thông qua tổ chức cung cấp dịch vụ hoá đơn điện tử. Trên tờ khai, chọn loại hoá đơn điện tử khởi tạo từ máy tính tiền.
2. **Chờ kết quả và xác nhận.** Khi thông tin khớp, hệ thống của cơ quan thuế gửi đề nghị xác nhận qua email hoặc số điện thoại đã đăng ký. Bạn xác nhận để hoàn tất.
3. **Khai báo trong {{ brand.name }}.** Vào Cài đặt, chọn Hoá đơn điện tử, nhập mã số thuế và thông tin hoá đơn đã đăng ký.
4. **Kết nối máy in.** {{ brand.name }} tìm máy in qua {{ facts.compatibility.printer_connections | join(", ") }}. In thử một trang để kiểm tra khổ giấy.
5. **Bán thử một đơn.** Tính tiền một món giá trị nhỏ, kiểm tra tờ hoá đơn in ra có mã QR tra cứu và quét thử bằng điện thoại.

<div class="note">{{ icon("info", 20) }}<div><p>Trong kịch bản demo, {{ brand.name }} đóng vai phần mềm bán hàng làm việc với một tổ chức cung cấp dịch vụ hoá đơn điện tử. {{ brand.name }} là thương hiệu giả lập, không phải tổ chức cung cấp dịch vụ hoá đơn điện tử thực tế. Bước 1 và bước 2 mô tả thủ tục thật theo quy định đã đối chiếu ngày {{ L.verified_on | date_vi }}.</p></div></div>

## Lỗi thường gặp và cách sửa

| Hiện tượng | Cách xử lý |
|---|---|
| Đăng ký bị từ chối vì thông tin không khớp | Kiểm tra lại họ tên, số định danh của chủ hộ và mã số thuế; cập nhật thông tin rồi đăng ký lại. |
| Hoá đơn in ra không có mã QR tra cứu | Kiểm tra kết nối mạng. Khi mất mạng, hoá đơn được gửi lên khi có mạng lại, sau đó bạn in lại từ lịch sử đơn. |
| Máy in in lệch khổ | Chọn đúng khổ 58 mm hoặc 80 mm trong Cài đặt máy in. |
| Báo hết số hoá đơn trong gói | Mua thêm gói hoá đơn ở trang [Bảng giá](/bang-gia/). |

## Hộ kinh doanh có bắt buộc làm việc này không?

Hộ có doanh thu năm trên {{ L.threshold_label }} phải dùng hoá đơn điện tử, có mã của cơ quan thuế hoặc khởi tạo từ máy tính tiền. Hộ từ {{ L.threshold_label }} trở xuống được tự nguyện đăng ký. Chi tiết ở trang [Hoá đơn điện tử](/tinh-nang/hoa-don-dien-tu/#ho-kinh-doanh-nao-phai-dung-hoa-don-dien-tu).
