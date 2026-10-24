import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { FullPageSpinner } from '@/components/common/FullPageSpinner';

export interface LoginLocationState {
  from?: string;
}

/** Chặn các route cần đăng nhập; chưa đăng nhập thì chuyển về /login và nhớ trang đang mở. */
export function ProtectedRoute() {
  const { status } = useAuth();
  const location = useLocation();

  if (status === 'checking') {
    return <FullPageSpinner label="Đang kiểm tra phiên đăng nhập…" />;
  }
  if (status === 'anonymous') {
    const state: LoginLocationState = { from: `${location.pathname}${location.search}` };
    return <Navigate to="/login" replace state={state} />;
  }
  return <Outlet />;
}
