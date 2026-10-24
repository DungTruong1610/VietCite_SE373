import { Badge, Empty, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from '@cnma/react-ui';
import type { NavItem } from '@/config/navigation';
import { PageHeader } from '@/components/common/PageHeader';

interface PlaceholderPageProps {
  item: NavItem;
}

/** Màn hình đã có route nhưng chưa xây: cho biết phase nào sẽ làm. */
export function PlaceholderPage({ item }: PlaceholderPageProps) {
  const Icon = item.icon;
  return (
    <>
      <PageHeader title={item.label} description={item.description} />
      <Empty className="rounded-lg border border-dashed border-border bg-card">
        <EmptyHeader>
          <EmptyMedia variant="icon">
            <Icon />
          </EmptyMedia>
          <EmptyTitle>Màn hình này chưa được xây</EmptyTitle>
          <EmptyDescription>
            {item.label} sẽ được làm ở {item.plannedPhase ?? 'phase sau'}. Phase 1 chỉ dựng khung ứng dụng,
            đăng nhập và trang Traces &amp; Eval.
          </EmptyDescription>
        </EmptyHeader>
        {item.plannedPhase ? <Badge variant="informativeBlue">{item.plannedPhase}</Badge> : null}
      </Empty>
    </>
  );
}
