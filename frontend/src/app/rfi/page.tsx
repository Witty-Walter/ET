'use client';
import { useState } from 'react';
import Card from '@/components/Card/Card';
import Button from '@/components/Button/Button';
import { apiClient } from '@/lib/apiClient';

export default function RfiPage() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<{role: 'user' | 'ai', content: string, citations?: any[]}[]>([]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userQ = query;
    setQuery("");
    setMessages(prev => [...prev, { role: 'user', content: userQ }]);
    setLoading(true);

    try {
      const res = await apiClient.queryRfi(userQ, "sess_" + Date.now());
      setMessages(prev => [...prev, { role: 'ai', content: res.answer, citations: res.citations }]);
    } catch (err: any) {
      setMessages(prev => [...prev, { role: 'ai', content: `Error: ${err.message}` }]);
    }
    setLoading(false);
  };

  return (
    <div className="h-full flex flex-col animate-in fade-in slide-in-from-bottom-8 duration-500">
      <header className="mb-6 flex-shrink-0">
        <h1 className="text-3xl font-bold mb-2">RFI Intelligence Agent</h1>
        <p className="text-[var(--text-secondary)]">Ask engineering questions against the historical RFI database.</p>
      </header>

      <Card className="flex-1 flex flex-col overflow-hidden p-0">
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-center opacity-50">
              <div className="text-6xl mb-4">📚</div>
              <p className="text-lg">Try asking: "What are the structural requirements for the backup generator pads?"</p>
            </div>
          )}
          
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] p-4 rounded-2xl ${
                msg.role === 'user' 
                  ? 'bg-[var(--accent-cyan)] text-[var(--bg-base)] rounded-br-none' 
                  : 'bg-[var(--bg-base)] border border-[var(--border-light)] text-white rounded-bl-none shadow-[var(--shadow-neon)]'
              }`}>
                <p className="whitespace-pre-wrap">{msg.content}</p>
                
                {msg.citations && msg.citations.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-[var(--border-light)] opacity-80 text-sm">
                    <p className="font-bold mb-2 text-[var(--accent-violet)]">Citations:</p>
                    <div className="flex flex-wrap gap-2">
                      {msg.citations.map((cit, idx) => (
                        <span key={idx} className="bg-black px-2 py-1 rounded text-xs">
                          {cit.source.split(/[\\/]/).pop()}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {loading && (
            <div className="flex justify-start">
              <div className="bg-[var(--bg-base)] border border-[var(--border-light)] p-4 rounded-2xl rounded-bl-none flex gap-2 items-center">
                <div className="w-2 h-2 rounded-full bg-[var(--accent-cyan)] animate-bounce"></div>
                <div className="w-2 h-2 rounded-full bg-[var(--accent-cyan)] animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                <div className="w-2 h-2 rounded-full bg-[var(--accent-cyan)] animate-bounce" style={{ animationDelay: '0.4s' }}></div>
              </div>
            </div>
          )}
        </div>

        <div className="p-4 bg-[var(--bg-base)] border-t border-[var(--border-light)] flex-shrink-0">
          <form onSubmit={handleSend} className="flex gap-4">
            <input 
              type="text" 
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="Ask an engineering question..." 
              className="flex-1 bg-[var(--bg-surface-glass)] border border-[var(--border-light)] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-[var(--accent-cyan)] transition-colors shadow-inner"
              disabled={loading}
            />
            <Button type="submit" disabled={loading || !query.trim()}>Send Query</Button>
          </form>
        </div>
      </Card>
    </div>
  );
}
