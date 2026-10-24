import { SidebarProvider } from '@cnma/react-ui';
import { Outlet } from 'react-router-dom';
import { AppHeader } from '@/components/layout/AppHeader';
import { AppSidebar } from '@/components/layout/AppSidebar';

export function AppLayout() {
  return (
    <SidebarProvider className="h-svh flex-col">
      <AppHeader />
      <div className="flex min-h-0 flex-1">
        <AppSidebar />
        <main className="min-w-0 flex-1 overflow-auto p-6">
          <Outlet />
        </main>
      </div>
    </SidebarProvider>
  );
}
