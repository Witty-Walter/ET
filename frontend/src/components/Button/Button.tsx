export default function Button({ 
  children, 
  onClick, 
  variant = "primary",
  type = "button",
  disabled = false,
  className = "" 
}: { 
  children: React.ReactNode, 
  onClick?: () => void,
  variant?: "primary" | "secondary" | "danger",
  type?: "button" | "submit" | "reset",
  disabled?: boolean,
  className?: string
}) {
  const baseStyle = "px-6 py-2 rounded-lg font-medium tracking-wide transition-all duration-300 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed";
  
  const variants = {
    primary: "bg-[var(--accent-cyan)] text-[var(--bg-base)] shadow-[var(--glow-cyan)] hover:shadow-[var(--glow-cyan-strong)] hover:bg-opacity-90",
    secondary: "bg-transparent text-[var(--text-primary)] border border-[var(--border-light)] hover:bg-[var(--bg-surface-glass-hover)]",
    danger: "bg-[var(--accent-red)] text-white shadow-[var(--glow-red)] hover:bg-opacity-90"
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyle} ${variants[variant]} ${className}`}
    >
      {children}
    </button>
  );
}
