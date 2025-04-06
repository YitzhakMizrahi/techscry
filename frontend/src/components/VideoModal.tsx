'use client';

import { X } from 'lucide-react';
import { useEffect } from 'react';

interface Props {
  videoId: string;
  onClose: () => void;
}

export function VideoModal({ videoId, onClose }: Props) {
  // Close on Escape key
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleKey);
    return () => document.removeEventListener('keydown', handleKey);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm transition-opacity animate-in fade-in-0">
      <div className="relative w-full max-w-4xl aspect-video animate-in zoom-in-95">
        <iframe
          className="w-full h-full rounded shadow-lg"
          src={`https://www.youtube.com/embed/${videoId}?autoplay=1`}
          title="YouTube video player"
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        />
        <button
          onClick={onClose}
          className="absolute -top-4 -right-4 bg-background text-foreground p-1.5 rounded-full shadow-md hover:bg-accent hover:text-accent-foreground transition"
          aria-label="Close video modal"
        >
          <X className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}
