'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  Settings,
  SendHorizonal,
  FileText,
  EyeOff,
  Clock,
  RefreshCcw,
  Package,
  BrainCircuit,
} from 'lucide-react';

interface UserConfig {
  cooldown_hours: number;
  notification_threshold: number;
  digest_threshold: number;
  max_per_digest: number;
}

interface UserData {
  user_id: string;
  email: string;
  queueLength: number;
  lastNotified?: string;
  config: UserConfig;
}

export function UserAdminPanel() {
  const [users, setUsers] = useState<UserData[]>([]);
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});
  const router = useRouter();

  useEffect(() => {
    setUsers([
      {
        user_id: 'default',
        email: 'yitzhak.tech@gmail.com',
        queueLength: 3,
        lastNotified: '2025-04-03T15:00:00Z',
        config: {
          cooldown_hours: 12,
          notification_threshold: 0.5,
          digest_threshold: 0.3,
          max_per_digest: 5,
        },
      },
    ]);
  }, []);

  const toggleExpanded = (userId: string) => {
    setExpanded((prev) => ({ ...prev, [userId]: !prev[userId] }));
  };

  const formatNextEligible = (last: string, cooldown: number) => {
    const lastDate = new Date(last);
    const next = new Date(lastDate.getTime() + cooldown * 60 * 60 * 1000);
    return next.toLocaleString();
  };

  return (
    <div className="grid gap-4">
      {users.map((user) => (
        <Card key={user.user_id} className="p-4 space-y-2">
          <div className="text-lg font-semibold">{user.email}</div>
          <div className="text-sm text-muted-foreground">
            Queue: {user.queueLength} | Last Digest:{' '}
            {user.lastNotified ?? 'Never'}
          </div>
          <div className="flex gap-2 pt-2 flex-wrap">
            <Button
              onClick={() => router.push(`/user/${user.user_id}`)}
              variant="default"
            >
              <FileText className="w-4 h-4 mr-2" />
              Preview
            </Button>
            <Button variant="outline">
              <EyeOff className="w-4 h-4 mr-2" />
              View Skipped
            </Button>
            <Button
              variant="secondary"
              onClick={() => {
                fetch('/api/send-digest', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ userId: user.user_id }),
                })
                  .then((res) => res.json())
                  .then((data) =>
                    console.log(`✅ Send result for ${user.user_id}:`, data)
                  )
                  .catch((err) => console.error('❌ Send failed:', err));
              }}
            >
              <SendHorizonal className="w-4 h-4 mr-2" />
              Send Now
            </Button>
            <Button
              variant="ghost"
              onClick={() => toggleExpanded(user.user_id)}
            >
              <Settings className="w-4 h-4 mr-2" />
              Settings
            </Button>
          </div>

          {expanded[user.user_id] && (
            <div className="mt-2 text-sm text-muted-foreground space-y-1 pl-1 border-l border-border">
              <div className="flex items-center gap-2">
                <RefreshCcw className="w-4 h-4" />
                Cooldown: {user.config.cooldown_hours}h
              </div>
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4" />
                Next eligible:{' '}
                {user.lastNotified
                  ? formatNextEligible(
                      user.lastNotified,
                      user.config.cooldown_hours
                    )
                  : 'Any time'}
              </div>
              <div className="flex items-center gap-2">
                <BrainCircuit className="w-4 h-4" />
                Thresholds — notif ≥ {user.config.notification_threshold},
                digest ≥ {user.config.digest_threshold}
              </div>
              <div className="flex items-center gap-2">
                <Package className="w-4 h-4" />
                Max items per digest: {user.config.max_per_digest}
              </div>
            </div>
          )}
        </Card>
      ))}
    </div>
  );
}
