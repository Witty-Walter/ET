import Card from "@/components/Card/Card";
import Link from "next/link";

export default function Home() {
  const engines = [
    { title: "Schedule Risk Engine", path: "/schedule", desc: "AI-driven critical path analysis & LLM mitigation strategies", icon: "⏱️" },
    { title: "Supply Chain Visibilty", path: "/supply-chain", desc: "Live global tracking with proactive delay alerts", icon: "🌍" },
    { title: "RFI Intelligence", path: "/rfi", desc: "RAG-powered historical engineering query resolution", icon: "📚" },
    { title: "Spec Compliance", path: "/compliance", desc: "Docling layout parsing & strict numerical validation", icon: "✅" },
    { title: "Field Inspection (VLM)", path: "/field", desc: "Llava-powered photo verification against P&ID specs", icon: "📸" }
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-12 animate-in fade-in slide-in-from-bottom-8 duration-700">
      
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl p-12 border border-[var(--border-light)] bg-gradient-to-br from-[var(--bg-surface-glass)] to-[var(--bg-base)]">
        <div className="absolute -top-32 -right-32 w-96 h-96 bg-[var(--accent-cyan)] rounded-full mix-blend-screen filter blur-[100px] opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-32 -left-32 w-96 h-96 bg-[var(--accent-violet)] rounded-full mix-blend-screen filter blur-[100px] opacity-20 animate-pulse delay-1000"></div>
        
        <div className="relative z-10 space-y-4 max-w-2xl">
          <h1 className="text-5xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-[var(--text-secondary)]">
            Intelligence Orchestrator
          </h1>
          <p className="text-lg text-[var(--text-secondary)] leading-relaxed">
            Welcome to the Data Centre EPC Project Intelligence Platform. Select an engine to run deep-tech autonomous analysis on construction risks, supply chains, and compliance.
          </p>
        </div>
      </section>

      {/* Engine Grid */}
      <section>
        <h2 className="text-2xl font-semibold mb-6 tracking-wide flex items-center gap-3">
          <span className="w-8 h-1 bg-[var(--accent-cyan)] rounded-full shadow-[var(--glow-cyan)]"></span>
          Core Engines
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {engines.map((engine) => (
            <Link key={engine.title} href={engine.path} className="block group">
              <Card className="h-full group-hover:border-[var(--accent-cyan)] group-hover:-translate-y-1 transition-all duration-300">
                <div className="text-4xl mb-4">{engine.icon}</div>
                <h3 className="text-xl font-bold mb-2 group-hover:text-[var(--accent-cyan)] transition-colors">{engine.title}</h3>
                <p className="text-[var(--text-secondary)] text-sm">{engine.desc}</p>
              </Card>
            </Link>
          ))}
        </div>
      </section>

    </div>
  );
}
