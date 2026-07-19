'use client';
import { useState } from 'react';
import Card from '@/components/Card/Card';
import Button from '@/components/Button/Button';
import StatusBadge from '@/components/StatusBadge/StatusBadge';
import { apiClient } from '@/lib/apiClient';

export default function CompliancePage() {
  const [eqId, setEqId] = useState("Pump-01");
  const [topic, setTopic] = useState("Fire safety");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleRun = async () => {
    setLoading(true);
    try {
      const res = await apiClient.runCompliance(eqId, topic);
      setResult(res);
    } catch (e: any) {
      alert(e.message);
    }
    setLoading(false);
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-500">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Spec Compliance Engine</h1>
        <p className="text-[var(--text-secondary)]">Baseline vs Submittal validation using Layout Parsing & QuestEval.</p>
      </header>

      <Card className="mb-8">
        <div className="flex gap-4 items-end">
          <div className="flex-1">
            <label className="block text-sm text-[var(--text-secondary)] mb-2">Equipment ID</label>
            <input 
              value={eqId} onChange={e => setEqId(e.target.value)}
              className="w-full bg-[var(--bg-base)] border border-[var(--border-light)] rounded-lg px-4 py-2 text-white"
            />
          </div>
          <div className="flex-1">
            <label className="block text-sm text-[var(--text-secondary)] mb-2">Narrative Topic</label>
            <input 
              value={topic} onChange={e => setTopic(e.target.value)}
              className="w-full bg-[var(--bg-base)] border border-[var(--border-light)] rounded-lg px-4 py-2 text-white"
            />
          </div>
          <Button onClick={handleRun} disabled={loading}>
            {loading ? "Parsing Documents..." : "Run Compliance Check"}
          </Button>
        </div>
      </Card>

      {loading && (
        <div className="h-64 flex flex-col items-center justify-center gap-4">
          <div className="w-12 h-12 border-4 border-[var(--border-light)] border-t-[var(--accent-cyan)] rounded-full animate-spin"></div>
          <span className="text-[var(--accent-cyan)] animate-pulse">Extracting JSON and running Bidirectional QA...</span>
        </div>
      )}

      {result && !loading && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Hard Data */}
          <Card>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold text-[var(--accent-cyan)]">Hard Data Extraction</h2>
              <StatusBadge status={result.spec_deltas.length === 0 ? "PASS" : "CRITICAL"} />
            </div>

            {result.spec_deltas.length === 0 ? (
              <p className="text-emerald-400">No numerical deviations found.</p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-black bg-opacity-50 text-[var(--text-secondary)]">
                    <tr>
                      <th className="p-3 rounded-tl-lg">Parameter</th>
                      <th className="p-3">Baseline</th>
                      <th className="p-3">Submittal</th>
                      <th className="p-3 rounded-tr-lg">Delta</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.spec_deltas.map((delta: any, i: number) => (
                      <tr key={i} className="border-b border-[var(--border-light)] bg-[var(--accent-red)] bg-opacity-10">
                        <td className="p-3 font-mono">{delta.field}</td>
                        <td className="p-3">{JSON.stringify(delta.baseline_value)}</td>
                        <td className="p-3 text-[var(--accent-red)]">{JSON.stringify(delta.submittal_value)}</td>
                        <td className="p-3 font-bold text-[var(--accent-red)]">{JSON.stringify(delta.delta)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </Card>

          {/* Narrative */}
          <Card>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold text-[var(--accent-cyan)]">Narrative Score</h2>
              <div className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[var(--accent-cyan)] to-[var(--accent-violet)]">
                {result.narrative_score.score_pct}%
              </div>
            </div>

            <div className="w-full bg-[var(--bg-base)] rounded-full h-3 mb-6 border border-[var(--border-light)] overflow-hidden">
              <div 
                className={`h-3 rounded-full shadow-[var(--glow-cyan)] ${result.narrative_score.score_pct >= 90 ? 'bg-emerald-500' : 'bg-[var(--accent-red)]'}`} 
                style={{ width: `${result.narrative_score.score_pct}%` }}
              ></div>
            </div>

            <h3 className="text-[var(--text-secondary)] text-sm mb-2 uppercase tracking-widest">AI Judge Reasoning</h3>
            <p className="bg-black bg-opacity-30 p-4 rounded-lg text-sm border border-[var(--border-light)] mb-4">
              {result.narrative_score.reasoning}
            </p>

            <details className="text-sm">
              <summary className="cursor-pointer text-[var(--accent-cyan)] mb-2">View Generated QA Pairs</summary>
              <div className="bg-black bg-opacity-50 p-4 rounded-lg space-y-4">
                {result.narrative_score.questions.map((q: string, idx: number) => (
                  <div key={idx}>
                    <div className="font-bold text-[var(--text-secondary)]">Q: {q}</div>
                    <div className="text-white ml-4">A: {result.narrative_score.answers[idx]}</div>
                  </div>
                ))}
              </div>
            </details>
          </Card>
        </div>
      )}
    </div>
  );
}
