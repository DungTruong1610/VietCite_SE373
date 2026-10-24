import {
  BookOpenCheck,
  FileText,
  LayoutDashboard,
  ListTree,
  Palette,
  Radar,
  Settings,
  Workflow,
  type LucideIcon,
} from 'lucide-react';

export interface NavItem {
  path: string;
  label: string;
  icon: LucideIcon;
  /** Mô tả ngắn hiển thị trên trang. */
  description: string;
  /** Phase sẽ xây màn hình này; không có nghĩa là đã làm trong Phase 1. */
  plannedPhase?: string;
}

/** 8 màn hình theo kế hoạch đồ án. Thứ tự ở đây là thứ tự trên sidebar. */
export const NAV_ITEMS: readonly NavItem[] = [
  {
    path: '/',
    label: 'Tổng quan',
    icon: LayoutDashboard,
    description: 'Trạng thái backend và các tích hợp.',
  },
  {
    path: '/brands',
    label: 'Brand Studio',
    icon: Palette,
    description: 'Hồ sơ thương hiệu, sản phẩm, bảng giá và nguồn trích dẫn của Tallyo.',
    plannedPhase: 'Phase 3',
  },
  {
    path: '/queries',
    label: 'Query Universe',
    icon: ListTree,
    description: 'Tập câu hỏi người dùng hỏi AI và nhóm chủ đề cần phủ.',
    plannedPhase: 'Phase 3',
  },
  {
    path: '/articles',
    label: 'Article Studio',
    icon: FileText,
    description: 'Lập dàn ý, viết và chỉnh bài tiếng Việt chuẩn GEO bằng hệ đa tác tử.',
    plannedPhase: 'Phase 4',
  },
  {
    path: '/review',
    label: 'Review & Approve',
    icon: BookOpenCheck,
    description: 'Kiểm duyệt bài, phê duyệt và cấp approval token trước khi đăng.',
    plannedPhase: 'Phase 5–6',
  },
  {
    path: '/visibility',
    label: 'Visibility Lab',
    icon: Radar,
    description: 'Đo mức độ thương hiệu được AI nhắc đến và trích dẫn.',
    plannedPhase: 'Phase 7',
  },
  {
    path: '/traces',
    label: 'Traces & Eval',
    icon: Workflow,
    description: 'Theo dõi từng bước của agent và chạy đánh giá.',
  },
  {
    path: '/settings',
    label: 'Settings',
    icon: Settings,
    description: 'Cấu hình model, khoá tích hợp và người dùng.',
    plannedPhase: 'Phase 8',
  },
];
