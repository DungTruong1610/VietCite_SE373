import { Button, Separator, SidebarTrigger } from '@cnma/react-ui';
import { LogOut, Palette, UserRound } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { THEME_LABELS, useTheme } from '@/contexts/ThemeContext';
import { RoleBadge } from '@/components/layout/RoleBadge';

export function AppHeader() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="flex h-14 shrink-0 items-center gap-3 border-b border-border bg-card px-4">
      <SidebarTrigger aria-label="Thu gọn hoặc mở rộng thanh bên" />
      <Separator orientation="vertical" className="h-6" />
      <span className="text-base font-semibold text-foreground">VietCite Studio</span>

      <div className="ml-auto flex items-center gap-3">
        <Button
          variant="ghost"
          size="sm"
          onClick={toggleTheme}
          title="Đổi giao diện"
          aria-label={`Giao diện hiện tại: ${THEME_LABELS[theme]}. Bấm để đổi.`}
        >
          <Palette className="size-4" />
          <span className="hidden sm:inline">{THEME_LABELS[theme]}</span>
        </Button>

        {user ? (
          <div className="flex items-center gap-2">
            <UserRound className="size-4 text-muted-foreground" aria-hidden />
            <span className="text-sm font-medium text-foreground">{user.username}</span>
            <RoleBadge role={user.role} />
          </div>
        ) : null}

        <Button variant="outline" size="sm" onClick={logout}>
          <LogOut className="size-4" />
          Đăng xuất
        </Button>
      </div>
    </header>
  );
}
