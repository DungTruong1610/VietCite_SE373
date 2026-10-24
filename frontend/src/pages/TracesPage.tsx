import { PageHeader } from '@/components/common/PageHeader';
import { DemoRunPanel } from '@/components/traces/DemoRunPanel';

export function TracesPage() {
  return (
    <>
      <PageHeader
        title="Traces & Eval"
        description="Theo dõi từng bước của agent. Phase 1 có một agent demo để kiểm tra luồng trace trực tiếp."
      />
      <DemoRunPanel />
    </>
  );
}
