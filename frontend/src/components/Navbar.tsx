import React from 'react';
import {
  ShieldCheck,
  Cpu,
  Database,
  Activity,
  BookOpen,
  Terminal,
  Dna,
  History,
  Zap
} from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  systemHealth: {
    status?: string;
    device?: string;
    torch_version?: string;
  } | null;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab, systemHealth }) => {
  const tabs = [
    { id: 'overview', label: 'Overview', icon: BookOpen },
    { id: 'analysis', label: 'CodeDNA Analysis', icon: Dna },
    { id: 'robustness', label: 'Robustness Lab', icon: Zap },
    { id: 'models', label: 'Model Laboratory', icon: Activity },
    { id: 'dataset', label: 'Dataset Explorer', icon: Database },
    { id: 'history', label: 'Research History', icon: History },
    { id: 'methodology', label: 'Methodology', icon: ShieldCheck },
  ];

  return (
    <header className="border-b border-research-800 bg-navy-950/95 sticky top-0 z-50 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Lab Branding */}
          <div
            className="flex items-center space-x-3 cursor-pointer group"
            onClick={() => setActiveTab('overview')}
          >
            <div className="h-9 w-9 rounded-lg bg-accent-blue/15 border border-accent-blue/40 flex items-center justify-center text-accent-blue font-mono font-bold text-sm tracking-wider shadow-inner group-hover:border-accent-blue/70 transition-all">
              <Dna className="w-5 h-5 text-accent-cyan" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-semibold text-research-50 tracking-tight text-base font-sans">
                  TriTrace
                </span>
                <span className="text-[10px] font-mono uppercase tracking-wider px-1.5 py-0.5 rounded bg-research-800/90 text-accent-cyan border border-research-700/80">
                  CodeDNA Core
                </span>
              </div>
              <p className="text-[11px] text-research-400 font-mono hidden sm:block">
                Code Authorship Intelligence & Explainable Attribution
              </p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="flex space-x-1 sm:space-x-1.5 overflow-x-auto py-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all whitespace-nowrap ${
                    isActive
                      ? 'bg-research-800 text-research-50 border border-research-700/80 shadow-sm shadow-black/20 text-accent-blue'
                      : 'text-research-400 hover:text-research-200 hover:bg-research-900/60'
                  }`}
                >
                  <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-accent-cyan' : 'text-research-500'}`} />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Backend / Device Status */}
          <div className="hidden xl:flex items-center space-x-2 text-xs font-mono">
            <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-navy-900 border border-research-800 text-research-300">
              <span className="w-1.5 h-1.5 rounded-full bg-accent-emerald animate-pulse" />
              <span className="text-research-400">Engine:</span>
              <span className="text-research-100 font-medium">{systemHealth?.device || 'CPU'}</span>
            </div>
            <div className="flex items-center space-x-1 px-2.5 py-1 rounded-full bg-navy-900 border border-research-800 text-research-400">
              <Cpu className="w-3 h-3 text-accent-blue" />
              <span>PyTorch {systemHealth?.torch_version ? systemHealth.torch_version.split('+')[0] : '2.15'}</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
