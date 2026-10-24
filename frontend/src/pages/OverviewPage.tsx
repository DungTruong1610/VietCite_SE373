import { useQuery } from '@tanstack/react-query';
import {
  Alert,
  AlertDescription,
  AlertTitle,
  Badge,
  Button,
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  Skeleton,
} from '@cnma/react-ui';
import { CircleAlert, RefreshCw } from 'lucide-react';
import type { HealthFeatures, HealthResponse } from '@/types/api';
import { fetchHealth } from '@/services/healthService';
import { PageHeader } from '@/components/common/PageHeader';

interface FeatureInfo {
  name: string;
  purpose: string;
}

const FEATURES: Record<keyof HealthFeatures, FeatureInfo> = {
  deepseek: { name: 'DeepSeek', purpose: 'Model ngôn ngữ chính của các agent' },
  jina: { name: 'Jina', purpose: 'Đọc trang web và tìm kiếm' },
  gemini: { name: 'Gemini', purpose: 'Model phụ, dùng khi đo mức hiển thị' },
};

const FEATURE_KEYS = Object.keys(FEATURES) as Array<keyof HealthFeatures>;

interface OnOffBadgeProps {
  enabled: boolean;
}

function OnOffBadge({ enabled }: OnOffBadgeProps) {
  return (
    <Badge variant={enabled ? 'positive' : 'obsoleted'} hasBorder>
      {enabled ? 'bật' : 'tắt'}
    </Badge>
  );
}

interface BackendStatusProps {
  health: HealthResponse | undefined;
  pending: boolean;
}

function BackendStatus({ health, pending }: BackendStatusProps) {
  if (pending) {
    return <Skeleton className="h-6 w-24" />;
  }
  if (!health) {
    return (
      <Badge variant="negative" hasBorder>
        không phản hồi
      </Badge>
    );
  }
  return (
    <span className="flex flex-wrap items-center gap-2">
      <Badge variant={health.status === 'ok' ? 'positive' : 'negative'} hasBorder>
        {health.status === 'ok' ? 'hoạt động' : health.status}
      </Badge>
      {health.offline ? (
        <Badge variant="attention" hasBorder>
          chế độ offline
        </Badge>
      ) : null}
    </span>
  );
}

export function OverviewPage() {
  const health = useQuery({
    queryKey: ['health'],
    queryFn: ({ signal }) => fetchHealth(signal),
  });

  return (
    <>
      <PageHeader
        title="Tổng quan"
        description="Trạng thái backend và các tích hợp bên ngoài."
        actions={
          <Button variant="outline" size="sm" onClick={() => void health.refetch()} disabled={health.isFetching}>
            <RefreshCw className="size-4" />
            Làm mới
          </Button>
        }
      />

      {health.isError ? (
        <Alert variant="destructive" className="mb-6">
          <CircleAlert />
          <AlertTitle>Không lấy được trạng thái backend</AlertTitle>
          <AlertDescription>{health.error.message}</AlertDescription>
        </Alert>
      ) : null}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <Card>
          <CardHeader>
            <CardDescription>Backend</CardDescription>
            <CardTitle>
              <BackendStatus health={health.data} pending={health.isPending} />
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Phiên bản: {health.data?.version ?? '—'}
          </CardContent>
        </Card>

        {FEATURE_KEYS.map((key) => (
          <Card key={key}>
            <CardHeader>
              <CardDescription>{FEATURES[key].purpose}</CardDescription>
              <CardTitle className="flex items-center justify-between gap-2">
                <span>{FEATURES[key].name}</span>
                {health.isPending ? <Skeleton className="h-5 w-10" /> : null}
                {health.data ? <OnOffBadge enabled={health.data.features[key]} /> : null}
              </CardTitle>
            </CardHeader>
          </Card>
        ))}
      </div>
    </>
  );
}
