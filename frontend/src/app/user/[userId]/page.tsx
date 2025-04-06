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
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <Newspaper className="w-7 h-7 text-muted-foreground" />
        Digest Preview for{' '}
        <span className="text-muted-foreground">{userId}</span>
      </h1>
      <DigestPreview userId={userId} />
      <SkippedVideos userId={userId} />
    </main>
  );
}
