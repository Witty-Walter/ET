'use client';
import { useState } from 'react';
import Card from '@/components/Card/Card';
import Button from '@/components/Button/Button';
import { apiClient } from '@/lib/apiClient';

export default function DocumentIngestionPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = e.target.files?.[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      setResult(null);
    }
  };

  const handleIngest = async () => {
    if (!file) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await apiClient.ingestDocument(file);
      setResult(res);
    } catch (err: any) {
      setResult({ error: err.message });
    }
    setLoading(false);
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-500 max-w-4xl mx-auto">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Document Ingestion</h1>
        <p className="text-[var(--text-secondary)]">Upload PDF specifications, datasheets, or manuals to ingest them into the knowledge base for RFI querying.</p>
      </header>

      <Card className="space-y-6">
        <div>
          <label className="block text-sm text-[var(--text-secondary)] mb-2 font-bold uppercase tracking-widest">PDF Document</label>
          <div className="border-2 border-dashed border-[var(--border-light)] rounded-xl p-12 text-center hover:bg-[var(--bg-surface-glass-hover)] transition-colors cursor-pointer relative">
            <input type="file" accept="application/pdf" onChange={handleFileUpload} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
            {file ? (
              <div className="flex flex-col items-center justify-center text-[var(--accent-cyan)]">
                <span className="text-5xl mb-4">📄</span>
                <span className="font-semibold text-lg">{file.name}</span>
                <span className="text-sm text-[var(--text-secondary)] mt-2">{(file.size / 1024 / 1024).toFixed(2)} MB</span>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center">
                <span className="text-4xl mb-4 opacity-50">📤</span>
                <span className="text-[var(--text-secondary)]">Click to upload or drag PDF document here</span>
              </div>
            )}
          </div>
        </div>

        <Button onClick={handleIngest} disabled={loading || !file} className="w-full">
          {loading ? "Parsing & Ingesting Document..." : "Ingest Document"}
        </Button>
      </Card>

      {result && (
        <Card className="animate-in fade-in slide-in-from-bottom-4 duration-300">
          <h2 className="text-xl font-semibold mb-4 text-[var(--accent-cyan)]">Ingestion Result</h2>
          {result.error ? (
            <div className="p-4 rounded-lg bg-[var(--accent-red)] bg-opacity-10 border border-[var(--accent-red)] border-opacity-30 flex items-center gap-3">
              <span className="text-[var(--accent-red)]">❌</span>
              <span className="text-sm">{result.error}</span>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center gap-3 p-4 rounded-lg bg-emerald-500 bg-opacity-10 border border-emerald-500 border-opacity-30">
                <span className="text-emerald-400 text-xl">✅</span>
                <span className="text-sm text-emerald-100">{result.message}</span>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-[var(--bg-base)] p-4 rounded-xl border border-[var(--border-light)]">
                  <span className="block text-xs text-[var(--text-secondary)] uppercase font-bold mb-1">Source File</span>
                  <span className="font-mono text-sm break-all">{result.source}</span>
                </div>
                <div className="bg-[var(--bg-base)] p-4 rounded-xl border border-[var(--border-light)]">
                  <span className="block text-xs text-[var(--text-secondary)] uppercase font-bold mb-1">Chunks Ingested</span>
                  <span className="font-bold text-2xl text-[var(--accent-cyan)]">{result.chunks_ingested}</span>
                </div>
              </div>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}
