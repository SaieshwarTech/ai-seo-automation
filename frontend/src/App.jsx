import { useMemo, useState } from "react";
import axios from "axios";
import { AlertTriangle, BarChart3, Bot, Download, Link2, ScanSearch } from "lucide-react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

const tabs = [
  { key: "audit", label: "SEO Audit", icon: ScanSearch },
  { key: "bulk", label: "Bulk Analyzer", icon: Link2 },
  { key: "ai", label: "AI Content Lab", icon: Bot }
];

export default function App() {
  const [activeTab, setActiveTab] = useState("audit");
  const [loading, setLoading] = useState(false);
  const [url, setUrl] = useState("");
  const [auditResult, setAuditResult] = useState(null);
  const [error, setError] = useState("");
  const [bulkInput, setBulkInput] = useState("");
  const [bulkResult, setBulkResult] = useState(null);

  const [rewriteInput, setRewriteInput] = useState("");
  const [focusKeyword, setFocusKeyword] = useState("");
  const [rewritten, setRewritten] = useState("");

  const [topic, setTopic] = useState("");
  const [keywords, setKeywords] = useState([]);
  const [blog, setBlog] = useState("");

  const chartData = useMemo(() => {
    if (!auditResult?.audit_breakdown) return [];
    return Object.entries(auditResult.audit_breakdown).map(([name, score]) => ({
      name: name.replaceAll("_", " "),
      score
    }));
  }, [auditResult]);

  const runAudit = async () => {
    if (!url.trim()) return;
    try {
      setError("");
      setLoading(true);
      const { data } = await axios.post(`${API_BASE}/api/analyze`, { url });
      setAuditResult(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to run audit.");
    } finally {
      setLoading(false);
    }
  };

  const runBulk = async () => {
    const urls = bulkInput
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);
    if (!urls.length) return;

    try {
      setError("");
      setLoading(true);
      const { data } = await axios.post(`${API_BASE}/api/bulk-analyze`, { urls });
      setBulkResult(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Bulk analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  const runRewrite = async () => {
    if (!rewriteInput.trim() || !focusKeyword.trim()) return;
    try {
      setLoading(true);
      const { data } = await axios.post(`${API_BASE}/api/rewrite`, {
        content: rewriteInput,
        focus_keyword: focusKeyword,
        tone: "premium and human"
      });
      setRewritten(data.rewritten_content || "");
    } catch {
      setError("Failed to rewrite content.");
    } finally {
      setLoading(false);
    }
  };

  const runKeywordGen = async () => {
    if (!topic.trim()) return;
    try {
      setLoading(true);
      const { data } = await axios.post(`${API_BASE}/api/keywords`, { topic, seed_keywords: [] });
      setKeywords(data.keywords || []);
    } catch {
      setError("Failed to generate keywords.");
    } finally {
      setLoading(false);
    }
  };

  const runBlogGen = async () => {
    if (!topic.trim() || !focusKeyword.trim()) return;
    try {
      setLoading(true);
      const { data } = await axios.post(`${API_BASE}/api/blog`, {
        topic,
        target_keyword: focusKeyword,
        audience: "business owners"
      });
      setBlog(data.blog_content || "");
    } catch {
      setError("Failed to generate blog.");
    } finally {
      setLoading(false);
    }
  };

  const exportPdf = async () => {
    if (!auditResult) return;
    try {
      const response = await axios.post(`${API_BASE}/api/export/pdf`, auditResult, {
        responseType: "blob"
      });
      const blob = new Blob([response.data], { type: "application/pdf" });
      const fileUrl = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = fileUrl;
      link.download = "seo-report.pdf";
      link.click();
      window.URL.revokeObjectURL(fileUrl);
    } catch {
      setError("Failed to export PDF.");
    }
  };

  return (
    <main className="min-h-screen bg-frame font-body text-slate-100">
      <div className="pointer-events-none absolute left-1/2 top-[-120px] h-[420px] w-[420px] -translate-x-1/2 rounded-full bg-accent/20 blur-3xl" />
      <div className="pointer-events-none absolute right-[-130px] top-[30%] h-[380px] w-[380px] rounded-full bg-accentSoft/20 blur-3xl" />

      <div className="relative mx-auto max-w-7xl px-6 py-10">
        <header className="mb-8 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-accent">AI SEO Automation Suite</p>
            <h1 className="font-display text-4xl font-bold text-white">Search Growth Command Center</h1>
            <p className="mt-2 max-w-2xl text-slate-300">
              Analyze websites, discover SEO issues, and generate optimized content with AI.
            </p>
          </div>
          {auditResult && (
            <button
              onClick={exportPdf}
              className="inline-flex items-center gap-2 rounded-xl border border-accent/40 bg-accent/20 px-4 py-2 text-sm font-semibold text-accent hover:bg-accent/30"
            >
              <Download size={16} />
              Export PDF Report
            </button>
          )}
        </header>

        <nav className="mb-8 flex flex-wrap gap-3">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const active = tab.key === activeTab;
            return (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-sm font-semibold transition ${
                  active ? "bg-accent text-slate-900" : "bg-panel text-slate-300 hover:text-white"
                }`}
              >
                <Icon size={16} />
                {tab.label}
              </button>
            );
          })}
        </nav>

        {error && (
          <div className="mb-5 flex items-center gap-2 rounded-xl border border-red-400/30 bg-red-400/10 p-3 text-red-200">
            <AlertTriangle size={16} />
            {error}
          </div>
        )}

        {activeTab === "audit" && (
          <section className="grid gap-6 lg:grid-cols-[1.2fr_1fr]">
            <div className="rounded-2xl border border-white/10 bg-panel/80 p-6 shadow-glow">
              <h2 className="mb-3 font-display text-xl text-white">Single URL Audit</h2>
              <div className="flex gap-3">
                <input
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://example.com"
                  className="w-full rounded-xl border border-white/15 bg-slate-900 px-4 py-3 outline-none ring-accent focus:ring-2"
                />
                <button
                  onClick={runAudit}
                  disabled={loading}
                  className="rounded-xl bg-accent px-5 py-3 font-semibold text-slate-900 disabled:opacity-50"
                >
                  {loading ? "Analyzing..." : "Analyze"}
                </button>
              </div>

              {auditResult && (
                <div className="mt-6 space-y-4">
                  <div className="rounded-xl bg-slate-900 p-4">
                    <p className="text-sm text-slate-300">SEO Score</p>
                    <p className="font-display text-4xl text-accent">{auditResult.seo_score}</p>
                  </div>
                  <div className="rounded-xl bg-slate-900 p-4">
                    <p className="mb-2 text-sm font-semibold text-white">Suggestions</p>
                    <ul className="space-y-2 text-sm text-slate-300">
                      {(auditResult.suggestions || []).map((s, idx) => (
                        <li key={`${s}-${idx}`}>• {s}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>

            <div className="space-y-6">
              <div className="rounded-2xl border border-white/10 bg-panel/80 p-6">
                <h3 className="mb-4 inline-flex items-center gap-2 font-display text-lg">
                  <BarChart3 size={18} className="text-accent" />
                  Audit Analytics
                </h3>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                      <XAxis dataKey="name" stroke="#94a3b8" tick={{ fontSize: 10 }} />
                      <YAxis stroke="#94a3b8" />
                      <Tooltip />
                      <Bar dataKey="score" fill="#00e7b3" radius={[8, 8, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="rounded-2xl border border-white/10 bg-panel/80 p-6">
                <h3 className="mb-3 font-display text-lg">Detected Issues</h3>
                <div className="space-y-2">
                  {(auditResult?.issues || []).slice(0, 6).map((issue, idx) => (
                    <div key={`${issue.issue}-${idx}`} className="rounded-lg bg-slate-900 p-3 text-sm">
                      <p className="font-semibold text-accent">{issue.category}</p>
                      <p className="text-slate-300">{issue.issue}</p>
                      <p className="text-slate-400">Fix: {issue.recommendation}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>
        )}

        {activeTab === "bulk" && (
          <section className="rounded-2xl border border-white/10 bg-panel/80 p-6">
            <h2 className="mb-2 font-display text-xl text-white">Bulk URL Analysis</h2>
            <p className="mb-4 text-sm text-slate-300">Add one URL per line and run concurrent SEO audits.</p>
            <textarea
              value={bulkInput}
              onChange={(e) => setBulkInput(e.target.value)}
              rows={8}
              placeholder={"https://site1.com\nhttps://site2.com"}
              className="w-full rounded-xl border border-white/15 bg-slate-900 px-4 py-3 outline-none ring-accent focus:ring-2"
            />
            <button
              onClick={runBulk}
              disabled={loading}
              className="mt-4 rounded-xl bg-accent px-5 py-2.5 font-semibold text-slate-900 disabled:opacity-50"
            >
              {loading ? "Running..." : "Run Bulk Audit"}
            </button>

            {bulkResult?.results && (
              <div className="mt-6 space-y-3">
                {bulkResult.results.map((item, idx) => (
                  <div key={idx} className="rounded-xl bg-slate-900 p-4 text-sm">
                    {item.status === "success" ? (
                      <p className="text-slate-200">
                        {item.result.url} - Score <span className="font-bold text-accent">{item.result.seo_score}</span>
                      </p>
                    ) : (
                      <p className="text-red-300">
                        {item.url} - Failed: {item.error}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </section>
        )}

        {activeTab === "ai" && (
          <section className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-white/10 bg-panel/80 p-6">
              <h3 className="mb-3 font-display text-lg">AI Rewrite</h3>
              <input
                value={focusKeyword}
                onChange={(e) => setFocusKeyword(e.target.value)}
                placeholder="Focus keyword"
                className="mb-3 w-full rounded-xl border border-white/15 bg-slate-900 px-4 py-3 outline-none ring-accent focus:ring-2"
              />
              <textarea
                value={rewriteInput}
                onChange={(e) => setRewriteInput(e.target.value)}
                rows={7}
                placeholder="Paste content to rewrite..."
                className="w-full rounded-xl border border-white/15 bg-slate-900 px-4 py-3 outline-none ring-accent focus:ring-2"
              />
              <button onClick={runRewrite} className="mt-4 rounded-xl bg-accent px-5 py-2.5 font-semibold text-slate-900">
                Rewrite Content
              </button>
              {rewritten && (
                <div className="mt-4 rounded-xl bg-slate-900 p-4 text-sm text-slate-200 whitespace-pre-wrap">{rewritten}</div>
              )}
            </div>

            <div className="space-y-6">
              <div className="rounded-2xl border border-white/10 bg-panel/80 p-6">
                <h3 className="mb-3 font-display text-lg">Keyword Generator</h3>
                <input
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="Enter topic"
                  className="w-full rounded-xl border border-white/15 bg-slate-900 px-4 py-3 outline-none ring-accent focus:ring-2"
                />
                <button onClick={runKeywordGen} className="mt-4 rounded-xl bg-accent px-5 py-2.5 font-semibold text-slate-900">
                  Generate Keywords
                </button>
                {!!keywords.length && (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {keywords.slice(0, 18).map((k) => (
                      <span key={k} className="rounded-full border border-accent/40 bg-accent/10 px-3 py-1 text-xs text-accent">
                        {k}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <div className="rounded-2xl border border-white/10 bg-panel/80 p-6">
                <h3 className="mb-3 font-display text-lg">AI Blog Generator</h3>
                <button onClick={runBlogGen} className="rounded-xl bg-accent px-5 py-2.5 font-semibold text-slate-900">
                  Generate Blog Post
                </button>
                {blog && <pre className="mt-4 max-h-72 overflow-auto rounded-xl bg-slate-900 p-4 text-sm text-slate-200 whitespace-pre-wrap">{blog}</pre>}
              </div>
            </div>
          </section>
        )}

        <footer className="mt-12 border-t border-white/10 pt-6 text-center text-sm text-slate-400">
          Built by Sai | saieshwar.xyz
        </footer>
      </div>
    </main>
  );
}

