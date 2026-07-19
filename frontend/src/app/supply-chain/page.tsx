'use client';
import { useState } from 'react';
import Card from '@/components/Card/Card';
import Button from '@/components/Button/Button';
import StatusBadge from '@/components/StatusBadge/StatusBadge';
import { apiClient } from '@/lib/apiClient';

const defaultShipments = [
  { tracking_number: "AWB-1092837", equipment_type: "HVAC Cooling Towers", origin: "Shenzhen, CN", destination: "Mumbai, IN", status: "Customs Hold", estimated_arrival: "2026-08-15", at_risk: true }
];

export default function SupplyChainPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [payloadText, setPayloadText] = useState(JSON.stringify({ shipments: defaultShipments }, null, 2));

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const parsedPayload = JSON.parse(payloadText);
      const res = await apiClient.analyzeSupplyChain(parsedPayload.shipments);
      setResult(res);
    } catch (e: any) {
      alert(e.message || "Invalid JSON Payload");
    }
    setLoading(false);
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-500">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Supply Chain Visibility</h1>
        <p className="text-[var(--text-secondary)]">Live global tracking and proactive delay alerts.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card>
          <h2 className="text-xl font-semibold mb-4 text-[var(--accent-cyan)]">Incoming Shipments</h2>
          <textarea
            className="w-full bg-black bg-opacity-50 p-4 rounded-lg text-sm text-[var(--text-secondary)] mb-6 font-mono outline-none border border-[var(--border-light)] focus:border-[var(--accent-cyan)] resize-y min-h-[300px]"
            value={payloadText}
            onChange={(e) => setPayloadText(e.target.value)}
            spellCheck="false"
          />
          <Button onClick={handleAnalyze} disabled={loading} className="w-full">
            {loading ? "Polling Logistics API..." : "Check Shipment Status"}
          </Button>
        </Card>

        <Card className="min-h-[400px]">
          <h2 className="text-xl font-semibold mb-4 text-[var(--accent-cyan)]">Alerts Dashboard</h2>
          
          {!result && !loading && (
            <div className="h-64 flex items-center justify-center text-[var(--text-secondary)] opacity-50">
              No active alerts.
            </div>
          )}

          {loading && (
            <div className="h-64 flex flex-col items-center justify-center gap-4">
              <div className="w-12 h-12 border-4 border-[var(--border-light)] border-t-[var(--accent-cyan)] rounded-full animate-spin"></div>
            </div>
          )}

          {result && !loading && (
            <div className="space-y-4">
              {result.alerts.map((alert: any, idx: number) => (
                <div key={idx} className="bg-[var(--bg-base)] p-5 rounded-xl border border-[var(--accent-red)] shadow-[var(--glow-red)] animate-pulse-glow">
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">⚠️</span>
                      <h3 className="font-bold text-white text-lg">{alert.alert_type}</h3>
                    </div>
                    <StatusBadge status={alert.severity} />
                  </div>
                  <p className="text-[var(--text-secondary)] mb-4">{alert.message}</p>
                  
                  <div className="space-y-2">
                    {alert.affected_shipments.map((ship: any) => (
                      <div key={ship.tracking_number} className="bg-black bg-opacity-50 p-3 rounded text-sm flex justify-between items-center border border-[var(--border-light)]">
                        <div>
                          <span className="font-mono text-[var(--accent-cyan)]">{ship.tracking_number}</span>
                          <span className="ml-2 text-white">{ship.equipment_type}</span>
                        </div>
                        <span className="text-orange-400">{ship.status}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
