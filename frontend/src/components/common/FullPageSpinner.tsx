import { Spinner } from '@cnma/react-ui';

interface FullPageSpinnerProps {
  label: string;
}

export function FullPageSpinner({ label }: FullPageSpinnerProps) {
  return (
    <div className="flex h-full min-h-svh items-center justify-center gap-3 text-muted-foreground" role="status">
      <Spinner />
      <span>{label}</span>
    </div>
  );
}
