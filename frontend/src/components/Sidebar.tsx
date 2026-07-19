'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Sidebar() {
  const pathname = usePathname();

  const links = [
    { name: 'Dashboard', path: '/' },
    { name: 'Schedule Risk', path: '/schedule' },
    { name: 'Supply Chain', path: '/supply-chain' },
    { name: 'RFI Intelligence', path: '/rfi' },
    { name: 'Spec Compliance', path: '/compliance' },
    { name: 'Field Inspection', path: '/field' },
    { name: 'Document Ingestion', path: '/documents' },
  ];

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 border-r border-[var(--border-light)] bg-[var(--bg-surface-glass)] backdrop-blur-xl z-50 flex flex-col shadow-[var(--shadow-neon)]">
      <div className="p-6 border-b border-[var(--border-light)]">
        <h1 className="text-xl font-bold tracking-wider text-[var(--accent-cyan)] drop-shadow-[var(--glow-cyan)]">
          EPC PLATFORM
        </h1>
        <div className="flex items-center gap-2 mt-2">
          <div className="w-2 h-2 rounded-full bg-[var(--accent-cyan)] shadow-[var(--glow-cyan)] animate-pulse"></div>
          <span className="text-xs text-[var(--text-secondary)] uppercase tracking-widest">System Online</span>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
        {links.map((link) => {
          const isActive = pathname === link.path;
          return (
            <Link
              key={link.name}
              href={link.path}
              className={`block px-4 py-3 rounded-lg transition-all duration-300 relative group overflow-hidden ${
                isActive
                  ? 'bg-[var(--accent-cyan)] bg-opacity-10 text-[var(--accent-cyan)] shadow-[inset_0_0_10px_var(--glow-cyan)] border border-[var(--accent-cyan)] border-opacity-30'
                  : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-surface-glass-hover)] border border-transparent'
              }`}
            >
              {isActive && (
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-[var(--accent-cyan)] shadow-[var(--glow-cyan)]"></div>
              )}
              <span className="relative z-10 font-medium tracking-wide">{link.name}</span>
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-[var(--border-light)] text-xs text-[var(--text-secondary)] text-center opacity-50">
        v2026.1 Build
      </div>
    </aside>
  );
}
