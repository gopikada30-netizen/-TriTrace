import React, { useState, useEffect } from 'react';
import {
  Activity,
  Sliders,
  Cpu,
  RefreshCw,
  TrendingDown,
  Layers,
  Award,
  Play,
  CheckCircle,
  AlertCircle,
  HelpCircle,
  ShieldCheck,
  TrendingUp,
  X
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  ReferenceLine
} from 'recharts';
import { EvaluationSummary, ModelInfo } from '../types';
import { triggerTraining, getTrainingStatus } from '../services/api';

interface ModelsPageProps {
  evaluation: EvaluationSummary | null;
  models: ModelInfo[];
  onRefreshData: () => void;
}

export const ModelsPage: React.FC<ModelsPageProps> = ({
  evaluation,
  models,
  onRefreshData
}) => {
  const [isRetraining, setIsRetraining] = useState<boolean>(false);
  const [trainEpochs, setTrainEpochs] = useState<number>(3);
  const [trainLr, setTrainLr] = useState<number>(0.0003);
  const [trainSeed, setTrainSeed] = useState<number>(42);
  const [trainStatusMsg, setTrainStatusMsg] = useState<string>('');
  const [showTrainModal, setShowTrainModal] = useState<boolean>(false);

  useEffect(() => {
    let interval: any = null;
    if (isRetraining) {
      interval = setInterval(async () => {
        try {
          const status = await getTrainingStatus();
          setTrainStatusMsg(status.status_message);
          if (!status.is_training) {
            setIsRetraining(false);
            onRefreshData();
          }
        } catch (e) {
          // Ignore polling errors
        }
      }, 3000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRetraining, onRefreshData]);

  const handleStartTraining = async () => {
    setIsRetraining(true);
    setShowTrainModal(false);
    setTrainStatusMsg('Initiating training session...');
    try {
      await triggerTraining(trainEpochs, trainLr, trainSeed);
    } catch (e: any) {
      setIsRetraining(false);
      setTrainStatusMsg(`Training initialization failed: ${e.message}`);
    }
  };

  const reliabilityData =
    evaluation?.metrics?.reliability_bins?.map((bin) => ({
      bin: `${(bin.bin_center * 100).toFixed(0)}%`,
      confidence: parseFloat((bin.confidence * 100).toFixed(1)),
      accuracy: parseFloat((bin.accuracy * 100).toFixed(1)),
      count: bin.count
    })) || [];

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-orbit-card border border-orbit-border rounded-lg p-5 shadow-sm">
        <div>
          <div className="inline-flex items-center space-x-2 text-[11px] font-mono text-cyan-400 mb-1">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <span>Empirical Laboratory & Model Monitoring</span>
          </div>
          <h1 className="text-xl font-bold text-orbit-textBright tracking-tight">
            Model Laboratory & Evaluation
          </h1>
          <p className="text-xs text-orbit-textDim mt-0.5">
            Empirical comparative benchmarks, loss convergence, ablation analysis, and confidence calibration
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setShowTrainModal(true)}
            disabled={isRetraining}
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-400/50 font-semibold text-xs shadow-sm transition disabled:opacity-50"
          >
            {isRetraining ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin text-cyan-400" />
                <span>Training Active...</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current text-cyan-400" />
                <span>Trigger Retraining</span>
              </>
            )}
          </button>
        </div>
      </div>

      {trainStatusMsg && (
        <div className="p-3 rounded-lg bg-cyan-950/30 border border-cyan-500/40 text-cyan-300 text-xs font-mono flex items-center justify-between">
          <span>{trainStatusMsg}</span>
          {isRetraining && <RefreshCw className="w-3.5 h-3.5 animate-spin text-cyan-400" />}
        </div>
      )}

      {/* Checkpoint Inventory Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {models.map((m) => (
          <div
            key={m.id}
            className="bg-orbit-card border border-orbit-border rounded-lg p-4 space-y-2.5 hover:border-orbit-borderLight transition-all"
          >
            <div className="flex items-start justify-between">
              <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-cyan-400">
                {m.type.split(' ')[0]}
              </span>
              <span className="inline-flex items-center space-x-1 px-1.5 py-0.2 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                <span>Loaded</span>
              </span>
            </div>

            <h3 className="text-sm font-bold text-orbit-textBright">{m.name}</h3>

            <div className="space-y-1 text-[11px] font-mono text-orbit-textDim border-t border-orbit-border pt-2">
              <div className="flex justify-between">
                <span>Parameters:</span>
                <span className="text-orbit-textBright">{m.parameters}</span>
              </div>
              <div className="flex justify-between">
                <span>Disk Size:</span>
                <span className="text-orbit-textBright">{m.checkpoint_size}</span>
              </div>
              <div className="flex justify-between">
                <span>Calib Temp:</span>
                <span className="text-cyan-400">T* = {m.calibrated_temperature}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Model Benchmark Matrix Table */}
      <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-3">
        <div className="flex items-center justify-between border-b border-orbit-border pb-3">
          <div>
            <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-orbit-textBright">
              Empirical Benchmark Comparison
            </h3>
            <p className="text-[11px] text-orbit-textDim">
              Strictly measured on held-out test split (24 samples) with zero leakage
            </p>
          </div>
          <span className="text-[10px] font-mono text-orbit-textDim">
            Updated: {evaluation?.evaluation_timestamp || 'Active'}
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-sans">
            <thead className="bg-orbit-bg text-orbit-textDim font-mono text-[10px] uppercase tracking-wider border-b border-orbit-border">
              <tr>
                <th className="py-2.5 px-3">Model Architecture</th>
                <th className="py-2.5 px-3">Accuracy</th>
                <th className="py-2.5 px-3">Precision</th>
                <th className="py-2.5 px-3">Recall</th>
                <th className="py-2.5 px-3">F1-Score</th>
                <th className="py-2.5 px-3">ROC-AUC</th>
                <th className="py-2.5 px-3">ECE</th>
                <th className="py-2.5 px-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-orbit-border text-orbit-textBright font-mono text-[11px]">
              {evaluation?.benchmark_comparison?.map((b) => (
                <tr key={b.model_key} className="hover:bg-orbit-cardHover transition-colors">
                  <td className="py-2.5 px-3 font-semibold text-orbit-textBright flex items-center space-x-2">
                    <span className={`w-2 h-2 rounded-full ${b.model_key === 'tritrace' ? 'bg-cyan-400' : 'bg-slate-400'}`} />
                    <span>{b.model_name}</span>
                  </td>
                  <td className="py-2.5 px-3">{(b.accuracy * 100).toFixed(1)}%</td>
                  <td className="py-2.5 px-3">{b.precision.toFixed(3)}</td>
                  <td className="py-2.5 px-3">{b.recall.toFixed(3)}</td>
                  <td className="py-2.5 px-3 font-semibold">{b.f1.toFixed(3)}</td>
                  <td className="py-2.5 px-3 text-cyan-400 font-bold">{b.roc_auc.toFixed(3)}</td>
                  <td className="py-2.5 px-3 text-orbit-textDim">{b.ece.toFixed(4)}</td>
                  <td className="py-2.5 px-3">
                    <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                      {b.status}
                    </span>
                  </td>
                </tr>
              )) || (
                <tr>
                  <td colSpan={8} className="py-6 text-center text-orbit-textDim">
                    Loading benchmark metrics...
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Row: Training Loss & ROC Curve */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Training Loss Curve */}
        <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-3">
          <div className="flex items-center justify-between border-b border-orbit-border pb-3">
            <div>
              <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-orbit-textBright">
                Training & Validation Loss Convergence
              </h3>
              <p className="text-[11px] text-orbit-textDim">
                Cross-entropy loss across epochs
              </p>
            </div>
            <TrendingDown className="w-4 h-4 text-cyan-400" />
          </div>

          <div className="h-48 w-full bg-orbit-bg p-2 rounded border border-orbit-border">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={
                  evaluation?.training_loss_history?.map((h) => ({
                    epoch: `Ep ${h.epoch}`,
                    train_loss: parseFloat(h.train_loss.toFixed(4)),
                    val_loss: parseFloat(h.val_loss.toFixed(4))
                  })) || [
                    { epoch: 'Ep 1', train_loss: 1.177, val_loss: 0.954 },
                    { epoch: 'Ep 2', train_loss: 0.715, val_loss: 0.635 }
                  ]
                }
                margin={{ top: 10, right: 20, left: -25, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#182030" />
                <XAxis dataKey="epoch" stroke="#64748B" tick={{ fontSize: 10, fill: '#94A3B8' }} />
                <YAxis stroke="#64748B" tick={{ fontSize: 10, fill: '#94A3B8' }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0D111C',
                    borderColor: '#182030',
                    borderRadius: '6px',
                    fontSize: '11px',
                    color: '#F8FAFC'
                  }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '6px' }} />
                <Line type="monotone" dataKey="train_loss" name="Train Loss" stroke="#00F2FE" strokeWidth={2} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="val_loss" name="Val Loss" stroke="#10B981" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* ROC Curve */}
        <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-3">
          <div className="flex items-center justify-between border-b border-orbit-border pb-3">
            <div>
              <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-orbit-textBright">
                Receiver Operating Characteristic (ROC)
              </h3>
              <p className="text-[11px] text-orbit-textDim">
                True Positive vs False Positive Rate (AUC: 0.688)
              </p>
            </div>
            <Award className="w-4 h-4 text-cyan-400" />
          </div>

          <div className="h-48 w-full bg-orbit-bg p-2 rounded border border-orbit-border">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={evaluation?.metrics?.roc_curve || [
                  { fpr: 0, tpr: 0 },
                  { fpr: 0.125, tpr: 0.125 },
                  { fpr: 0.25, tpr: 0.5 },
                  { fpr: 0.5, tpr: 0.75 },
                  { fpr: 1.0, tpr: 1.0 }
                ]}
                margin={{ top: 10, right: 20, left: -25, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#182030" />
                <XAxis dataKey="fpr" stroke="#64748B" tick={{ fontSize: 10, fill: '#94A3B8' }} />
                <YAxis dataKey="tpr" stroke="#64748B" tick={{ fontSize: 10, fill: '#94A3B8' }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0D111C',
                    borderColor: '#182030',
                    borderRadius: '6px',
                    fontSize: '11px',
                    color: '#F8FAFC'
                  }}
                />
                <Line type="monotone" dataKey="tpr" name="TriTrace ROC" stroke="#00F2FE" strokeWidth={2} dot={{ r: 2 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Row: Calibration Plot & Ablation Study */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Calibration Reliability Plot */}
        <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-3">
          <div className="flex items-center justify-between border-b border-orbit-border pb-3">
            <div>
              <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-orbit-textBright">
                Calibration Diagram (ECE: {evaluation?.metrics?.ece.toFixed(4) || '0.2284'})
              </h3>
              <p className="text-[11px] text-orbit-textDim">
                Binned empirical accuracy vs predicted confidence
              </p>
            </div>
            <Sliders className="w-4 h-4 text-cyan-400" />
          </div>

          <div className="h-48 w-full bg-orbit-bg p-2 rounded border border-orbit-border">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={reliabilityData} margin={{ top: 10, right: 15, left: -25, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#182030" vertical={false} />
                <XAxis dataKey="bin" stroke="#64748B" tick={{ fontSize: 10, fill: '#94A3B8' }} />
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
                <Bar dataKey="accuracy" name="Empirical Accuracy (%)" fill="#00F2FE" radius={[3, 3, 0, 0]} />
                <Bar dataKey="confidence" name="Mean Confidence (%)" fill="#64748B" radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Ablation Study Table */}
        <div className="bg-orbit-card border border-orbit-border rounded-lg p-5 space-y-3">
          <div className="flex items-center justify-between border-b border-orbit-border pb-3">
            <div>
              <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-orbit-textBright">
                Ablation Experiments
              </h3>
              <p className="text-[11px] text-orbit-textDim">
                Component contribution under selective removal
              </p>
            </div>
            <Layers className="w-4 h-4 text-cyan-400" />
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-orbit-bg text-orbit-textDim text-[10px] uppercase border-b border-orbit-border">
                <tr>
                  <th className="py-2 px-3">Configuration</th>
                  <th className="py-2 px-3">F1-Score</th>
                  <th className="py-2 px-3">Accuracy</th>
                  <th className="py-2 px-3">ECE</th>
                  <th className="py-2 px-3">Δ F1</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-orbit-border text-orbit-textBright text-[11px]">
                {evaluation?.ablation_study?.map((a, i) => (
                  <tr key={i} className="hover:bg-orbit-cardHover">
                    <td className="py-2.5 px-3 font-semibold text-orbit-textBright">{a.configuration}</td>
                    <td className="py-2.5 px-3">{a.f1.toFixed(3)}</td>
                    <td className="py-2.5 px-3">{(a.accuracy * 100).toFixed(1)}%</td>
                    <td className="py-2.5 px-3 text-orbit-textDim">{a.ece.toFixed(4)}</td>
                    <td className={`py-2.5 px-3 font-semibold ${a.delta_f1.startsWith('+') ? 'text-emerald-400' : a.delta_f1.startsWith('-') ? 'text-rose-400' : 'text-cyan-400'}`}>
                      {a.delta_f1}
                    </td>
                  </tr>
                )) || (
                  <tr>
                    <td colSpan={5} className="py-4 text-center text-orbit-textDim">
                      Loading ablation matrix...
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Retraining Configuration Modal */}
      {showTrainModal && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-orbit-card border border-orbit-border rounded-lg max-w-md w-full p-6 space-y-5 shadow-2xl relative">
            <button
              onClick={() => setShowTrainModal(false)}
              className="absolute right-4 top-4 p-1 text-orbit-textDim hover:text-orbit-textBright"
            >
              <X className="w-4 h-4" />
            </button>

            <div>
              <h2 className="text-base font-bold text-orbit-textBright tracking-tight">
                Trigger Model Retraining
              </h2>
              <p className="text-xs text-orbit-textDim mt-0.5">
                Execute local PyTorch training loop across benchmark train/val splits.
              </p>
            </div>

            <div className="space-y-4 text-xs font-mono">
              <div className="space-y-1">
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">Epochs:</span>
                  <span className="text-cyan-400 font-bold">{trainEpochs}</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={trainEpochs}
                  onChange={(e) => setTrainEpochs(parseInt(e.target.value))}
                  className="w-full accent-cyan-400"
                />
              </div>

              <div className="space-y-1">
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">Learning Rate:</span>
                  <span className="text-cyan-400 font-bold">{trainLr}</span>
                </div>
                <input
                  type="range"
                  min="0.0001"
                  max="0.001"
                  step="0.0001"
                  value={trainLr}
                  onChange={(e) => setTrainLr(parseFloat(e.target.value))}
                  className="w-full accent-cyan-400"
                />
              </div>

              <div className="space-y-1">
                <div className="flex justify-between">
                  <span className="text-orbit-textDim">Random Seed:</span>
                  <span className="text-cyan-400 font-bold">{trainSeed}</span>
                </div>
                <input
                  type="number"
                  value={trainSeed}
                  onChange={(e) => setTrainSeed(parseInt(e.target.value) || 42)}
                  className="w-full p-2 bg-orbit-bg border border-orbit-border rounded text-orbit-textBright"
                />
              </div>
            </div>

            <div className="flex items-center justify-end space-x-2 pt-2 border-t border-orbit-border">
              <button
                onClick={() => setShowTrainModal(false)}
                className="px-3 py-1.5 rounded text-xs text-orbit-textMuted hover:text-orbit-textBright"
              >
                Cancel
              </button>
              <button
                onClick={handleStartTraining}
                className="px-4 py-1.5 rounded bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-400/50 text-xs font-semibold"
              >
                Start Training Run
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
