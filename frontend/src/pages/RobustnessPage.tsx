import React, { useState } from 'react';
import {
  Zap,
  ShieldCheck,
  AlertTriangle,
  RefreshCw,
  Sliders,
  CheckCircle2,
  FileCode,
  ArrowRight,
  GitBranch,
  TrendingDown,
  Layers,
  HelpCircle,
  Copy,
  Check
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine
} from 'recharts';
import { RobustnessSummary, PerturbationResult } from '../types';
import { evaluateRobustness } from '../services/api';
import { SAMPLE_CODES } from '../services/sampleSnippets';

export const RobustnessPage: React.FC = () => {
  const [code, setCode] = useState<string>(SAMPLE_CODES.human_lru.code);
  const [language, setLanguage] = useState<string>('python');
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [summary, setSummary] = useState<RobustnessSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedPerturbationKey, setSelectedPerturbationKey] = useState<string>('identifier_renaming');
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  const handleRunStressTest = async () => {
    if (!code || code.trim().length < 5) {
      setError('Please provide at least 5 characters of source code to stress test.');
      return;
    }
    setIsRunning(true);
    setError(null);
    try {
      const res = await evaluateRobustness(code, language);
      setSummary(res);
      const keys = Object.keys(res.perturbations);
      if (keys.length > 0) {
        setSelectedPerturbationKey(keys[0]);
      }
    } catch (err: any) {
      setError(err.message || 'Robustness test execution failed.');
    } finally {
      setIsRunning(false);
    }
  };

  const handleCopyCode = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const chartData = summary
    ? Object.entries(summary.perturbations)
        .filter(([_, p]) => p.supported !== false)
        .map(([key, p]) => ({
          name: p.name.split(' (')[0],
          original_conf: Math.round(summary.original.confidence * 100),
          perturbed_conf: Math.round((p.confidence ?? summary.original.confidence) * 100),
          delta: ((p.confidence_delta ?? 0) * 100).toFixed(1),
          flipped: p.label_flipped ?? false
        }))
    : [];

  const selectedPerturbation: PerturbationResult | undefined = summary?.perturbations[selectedPerturbationKey];

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center space-x-2 text-[11px] font-mono text-cyan-400 mb-1">
            <Zap className="w-4 h-4 text-cyan-400" />
            <span>Adversarial Perturbation & Sensitivity Suite</span>
          </div>
          <h1 className="text-xl font-bold text-orbit-textBright tracking-tight">
            Robustness Laboratory
          </h1>
          <p className="text-xs text-orbit-textDim mt-0.5 max-w-2xl">
            Evaluate whether code authorship attribution remains invariant under semantics-preserving transformations:
            identifier obfuscation, comment stripping, whitespace perturbation, and safe equivalent refactoring.
          </p>
        </div>

        <button
          onClick={handleRunStressTest}
          disabled={isRunning}
          className="flex items-center space-x-1.5 px-4 py-2 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-400/50 font-semibold text-xs shadow-sm transition disabled:opacity-50"
        >
          {isRunning ? (
            <>
              <RefreshCw className="w-3.5 h-3.5 animate-spin text-cyan-400" />
              <span>Perturbing & Evaluating...</span>
            </>
          ) : (
            <>
              <Zap className="w-3.5 h-3.5 text-cyan-400" />
              <span>Run Stress Test Suite</span>
            </>
          )}
        </button>
      </div>

      {/* Editor & Controls */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        <div className="lg:col-span-6 space-y-3">
          <div className="bg-orbit-card border border-orbit-border rounded-lg overflow-hidden flex flex-col h-[460px]">
            <div className="px-4 py-2.5 border-b border-orbit-border bg-orbit-bg flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <FileCode className="w-4 h-4 text-cyan-400" />
                <span className="text-xs font-semibold text-orbit-textBright font-mono">Target Source Code</span>
              </div>
              <div className="flex items-center space-x-2 text-xs font-mono">
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="bg-orbit-card text-orbit-textBright border border-orbit-border rounded px-2 py-1 text-xs focus:outline-none focus:border-cyan-400"
                >
                  <option value="python">Python</option>
                  <option value="javascript">JavaScript</option>
                  <option value="typescript">TypeScript</option>
                  <option value="java">Java</option>
                  <option value="cpp">C++</option>
                </select>
                <button
                  onClick={() => {
                    setCode(SAMPLE_CODES.ai_quicksort.code);
                    setLanguage(SAMPLE_CODES.ai_quicksort.language);
                  }}
                  className="text-cyan-400 hover:text-cyan-300 text-[11px] underline"
                >
                  Load Sample
                </button>
              </div>
            </div>

            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Paste code snippet to stress test..."
              className="w-full flex-1 p-3.5 bg-orbit-bg text-orbit-textBright font-mono text-xs focus:outline-none resize-none leading-relaxed border-none"
              spellCheck={false}
            />

            <div className="px-4 py-2 bg-orbit-bg border-t border-orbit-border text-[11px] font-mono text-orbit-textDim flex justify-between">
              <span>{code.split('\n').length} lines</span>
              <span>{code.length} characters</span>
            </div>
          </div>

          {error && (
            <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* High-Level Robustness Score Card */}
        <div className="lg:col-span-6 space-y-3">
          {summary ? (
            <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-5">
              <div className="flex items-center justify-between border-b border-orbit-border pb-3">
                <div>
                  <span className="text-[10px] font-mono uppercase tracking-wider text-orbit-textDim block">
                    Baseline Prediction
                  </span>
                  <div className="flex items-center space-x-2 mt-0.5">
                    <span
                      className={`text-sm font-bold ${
                        summary.original.predicted_class.includes('Human')
                          ? 'text-emerald-400'
                          : summary.original.predicted_class.includes('AI')
                          ? 'text-rose-400'
                          : 'text-amber-400'
                      }`}
                    >
                      {summary.original.predicted_class}
                    </span>
                    <span className="text-xs font-mono text-orbit-textDim">
                      ({(summary.original.confidence * 100).toFixed(1)}% conf)
                    </span>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-[10px] font-mono uppercase tracking-wider text-orbit-textDim block">
                    Robustness Score
                  </span>
                  <div className="text-2xl font-bold font-mono text-cyan-400">
                    {(summary.overall_robustness_score * 100).toFixed(1)}%
                  </div>
                </div>
              </div>

              {/* 3 Metric Pills */}
              <div className="grid grid-cols-3 gap-2.5">
                <div className="bg-orbit-bg p-2.5 rounded border border-orbit-border">
                  <span className="text-[10px] font-mono text-orbit-textDim block uppercase">Stability Rate</span>
                  <span className="text-sm font-bold font-mono text-emerald-400">
                    {(summary.label_stability_rate * 100).toFixed(0)}%
                  </span>
                </div>

                <div className="bg-orbit-bg p-2.5 rounded border border-orbit-border">
                  <span className="text-[10px] font-mono text-orbit-textDim block uppercase">Mean Drift</span>
                  <span className="text-sm font-bold font-mono text-amber-400">
                    {(summary.mean_confidence_drift * 100).toFixed(2)}%
                  </span>
                </div>

                <div className="bg-orbit-bg p-2.5 rounded border border-orbit-border">
                  <span className="text-[10px] font-mono text-orbit-textDim block uppercase">Variants Tested</span>
                  <span className="text-sm font-bold font-mono text-cyan-400">
                    {Object.keys(summary.perturbations).length}
                  </span>
                </div>
              </div>

              {/* Comparison Chart */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between text-[11px] font-mono text-orbit-textDim">
                  <span>Confidence Sensitivity Across Perturbations</span>
                  <span>Orig vs Transformed</span>
                </div>
                <div className="h-40 w-full bg-orbit-bg p-2 rounded border border-orbit-border">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} margin={{ top: 10, right: 10, left: -25, bottom: 15 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#182030" vertical={false} />
                      <XAxis dataKey="name" stroke="#64748B" tick={{ fontSize: 9, fill: '#94A3B8' }} />
                      <YAxis domain={[0, 100]} stroke="#64748B" tick={{ fontSize: 10, fill: '#94A3B8' }} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#0D111C',
                          borderColor: '#182030',
                          borderRadius: '6px',
                          fontSize: '11px',
                          color: '#F8FAFC'
                        }}
                      />
                      <ReferenceLine y={summary.original.confidence * 100} stroke="#00F2FE" strokeDasharray="3 3" />
                      <Bar dataKey="perturbed_conf" name="Transformed (%)" fill="#06B6D4" radius={[3, 3, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-orbit-card border border-orbit-border rounded-lg p-10 text-center flex flex-col items-center justify-center h-full min-h-[340px]">
              <Zap className="w-10 h-10 text-orbit-textDim mb-3" />
              <h3 className="text-xs font-semibold text-orbit-textBright font-mono uppercase">
                Awaiting Stress Test Run
              </h3>
              <p className="text-xs text-orbit-textDim max-w-xs mt-1">
                Click <strong>"Run Stress Test Suite"</strong> to perturb the snippet and measure confidence stability across 5 transformations.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Detailed Transformation Inspector */}
      {summary && (
        <div className="space-y-4 pt-2">
          <div className="flex items-center justify-between border-b border-orbit-border pb-2">
            <h2 className="text-xs font-bold font-mono uppercase tracking-wider text-orbit-textBright flex items-center space-x-2">
              <Layers className="w-4 h-4 text-cyan-400" />
              <span>Transformation Variants & Behavioral Delta</span>
            </h2>
            <span className="text-[11px] font-mono text-orbit-textDim">
              Select transformation to inspect side-by-side
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2.5">
            {Object.entries(summary.perturbations).map(([key, p]) => {
              const isSelected = selectedPerturbationKey === key;
              const hasFlipped = p.label_flipped;
              const delta = p.confidence_delta ?? 0;
              return (
                <button
                  key={key}
                  onClick={() => setSelectedPerturbationKey(key)}
                  className={`p-3 rounded-lg border text-left transition-all ${
                    isSelected
                      ? 'bg-cyan-950/40 border-cyan-400 text-orbit-textBright shadow-sm'
                      : 'bg-orbit-card border-orbit-border text-orbit-textMuted hover:border-orbit-borderLight'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-semibold truncate block">
                      {p.name.split(' (')[0]}
                    </span>
                    {hasFlipped ? (
                      <span className="text-[9px] px-1 py-0.2 rounded bg-rose-500/20 text-rose-400 font-mono font-bold">
                        Flipped
                      </span>
                    ) : (
                      <span className="text-[9px] px-1 py-0.2 rounded bg-emerald-500/20 text-emerald-400 font-mono">
                        Stable
                      </span>
                    )}
                  </div>
                  <div className="flex items-center justify-between text-xs font-mono">
                    <span className="text-orbit-textDim text-[11px]">
                      {p.confidence !== undefined ? `${(p.confidence * 100).toFixed(1)}%` : 'Unsupported'}
                    </span>
                    {p.supported !== false && (
                      <span className={`text-[11px] ${delta >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                        {delta >= 0 ? `+${(delta * 100).toFixed(1)}%` : `${(delta * 100).toFixed(1)}%`}
                      </span>
                    )}
                  </div>
                </button>
              );
            })}
          </div>

          {selectedPerturbation && (
            <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-orbit-border pb-3">
                <div>
                  <h3 className="text-xs font-bold font-mono text-orbit-textBright flex items-center space-x-2">
                    <span>{selectedPerturbation.name}</span>
                    {selectedPerturbation.resilience && (
                      <span className="text-[10px] px-2 py-0.2 rounded bg-orbit-bg text-cyan-400 font-mono border border-orbit-border">
                        Resilience: {selectedPerturbation.resilience}
                      </span>
                    )}
                  </h3>
                  <p className="text-xs text-orbit-textDim mt-0.5">
                    {selectedPerturbation.description}
                  </p>
                </div>

                {selectedPerturbation.perturbed_code && (
                  <button
                    onClick={() => handleCopyCode(selectedPerturbation.perturbed_code!, selectedPerturbationKey)}
                    className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-orbit-bg hover:bg-orbit-card text-orbit-textBright text-xs font-mono border border-orbit-border self-start"
                  >
                    {copiedKey === selectedPerturbationKey ? (
                      <>
                        <Check className="w-3.5 h-3.5 text-emerald-400" />
                        <span>Copied!</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-3.5 h-3.5" />
                        <span>Copy Transformed Code</span>
                      </>
                    )}
                  </button>
                )}
              </div>

              {selectedPerturbation.supported === false ? (
                <div className="p-3.5 rounded bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs space-y-1">
                  <div className="font-semibold flex items-center space-x-1.5">
                    <AlertTriangle className="w-4 h-4" />
                    <span>Transformation Unsupported / Incompatible</span>
                  </div>
                  <p className="text-orbit-textDim">
                    {selectedPerturbation.error || 'This transformation requires a dedicated AST grammar parser.'}
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <span className="text-[10px] font-mono text-orbit-textDim uppercase">Original Snippet:</span>
                    <pre className="p-3.5 rounded bg-orbit-bg border border-orbit-border text-orbit-textMuted font-mono text-xs overflow-x-auto max-h-64 leading-relaxed">
                      {code}
                    </pre>
                  </div>

                  <div className="space-y-1">
                    <span className="text-[10px] font-mono text-cyan-400 uppercase">Perturbed / Transformed Snippet:</span>
                    <pre className="p-3.5 rounded bg-orbit-bg border border-cyan-500/30 text-orbit-textBright font-mono text-xs overflow-x-auto max-h-64 leading-relaxed">
                      {selectedPerturbation.perturbed_code}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          )}

          <div className="p-3.5 rounded-lg bg-orbit-card border border-orbit-border text-orbit-textDim text-xs leading-relaxed flex items-start space-x-2.5">
            <HelpCircle className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
            <p>
              <strong>Scientific Notice on Robustness:</strong> Invariance under controlled transformations measures semantic robustness, but code refactoring cannot be treated as definitive proof of human intervention or synthetic origin. Real developers routinely apply automated formatting tools (e.g. Black, Prettier) and LLM-assisted renamers during standard software development workflows.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
