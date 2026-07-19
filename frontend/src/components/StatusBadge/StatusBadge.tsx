export default function StatusBadge({ status, text }: { status: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "PASS", text?: string }) {
  const styles = {
    CRITICAL: "bg-[var(--accent-red)] bg-opacity-20 text-[var(--accent-red)] border-[var(--accent-red)] shadow-[var(--glow-red)] animate-pulse-glow",
    HIGH: "bg-orange-500 bg-opacity-20 text-orange-400 border-orange-500 shadow-[0_0_15px_rgba(249,115,22,0.4)]",
    MEDIUM: "bg-yellow-500 bg-opacity-20 text-yellow-400 border-yellow-500",
    LOW: "bg-blue-500 bg-opacity-20 text-blue-400 border-blue-500",
    PASS: "bg-emerald-500 bg-opacity-20 text-emerald-400 border-emerald-500 shadow-[0_0_15px_rgba(16,185,129,0.3)]",
  };

  return (
    <span className={`px-3 py-1 text-xs font-bold uppercase tracking-wider rounded-full border ${styles[status]}`}>
      {text || status}
    </span>
  );
}
