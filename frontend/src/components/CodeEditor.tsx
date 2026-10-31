import React, { useState } from 'react';
import { Play, RotateCcw, FileCode, CheckCircle, Sliders, Sparkles } from 'lucide-react';
import Editor from '@monaco-editor/react';

interface CodeEditorProps {
  code: string;
  setCode: (code: string) => void;
  language: string;
  setLanguage: (lang: string) => void;
  onAnalyze: () => void;
  onClear: () => void;
  onLoadSample: (key: string) => void;
  isAnalyzing: boolean;
  threshold: number;
  setThreshold: (t: number) => void;
}

export const CodeEditor: React.FC<CodeEditorProps> = ({
  code,
  setCode,
  language,
  setLanguage,
  onAnalyze,
  onClear,
  onLoadSample,
  isAnalyzing,
  threshold,
  setThreshold,
}) => {
  const [useMonaco, setUseMonaco] = useState<boolean>(true);
  const lines = code.split('\n');
  const lineCount = lines.length;
  const nonBlankLines = lines.filter((l) => l.trim().length > 0).length;
  const charCount = code.length;

  const monacoLanguage = language === 'cpp' ? 'cpp' : language;

  return (
    <div className="bg-orbit-card border border-orbit-border rounded-lg overflow-hidden shadow-sm flex flex-col">
      {/* Editor Toolbar */}
      <div className="bg-orbit-bg border-b border-orbit-border px-4 py-2.5 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500/80 inline-block" />
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500/80 inline-block" />
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500/80 inline-block" />
          </div>
          <span className="text-xs font-mono text-cyan-400 font-semibold pl-2 border-l border-orbit-border">
            Monaco Code Inspector
          </span>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-orbit-card border border-orbit-border text-orbit-textBright text-xs rounded px-2.5 py-1 font-mono focus:outline-none focus:border-cyan-400"
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="typescript">TypeScript</option>
            <option value="java">Java</option>
            <option value="cpp">C++</option>
          </select>
        </div>

        {/* Preset Benchmark Samples & Top Analyze Button */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2">
            <span className="text-xs text-orbit-textDim hidden sm:inline">Benchmark Samples:</span>
            <select
              defaultValue=""
              onChange={(e) => {
                if (e.target.value) {
                  onLoadSample(e.target.value);
                  e.target.value = '';
                }
              }}
              className="bg-orbit-card border border-orbit-border text-orbit-textBright text-xs rounded px-2.5 py-1 font-mono hover:border-orbit-borderLight focus:outline-none"
            >
              <option value="" disabled>
                Select benchmark sample...
              </option>
              <option value="human_lru">Human: LRU Cache (cpython)</option>
              <option value="ai_lru">AI: LRU Cache (GPT-4)</option>
              <option value="human_dijkstra">Human: Dijkstra (algorithms-py)</option>
              <option value="ai_dijkstra">AI: Dijkstra (GPT-4)</option>
              <option value="human_bisect">Human: Binary Search (bisect)</option>
              <option value="ai_binary_search">AI: Binary Search (GPT-4)</option>
              <option value="human_js_debounce">Human: Debounce (lodash)</option>
              <option value="ai_js_debounce">AI: Debounce (GPT-4)</option>
            </select>
          </div>

          {/* Top Analyze Code Button */}
          <button
            onClick={onAnalyze}
            disabled={isAnalyzing || code.trim().length < 5}
            title="Execute Code Authorship Analysis"
            className="flex items-center space-x-1.5 px-3 py-1 rounded text-xs font-semibold bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-400/50 shadow-sm disabled:opacity-40 disabled:cursor-not-allowed transition"
          >
            {isAnalyzing ? (
              <>
                <span className="w-3 h-3 border-2 border-cyan-400/30 border-t-cyan-400 rounded-full animate-spin" />
                <span className="hidden sm:inline">Analyzing...</span>
              </>
            ) : (
              <>
                <Play className="w-3 h-3 fill-current text-cyan-400" />
                <span>Analyze Code</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Editor Workspace: Professional Monaco Editor */}
      <div className="relative w-full h-[360px] bg-[#0A0E17]">
        {useMonaco ? (
          <Editor
            height="100%"
            language={monacoLanguage}
            value={code}
            onChange={(value) => setCode(value || '')}
            theme="vs-dark"
            options={{
              minimap: { enabled: false },
              fontSize: 12,
              fontFamily: '"JetBrains Mono", Consolas, monospace',
              lineNumbers: 'on',
              scrollBeyondLastLine: false,
              automaticLayout: true,
              tabSize: 4,
              renderLineHighlight: 'all',
              lineHeight: 20,
              padding: { top: 12, bottom: 12 }
            }}
          />
        ) : (
          <div className="relative flex flex-1 h-full font-mono text-xs bg-orbit-bg">
            <div className="select-none py-3 px-3 text-right bg-orbit-sidebar border-r border-orbit-border text-orbit-textDim font-mono w-12 flex-shrink-0">
              {lines.map((_, i) => (
                <div key={i} className="leading-5">
                  {i + 1}
                </div>
              ))}
            </div>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="# Paste or type source code snippet here..."
              spellCheck={false}
              className="w-full h-full p-3 bg-transparent text-orbit-textBright font-mono leading-5 resize-none focus:outline-none"
            />
          </div>
        )}
      </div>

      {/* Footer / Threshold & Controls */}
      <div className="bg-orbit-bg border-t border-orbit-border px-4 py-3 flex flex-wrap items-center justify-between gap-4">
        {/* Metric Counts */}
        <div className="flex items-center space-x-3 text-xs font-mono text-orbit-textDim">
          <span>{lineCount} lines ({nonBlankLines} active)</span>
          <span>•</span>
          <span>{charCount} chars</span>
          <span>•</span>
          <span className="flex items-center space-x-1.5">
            <Sliders className="w-3.5 h-3.5 text-cyan-400" />
            <span>Abstain (τ):</span>
            <span className="text-cyan-400 font-semibold">{Math.round(threshold * 100)}%</span>
            <input
              type="range"
              min="0.50"
              max="0.95"
              step="0.05"
              value={threshold}
              onChange={(e) => setThreshold(parseFloat(e.target.value))}
              className="w-20 accent-cyan-400 h-1 bg-orbit-border rounded cursor-pointer ml-1"
              title="Predictions below this confidence threshold will trigger abstention"
            />
          </span>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center space-x-2">
          <button
            onClick={onClear}
            disabled={isAnalyzing || !code}
            className="flex items-center space-x-1 px-3 py-1.5 rounded text-xs font-medium text-orbit-textMuted hover:text-orbit-textBright hover:bg-orbit-card disabled:opacity-40 transition"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Clear</span>
          </button>
          <button
            onClick={onAnalyze}
            disabled={isAnalyzing || code.trim().length < 5}
            className="flex items-center space-x-1.5 px-4 py-1.5 rounded-lg text-xs font-semibold bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-400/50 shadow-sm disabled:opacity-50 transition"
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
    </div>
  );
};
