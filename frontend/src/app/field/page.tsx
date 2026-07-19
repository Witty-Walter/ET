'use client';
import { useState } from 'react';
import Card from '@/components/Card/Card';
import Button from '@/components/Button/Button';
import StatusBadge from '@/components/StatusBadge/StatusBadge';
import { apiClient } from '@/lib/apiClient';

export default function FieldPage() {
  const [photoFile, setPhotoFile] = useState<File | null>(null);
  const [photoPreview, setPhotoPreview] = useState<string>("");
  const [pidFile, setPidFile] = useState<File | null>(null);
  const [pidPreview, setPidPreview] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handlePhotoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setPhotoFile(file);
      const reader = new FileReader();
      reader.onload = (ev) => {
        setPhotoPreview(ev.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handlePidUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setPidFile(file);
      if (file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')) {
        setPidPreview('PDF_DOCUMENT');
      } else {
        const reader = new FileReader();
        reader.onload = (ev) => {
          setPidPreview(ev.target?.result as string);
        };
        reader.readAsDataURL(file);
      }
    }
  };

  const handleAnalyze = async () => {
    if (!photoFile || !pidFile) return;
    setLoading(true);
    try {
      const res = await apiClient.inspectField(photoFile, pidFile);
      setResult(res);
    } catch (err: any) {
      alert(err.message);
    }
    setLoading(false);
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-500">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Field Inspection (VLM)</h1>
        <p className="text-[var(--text-secondary)]">Upload field photos to instantly verify them against P&ID schematic drawings.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card className="space-y-6">
          <div>
            <label className="block text-sm text-[var(--text-secondary)] mb-2 font-bold uppercase tracking-widest">Field Photo (JPEG/PNG)</label>
            <div className="border-2 border-dashed border-[var(--border-light)] rounded-xl p-8 text-center hover:bg-[var(--bg-surface-glass-hover)] transition-colors cursor-pointer relative">
              <input type="file" accept="image/*" onChange={handlePhotoUpload} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
              {photoPreview ? (
                <img src={photoPreview} alt="Field" className="max-h-48 mx-auto rounded" />
              ) : (
                <span className="text-[var(--text-secondary)]">Click to upload or drag image here</span>
              )}
            </div>
          </div>

          <div>
            <label className="block text-sm text-[var(--text-secondary)] mb-2 font-bold uppercase tracking-widest">P&ID Diagram (PDF/JPEG)</label>
            <div className="border-2 border-dashed border-[var(--border-light)] rounded-xl p-8 text-center hover:bg-[var(--bg-surface-glass-hover)] transition-colors cursor-pointer relative">
              <input type="file" accept="image/*, application/pdf" onChange={handlePidUpload} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
              {pidPreview === 'PDF_DOCUMENT' ? (
                <div className="flex flex-col items-center justify-center text-[var(--accent-cyan)] h-32">
                  <span className="text-5xl mb-2">📄</span>
                  <span className="font-semibold">{pidFile?.name}</span>
                </div>
              ) : pidPreview ? (
                <img src={pidPreview} alt="P&ID" className="max-h-48 mx-auto rounded" />
              ) : (
                <span className="text-[var(--text-secondary)]">Click to upload or drag drawing here (PDF/Image)</span>
              )}
            </div>
          </div>

          <Button onClick={handleAnalyze} disabled={loading || !photoFile || !pidFile} className="w-full">
            {loading ? "Running Llava Vision Model..." : "Analyze Imagery"}
          </Button>

        </Card>

        <Card className="min-h-[400px]">
          <h2 className="text-xl font-semibold mb-6 text-[var(--accent-cyan)]">Inspection Results</h2>
          
          {!result && !loading && (
            <div className="h-64 flex flex-col items-center justify-center text-[var(--text-secondary)] opacity-50 text-center">
              <span className="text-4xl mb-4">📷</span>
              Upload both images and run analysis to see compliance results.
            </div>
          )}

          {loading && (
            <div className="h-64 flex flex-col items-center justify-center gap-4">
              <div className="w-12 h-12 border-4 border-[var(--border-light)] border-t-[var(--accent-cyan)] rounded-full animate-spin"></div>
              <span className="text-[var(--accent-cyan)] animate-pulse text-sm text-center">Transferring images to Llava VLM.<br/>This may take 15-30s...</span>
            </div>
          )}

          {result && !loading && (
            <div className="space-y-6">
              <div className="flex justify-between items-center bg-[var(--bg-base)] p-4 rounded-xl border border-[var(--border-light)]">
                <span className="font-bold text-lg">Overall Compliance</span>
                <StatusBadge status={result.is_compliant ? "PASS" : "CRITICAL"} />
              </div>

              <div>
                <h3 className="font-semibold mb-3 border-b border-[var(--border-light)] pb-2">Identified Discrepancies</h3>
                {result.discrepancies.length === 0 ? (
                  <p className="text-emerald-400">No discrepancies found! Built to spec.</p>
                ) : (
                  <ul className="space-y-3">
                    {result.discrepancies.map((d: string, i: number) => (
                      <li key={i} className="flex gap-3 bg-[var(--accent-red)] bg-opacity-10 p-4 rounded-lg border border-[var(--accent-red)] border-opacity-30">
                        <span className="text-[var(--accent-red)]">❌</span>
                        <span className="text-sm">{d}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              <div className="bg-[var(--accent-violet)] bg-opacity-10 border border-[var(--accent-violet)] p-5 rounded-xl">
                <h3 className="font-bold text-[var(--accent-violet)] mb-2 flex gap-2"><span className="text-xl">🤖</span> Action Required</h3>
                <p className="text-sm text-[var(--text-primary)] leading-relaxed">{result.recommended_action}</p>
                
                {result.procore_sync_status && (
                  <div className="mt-4 pt-4 border-t border-[var(--accent-violet)] border-opacity-30 flex items-center justify-between text-xs">
                    <span className="text-[var(--text-secondary)]">Procore Sync:</span>
                    <span className="bg-[var(--accent-violet)] text-white px-2 py-1 rounded shadow-[var(--glow-violet)]">
                      {result.procore_sync_status}
                    </span>
                  </div>
                )}
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
