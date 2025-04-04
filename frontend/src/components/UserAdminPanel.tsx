// src/components/UserAdminPanel.tsx
'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface UserData {
  user_id: string;
  email: string;
  queueLength: number;
  lastNotified?: string;
}

export function UserAdminPanel() {
  const [users, setUsers] = useState<UserData[]>([]);
  const router = useRouter();

  useEffect(() => {
    // Replace with actual API or JSON fetch in the future
    setUsers([
      {
        user_id: 'default',
        email: 'test@gmail.com',
        queueLength: 3,
        lastNotified: '2025-04-03T15:00:00Z',
      },
    ]);
  }, []);

  return (
    <div className="grid gap-4">
      {users.map((user) => (
        <Card key={user.user_id} className="p-4 space-y-2">
          <div className="text-lg font-semibold">{user.email}</div>
          <div className="text-sm text-muted-foreground">
            Queue: {user.queueLength} | Last Digest:{' '}
            {user.lastNotified ?? 'Never'}
          </div>
          <div className="flex gap-2 pt-2">
            <Button
              onClick={() => router.push(`/user/${user.user_id}`)}
              variant="default"
            >
              Preview Digest
            </Button>
            <Button variant="outline">View Skipped</Button>
            <Button variant="secondary">Send Now</Button>
          </div>
        </Card>
      ))}
    </div>
  );
}
