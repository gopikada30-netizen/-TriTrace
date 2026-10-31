import React from 'react';
import {
  Search,
  Bell,
  RefreshCw,
  Sliders,
  Play,
  Terminal,
  ExternalLink,
  ShieldAlert,
  CheckCircle2,
  Cpu
} from 'lucide-react';

interface TopBarProps {
  title: string;
  subtitle: string;
  onRefresh: () => void;
  isLoading: boolean;
  onNavigateToAnalysis: () => void;
  onOpenNotifications: () => void;
  unreadCount?: number;
}

export const TopBar: React.FC<TopBarProps> = ({
  title,
  subtitle,
  onRefresh,
  isLoading,
  onNavigateToAnalysis,
  onOpenNotifications,
  unreadCount = 0
}) => {
  return (
    <header className="h-16 border-b border-orbit-border bg-orbit-bg/90 sticky top-0 z-30 backdrop-blur-md px-6 flex items-center justify-between">
      {/* Page Title & Context */}
      <div>
        <h1 className="text-base font-bold text-orbit-textBright tracking-tight">
          {title}
        </h1>
        <p className="text-[11px] font-mono text-orbit-textDim">
          {subtitle}
        </p>
      </div>

      {/* Actions & Global Controls */}
      <div className="flex items-center space-x-3">
        {/* Quick Refresh */}
        <button
          onClick={onRefresh}
          disabled={isLoading}
          title="Refresh Telemetry & Metrics"
          className="p-2 rounded-lg bg-orbit-card border border-orbit-border text-orbit-textMuted hover:text-orbit-textBright hover:border-orbit-borderLight transition-all disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin text-cyan-400' : ''}`} />
        </button>

        {/* Notifications */}
        <button
          onClick={onOpenNotifications}
          title="System Alerts & Telemetry"
          className="relative p-2 rounded-lg bg-orbit-card border border-orbit-border text-orbit-textMuted hover:text-orbit-textBright hover:border-orbit-borderLight transition-all"
        >
          <Bell className="w-3.5 h-3.5" />
          {unreadCount > 0 && (
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-cyan-400 ring-2 ring-orbit-bg" />
          )}
        </button>

        {/* Primary CTA */}
        <button
          onClick={onNavigateToAnalysis}
          className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-cyan-500/15 hover:bg-cyan-500/25 border border-cyan-400/40 text-cyan-300 font-medium text-xs shadow-sm transition-all"
        >
          <Play className="w-3.5 h-3.5 fill-current text-cyan-400" />
          <span>Analyze Code</span>
        </button>
      </div>
    </header>
  );
};
