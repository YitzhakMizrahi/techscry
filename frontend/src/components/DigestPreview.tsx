'use client';

import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import Image from 'next/image';
import { VideoModal } from './VideoModal';

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

function getBadgeProps(score: number): {
  label: string;
  variant: 'default' | 'secondary' | 'destructive' | 'outline';
} {
  if (score >= 0.95)
    return { label: '🔥 High Relevance', variant: 'destructive' };
  if (score >= 0.8) return { label: 'Strong Signal', variant: 'default' };
  if (score >= 0.6) return { label: 'Relevant', variant: 'secondary' };
  return { label: 'Mild Signal', variant: 'secondary' };
}

export function DigestPreview({ userId }: Props) {
  const [items, setItems] = useState<DigestItem[]>([]);
  const [activeVideoId, setActiveVideoId] = useState<string | null>(null);

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
    <>
      <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-4">
        {items.map((item) => {
          const thumbnailUrl = `https://img.youtube.com/vi/${item.video_id}/hqdefault.jpg`;
          const badge = getBadgeProps(item.score);

          return (
            <Card
              key={item.video_id}
              className="group relative overflow-hidden rounded-lg border p-4 transition-shadow hover:shadow-md"
            >
              <div
                className="relative mb-4 h-40 w-full cursor-pointer overflow-hidden rounded border"
                onClick={() => setActiveVideoId(item.video_id)}
              >
                <Image
                  src={thumbnailUrl}
                  alt={item.title}
                  fill
                  sizes="(max-width: 768px) 100vw, 33vw"
                  className="object-cover group-hover:brightness-75 transition duration-200"
                  placeholder="blur"
                  blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..." // you can use a tiny image or a blur hash here
                />
                <Badge
                  className={`absolute top-2 right-2 text-xs italic opacity-60`}
                  variant={badge.variant}
                >
                  {badge.label}
                </Badge>
                <span className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                  <div className="bg-white/80 rounded-full p-3 backdrop-blur-sm shadow-md">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="w-4 h-4 sm:w-5 sm:h-5 text-black"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path d="M8 5v14l11-7z" />
                    </svg>
                  </div>
                </span>
              </div>

              <div className="flex flex-col gap-2">
                <h3 className="text-base font-semibold leading-tight line-clamp-2">
                  {item.title}
                </h3>
                <div className="text-sm text-muted-foreground">
                  {item.channel}
                </div>
                <p className="text-sm text-muted-foreground line-clamp-4">
                  {item.summary}
                </p>
                <a
                  href={item.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-1 text-sm font-medium text-primary hover:underline"
                >
                  Watch on YouTube →
                </a>
              </div>
            </Card>
          );
        })}
      </div>

      {activeVideoId && (
        <VideoModal
          videoId={activeVideoId}
          onClose={() => setActiveVideoId(null)}
        />
      )}
    </>
  );
}
