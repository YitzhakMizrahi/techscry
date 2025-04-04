// src/components/DigestPreview.tsx
'use client';

import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';

interface DigestItem {
  video_id: string;
  title: string;
  channel: string;
  summary: string;
  url: string;
  score: number;
}

interface Props {
  userId: string;
}

export function DigestPreview({ userId }: Props) {
  const [items, setItems] = useState<DigestItem[]>([]);

  useEffect(() => {
    const loadDigest = async () => {
      try {
        const res = await fetch('/mock/curation_pool.json');
        if (!res.ok) throw new Error('Failed to fetch mock digest');
        const data = await res.json();
        setItems(data);
      } catch (err) {
        console.error('Error loading digest:', err);
      }
    };

    loadDigest();
  }, [userId]);

  return (
    <div className="grid gap-4">
      {items.map((item) => (
        <Card key={item.video_id} className="p-4">
          <div className="text-lg font-semibold mb-1">{item.title}</div>
          <div className="text-sm text-muted-foreground mb-2">
            {item.channel}
          </div>
          <div className="text-sm mb-2">{item.summary}</div>
          <a
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline text-sm"
          >
            🔗 Watch on YouTube
          </a>
        </Card>
      ))}
    </div>
  );
}
