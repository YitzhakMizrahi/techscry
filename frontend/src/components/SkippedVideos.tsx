'use client';

import { useEffect, useState } from 'react';
import { EyeOff } from 'lucide-react';

interface SkippedVideo {
  video_id: string;
  title: string;
  channel: string;
  url: string;
}

interface Props {
  userId: string;
}

export function SkippedVideos({ userId }: Props) {
  const [skipped, setSkipped] = useState<SkippedVideo[]>([]);

  useEffect(() => {
    if (!userId) return; // ✅ Guard against undefined during hydration

    fetch(`/mock/skipped.json`)
      .then((res) => res.json())
      .then((data) => setSkipped(data))
      .catch((err) => console.error('Error loading skipped.json:', err));
  }, [userId]);

  if (!skipped.length) return null;

  return (
    <div className="mt-6">
      <h2 className="text-sm font-medium text-muted-foreground mb-2 flex items-center gap-1">
        <EyeOff className="w-4 h-4" />
        Skipped Videos (No Transcript)
      </h2>
      <ul className="text-sm space-y-1">
        {skipped.map((v) => (
          <li key={v.video_id}>
            <span className="font-semibold">{v.title}</span> —{' '}
            <a
              href={v.url}
              className="text-blue-600 hover:underline"
              target="_blank"
            >
              Watch
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
