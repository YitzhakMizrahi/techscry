// src/app/admin/page.tsx
import { UserAdminPanel } from '@/components/UserAdminPanel';

export default function AdminPage() {
  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-6">🛠 Admin Dashboard</h1>
      <p className="text-sm text-muted-foreground mb-4">
        Welcome to the TechScry admin panel. Here you can view users, review
        their digests, and manage deliveries.
      </p>
      <UserAdminPanel />
    </main>
  );
}
