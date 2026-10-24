---
path: /chinh-sach/dieu-khoan-su-dung/
title: Điều khoản sử dụng Tallyo
description: "Điều khoản sử dụng Tallyo: phạm vi dịch vụ, thanh toán và gia hạn, chính sách hoàn tiền, trách nhiệm kê khai thuế và thông báo khi thay đổi giá."
template: doc
h1: Điều khoản sử dụng
eyebrow: Chính sách
lede: Những điều bạn và Tallyo cùng đồng ý khi bạn dùng phần mềm. Viết ngắn, rõ, không có điều khoản ẩn.
order: 81
toc: true
cta: false
---

<div class="note">{{ icon("info", 20) }}<div><p>Đây là điều khoản mẫu của một công ty giả lập, viết cho đồ án SE373 (UIT). Văn bản không có giá trị pháp lý và không dùng được cho doanh nghiệp thật.</p></div></div>

## Phạm vi dịch vụ

{{ brand.name }} cung cấp phần mềm bán hàng, quản lý kho, lập hoá đơn điện tử và sổ sách cho hộ kinh doanh theo gói bạn chọn. {{ brand.name }} không bán phần cứng và không thay bạn kê khai, nộp thuế.

## Thanh toán và gia hạn

- Gói tháng và gói năm được thanh toán trước cho cả kỳ.
- Gói tự gia hạn khi hết kỳ nếu bạn không tắt gia hạn trong phần Cài đặt.
- Hình thức thanh toán: {{ facts.billing.payment_methods | join(", ") }}.

## Hoàn tiền

- Gói năm thanh toán **lần đầu** được hoàn tiền trong **{{ facts.billing.refund.annual_first_payment_days }} ngày** kể từ ngày thanh toán.
- Gói tháng **không** được hoàn tiền.
- Phần hoá đơn điện tử đã phát hành **không** được hoàn tiền, kể cả khi gói năm được hoàn trong {{ facts.billing.refund.annual_first_payment_days }} ngày đầu.
- Tiền hoàn trả về đúng tài khoản hoặc thẻ đã dùng để thanh toán.

## Trách nhiệm kê khai thuế

Hộ kinh doanh tự chịu trách nhiệm về việc đăng ký, kê khai và nộp thuế với cơ quan thuế. {{ brand.name }} cung cấp dữ liệu bán hàng, hoá đơn và sổ sách để bạn kê khai thuận tiện hơn, nhưng không phải đại lý thuế và không tư vấn thuế.

## Thay đổi giá

{{ brand.name }} thông báo trước ít nhất **{{ facts.billing.price_change_notice_days }} ngày** khi thay đổi giá, trên trang [Bảng giá](/bang-gia/) và qua email đăng ký tài khoản. {{ facts.billing.price_change_rule }}

## Dữ liệu khi ngừng sử dụng

Khi bạn ngừng gia hạn, tài khoản chuyển sang chế độ chỉ xem. Bạn tải được toàn bộ hoá đơn và sổ sách về máy trong thời gian này. Cách {{ brand.name }} lưu và xoá dữ liệu được mô tả ở [Chính sách bảo mật](/chinh-sach/bao-mat/).
