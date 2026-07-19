export default function Card({ children, className = "" }: { children: React.ReactNode, className?: string }) {
  return (
    <div className={`bg-[var(--bg-surface-glass)] backdrop-blur-xl border border-[var(--border-light)] rounded-2xl p-6 shadow-lg hover:shadow-[var(--shadow-neon)] transition-shadow duration-300 ${className}`}>
      {children}
    </div>
  );
}
