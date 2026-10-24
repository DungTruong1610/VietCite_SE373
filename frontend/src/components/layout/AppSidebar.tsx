import {
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  cn,
  useSidebar,
} from '@cnma/react-ui';
import { NavLink, useLocation } from 'react-router-dom';
import { NAV_ITEMS } from '@/config/navigation';

function isActivePath(itemPath: string, currentPath: string): boolean {
  return itemPath === '/' ? currentPath === '/' : currentPath.startsWith(itemPath);
}

/**
 * Thanh điều hướng bên trái. Dùng các phần SidebarMenu* của @cnma/react-ui;
 * component `Sidebar` của thư viện có menu cố định nên không dùng được cho app này.
 */
export function AppSidebar() {
  const { state, isMobile, openMobile } = useSidebar();
  const { pathname } = useLocation();
  const collapsed = isMobile ? !openMobile : state === 'collapsed';

  return (
    <aside
      aria-label="Điều hướng chính"
      className={cn(
        'shrink-0 border-r border-sidebar-border bg-sidebar text-sidebar-foreground transition-[width] duration-200',
        collapsed ? 'w-14' : 'w-60',
      )}
    >
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {NAV_ITEMS.map((item) => {
                const Icon = item.icon;
                return (
                  <SidebarMenuItem key={item.path}>
                    <SidebarMenuButton
                      asChild
                      isActive={isActivePath(item.path, pathname)}
                      tooltip={collapsed ? item.label : undefined}
                    >
                      <NavLink to={item.path} end={item.path === '/'}>
                        <Icon />
                        {collapsed ? <span className="sr-only">{item.label}</span> : <span>{item.label}</span>}
                      </NavLink>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </aside>
  );
}
