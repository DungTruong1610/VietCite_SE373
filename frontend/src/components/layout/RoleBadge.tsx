import { Badge } from '@cnma/react-ui';
import type { UserRole } from '@/types/api';

const ROLE_LABELS: Record<UserRole, string> = {
  editor: 'Biên tập viên',
  approver: 'Người duyệt',
};

interface RoleBadgeProps {
  role: UserRole;
}

export function RoleBadge({ role }: RoleBadgeProps) {
  return (
    <Badge variant={role === 'approver' ? 'positive' : 'informativeBlue'} hasBorder>
      {ROLE_LABELS[role] ?? role}
    </Badge>
  );
}
