'use client';
import { useState } from 'react';
import Card from '@/components/Card/Card';
import Button from '@/components/Button/Button';
import StatusBadge from '@/components/StatusBadge/StatusBadge';
import { apiClient } from '@/lib/apiClient';

const defaultTasks = [
  { task_id: "T-001", name: "HVAC Installation", start_date: "2026-08-01", end_date: "2026-08-10", float_days: 0, critical_path: true },
  { task_id: "T-002", name: "Landscaping", start_date: "2026-08-05", end_date: "2026-08-15", float_days: 12, critical_path: false }
];

export default function SchedulePage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [payloadText, setPayloadText] = useState(JSON.stringify({ tasks: defaultTasks }, null, 2));

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const parsedPayload = JSON.parse(payloadText);
      const res = await apiClient.analyzeSchedule(parsedPayload.tasks);
      setResult(res);
    } catch (e: any) {
      alert(e.message || "Invalid JSON Payload");
    }
    setLoading(false);
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-500">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Schedule Risk Engine</h1>
        <p className="text-[var(--text-secondary)]">Analyze CPM networks and generate AI mitigation strategies.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Card */}
        <Card>
          <h2 className="text-xl font-semibold mb-4 text-[var(--accent-cyan)]">Input Payload</h2>
          <textarea
            className="w-full bg-black bg-opacity-50 p-4 rounded-lg text-sm text-[var(--text-secondary)] mb-6 font-mono outline-none border border-[var(--border-light)] focus:border-[var(--accent-cyan)] resize-y min-h-[300px]"
            value={payloadText}
            onChange={(e) => setPayloadText(e.target.value)}
            spellCheck="false"
          />
          <Button onClick={handleAnalyze} disabled={loading} className="w-full">
            {loading ? "Analyzing CPM..." : "Run Risk Analysis"}
          </Button>
        </Card>

        {/* Results Card */}
        <Card className="min-h-[400px] flex flex-col">
          <h2 className="text-xl font-semibold mb-4 text-[var(--accent-cyan)]">Analysis Output</h2>
          
          {!result && !loading && (
            <div className="flex-1 flex items-center justify-center text-[var(--text-secondary)] opacity-50">
              Awaiting payload execution...
            </div>
          )}

          {loading && (
            <div className="flex-1 flex flex-col items-center justify-center gap-4">
              <div className="w-12 h-12 border-4 border-[var(--border-light)] border-t-[var(--accent-cyan)] rounded-full animate-spin"></div>
              <span className="text-[var(--accent-cyan)] animate-pulse">Running Monte Carlo & LLM Evaluation...</span>
            </div>
          )}

          {result && !loading && (
            <div className="space-y-6">
              <div className="flex gap-4">
                <div className="bg-[var(--bg-base)] p-4 rounded-lg flex-1 border border-[var(--border-light)]">
                  <div className="text-sm text-[var(--text-secondary)]">Total Tasks</div>
                  <div className="text-2xl font-bold">{result.total_tasks}</div>
                </div>
                <div className="bg-[var(--bg-base)] p-4 rounded-lg flex-1 border border-[var(--border-light)]">
                  <div className="text-sm text-[var(--text-secondary)]">At Risk</div>
                  <div className="text-2xl font-bold text-[var(--accent-red)]">{result.at_risk_count}</div>
                </div>
              </div>

              <div>
                <h3 className="font-semibold mb-3 border-b border-[var(--border-light)] pb-2">At-Risk Tasks</h3>
                {result.at_risk_tasks.map((task: any) => (
                  <div key={task.task_id} className="bg-[var(--bg-base)] p-4 rounded-lg border border-[var(--accent-red)] border-opacity-30 mb-2">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-mono font-bold">{task.task_id}</span>
                      <StatusBadge status={task.risk_level} />
                    </div>
                    <ul className="text-sm text-[var(--text-secondary)] list-disc pl-5">
                      {task.factors.map((f: string, i: number) => <li key={i}>{f}</li>)}
                    </ul>
                  </div>
                ))}
              </div>

              <div>
                <h3 className="font-semibold mb-3 border-b border-[var(--border-light)] pb-2 text-[var(--accent-violet)]">AI Mitigation Strategies</h3>
                <div className="space-y-4">
                  {result.mitigations.map((plan: any, i: number) => (
                    <div key={i} className="bg-[var(--bg-base)] p-4 rounded-lg border border-[var(--border-light)]">
                      <h4 className="font-bold text-white mb-3 text-sm">Strategies for {plan.task_name} ({plan.task_id})</h4>
                      <ul className="space-y-3">
                        {plan.mitigations.map((m: any, j: number) => (
                          <li key={j} className="bg-black bg-opacity-30 p-3 rounded-md border border-[var(--border-light)] border-opacity-50 text-sm">
                            <span className="text-[var(--text-secondary)] block mb-3">{m.description}</span>
                            <div className="flex justify-between items-center text-xs font-semibold">
                              <span className="text-[var(--accent-cyan)]">Cost Impact: {m.cost_impact}</span>
                              <span className="text-orange-400">Time Saved: {m.estimated_time_saved_days} days</span>
                            </div>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
