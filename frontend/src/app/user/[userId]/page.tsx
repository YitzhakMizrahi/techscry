import { DigestPreview } from '@/components/DigestPreview';
import { SkippedVideos } from '@/components/SkippedVideos';
import { Newspaper } from 'lucide-react';

export default async function UserDigestPage({
  params,
}: {
  params: Promise<{ userId: string }>;
}) {
  const { userId } = await params;

  return (
    <main className="px-6 py-10 max-w-7xl mx-auto">
      <header className="mb-8 flex flex-col gap-1">
        <h1 className="text-3xl font-semibold flex items-center gap-3">
          <Newspaper className="w-7 h-7 text-muted-foreground shrink-0" />
          <span>Your Personalized Intelligence Stream</span>
        </h1>
        <p className="text-sm text-muted-foreground">
          Curated, high-signal content selected just for{' '}
          <span className="font-medium">{userId}</span>.
        </p>
      </header>

      <DigestPreview userId={userId} />
      <SkippedVideos userId={userId} />
    </main>
  );
}
