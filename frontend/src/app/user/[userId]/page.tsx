// src/app/user/[userId]/page.tsx
import { notFound } from 'next/navigation';
import { DigestPreview } from '@/components/DigestPreview';

interface Props {
  params: { userId: string };
}

export default function UserDigestPage({ params }: Props) {
  const { userId } = params;

  if (!userId) return notFound();

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4">
        📰 Digest Preview for{' '}
        <span className="text-muted-foreground">{userId}</span>
      </h1>
      <DigestPreview userId={userId} />
    </main>
  );
}
