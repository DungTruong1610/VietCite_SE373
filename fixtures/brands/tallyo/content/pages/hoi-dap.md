---
path: /hoi-dap/
title: Câu hỏi thường gặp về Tallyo
description: "Giải đáp về dùng thử, bảng giá, hoá đơn điện tử, máy in, dữ liệu và hoàn tiền khi dùng Tallyo cho hộ kinh doanh và cửa hàng nhỏ."
template: faq
h1: Câu hỏi thường gặp về Tallyo
nav: Hỏi đáp
eyebrow: Hỏi đáp
lede: Câu trả lời ngắn cho những câu chủ cửa hàng hỏi nhiều nhất. Không thấy câu của bạn, hãy gửi email cho đội hỗ trợ.
order: 45
toc: true
laws: [254/2026/NĐ-CP, 141/2026/NĐ-CP]
---

{% set L = facts.legal_facts %}
## Dùng thử và giá

### Dùng thử có mất phí không?

Không. Bạn dùng thử gói {{ plans.shop.name }} trong {{ facts.trial.days }} ngày, không cần nhập thẻ thanh toán.

### Hết dùng thử thì dữ liệu còn không?

Còn. Nếu chưa chọn gói, tài khoản chuyển sang chế độ chỉ xem và dữ liệu được giữ {{ facts.trial.data_kept_days }} ngày. Chọn gói trong thời gian này thì mọi dữ liệu được dùng tiếp.

### Trả theo năm được ưu đãi gì?

{{ facts.billing.year_discount_note }}. Giá từng gói ở trang [Bảng giá](/bang-gia/).

### Tallyo có thông báo trước khi đổi giá không?

Có. {{ brand.name }} thông báo trước ít nhất {{ facts.billing.price_change_notice_days }} ngày trên trang Bảng giá và qua email. {{ facts.billing.price_change_rule }}

## Hoá đơn điện tử

### Hộ kinh doanh nào phải dùng hoá đơn điện tử?

Theo {{ law(facts.legal_refs.einvoice) }}, hộ kinh doanh có doanh thu năm trên {{ L.threshold_label }} phải dùng hoá đơn điện tử có mã của cơ quan thuế hoặc hoá đơn điện tử khởi tạo từ máy tính tiền. Hộ từ {{ L.threshold_label }} trở xuống không bắt buộc nhưng được tự nguyện đăng ký. Xem thêm ở trang [Hoá đơn điện tử](/tinh-nang/hoa-don-dien-tu/).

### Doanh thu vượt {{ L.threshold_label }} giữa năm thì phải làm gì?

Đăng ký sử dụng hoá đơn điện tử trong {{ L.einvoice_register_days }} ngày kể từ ngày cuối cùng của kỳ tính thuế có doanh thu luỹ kế vượt {{ L.threshold_label }} ({{ law(facts.legal_refs.threshold) }}).

### Hết số hoá đơn trong gói thì sao?

Bạn mua thêm {{ facts.addons[0].name | lower }} ở trang Bảng giá, dùng trong {{ facts.addons[0].validity_months }} tháng. {{ brand.name }} báo trước khi số hoá đơn còn lại xuống thấp.

### Khách muốn lấy hoá đơn ghi tên công ty thì làm thế nào?

Trước khi thanh toán, nhân viên chọn "Khách cần hoá đơn" và nhập mã số thuế của khách. Hoá đơn lập ra sẽ có tên và mã số thuế đó.

### Mất mạng có xuất hoá đơn được không?

{{ facts.compatibility.offline_mode }}

### Tallyo có phải tổ chức cung cấp dịch vụ hoá đơn điện tử không?

Không. {{ brand.name }} là thương hiệu giả lập phục vụ đồ án SE373 (UIT), không phải tổ chức cung cấp dịch vụ hoá đơn điện tử thực tế và không kết nối với hệ thống của cơ quan thuế.

## Thiết bị

### Tallyo có bán máy in không?

Không. {{ brand.name }} chỉ cung cấp phần mềm, dùng được với {{ facts.compatibility.printers | join(" và ") }}.

### Có chạy trên iPhone không?

Có. {{ brand.name }} chạy trên {{ facts.compatibility.platforms | join(", ") }}.

## Tài khoản và dữ liệu

### Một tài khoản dùng cho mấy nhân viên?

Mỗi nhân viên có tài khoản riêng. Gói {{ plans.start.name }} có {{ plans.start.staff_accounts }} tài khoản, gói {{ plans.shop.name }} có {{ plans.shop.staff_accounts }}, gói {{ plans.chain.name }} có {{ plans.chain.staff_accounts }}.

### Dữ liệu của tôi lưu ở đâu?

Dữ liệu lưu tại {{ facts.privacy.data_location }}. Chi tiết ở [Chính sách bảo mật](/chinh-sach/bao-mat/).

## Hoàn tiền

### Gói tháng có được hoàn tiền không?

Không. Gói tháng không được hoàn tiền.

### Gói năm hoàn tiền trong bao lâu?

Gói năm thanh toán lần đầu được hoàn tiền trong {{ facts.billing.refund.annual_first_payment_days }} ngày kể từ ngày thanh toán. Phần hoá đơn điện tử đã phát hành không được hoàn.
