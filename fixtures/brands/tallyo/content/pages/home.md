---
path: /
title: "Tallyo: bán hàng và hoá đơn điện tử cho hộ kinh doanh"
description: "Tallyo giúp hộ kinh doanh tính tiền tại quầy, xuất hoá đơn điện tử từ máy tính tiền và tự lập sổ sách. Dùng thử 15 ngày, không cần thẻ."
template: home
h1: Tính tiền xong là có hoá đơn điện tử
order: 0
data:
  hero:
    badge: Hoá đơn điện tử khởi tạo từ máy tính tiền
    title_dark: Tính tiền xong là có
    title_red: hoá đơn điện tử
    lead: "{{ brand.tagline }} {{ brand.name }} dành cho tiệm tạp hoá, quán cà phê và shop nhỏ đang chuyển từ ghi sổ tay sang bán hàng và kê khai đúng quy định."
    note: "Dùng thử {{ facts.trial.days }} ngày, không cần thẻ thanh toán"
  pillars:
    eyebrow: Tallyo làm gì
    title: Bốn việc Tallyo làm thay bạn
    lead: Mỗi việc trước đây bạn làm bằng tay, ghi vào sổ hoặc nhập lại vào Excel cuối ngày.
    items:
      - icon: scan-barcode
        title: Bán hàng tại quầy
        text: Quét mã vạch hoặc chạm chọn món, in hoá đơn ra máy in nhiệt, nhận tiền qua mã VietQR.
        href: /tinh-nang/ban-hang-tai-quay/
      - icon: receipt
        title: Hoá đơn điện tử từ máy tính tiền
        text: Mỗi lần tính tiền tạo một hoá đơn điện tử khởi tạo từ máy tính tiền, khách quét mã QR để tra cứu.
        href: /tinh-nang/hoa-don-dien-tu/
      - icon: package
        title: Quản lý kho
        text: Bán đến đâu trừ kho đến đó. Sắp hết hàng thì Tallyo nhắc, kiểm kho bằng điện thoại.
        href: /tinh-nang/ban-hang-tai-quay/#quan-ly-kho
      - icon: book-open-check
        title: Sổ sách hộ kinh doanh
        text: Sổ doanh thu và chi phí tự lập từ dữ liệu bán hàng, xuất Excel khi cần kê khai.
        href: "/tinh-nang/#so-sach-ho-kinh-doanh"
  compare:
    eyebrow: Trước và sau
    title: Ghi sổ tay và dùng Tallyo khác nhau thế nào
    lead: So sánh cách một tiệm tạp hoá làm việc hằng ngày khi ghi sổ tay hoặc Excel, và khi dùng Tallyo.
    bad_title: Sổ tay hoặc Excel
    good_title: Dùng Tallyo
    rows:
      - bad: Cuối ngày cộng sổ bằng máy tính bỏ túi, lệch vài chục nghìn là phải dò lại từng trang.
        good: Doanh thu cộng tự động sau mỗi đơn, xem theo ngày, tuần, tháng.
      - bad: Khách xin hoá đơn thì phải hẹn hôm sau, mở phần mềm khác để nhập lại.
        good: Hoá đơn điện tử tạo ngay lúc tính tiền, in kèm mã QR để khách tra cứu.
      - bad: Hết hàng mới biết vì kệ trống.
        good: Tallyo nhắc khi một mặt hàng xuống dưới mức tồn bạn đặt.
      - bad: Nhân viên bán, chủ không biết ai huỷ đơn, ai giảm giá.
        good: Mỗi nhân viên một tài khoản, mọi lần huỷ và giảm giá đều có tên người làm.
      - bad: Đến kỳ kê khai phải gom sổ, hoá đơn giấy và tin nhắn chuyển khoản.
        good: Sổ doanh thu, chi phí lập sẵn từ dữ liệu bán hàng, xuất Excel trong vài phút.
  metrics:
    eyebrow: Thông tin nhanh
    title: Vài con số về Tallyo
    items:
      - value: "{{ facts.trial.days }} ngày"
        label: Dùng thử miễn phí
        text: "Dùng thử đủ tính năng của gói {{ plans.shop.name }}, không cần thẻ thanh toán."
      - value: "{{ plans.start.price.price_month | vnd }}"
        label: Giá mỗi tháng từ
        text: "Gói {{ plans.start.name }} cho hộ kinh doanh một cửa hàng. Trả theo năm bằng giá 10 tháng."
      - value: "{{ brand.customers.count | number_vi }}+"
        label: Hộ kinh doanh đang dùng
        text: "Số liệu giả lập tính đến {{ brand.customers.as_of | date_vi }}."
  steps:
    eyebrow: Bắt đầu
    title: Bắt đầu trong 4 bước
    lead: Phần lớn cửa hàng bắt đầu bán được ngay trong buổi đầu tiên.
    items:
      - title: Tạo tài khoản
        text: Đăng ký bằng số điện thoại hoặc email, chọn loại hình kinh doanh.
        who: Bạn làm
      - title: Nhập mặt hàng
        text: Quét mã vạch có sẵn trên sản phẩm hoặc tải danh sách từ file Excel.
        who: Bạn làm
      - title: Kết nối máy in
        text: Tallyo tự tìm máy in nhiệt khổ 58 mm hoặc 80 mm qua Bluetooth, USB hoặc mạng nội bộ.
        who: Tallyo làm
      - title: Bán đơn đầu tiên
        text: Tính tiền, in hoá đơn, xem đơn hiện ngay trong báo cáo doanh thu của ngày.
        who: Bạn làm
  cta:
    title: Thử Tallyo ở cửa hàng của bạn
    text: "Dùng thử gói {{ plans.shop.name }} miễn phí {{ facts.trial.days }} ngày, không cần thẻ thanh toán. Hết hạn dùng thử, bạn chọn gói phù hợp hoặc dừng; dữ liệu được giữ {{ facts.trial.data_kept_days }} ngày."
---
