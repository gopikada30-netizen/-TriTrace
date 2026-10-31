import React, { useState } from 'react';
import {
  Dna,
  Cpu,
  Layers,
  Activity,
  Sliders,
  CheckCircle2,
  AlertCircle,
  Copy,
  Check,
  Play,
  RotateCcw,
  Sparkles,
  ShieldCheck,
  Compass,
  FileCode,
  ArrowRight
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell
} from 'recharts';
import { AnalysisResponse, CodeDNAProfile } from '../types';
import { analyzeCode } from '../services/api';
import { SAMPLE_CODES } from '../services/sampleSnippets';

export const CodeDNAPage: React.FC = () => {
  const [code, setCode] = useState<string>(SAMPLE_CODES.human_lru.code);
  const [language, setLanguage] = useState<string>('python');
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [profile, setProfile] = useState<CodeDNAProfile | null>(null);
  const [analysisMeta, setAnalysisMeta] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  const handleGenerate = async () => {
    if (!code || code.trim().length < 5) {
      setError('Please enter at least 5 characters of code.');
      return;
    }
    setIsGenerating(true);
    setError(null);
    try {
      const res = await analyzeCode(code, language, 0.70, 'tritrace');
      setAnalysisMeta(res);
      if (res.codedna) {
        setProfile(res.codedna);
      }
    } catch (e: any) {
      setError(e.message || 'Failed to extract CodeDNA fingerprint.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCopyHash = () => {
    if (profile?.fingerprint_id) {
      navigator.clipboard.writeText(profile.fingerprint_id);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const contributionChartData = profile?.dimension_contributions
    ? [
        { name: 'Semantic DNA', weight: profile.dimension_contributions.semantic, fill: '#00F2FE' },
        { name: 'Structural DNA', weight: profile.dimension_contributions.structural, fill: '#06B6D4' },
        { name: 'Stylistic DNA', weight: profile.dimension_contributions.stylistic, fill: '#F59E0B' },
        { name: 'Reliability DNA', weight: profile.dimension_contributions.reliability, fill: '#10B981' }
      ]
    : [];

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-orbit-card border border-orbit-border rounded-lg p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center space-x-2 text-[11px] font-mono text-cyan-400 mb-1">
            <Dna className="w-4 h-4 text-cyan-400" />
            <span>Core Proposed Novelty | Program Authorship Fingerprinting</span>
          </div>
          <h1 className="text-xl md:text-2xl font-bold text-orbit-textBright tracking-tight">
            CodeDNA™ Multi-Dimensional Authorship Engine
          </h1>
          <p className="text-xs text-orbit-textDim mt-1 max-w-2xl leading-relaxed">
            Deconstructs source code into four orthogonal forensic dimensions: deep contextual CodeBERT sequence semantics,
            hierarchical AST topologies, lexical stylometry, and validation-calibrated uncertainty.
          </p>
        </div>

        {profile && (
          <div className="bg-orbit-bg p-3 px-4 rounded-lg border border-orbit-border flex items-center space-x-3 self-start md:self-auto font-mono">
            <div>
              <span className="text-[10px] uppercase text-orbit-textDim block">Composite Fingerprint</span>
              <span className="text-sm font-bold text-cyan-400">{profile.fingerprint_id}</span>
            </div>
            <button
              onClick={handleCopyHash}
              title="Copy Fingerprint Hash"
              className="p-1.5 rounded bg-orbit-card hover:bg-orbit-cardHover border border-orbit-border text-orbit-textMuted hover:text-cyan-400 transition"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            </button>
          </div>
        )}
      </div>

      {/* Input Code Snippet & Generator Box */}
      <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-orbit-border pb-3">
          <div className="flex items-center space-x-2">
            <FileCode className="w-4 h-4 text-cyan-400" />
            <span className="text-xs font-semibold text-orbit-textBright font-mono">Target Snippet</span>
          </div>

          <div className="flex items-center space-x-3 text-xs font-mono">
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-orbit-bg text-orbit-textMuted border border-orbit-border rounded px-2.5 py-1 text-xs focus:outline-none focus:border-cyan-400"
            >
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
              <option value="typescript">TypeScript</option>
              <option value="java">Java</option>
              <option value="cpp">C++</option>
            </select>

            <button
              onClick={() => {
                setCode(SAMPLE_CODES.ai_lru.code);
                setLanguage(SAMPLE_CODES.ai_lru.language);
              }}
              className="text-cyan-400 hover:text-cyan-300 underline text-[11px]"
            >
              Load AI Sample
            </button>

            <button
              onClick={() => {
                setCode(SAMPLE_CODES.human_lru.code);
                setLanguage(SAMPLE_CODES.human_lru.language);
              }}
              className="text-emerald-400 hover:text-emerald-300 underline text-[11px]"
            >
              Load Human Sample
            </button>
          </div>
        </div>

        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="# Enter source code to compute CodeDNA forensic profile..."
          className="w-full h-44 p-3 bg-orbit-bg text-orbit-textBright font-mono text-xs rounded border border-orbit-border focus:outline-none focus:border-cyan-400 resize-y leading-relaxed"
          spellCheck={false}
        />

        <div className="flex items-center justify-between pt-1">
          <span className="text-[11px] font-mono text-orbit-textDim">
            {code.split('\n').length} lines • {code.length} characters
          </span>

          <button
            onClick={handleGenerate}
            disabled={isGenerating || code.trim().length < 5}
            className="flex items-center space-x-1.5 px-4 py-2 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-400/50 font-semibold text-xs transition shadow-sm disabled:opacity-50"
          >
            {isGenerating ? (
              <>
                <span className="w-3.5 h-3.5 border-2 border-cyan-400/30 border-t-cyan-400 rounded-full animate-spin" />
                <span>Sequencing CodeDNA...</span>
              </>
            ) : (
              <>
                <Dna className="w-3.5 h-3.5" />
                <span>Compute CodeDNA Fingerprint</span>
              </>
            )}
          </button>
        </div>

        {error && (
          <div className="p-3 rounded bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* 4 Dimension Detail Panels */}
      {profile && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* 1. Semantic DNA */}
            <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-3 hover:border-orbit-borderLight transition-all">
              <div className="flex items-center justify-between border-b border-orbit-border pb-2">
                <span className="text-xs font-mono uppercase font-bold text-cyan-400">
                  1. Semantic DNA
                </span>
                <span className="text-xs font-mono font-bold text-orbit-textBright bg-orbit-bg px-2 py-0.5 rounded border border-orbit-border">
                  Score: {profile.semantic_dna.score}
                </span>
              </div>
              <p className="text-xs text-orbit-textMuted leading-relaxed">
                {profile.semantic_dna.summary}
              </p>
              <div className="p-2.5 rounded bg-orbit-bg border border-orbit-border space-y-1 text-[11px] font-mono">
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">Activation Norm:</span>
                  <span className="text-orbit-textBright font-semibold">{profile.semantic_dna.norm ?? 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">Dispersion:</span>
                  <span className="text-orbit-textBright">{profile.semantic_dna.dispersion ?? 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">Variance:</span>
                  <span className="text-orbit-textBright">{profile.semantic_dna.variance ?? 'N/A'}</span>
                </div>
              </div>
              <ul className="text-[11px] text-orbit-textDim space-y-1 list-disc list-inside">
                {profile.semantic_dna.indicators.map((ind, i) => (
                  <li key={i}>{ind}</li>
                ))}
              </ul>
            </div>

            {/* 2. Structural DNA */}
            <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-3 hover:border-orbit-borderLight transition-all">
              <div className="flex items-center justify-between border-b border-orbit-border pb-2">
                <span className="text-xs font-mono uppercase font-bold text-cyan-300">
                  2. Structural DNA
                </span>
                <span className="text-xs font-mono font-bold text-orbit-textBright bg-orbit-bg px-2 py-0.5 rounded border border-orbit-border">
                  Score: {profile.structural_dna.score}
                </span>
              </div>
              <p className="text-xs text-orbit-textMuted leading-relaxed">
                {profile.structural_dna.summary}
              </p>
              <div className="p-2.5 rounded bg-orbit-bg border border-orbit-border space-y-1 text-[11px] font-mono">
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">Max Nesting Depth:</span>
                  <span className="text-orbit-textBright font-semibold">{profile.structural_dna.max_nesting_depth ?? 1}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">Control Flow Nodes:</span>
                  <span className="text-orbit-textBright">{profile.structural_dna.control_flow_nodes ?? 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">Cyclomatic Est.:</span>
                  <span className="text-orbit-textBright">{profile.structural_dna.cyclomatic_estimate ?? 1.0}</span>
                </div>
              </div>
              <ul className="text-[11px] text-orbit-textDim space-y-1 list-disc list-inside">
                {profile.structural_dna.indicators.map((ind, i) => (
                  <li key={i}>{ind}</li>
                ))}
              </ul>
            </div>

            {/* 3. Stylistic DNA */}
            <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-3 hover:border-orbit-borderLight transition-all">
              <div className="flex items-center justify-between border-b border-orbit-border pb-2">
                <span className="text-xs font-mono uppercase font-bold text-amber-400">
                  3. Stylistic DNA
                </span>
                <span className="text-xs font-mono font-bold text-orbit-textBright bg-orbit-bg px-2 py-0.5 rounded border border-orbit-border">
                  Score: {profile.stylistic_dna.score}
                </span>
              </div>
              <p className="text-xs text-orbit-textMuted leading-relaxed">
                {profile.stylistic_dna.summary}
              </p>
              <div className="p-2.5 rounded bg-orbit-bg border border-orbit-border space-y-1 text-[11px] font-mono">
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">Type-Token Ratio:</span>
                  <span className="text-orbit-textBright font-semibold">{profile.stylistic_dna.type_token_ratio ?? 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">ID Entropy:</span>
                  <span className="text-orbit-textBright">{profile.stylistic_dna.identifier_entropy ?? 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">Casing:</span>
                  <span className="text-orbit-textBright uppercase text-[10px]">{profile.stylistic_dna.casing_conformity ?? 'snake_case'}</span>
                </div>
              </div>
              <ul className="text-[11px] text-orbit-textDim space-y-1 list-disc list-inside">
                {profile.stylistic_dna.indicators.map((ind, i) => (
                  <li key={i}>{ind}</li>
                ))}
              </ul>
            </div>

            {/* 4. Reliability DNA */}
            <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-3 hover:border-orbit-borderLight transition-all">
              <div className="flex items-center justify-between border-b border-orbit-border pb-2">
                <span className="text-xs font-mono uppercase font-bold text-emerald-400">
                  4. Reliability DNA
                </span>
                <span className="text-xs font-mono font-bold text-orbit-textBright bg-orbit-bg px-2 py-0.5 rounded border border-orbit-border">
                  Score: {profile.reliability_dna.score}
                </span>
              </div>
              <p className="text-xs text-orbit-textMuted leading-relaxed">
                {profile.reliability_dna.summary}
              </p>
              <div className="p-2.5 rounded bg-orbit-bg border border-orbit-border space-y-1 text-[11px] font-mono">
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">Calibrated Conf:</span>
                  <span className="text-orbit-textBright font-semibold">
                    {profile.reliability_dna.calibrated_confidence ? `${(profile.reliability_dna.calibrated_confidence * 100).toFixed(1)}%` : 'N/A'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">Shannon Entropy:</span>
                  <span className="text-orbit-textBright">{profile.reliability_dna.entropy_bits?.toFixed(3) ?? 'N/A'} bits</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">Abstention:</span>
                  <span className={profile.reliability_dna.abstention_triggered ? 'text-amber-400' : 'text-emerald-400'}>
                    {profile.reliability_dna.abstention_triggered ? 'Triggered (Uncertain)' : 'Passed (Safe)'}
                  </span>
                </div>
              </div>
              <ul className="text-[11px] text-orbit-textDim space-y-1 list-disc list-inside">
                {profile.reliability_dna.indicators.map((ind, i) => (
                  <li key={i}>{ind}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Model Dimension Contributions Breakdown Chart */}
          <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-orbit-border pb-3">
              <div>
                <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-orbit-textBright">
                  Neural Gating Head — Dimension Energy Weights
                </h3>
                <p className="text-[11px] text-orbit-textDim">
                  Calculated dynamically from layer activations and cross-modal gating sigmoid weights
                </p>
              </div>
              <div className="text-xs font-mono text-cyan-400">
                Sum: 100%
              </div>
            </div>

            <div className="h-44 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={contributionChartData} layout="vertical" margin={{ top: 10, right: 30, left: 60, bottom: 10 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#182030" horizontal={false} />
                  <XAxis type="number" domain={[0, 100]} stroke="#64748B" tick={{ fontSize: 10, fill: '#94A3B8' }} />
                  <YAxis type="category" dataKey="name" stroke="#64748B" tick={{ fontSize: 11, fill: '#F8FAFC' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0D111C',
                      borderColor: '#182030',
                      borderRadius: '6px',
                      fontSize: '11px',
                      color: '#F8FAFC'
                    }}
                  />
                  <Bar dataKey="weight" radius={[0, 4, 4, 0]}>
                    {contributionChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
