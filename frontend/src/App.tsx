import type { ComponentType } from 'react';
import { createBrowserRouter, Navigate, RouterProvider, type RouteObject } from 'react-router-dom';
import { NAV_ITEMS } from '@/config/navigation';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { AppLayout } from '@/components/layout/AppLayout';
import { LoginPage } from '@/pages/LoginPage';
import { OverviewPage } from '@/pages/OverviewPage';
import { PlaceholderPage } from '@/pages/PlaceholderPage';
import { TracesPage } from '@/pages/TracesPage';

/** Màn hình đã xây trong Phase 1; các route còn lại hiển thị PlaceholderPage. */
const BUILT_PAGES: Record<string, ComponentType> = {
  '/': OverviewPage,
  '/traces': TracesPage,
};

const appRoutes: RouteObject[] = NAV_ITEMS.map((item) => {
  const Page = BUILT_PAGES[item.path];
  const element = Page ? <Page /> : <PlaceholderPage item={item} />;
  return item.path === '/' ? { index: true, element } : { path: item.path.slice(1), element };
});

const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  {
    element: <ProtectedRoute />,
    children: [
      {
        path: '/',
        element: <AppLayout />,
        children: [...appRoutes, { path: '*', element: <Navigate to="/" replace /> }],
      },
    ],
  },
]);

export function App() {
  return <RouterProvider router={router} />;
}
