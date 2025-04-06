// src/components/VideoModal.tsx
'use client';

import { X } from 'lucide-react';
import { useEffect } from 'react';

interface Props {
  videoId: string;
  onClose: () => void;
}

export function VideoModal({ videoId, onClose }: Props) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4">
      <div className="relative w-full max-w-4xl aspect-video">
        <iframe
          className="w-full h-full rounded-lg"
          src={`https://www.youtube.com/embed/${videoId}?autoplay=1`}
          title="YouTube player"
          allow="autoplay; encrypted-media"
          allowFullScreen
        />
        <button
          onClick={onClose}
          className="absolute -top-3 -right-3 bg-white text-black p-1 rounded-full shadow"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
