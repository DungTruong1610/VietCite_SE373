# packages/

Thư mục chứa gói npm nội bộ dùng cho frontend. **File `.tgz` không được commit** (đã có trong `.gitignore`); mỗi thành viên tự đặt file vào đây.

## `@cnma/react-ui` 1.1.4

Thư viện component React của công ty (dựa trên Radix UI, Tailwind v4, có i18n). Được phép dùng trong đồ án; **không phát tán ra ngoài nhóm** và không đưa lên repo public.

| Thuộc tính | Giá trị |
|---|---|
| File | `packages/cnma-react-ui-1.1.4.tgz` |
| SHA-256 | `1c7926fc569a528ca12585b93607cbcb307f557bf1a1a9f8e7d2aa41ecf3bd1f` |
| Lấy ở đâu | Xin TV1 gửi trực tiếp (không qua kênh công khai) |
| Kiểm tra | `node scripts/check-ui-package.mjs` |

### Cách frontend dùng gói

`frontend/package.json`:

```json
"dependencies": {
  "@cnma/react-ui": "file:../packages/cnma-react-ui-1.1.4.tgz",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "i18next": "^25.2.0",
  "react-i18next": "^16.5.0",
  "@radix-ui/react-aspect-ratio": "^1.1.0",
  "radix-ui": "^1.4.0",
  "recharts": "^3.0.0",
  "react-is": "^19.0.0"
}
```

`frontend/src/index.css`:

```css
@import '@cnma/react-ui/styles.css';
```

### Lưu ý đã kiểm chứng (24/10/2026)

- Gói **import nhưng không khai báo** `@radix-ui/react-aspect-ratio`, `radix-ui`, `recharts`. Thiếu các gói này thì lỗi `ERR_MODULE_NOT_FOUND`, nên frontend phải tự khai báo (như trên). `recharts` lại cần `react-is`.
- Gói yêu cầu `react-i18next` **^16.5**. Không để npm tự lấy bản 17 trở lên.
- Phải dùng **Tailwind v4**; không dùng cú pháp `@tailwind base/components/utilities` của v3.
- Import thử với React 19: có 349 export, gồm `Button`, `Input`, `Select`, `Dialog`, `Badge`, `DataTable`, `FilterBar`, `Tabs`, `Card`, `Tooltip`; subpath `@cnma/react-ui/i18n` dùng được.
- CI trên GitHub không có file này nên **bỏ qua bước build frontend** khi thiếu gói (xem ADR 0002).
