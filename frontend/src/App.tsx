import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { TopBar } from './components/TopBar';
import { OverviewPage } from './pages/OverviewPage';
import { AnalysisPage } from './pages/AnalysisPage';
import { CodeDNAPage } from './pages/CodeDNAPage';
import { RobustnessPage } from './pages/RobustnessPage';
import { ModelsPage } from './pages/ModelsPage';
import { DatasetPage } from './pages/DatasetPage';
import { HistoryPage } from './pages/HistoryPage';
import { MethodologyPage } from './pages/MethodologyPage';
import {
  getEvaluationSummary,
  getDatasetSummary,
  getAvailableModels,
  getHealthStatus,
  getAnalysisHistory
} from './services/api';
import { EvaluationSummary, DatasetSummary, ModelInfo, HistoryRecord } from './types';
import { Bell, X, ShieldAlert, Cpu, CheckCircle2, Settings, ExternalLink } from 'lucide-react';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [selectedModelFilter, setSelectedModelFilter] = useState<string>('tritrace');
  const [evaluation, setEvaluation] = useState<EvaluationSummary | null>(null);
  const [dataset, setDataset] = useState<DatasetSummary | null>(null);
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [systemHealth, setSystemHealth] = useState<any>(null);
  const [recentRecords, setRecentRecords] = useState<HistoryRecord[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);

  // Modals
  const [showNotifications, setShowNotifications] = useState<boolean>(false);
  const [showSettings, setShowSettings] = useState<boolean>(false);

  const loadData = async (silent: boolean = false) => {
    if (!silent) setIsLoading(true);
    setIsRefreshing(true);
    try {
      const [evalRes, dataRes, modRes, healthRes, histRes] = await Promise.all([
        getEvaluationSummary().catch(() => null),
        getDatasetSummary().catch(() => null),
        getAvailableModels().catch(() => []),
        getHealthStatus().catch(() => null),
        getAnalysisHistory(10).catch(() => [])
      ]);
      if (evalRes) setEvaluation(evalRes);
      if (dataRes) setDataset(dataRes);
      if (modRes && modRes.length > 0) setModels(modRes);
      if (healthRes) setSystemHealth(healthRes);
      if (histRes) setRecentRecords(histRes);
    } catch (err) {
      console.error('Error fetching global telemetry:', err);
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSelectModelFilter = (modelId: string) => {
    setSelectedModelFilter(modelId);
    setActiveTab('models');
  };

  const getPageMeta = () => {
    switch (activeTab) {
      case 'overview':
        return {
          title: 'Research Overview',
          subtitle: 'AI Code Authorship Intelligence | Live Telemetry & Model Monitoring'
        };
      case 'analysis':
        return {
          title: 'Code Analysis Console',
          subtitle: 'Multi-Signal Syntactic, Stylistic & CodeBERT Contextual Inference'
        };
      case 'codedna':
        return {
          title: 'CodeDNA Engine',
          subtitle: '4-Dimensional Authorship Fingerprinting & Signal Contribution Decomposition'
        };
      case 'robustness':
        return {
          title: 'Robustness Laboratory',
          subtitle: 'Controlled Semantic Perturbation Stress Testing & Adversarial Invariance'
        };
      case 'models':
        return {
          title: 'Model Laboratory',
          subtitle: 'Architecture Checkpoints, Calibration, Loss Curves & Ablation Benchmarks'
        };
      case 'dataset':
        return {
          title: 'Dataset Explorer',
          subtitle: 'Class Distribution, Token Density, Stratification & Dataset Ingestion'
        };
      case 'methodology':
        return {
          title: 'Research Methodology',
          subtitle: 'TriTrace 9-Stage Architecture, Formulation & Theoretical Principles'
        };
      case 'history':
        return {
          title: 'Audit & Analysis History',
          subtitle: 'Verifiable Inference Log, Confidence Records & Exportable Dossiers'
        };
      default:
        return {
          title: 'TriTrace Intelligence',
          subtitle: 'AI-Generated Source Code Detection Platform'
        };
    }
  };

  const handleTopBarAnalyze = () => {
    if (activeTab === 'analysis') {
      window.dispatchEvent(new CustomEvent('tritrace:analyze'));
    } else {
      setActiveTab('analysis');
      setTimeout(() => {
        window.dispatchEvent(new CustomEvent('tritrace:analyze'));
      }, 150);
    }
  };

  const meta = getPageMeta();

  return (
    <div className="min-h-screen bg-orbit-bg text-orbit-textBright font-sans flex antialiased">
      {/* Fixed Left Sidebar ~250px */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        selectedModelFilter={selectedModelFilter}
        onSelectModelFilter={handleSelectModelFilter}
        systemHealth={systemHealth}
        unreadAlertsCount={1}
        onOpenNotifications={() => setShowNotifications(true)}
        onOpenSettings={() => setShowSettings(true)}
      />

      {/* Main Content Area offset by sidebar width */}
      <div className="ml-[250px] flex-1 flex flex-col min-h-screen min-w-0 bg-orbit-bg overflow-x-hidden">
        {/* Top Header Bar */}
        <TopBar
          title={meta.title}
          subtitle={meta.subtitle}
          onRefresh={() => loadData(true)}
          isLoading={isRefreshing}
          onNavigateToAnalysis={handleTopBarAnalyze}
          onOpenNotifications={() => setShowNotifications(true)}
          unreadCount={1}
        />

        {/* Page Content */}
        <main className="flex-1 p-6 max-w-[1600px] w-full mx-auto">
          {activeTab === 'overview' && (
            <OverviewPage
              onNavigate={(tab) => setActiveTab(tab)}
              evaluation={evaluation}
              dataset={dataset}
              models={models}
              recentRecords={recentRecords}
              isLoading={isLoading}
              systemHealth={systemHealth}
            />
          )}

          {activeTab === 'analysis' && (
            <AnalysisPage
              onNavigateToRobustness={() => setActiveTab('robustness')}
            />
          )}

          {activeTab === 'codedna' && (
            <CodeDNAPage />
          )}

          {activeTab === 'robustness' && (
            <RobustnessPage />
          )}

          {activeTab === 'models' && (
            <ModelsPage
              evaluation={evaluation}
              models={models}
              onRefreshData={() => loadData(true)}
            />
          )}

          {activeTab === 'dataset' && (
            <DatasetPage dataset={dataset} />
          )}

          {activeTab === 'methodology' && (
            <MethodologyPage />
          )}

          {activeTab === 'history' && (
            <HistoryPage />
          )}
        </main>
      </div>

      {/* Notifications Drawer Modal */}
      {showNotifications && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-orbit-card border border-orbit-borderLight rounded-lg w-full max-w-md p-5 shadow-2xl space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-orbit-border">
              <div className="flex items-center space-x-2">
                <Bell className="w-4 h-4 text-orbit-cyan" />
                <h3 className="text-sm font-semibold text-orbit-textBright">System Alerts & Notifications</h3>
              </div>
              <button
                onClick={() => setShowNotifications(false)}
                className="text-orbit-textDim hover:text-orbit-textBright p-1"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3">
              <div className="p-3 bg-orbit-sidebar border border-amber-500/30 rounded text-xs space-y-1">
                <div className="flex items-center space-x-2 text-amber-400 font-semibold">
                  <ShieldAlert className="w-3.5 h-3.5" />
                  <span>Uncertainty Threshold Active</span>
                </div>
                <p className="text-orbit-textMuted text-[11px] leading-relaxed">
                  Selective abstention is enabled at 70% confidence. Predictions between 45% and 55% AI probability will trigger an `Uncertain / Human Review Required` advisory.
                </p>
              </div>

              <div className="p-3 bg-orbit-sidebar border border-orbit-border rounded text-xs space-y-1">
                <div className="flex items-center space-x-2 text-orbit-cyan font-semibold">
                  <Cpu className="w-3.5 h-3.5" />
                  <span>PyTorch Runtime Engine</span>
                </div>
                <p className="text-orbit-textMuted text-[11px] leading-relaxed">
                  Execution device: <strong className="text-orbit-textBright">{systemHealth?.device || 'CPU'}</strong>. CodeBERT checkpoint fine-tuned weights loaded with full AST tree-sitter feature extractors.
                </p>
              </div>

              <div className="p-3 bg-orbit-sidebar border border-orbit-border rounded text-xs space-y-1">
                <div className="flex items-center space-x-2 text-emerald-400 font-semibold">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Database History Sync</span>
                </div>
                <p className="text-orbit-textMuted text-[11px] leading-relaxed">
                  SQLite persistence active. Auditable records saved with token-saliency arrays and perturbation invariance indices.
                </p>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => setShowNotifications(false)}
                className="px-3 py-1.5 bg-orbit-sidebar hover:bg-orbit-cardHover border border-orbit-border text-xs rounded text-orbit-textBright font-medium transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Settings Modal */}
      {showSettings && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-orbit-card border border-orbit-borderLight rounded-lg w-full max-w-lg p-6 shadow-2xl space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-orbit-border">
              <div className="flex items-center space-x-2">
                <Settings className="w-4 h-4 text-orbit-cyan" />
                <h3 className="text-sm font-semibold text-orbit-textBright">TriTrace Engine Configuration</h3>
              </div>
              <button
                onClick={() => setShowSettings(false)}
                className="text-orbit-textDim hover:text-orbit-textBright p-1"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-4 text-xs">
              <div className="space-y-1.5">
                <label className="text-orbit-textBright font-medium">Default Classification Threshold</label>
                <p className="text-orbit-textDim text-[11px]">
                  Probability above which code is labeled as AI-generated. Lowering this increases sensitivity to AI patterns.
                </p>
                <input
                  type="text"
                  readOnly
                  value="0.70 (Calibrated with Selective Abstention)"
                  className="w-full bg-orbit-sidebar border border-orbit-border rounded px-3 py-2 text-orbit-textBright text-xs font-mono"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-orbit-textBright font-medium">Feature Fusion Architecture</label>
                <p className="text-orbit-textDim text-[11px]">
                  Multi-signal fusion combining CodeBERT contextual representations, AST depth signals, and stylistic token metrics.
                </p>
                <input
                  type="text"
                  readOnly
                  value="CodeDNA Engine (Semantic 40% + Structural 25% + Stylistic 20% + Reliability 15%)"
                  className="w-full bg-orbit-sidebar border border-orbit-border rounded px-3 py-2 text-orbit-textBright text-xs font-mono"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-orbit-textBright font-medium">Backend REST Endpoint</label>
                <input
                  type="text"
                  readOnly
                  value="http://127.0.0.1:8000/api"
                  className="w-full bg-orbit-sidebar border border-orbit-border rounded px-3 py-2 text-orbit-textBright text-xs font-mono"
                />
              </div>
            </div>

            <div className="pt-2 flex justify-end space-x-2">
              <button
                onClick={() => setShowSettings(false)}
                className="px-4 py-1.5 bg-orbit-cyan text-orbit-bg font-semibold text-xs rounded hover:brightness-110 transition-colors"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
