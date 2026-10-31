import React from 'react';
import {
  LayoutDashboard,
  Code2,
  Dna,
  Zap,
  Cpu,
  Database,
  BookOpen,
  History,
  Settings,
  FileText,
  Bell,
  Activity,
  Terminal,
  ShieldCheck,
  CheckCircle2,
  Flame,
  Radio
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  selectedModelFilter?: string;
  onSelectModelFilter?: (modelId: string) => void;
  systemHealth: {
    status?: string;
    device?: string;
    torch_version?: string;
  } | null;
  unreadAlertsCount?: number;
  onOpenNotifications?: () => void;
  onOpenSettings?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  selectedModelFilter,
  onSelectModelFilter,
  systemHealth,
  unreadAlertsCount = 0,
  onOpenNotifications,
  onOpenSettings
}) => {
  const mainNav = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'analysis', label: 'Code Analysis', icon: Code2 },
    { id: 'codedna', label: 'CodeDNA Engine', icon: Dna, badge: 'NOVELTY' },
    { id: 'robustness', label: 'Robustness Lab', icon: Zap },
    { id: 'models', label: 'Model Laboratory', icon: Cpu },
    { id: 'dataset', label: 'Dataset Explorer', icon: Database },
    { id: 'methodology', label: 'Research Methodology', icon: BookOpen },
    { id: 'history', label: 'Analysis History', icon: History },
  ];

  const modelsList = [
    { id: 'tritrace', name: 'CodeDNA Fusion', type: 'Proposed' },
    { id: 'codebert', name: 'CodeBERT', type: 'Semantic' },
    { id: 'transformer_branch', name: 'Transformer', type: 'Structural' },
    { id: 'random_forest', name: 'Random Forest', type: 'Traditional' },
  ];

  return (
    <aside className="fixed top-0 left-0 bottom-0 w-[250px] bg-orbit-sidebar border-r border-orbit-border flex flex-col z-40 select-none">
      {/* Brand Header */}
      <div className="h-16 px-5 border-b border-orbit-border flex items-center space-x-3">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-400/20 to-teal-500/20 border border-cyan-400/40 flex items-center justify-center text-cyan-400 shadow-sm shadow-cyan-950">
          <Dna className="w-4 h-4 text-cyan-300" />
        </div>
        <div>
          <div className="flex items-center space-x-1.5">
            <span className="font-bold text-sm tracking-tight text-orbit-textBright font-sans">
              TriTrace
            </span>
            <span className="text-[9px] font-mono font-semibold px-1 py-0.2 rounded bg-cyan-950/80 text-cyan-400 border border-cyan-800/60 uppercase">
              v1.0
            </span>
          </div>
          <p className="text-[10px] text-orbit-textDim tracking-tight leading-none mt-0.5">
            AI Code Authorship Intelligence
          </p>
        </div>
      </div>

      {/* Navigation Scrollable Body */}
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-6">
        {/* MAIN Section */}
        <div>
          <div className="px-3 mb-2 text-[10px] font-mono font-semibold uppercase tracking-wider text-orbit-textDim">
            Main
          </div>
          <nav className="space-y-0.5">
            {mainNav.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center justify-between px-3 py-2 rounded-md text-xs font-medium transition-all group ${
                    isActive
                      ? 'bg-cyan-950/40 text-cyan-300 border-l-2 border-cyan-400 shadow-sm'
                      : 'text-orbit-textMuted hover:text-orbit-textBright hover:bg-orbit-card'
                  }`}
                >
                  <div className="flex items-center space-x-2.5">
                    <Icon
                      className={`w-4 h-4 transition-colors ${
                        isActive
                          ? 'text-cyan-400'
                          : 'text-orbit-textDim group-hover:text-orbit-textBright'
                      }`}
                    />
                    <span className="truncate">{item.label}</span>
                  </div>
                  {item.badge && (
                    <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-cyan-900/40 text-cyan-300 border border-cyan-800/40">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* MODELS Section */}
        <div>
          <div className="px-3 mb-2 text-[10px] font-mono font-semibold uppercase tracking-wider text-orbit-textDim flex items-center justify-between">
            <span>Models</span>
            <span className="text-[9px] font-mono text-cyan-400">4 Active</span>
          </div>
          <div className="space-y-0.5">
            {modelsList.map((m) => {
              const isSelected = selectedModelFilter === m.id;
              return (
                <button
                  key={m.id}
                  onClick={() => {
                    setActiveTab('models');
                    if (onSelectModelFilter) onSelectModelFilter(m.id);
                  }}
                  className={`w-full flex items-center justify-between px-3 py-1.5 rounded-md text-xs transition-all ${
                    isSelected && activeTab === 'models'
                      ? 'bg-cyan-950/30 text-cyan-300 border border-cyan-800/50'
                      : 'text-orbit-textMuted hover:text-orbit-textBright hover:bg-orbit-card'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                    <span className="truncate">{m.name}</span>
                  </div>
                  <span className="text-[9px] font-mono text-orbit-textDim uppercase">
                    {m.type}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* PLATFORM Section */}
        <div>
          <div className="px-3 mb-2 text-[10px] font-mono font-semibold uppercase tracking-wider text-orbit-textDim">
            Platform
          </div>
          <nav className="space-y-0.5">
            <button
              onClick={() => {
                if (onOpenSettings) onOpenSettings();
              }}
              className="w-full flex items-center space-x-2.5 px-3 py-2 rounded-md text-xs font-medium text-orbit-textMuted hover:text-orbit-textBright hover:bg-orbit-card transition-all"
            >
              <Settings className="w-4 h-4 text-orbit-textDim" />
              <span>Settings</span>
            </button>

            <button
              onClick={() => setActiveTab('methodology')}
              className="w-full flex items-center space-x-2.5 px-3 py-2 rounded-md text-xs font-medium text-orbit-textMuted hover:text-orbit-textBright hover:bg-orbit-card transition-all"
            >
              <FileText className="w-4 h-4 text-orbit-textDim" />
              <span>Documentation</span>
            </button>

            <button
              onClick={() => {
                if (onOpenNotifications) onOpenNotifications();
              }}
              className="w-full flex items-center justify-between px-3 py-2 rounded-md text-xs font-medium text-orbit-textMuted hover:text-orbit-textBright hover:bg-orbit-card transition-all"
            >
              <div className="flex items-center space-x-2.5">
                <Bell className="w-4 h-4 text-orbit-textDim" />
                <span>Notifications</span>
              </div>
              {unreadAlertsCount > 0 && (
                <span className="text-[10px] font-mono px-1.5 py-0.2 rounded-full bg-cyan-500/20 text-cyan-300 font-semibold border border-cyan-500/40">
                  {unreadAlertsCount}
                </span>
              )}
            </button>
          </nav>
        </div>
      </div>

      {/* Bottom Health & Engine Telemetry */}
      <div className="p-3 border-t border-orbit-border bg-orbit-bg/80 text-[11px] font-mono">
        <div className="p-2.5 rounded-lg bg-orbit-card border border-orbit-border space-y-1.5">
          <div className="flex items-center justify-between text-[10px] text-orbit-textDim">
            <span className="flex items-center space-x-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-emerald-400 font-semibold">API Operational</span>
            </span>
            <span className="text-orbit-textMuted">127.0.0.1:8000</span>
          </div>

          <div className="flex items-center justify-between text-orbit-textBright text-[11px]">
            <span className="text-orbit-textDim">Engine:</span>
            <span>PyTorch {systemHealth?.torch_version?.split('+')[0] || '2.15'}</span>
          </div>

          <div className="flex items-center justify-between text-orbit-textDim text-[10px]">
            <span>Device: {systemHealth?.device || 'CPU'}</span>
            <span className="text-cyan-400">Latency: ~14ms</span>
          </div>
        </div>
      </div>
    </aside>
  );
};
