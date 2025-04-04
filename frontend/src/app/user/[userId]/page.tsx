// src/app/user/[userId]/page.tsx
import { DigestPreview } from '@/components/DigestPreview';
import { SkippedVideos } from '@/components/SkippedVideos';

export default function UserDigestPage({
  params,
}: {
  params: { userId: string };
}) {
  const { userId } = params;

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4">
        📰 Digest Preview for{' '}
        <span className="text-muted-foreground">{userId}</span>
      </h1>
      <DigestPreview userId={userId} />
      <SkippedVideos userId={userId} />
    </main>
  );
}
