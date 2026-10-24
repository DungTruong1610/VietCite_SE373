import { useState, type FormEvent } from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import {
  Alert,
  AlertDescription,
  AlertTitle,
  Button,
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  Field,
  FieldGroup,
  FieldLabel,
  Input,
  Spinner,
} from '@cnma/react-ui';
import { CircleAlert } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { ApiError } from '@/services/apiClient';
import type { LoginLocationState } from '@/components/auth/ProtectedRoute';

interface LoginErrorView {
  title: string;
  message: string;
}

function describeLoginError(error: unknown): LoginErrorView {
  if (error instanceof ApiError) {
    if (error.status === 401) {
      return { title: 'Sai thông tin đăng nhập', message: error.message };
    }
    if (error.status === 503) {
      // Server chưa cấu hình tài khoản đăng nhập: hiển thị nguyên văn thông điệp của backend.
      return { title: 'Server chưa bật đăng nhập', message: error.message };
    }
    return { title: 'Không đăng nhập được', message: error.message };
  }
  return { title: 'Không đăng nhập được', message: 'Đã xảy ra lỗi không xác định. Thử lại sau.' };
}

export function LoginPage() {
  const { status, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as LoginLocationState | null)?.from ?? '/';

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<LoginErrorView | null>(null);

  if (status === 'authenticated') {
    return <Navigate to={from} replace />;
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await login({ username: username.trim(), password });
      navigate(from, { replace: true });
    } catch (loginError) {
      setError(describeLoginError(loginError));
    } finally {
      setSubmitting(false);
    }
  };

  const canSubmit = username.trim() !== '' && password !== '' && !submitting;

  return (
    <div className="flex min-h-svh items-center justify-center bg-background p-4">
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle className="text-xl">VietCite Studio</CardTitle>
          <CardDescription>Đăng nhập để viết và duyệt bài cho thương hiệu Tallyo.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} noValidate>
            <FieldGroup>
              <Field>
                <FieldLabel htmlFor="username">Tên đăng nhập</FieldLabel>
                <Input
                  id="username"
                  name="username"
                  autoComplete="username"
                  autoFocus
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  required
                />
              </Field>
              <Field>
                <FieldLabel htmlFor="password">Mật khẩu</FieldLabel>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                />
              </Field>

              {error ? (
                <Alert variant="destructive" role="alert">
                  <CircleAlert />
                  <AlertTitle>{error.title}</AlertTitle>
                  <AlertDescription>{error.message}</AlertDescription>
                </Alert>
              ) : null}

              <Button type="submit" disabled={!canSubmit} className="w-full">
                {submitting ? <Spinner size="sm" /> : null}
                {submitting ? 'Đang đăng nhập…' : 'Đăng nhập'}
              </Button>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
