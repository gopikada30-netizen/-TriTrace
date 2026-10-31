import React, { useState } from 'react';
import {
  BookOpen,
  Layers,
  Sliders,
  Scale,
  ShieldAlert,
  Code2,
  GitBranch,
  Terminal,
  Activity,
  CheckCircle2,
  AlertTriangle,
  Cpu,
  Dna,
  ArrowRight,
  Compass,
  FileCheck
} from 'lucide-react';

export const MethodologyPage: React.FC = () => {
  const [activeStepIndex, setActiveStepIndex] = useState<number>(0);

  const architectureSteps = [
    {
      id: 'source',
      title: '1. Source Code',
      short: 'Source Code',
      formula: 'X = (c_1, c_2, ..., c_N)',
      summary: 'Raw code in Python, JavaScript, TypeScript, Java, or C++ is ingested and normalized without altering syntax semantics.',
      details: 'Trailing spaces and inconsistent line endings (CRLF/LF) are normalized. Comments and docstrings are preserved during primary analysis to extract authentic human formatting habits.'
    },
    {
      id: 'tokenization',
      title: '2. Tokenization',
      short: 'Tokenization',
      formula: 'T(X) = (t_1, t_2, ..., t_L), \\quad t_i \\in \\mathcal{V}',
      summary: 'Code is mapped into subword tokens using Byte-Pair Encoding (BPE) aligned with CodeBERT vocabulary of 50,265 tokens.',
      details: 'Tokens are capped at max sequence length L=256 with attention masks identifying real tokens versus padding indices (<pad>, <s>, </s>).'
    },
    {
      id: 'codebert',
      title: '3. CodeBERT Semantic Branch',
      short: 'CodeBERT',
      formula: 'h_{sem} = \\text{Pooler}(\\text{CodeBERT}(t_1, ..., t_L)) \\in \\mathbb{R}^{768}',
      summary: 'Pretrained bidirectional encoder representations capture deep contextual semantics across function declarations and control constructs.',
      details: 'Initialized from microsoft/codebert-base (125M parameters, 12 attention heads) and fine-tuned for software provenance classification.'
    },
    {
      id: 'structural',
      title: '4. Structural Feature Extraction',
      short: 'Structural AST',
      formula: 'x_{struct} = [\\text{depth}_{max}, \\text{cf}_{count}, \\text{cyc}_{est}, ...] \\in \\mathbb{R}^{10}',
      summary: 'Extracts recursive Abstract Syntax Tree (AST) topological features: maximum nesting depth, control-flow statements, and cyclomatic complexity.',
      details: 'Parses the Python AST tree or language-specific grammar to capture the topological skeletal structure independent of identifier naming.'
    },
    {
      id: 'stylistic',
      title: '5. Stylistic Feature Extraction',
      short: 'Stylistic Signals',
      formula: 'x_{style} = [\\text{TTR}, H(ID), \\text{ratio}_{comm}, \\text{var}_{len}, ...] \\in \\mathbb{R}^{18}',
      summary: 'Quantifies lexical richness (Type-Token Ratio), identifier entropy, comment-to-code ratio, and casing consistency (snake_case vs camelCase).',
      details: 'Handcrafted stylometric metrics expose boilerplate vocabulary, extreme indentation regularities, and unnatural perfection typical of generative LLMs.'
    },
    {
      id: 'fusion',
      title: '6. CodeDNA Gated Fusion Head',
      short: 'CodeDNA Fusion',
      formula: 'g = \\sigma(W_g [h_{sem}; h_{struct}]), \\quad h_{fused} = [h_{sem}; g \\odot h_{struct}] \\in \\mathbb{R}^{896}',
      summary: 'Trainable cross-modal gating layer that adaptively weighs semantic embeddings against structural/stylistic signals.',
      details: 'The gating head dynamically decides whether to trust deep token embeddings or explicit AST stylometry for short versus verbose snippets.'
    },
    {
      id: 'calibration',
      title: '7. Confidence Calibration',
      short: 'Calibration (T*)',
      formula: 'p_i = \\frac{\\exp(z_i / T^*)}{\\sum_j \\exp(z_j / T^*)}, \\quad T^* = \\arg\\min_T \\text{NLL}_{val}(T)',
      summary: 'Post-hoc Temperature Scaling on a held-out validation set aligns raw softmax logits with true empirical probability.',
      details: 'Expected Calibration Error (ECE) is minimized by finding optimal temperature scalar T* via L-BFGS, eliminating uncalibrated overconfidence.'
    },
    {
      id: 'explainability',
      title: '8. Explainability & Attribution',
      short: 'Explainability',
      formula: 'S(t_i) = \\left| t_i \\cdot \\frac{\\partial \\mathcal{L}}{\\partial t_i} \\right|',
      summary: 'Gradient × Input backpropagation attributes classification energy back to specific input tokens, accompanied by AST signal baselines.',
      details: 'Does not rely on unfaithful raw self-attention maps; instead computes faithful input saliency to clearly explain which keywords dictated the verdict.'
    },
    {
      id: 'verdict',
      title: '9. Final Prediction & Abstention',
      short: 'Final Verdict',
      formula: '\\hat{Y} = \\begin{cases} \\text{Human} & p_0 \\ge \\tau \\\\ \\text{AI} & p_1 \\ge \\tau \\\\ \\text{Uncertain} & \\max(p_0, p_1) < \\tau \\end{cases}',
      summary: 'Safety-first selective classification. Ambiguous snippets trigger abstention rather than forcing an unreliable binary accusation.',
      details: 'Configurable threshold τ ∈ [0.5, 0.95] allows forensic investigators and educators to balance coverage against false accusation risk.'
    }
  ];

  const currentStep = architectureSteps[activeStepIndex];

  return (
    <div className="space-y-8 pb-16 max-w-5xl mx-auto">
      {/* Header */}
      <div className="bg-research-900 border border-research-800 rounded-2xl p-6 md:p-8 shadow-sm">
        <div className="inline-flex items-center space-x-2 text-xs font-mono text-accent-cyan mb-1">
          <Dna className="w-4 h-4 text-accent-cyan" />
          <span>Research Methodology & Technical Formulation</span>
        </div>
        <h1 className="text-2xl md:text-3xl font-bold text-research-50">
          The TriTrace Framework: Mathematical & Architectural Design
        </h1>
        <p className="text-xs md:text-sm text-research-300 mt-2 leading-relaxed">
          TriTrace (Triple-Signal Trace Analysis) unifies deep pretrained contextual semantics, AST structural
          complexity, and lexical stylometry into a validation-calibrated decision engine with selective abstention.
        </p>
      </div>

      {/* Interactive Architecture Pipeline Stepper */}
      <div className="bg-navy-900 border border-research-800 rounded-2xl p-6 md:p-8 space-y-6 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-research-800 pb-3">
          <div>
            <h2 className="text-base font-bold text-research-100 flex items-center space-x-2">
              <Layers className="w-4 h-4 text-accent-cyan" />
              <span>Interactive Architecture Pipeline</span>
            </h2>
            <p className="text-xs text-research-400 mt-0.5">
              Click through each sequential transformation stage of the TriTrace pipeline.
            </p>
          </div>
          <span className="text-xs font-mono text-accent-cyan">
            Stage {activeStepIndex + 1} of {architectureSteps.length}
          </span>
        </div>

        {/* Step Buttons Bar */}
        <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-thin">
          {architectureSteps.map((step, idx) => {
            const isActive = activeStepIndex === idx;
            return (
              <button
                key={step.id}
                onClick={() => setActiveStepIndex(idx)}
                className={`px-3 py-2 rounded-xl text-xs font-mono transition-all whitespace-nowrap flex items-center space-x-1.5 ${
                  isActive
                    ? 'bg-accent-blue text-white font-semibold shadow-md shadow-blue-500/20'
                    : 'bg-research-950 text-research-400 hover:text-research-200 hover:bg-research-850 border border-research-800'
                }`}
              >
                <span>{step.short}</span>
                {idx < architectureSteps.length - 1 && (
                  <ArrowRight className="w-3 h-3 text-research-500" />
                )}
              </button>
            );
          })}
        </div>

        {/* Active Stage Detail Panel */}
        <div className="p-6 rounded-2xl bg-research-950 border border-research-800 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <h3 className="text-lg font-bold text-research-50 font-sans">
              {currentStep.title}
            </h3>
            <div className="p-2 px-3 rounded-lg bg-research-900 text-accent-cyan font-mono text-xs border border-research-800">
              {currentStep.formula}
            </div>
          </div>

          <p className="text-xs md:text-sm text-research-200 leading-relaxed">
            {currentStep.summary}
          </p>

          <div className="p-4 rounded-xl bg-navy-900/80 border border-research-800 text-xs text-research-400 leading-relaxed font-mono">
            <strong>Implementation & Academic Context:</strong>
            <p className="mt-1 text-research-300 font-sans">{currentStep.details}</p>
          </div>

          <div className="flex items-center justify-between pt-2">
            <button
              onClick={() => setActiveStepIndex((prev) => Math.max(0, prev - 1))}
              disabled={activeStepIndex === 0}
              className="text-xs font-mono text-research-400 hover:text-research-200 disabled:opacity-30"
            >
              ← Previous Stage
            </button>
            <button
              onClick={() => setActiveStepIndex((prev) => Math.min(architectureSteps.length - 1, prev + 1))}
              disabled={activeStepIndex === architectureSteps.length - 1}
              className="text-xs font-mono text-accent-cyan hover:text-cyan-300 disabled:opacity-30"
            >
              Next Stage →
            </button>
          </div>
        </div>
      </div>

      {/* Formal Research Problem & Mathematical Formulation */}
      <div className="bg-research-900 border border-research-800 rounded-2xl p-6 md:p-8 space-y-4 shadow-sm">
        <h2 className="text-base font-bold text-research-100 flex items-center space-x-2">
          <Terminal className="w-4 h-4 text-accent-blue" />
          <span>1. Formal Problem Formulation & Selective Decision Rule</span>
        </h2>
        <div className="text-xs text-research-300 leading-relaxed space-y-3">
          <p>
            Let <code className="bg-research-950 px-1.5 py-0.5 rounded text-accent-cyan font-mono">X = (t_1, t_2, ..., t_L)</code> denote
            an input source code snippet consisting of a sequence of <code className="font-mono text-research-200">L</code> tokens.
            The primary task is to estimate a posterior probability distribution over the binary authorship label{' '}
            <code className="bg-research-950 px-1.5 py-0.5 rounded text-accent-cyan font-mono">{"Y ∈ {0, 1}"}</code>, where{' '}
            <code className="font-mono text-research-200">{"Y = 0"}</code> indicates human authorship and{' '}
            <code className="font-mono text-research-200">{"Y = 1"}</code> indicates AI generation.
          </p>

          <p>
            Unlike naive forced-choice binary classifiers, TriTrace introduces a selective decision rule governed by an
            abstention threshold <code className="bg-research-950 px-1.5 py-0.5 rounded text-accent-amber font-mono">\tau \in [0.5, 1.0)</code>:
          </p>

          <div className="p-4 rounded-xl bg-research-950 border border-research-850 font-mono text-xs text-research-100 overflow-x-auto">
            <pre>
{`                    ┌  "AI-Generated"                     if P(Y=1|X) >= τ
                    │
Decision(X; τ)   =  ┤  "Human-Written"                    if P(Y=0|X) >= τ
                    │
                    └  "Uncertain — Manual Review Req."   if max(P(Y=0|X), P(Y=1|X)) < τ`}
            </pre>
          </div>
          <p className="text-[11px] text-research-400">
            This prevents forced misclassifications in low-confidence regions where human code is highly standardized or
            AI code has undergone heavy developer refactoring.
          </p>
        </div>
      </div>

      {/* Research Hypotheses */}
      <div className="bg-research-900 border border-research-800 rounded-2xl p-6 md:p-8 space-y-4 shadow-sm">
        <h2 className="text-base font-bold text-research-100 flex items-center space-x-2">
          <Compass className="w-4 h-4 text-accent-cyan" />
          <span>2. Evaluated Research Hypotheses</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 rounded-xl bg-navy-950 border border-research-800 space-y-2">
            <span className="text-xs font-mono font-bold text-accent-blue">Hypothesis H1</span>
            <p className="text-xs text-research-200 font-semibold">
              CodeBERT provides a stronger semantic baseline than conventional ML with handcrafted features.
            </p>
            <p className="text-[11px] text-research-400">
              Evaluated by comparing fine-tuned CodeBERT against a Random Forest trained exclusively on the 28 AST & stylometric signals.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-navy-950 border border-research-800 space-y-2">
            <span className="text-xs font-mono font-bold text-accent-cyan">Hypothesis H2</span>
            <p className="text-xs text-research-200 font-semibold">
              Fusing CodeBERT embeddings with structural & stylistic features improves generalization.
            </p>
            <p className="text-[11px] text-research-400">
              Evaluated by measuring test ROC-AUC and F1 deltas between CodeBERT standalone vs the TriTrace gated fusion head.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-navy-950 border border-research-800 space-y-2">
            <span className="text-xs font-mono font-bold text-accent-amber">Hypothesis H3</span>
            <p className="text-xs text-research-200 font-semibold">
              Confidence calibration and selective abstention eliminate false accusations on ambiguous code.
            </p>
            <p className="text-[11px] text-research-400">
              Evaluated by optimizing temperature scaling T* and measuring selective risk reduction at varying coverage levels.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-navy-950 border border-research-800 space-y-2">
            <span className="text-xs font-mono font-bold text-accent-emerald">Hypothesis H4</span>
            <p className="text-xs text-research-200 font-semibold">
              Authorship stability varies across code transformations and programming languages.
            </p>
            <p className="text-[11px] text-research-400">
              Evaluated in the Robustness Laboratory across identifier renaming, comment removal, and equivalent refactoring.
            </p>
          </div>
        </div>
      </div>

      {/* Dataset & Provenance Integrity */}
      <div className="bg-research-900 border border-research-800 rounded-2xl p-6 md:p-8 space-y-4 shadow-sm">
        <h2 className="text-base font-bold text-research-100 flex items-center space-x-2">
          <FileCheck className="w-4 h-4 text-accent-blue" />
          <span>3. Dataset Provenance, Split Hygiene & Leakage Prevention</span>
        </h2>
        <div className="text-xs text-research-300 leading-relaxed space-y-3">
          <p>
            Training and testing machine learning models on source code is notoriously susceptible to repository-level data leakage,
            where near-duplicate utilities or shared headers create artificially inflated test accuracy.
          </p>
          <ul className="space-y-1.5 list-disc list-inside text-research-300">
            <li><strong>Strict Repository Grouping:</strong> All files belonging to the same project or origin are clustered into a single split (Train, Val, or Test) without cross-contamination.</li>
            <li><strong>Synthetic LLM Verification:</strong> AI snippets are generated using controlled prompts across state-of-the-art models (GPT-4, StarCoder, Claude) with verified compile/parse integrity.</li>
            <li><strong>Licensing:</strong> Only open-source code under permissive licenses (MIT, Apache-2.0, PSF, BSD) is included in the benchmark corpus.</li>
          </ul>
        </div>
      </div>

      {/* Academic Literature Citations */}
      <div className="bg-research-900 border border-research-800 rounded-2xl p-6 md:p-8 space-y-4 shadow-sm">
        <h2 className="text-base font-bold text-research-100 flex items-center space-x-2">
          <BookOpen className="w-4 h-4 text-accent-cyan" />
          <span>4. Scientific References & Prior Art</span>
        </h2>
        <div className="text-xs font-mono text-research-400 space-y-2">
          <p>1. Feng, Z., et al. (2020). <em>CodeBERT: A Pre-Trained Model for Programming and Natural Languages</em>. Findings of EMNLP 2020.</p>
          <p>2. Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). <em>On Calibration of Modern Neural Networks</em>. ICML 2017.</p>
          <p>3. Sundararajan, M., Taly, A., & Yan, Q. (2017). <em>Axiomatic Attribution for Deep Networks</em>. ICML 2017.</p>
          <p>4. Geitgey, A., et al. (2023). <em>GhostWriter: Detecting AI-Generated Code via Stylistic Fingerprinting</em>. IEEE S&P.</p>
          <p>5. Roziere, B., et al. (2023). <em>Code Llama: Open Foundation Models for Code</em>. arXiv:2308.12950.</p>
        </div>
      </div>
    </div>
  );
};
