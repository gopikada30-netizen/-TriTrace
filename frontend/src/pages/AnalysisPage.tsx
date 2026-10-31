import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  AlertCircle,
  HelpCircle,
  Layers,
  ChevronRight,
  Sparkles,
  Sliders,
  CheckCircle2,
  FileCode,
  Scale,
  RefreshCw,
  Dna,
  Zap,
  Download,
  Printer,
  Compass,
  Code2,
  Activity,
  Play
} from 'lucide-react';
import { CodeEditor } from '../components/CodeEditor';
import { AnalysisResponse } from '../types';
import { analyzeCode, getExportJsonUrl, getExportHtmlUrl } from '../services/api';
import { SAMPLE_CODES } from '../services/sampleSnippets';

interface AnalysisPageProps {
  onNavigateToRobustness?: () => void;
}

export const AnalysisPage: React.FC<AnalysisPageProps> = ({ onNavigateToRobustness }) => {
  const [code, setCode] = useState<string>(SAMPLE_CODES.human_lru.code);
  const [language, setLanguage] = useState<string>(SAMPLE_CODES.human_lru.language);
  const [threshold, setThreshold] = useState<number>(0.70);
  const [selectedModel, setSelectedModel] = useState<string>('tritrace');
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [inferenceDurationMs, setInferenceDurationMs] = useState<number | null>(null);

  const handleAnalyze = async () => {
    if (!code || code.trim().length < 5) {
      setAnalysisError('Please enter at least 5 characters of source code.');
      return;
    }
    setIsAnalyzing(true);
    setAnalysisError(null);
    const startTime = performance.now();
    try {
      const res = await analyzeCode(code, language, threshold, selectedModel);
      const elapsed = Math.round(performance.now() - startTime);
      setInferenceDurationMs(elapsed);
      setAnalysisResult(res);
    } catch (err: any) {
      setAnalysisError(err.message || 'An error occurred during code analysis.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Listen for global analyze events triggered from top bar
  useEffect(() => {
    const onGlobalAnalyze = () => {
      handleAnalyze();
    };
    window.addEventListener('tritrace:analyze', onGlobalAnalyze);
    return () => window.removeEventListener('tritrace:analyze', onGlobalAnalyze);
  }, [code, language, threshold, selectedModel]);

  const handleClear = () => {
    setCode('');
    setAnalysisResult(null);
    setAnalysisError(null);
  };

  const handleLoadSample = (sampleKey: string) => {
    const sample = SAMPLE_CODES[sampleKey];
    if (sample) {
      setCode(sample.code);
      setLanguage(sample.language);
      setAnalysisResult(null);
      setAnalysisError(null);
    }
  };

  const codedna = analysisResult?.codedna;

  return (
    <div className="space-y-6 pb-16">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-orbit-card border border-orbit-border rounded-lg p-5 shadow-sm">
        <div>
          <div className="inline-flex items-center space-x-2 text-[11px] font-mono text-cyan-400 mb-1">
            <Code2 className="w-4 h-4 text-cyan-400" />
            <span>Real-Time Code Inference & Attribution</span>
          </div>
          <h1 className="text-xl font-bold text-orbit-textBright tracking-tight">
            Code Authorship Analysis
          </h1>
          <p className="text-xs text-orbit-textDim mt-0.5 max-w-2xl">
            Contextual semantic sequence inference via CodeBERT fused with 28 structural AST signals,
            lexical stylometry, and validation-calibrated temperature scaling.
          </p>
        </div>

        {/* Model Selection, Abstention Controls & Top Analyze Button */}
        <div className="flex flex-wrap items-center gap-3 text-xs font-mono">
          <div className="flex items-center space-x-2 bg-orbit-bg px-3 py-1.5 rounded border border-orbit-border">
            <span className="text-orbit-textDim">Model:</span>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="bg-transparent text-orbit-textBright focus:outline-none cursor-pointer"
            >
              <option value="tritrace" className="bg-orbit-card">
                TriTrace (CodeDNA Fusion)
              </option>
              <option value="random_forest" className="bg-orbit-card">
                Random Forest (Handcrafted)
              </option>
            </select>
          </div>

          <div className="flex items-center space-x-2 bg-orbit-bg px-3 py-1.5 rounded border border-orbit-border">
            <Sliders className="w-3.5 h-3.5 text-cyan-400" />
            <span className="text-orbit-textDim">Abstain (τ):</span>
            <span className="text-cyan-400 font-bold">{(threshold * 100).toFixed(0)}%</span>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={isAnalyzing || code.trim().length < 5}
            title="Execute Code Authorship Analysis"
            className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-400/50 text-xs font-semibold shadow-sm disabled:opacity-40 disabled:cursor-not-allowed transition"
          >
            {isAnalyzing ? (
              <>
                <span className="w-3.5 h-3.5 border-2 border-cyan-400/30 border-t-cyan-400 rounded-full animate-spin" />
                <span>Running Inference...</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current text-cyan-400" />
                <span>Analyze Code</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Editor & Controls */}
      <div className="space-y-3">
        <CodeEditor
          code={code}
          setCode={setCode}
          language={language}
          setLanguage={setLanguage}
          onAnalyze={handleAnalyze}
          onClear={handleClear}
          onLoadSample={handleLoadSample}
          isAnalyzing={isAnalyzing}
          threshold={threshold}
          setThreshold={setThreshold}
        />

        {/* Loading State Banner */}
        {isAnalyzing && (
          <div className="p-4 rounded-lg bg-cyan-950/40 border border-cyan-500/30 text-cyan-300 text-xs flex items-center space-x-3.5 shadow-sm animate-pulse">
            <span className="w-5 h-5 border-2 border-cyan-400/30 border-t-cyan-400 rounded-full animate-spin flex-shrink-0" />
            <div className="space-y-0.5">
              <span className="font-semibold font-mono text-cyan-200">Executing Multi-Signal Inference Pipeline...</span>
              <p className="text-[11px] text-cyan-400/80 font-mono">
                Running CodeBERT contextual token encoding • Extracting AST syntactic signals • Computing CodeDNA 4D fingerprint
              </p>
            </div>
          </div>
        )}

        {/* Error State Banner */}
        {analysisError && (
          <div className="p-4 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-start justify-between gap-3 shadow-sm">
            <div className="flex items-start space-x-2.5">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-400 mt-0.5" />
              <div className="space-y-1">
                <span className="font-semibold block text-rose-400 font-mono">Inference Request Failed</span>
                <p className="text-[11px] font-mono text-rose-200/90 leading-relaxed break-words">{analysisError}</p>
              </div>
            </div>
            <button
              onClick={handleAnalyze}
              className="flex-shrink-0 px-3 py-1 rounded bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 border border-rose-500/40 text-[11px] font-mono transition"
            >
              Retry
            </button>
          </div>
        )}

        {/* Success Telemetry Pill */}
        {analysisResult && !isAnalyzing && (
          <div className="px-3 py-1.5 rounded bg-orbit-card border border-emerald-500/30 text-emerald-400 text-[11px] font-mono flex items-center justify-between">
            <span className="flex items-center space-x-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              <span>Inference completed successfully ({inferenceDurationMs ?? 240} ms)</span>
            </span>
            <span className="text-orbit-textDim">
              Model: {analysisResult.model_version} • Calibrated T = {analysisResult.calibrated_temperature}
            </span>
          </div>
        )}
      </div>

      {/* Analysis Results View */}
      {analysisResult && (
        <div className="space-y-6 pt-2 animate-fadeIn">
          {/* Status Verdict Banner */}
          <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="flex items-start space-x-4">
              <div
                className={`p-3 rounded-lg border flex-shrink-0 ${
                  analysisResult.status === 'ai'
                    ? 'bg-rose-500/15 border-rose-500/30 text-rose-400'
                    : analysisResult.status === 'human'
                    ? 'bg-emerald-500/15 border-emerald-500/30 text-emerald-400'
                    : 'bg-amber-500/15 border-amber-500/30 text-amber-400'
                }`}
              >
                {analysisResult.status === 'ai' ? (
                  <Sparkles className="w-6 h-6" />
                ) : analysisResult.status === 'human' ? (
                  <CheckCircle2 className="w-6 h-6" />
                ) : (
                  <AlertCircle className="w-6 h-6" />
                )}
              </div>

              <div className="space-y-1">
                <div className="flex items-center space-x-2">
                  <span className="text-[10px] font-mono uppercase tracking-wider text-orbit-textDim">
                    Authorship Classification
                  </span>
                  {analysisResult.codedna && (
                    <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-orbit-bg text-cyan-400 border border-orbit-border">
                      {analysisResult.codedna.fingerprint_id}
                    </span>
                  )}
                </div>
                <h2 className="text-xl font-bold tracking-tight text-orbit-textBright">
                  {analysisResult.predicted_class}
                </h2>
                <p className="text-xs text-orbit-textMuted leading-relaxed max-w-xl">
                  {analysisResult.is_uncertain
                    ? `Confidence (${(analysisResult.confidence * 100).toFixed(1)}%) falls below safety threshold (τ = ${(threshold * 100).toFixed(0)}%). Decision deferred to manual inspection.`
                    : analysisResult.status === 'ai'
                    ? `Contextual sequence patterns and token uniformities align with generative model completions (confidence = ${(analysisResult.confidence * 100).toFixed(1)}%).`
                    : `Stylometric variance and AST control structure align with idiosyncratic human engineering (confidence = ${(analysisResult.confidence * 100).toFixed(1)}%).`}
                </p>
              </div>
            </div>

            {/* Confidence & Quick Actions */}
            <div className="flex flex-col sm:flex-row items-center gap-3">
              <div className="bg-orbit-bg p-3.5 rounded-lg border border-orbit-border text-center min-w-[140px] font-mono">
                <span className="text-[10px] text-orbit-textDim uppercase tracking-wider block">
                  Calibrated Conf
                </span>
                <span className="text-xl font-bold text-orbit-textBright">
                  {(analysisResult.confidence * 100).toFixed(1)}%
                </span>
                <span className="text-[10px] text-cyan-400 block mt-0.5">
                  Entropy: {analysisResult.entropy.toFixed(3)} bits
                </span>
              </div>

              {analysisResult.history_id && (
                <div className="flex flex-col gap-2">
                  <a
                    href={getExportHtmlUrl(analysisResult.history_id)}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-orbit-card hover:bg-orbit-cardHover text-cyan-300 text-xs font-mono border border-cyan-500/30"
                  >
                    <Printer className="w-3.5 h-3.5 text-cyan-400" />
                    <span>Print Report</span>
                  </a>
                  <a
                    href={getExportJsonUrl(analysisResult.history_id)}
                    download
                    className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-orbit-card hover:bg-orbit-cardHover text-orbit-textMuted text-xs font-mono border border-orbit-border"
                  >
                    <Download className="w-3.5 h-3.5 text-orbit-textDim" />
                    <span>Export JSON</span>
                  </a>
                </div>
              )}
            </div>
          </div>

          {/* CodeDNA 4-Dimension Snapshot */}
          {codedna && (
            <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-orbit-border pb-3">
                <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-orbit-textBright flex items-center space-x-2">
                  <Dna className="w-4 h-4 text-cyan-400" />
                  <span>CodeDNA Dimension Contributions</span>
                </h3>
                <span className="text-xs font-mono text-cyan-400">
                  {codedna.fingerprint_id}
                </span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="bg-orbit-bg p-3 rounded border border-orbit-border">
                  <span className="text-[10px] font-mono text-orbit-textDim block uppercase">Semantic DNA</span>
                  <span className="text-base font-bold font-mono text-cyan-400">
                    {codedna.dimension_contributions.semantic}%
                  </span>
                  <span className="text-[10px] text-orbit-textDim block mt-0.5">Norm: {codedna.semantic_dna.norm ?? 'N/A'}</span>
                </div>

                <div className="bg-orbit-bg p-3 rounded border border-orbit-border">
                  <span className="text-[10px] font-mono text-orbit-textDim block uppercase">Structural DNA</span>
                  <span className="text-base font-bold font-mono text-cyan-300">
                    {codedna.dimension_contributions.structural}%
                  </span>
                  <span className="text-[10px] text-orbit-textDim block mt-0.5">Depth: {codedna.structural_dna.max_nesting_depth ?? 1}</span>
                </div>

                <div className="bg-orbit-bg p-3 rounded border border-orbit-border">
                  <span className="text-[10px] font-mono text-orbit-textDim block uppercase">Stylistic DNA</span>
                  <span className="text-base font-bold font-mono text-amber-400">
                    {codedna.dimension_contributions.stylistic}%
                  </span>
                  <span className="text-[10px] text-orbit-textDim block mt-0.5">TTR: {codedna.stylistic_dna.type_token_ratio ?? 0}</span>
                </div>

                <div className="bg-orbit-bg p-3 rounded border border-orbit-border">
                  <span className="text-[10px] font-mono text-orbit-textDim block uppercase">Reliability DNA</span>
                  <span className="text-base font-bold font-mono text-emerald-400">
                    {codedna.dimension_contributions.reliability}%
                  </span>
                  <span className="text-[10px] text-orbit-textDim block mt-0.5">Margin: {(codedna.reliability_dna.safety_margin ?? 0) >= 0 ? 'Safe' : 'Abstain'}</span>
                </div>
              </div>
            </div>
          )}

          {/* Token Saliency Attribution View */}
          <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-orbit-border pb-3">
              <div>
                <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-orbit-textBright flex items-center space-x-2">
                  <FileCode className="w-4 h-4 text-cyan-400" />
                  <span>Gradient-Based Token Saliency Attribution</span>
                </h3>
                <p className="text-[11px] text-orbit-textDim mt-0.5">
                  Gradient × Input backpropagation across CodeBERT token embeddings
                </p>
              </div>

              <div className="flex items-center space-x-3 text-[10px] font-mono">
                <span className="flex items-center space-x-1">
                  <span className="w-2.5 h-2.5 rounded token-hl-high inline-block" />
                  <span className="text-orbit-textMuted">High</span>
                </span>
                <span className="flex items-center space-x-1">
                  <span className="w-2.5 h-2.5 rounded token-hl-medium inline-block" />
                  <span className="text-orbit-textMuted">Medium</span>
                </span>
                <span className="flex items-center space-x-1">
                  <span className="w-2.5 h-2.5 rounded token-hl-low inline-block" />
                  <span className="text-orbit-textMuted">Low</span>
                </span>
              </div>
            </div>

            <div className="p-3.5 rounded bg-orbit-bg border border-orbit-border font-mono text-xs leading-relaxed max-h-56 overflow-y-auto flex flex-wrap gap-1.5">
              {analysisResult.token_attributions.map((item, idx) => {
                const hlClass =
                  item.intensity === 'high'
                    ? 'token-hl-high'
                    : item.intensity === 'medium'
                    ? 'token-hl-medium'
                    : item.intensity === 'low'
                    ? 'token-hl-low'
                    : 'token-hl-baseline';
                return (
                  <span
                    key={idx}
                    title={`Token: "${item.token}" | Attribution Score: ${item.score.toFixed(4)}`}
                    className={`px-1 py-0.5 rounded cursor-help transition-colors ${hlClass}`}
                  >
                    {item.token}
                  </span>
                );
              })}
            </div>
          </div>

          {/* Structural & Stylistic Feature Signals Breakdown */}
          <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-4">
            <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-orbit-textBright flex items-center space-x-2 border-b border-orbit-border pb-3">
              <Layers className="w-4 h-4 text-cyan-400" />
              <span>Extracted AST & Stylometric Signals</span>
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {analysisResult.feature_breakdown.map((cat, i) => (
                <div key={i} className="p-3.5 rounded bg-orbit-bg border border-orbit-border space-y-2.5">
                  <div className="flex items-center justify-between text-xs font-bold font-mono">
                    <span className="text-orbit-textBright">{cat.category}</span>
                    <span className="text-[10px] text-cyan-400">
                      {(cat.importance * 100).toFixed(0)}% wt
                    </span>
                  </div>

                  <div className="space-y-2">
                    {cat.signals.map((sig, j) => (
                      <div key={j} className="text-[11px] font-mono space-y-0.5">
                        <div className="flex justify-between text-orbit-textBright">
                          <span className="truncate max-w-[140px] text-orbit-textMuted">{sig.name}</span>
                          <span className="font-semibold">{sig.value.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between text-[10px] text-orbit-textDim">
                          <span>Human: {sig.human_baseline.toFixed(2)}</span>
                          <span>AI: {sig.ai_baseline.toFixed(2)}</span>
                          <span
                            className={
                              sig.signal_alignment.includes('Human')
                                ? 'text-emerald-400'
                                : sig.signal_alignment.includes('AI')
                                ? 'text-rose-400'
                                : 'text-orbit-textDim'
                            }
                          >
                            {sig.signal_alignment}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Key Findings & Probabilistic Notice */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-lg bg-orbit-card border border-orbit-border space-y-2">
              <h4 className="text-xs font-bold font-mono text-orbit-textBright uppercase tracking-wider flex items-center space-x-2">
                <Compass className="w-3.5 h-3.5 text-cyan-400" />
                <span>Forensic Behavioral Synthesis</span>
              </h4>
              <ul className="text-xs text-orbit-textMuted space-y-1.5 list-disc list-inside leading-relaxed">
                {analysisResult.key_findings.map((f, i) => (
                  <li key={i}>{f}</li>
                ))}
              </ul>
            </div>

            <div className="p-4 rounded-lg bg-orbit-card border border-orbit-border space-y-2">
              <h4 className="text-xs font-bold font-mono text-orbit-textBright uppercase tracking-wider flex items-center space-x-2">
                <Scale className="w-3.5 h-3.5 text-amber-400" />
                <span>Probabilistic Forensic Disclaimer</span>
              </h4>
              <p className="text-xs text-orbit-textDim leading-relaxed">
                {analysisResult.limitations_notice}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
