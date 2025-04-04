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
    // TEMP: local mock data — replace with fetch from real API or file
    const mock: DigestItem[] = [
      {
        video_id: 'abc123',
        title: 'LangChain Agents vs AutoGen: Which One Wins?',
        channel: 'Fireship',
        summary: 'This video compares LangChain agents to AutoGen workflows...',
        url: 'https://youtu.be/abc123',
        score: 0.87,
      },
      {
        video_id: 'xyz456',
        title: 'New OpenAI SDK Features in 2025',
        channel: 'OpenAI',
        summary: 'An overview of the newest OpenAI SDK capabilities...',
        url: 'https://youtu.be/xyz456',
        score: 0.78,
      },
    ];
    setItems(mock);
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
            className="text-blue-600 hover:underline text-sm"
          >
            🔗 Watch on YouTube
          </a>
        </Card>
      ))}
    </div>
  );
}
