import React, { useState, useEffect } from 'react';
import {
  History,
  Download,
  Printer,
  Trash2,
  ExternalLink,
  Search,
  Filter,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Dna,
  FileCode,
  Calendar,
  X,
  RefreshCw
} from 'lucide-react';
import { HistoryRecord } from '../types';
import {
  getAnalysisHistory,
  deleteHistoryRecord,
  clearAllHistory,
  getExportJsonUrl,
  getExportHtmlUrl
} from '../services/api';

export const HistoryPage: React.FC = () => {
  const [records, setRecords] = useState<HistoryRecord[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [selectedRecord, setSelectedRecord] = useState<HistoryRecord | null>(null);
  const [isDeleting, setIsDeleting] = useState<boolean>(false);

  const loadHistory = async () => {
    setIsLoading(true);
    try {
      const data = await getAnalysisHistory(50, statusFilter);
      setRecords(data);
    } catch (e) {
      console.error('Failed to load history:', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, [statusFilter]);

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!window.confirm('Delete this analysis record from research history?')) return;
    try {
      await deleteHistoryRecord(id);
      setRecords((prev) => prev.filter((r) => r.id !== id));
      if (selectedRecord?.id === id) setSelectedRecord(null);
    } catch (err) {
      alert('Failed to delete record.');
    }
  };

  const handleClearAll = async () => {
    if (!window.confirm('Clear all analysis history records? This action is permanent.')) return;
    setIsDeleting(true);
    try {
      await clearAllHistory();
      setRecords([]);
      setSelectedRecord(null);
    } catch (err) {
      alert('Failed to clear history.');
    } finally {
      setIsDeleting(false);
    }
  };

  const filteredRecords = records.filter((r) => {
    const matchesSearch =
      r.code_snippet.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.language.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (r.fingerprint_id && r.fingerprint_id.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesSearch;
  });

  return (
    <div className="space-y-8 pb-16">
      {/* Header */}
      <div className="bg-research-900 border border-research-800 rounded-2xl p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center space-x-2 text-xs font-mono text-accent-cyan mb-1">
            <History className="w-4 h-4 text-accent-cyan" />
            <span>Telemetry & Forensic Archive</span>
          </div>
          <h1 className="text-xl md:text-2xl font-bold text-research-50">
            Research Prediction History
          </h1>
          <p className="text-xs text-research-400 mt-1">
            Auditable repository of past code analysis executions, calibrated confidence estimates, CodeDNA fingerprints, and printable forensic reports.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={loadHistory}
            disabled={isLoading}
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-research-800 hover:bg-research-750 text-research-200 text-xs font-medium border border-research-700"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
          {records.length > 0 && (
            <button
              onClick={handleClearAll}
              disabled={isDeleting}
              className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-accent-rose/10 hover:bg-accent-rose/20 text-accent-rose text-xs font-medium border border-accent-rose/30"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear History</span>
            </button>
          )}
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-research-900 border border-research-800 rounded-2xl p-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="relative w-full sm:w-96">
          <Search className="w-4 h-4 text-research-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by code snippet, fingerprint, or UUID..."
            className="w-full pl-10 pr-4 py-2 bg-research-950 border border-research-800 rounded-xl text-xs text-research-100 placeholder-research-500 focus:outline-none focus:border-accent-cyan"
          />
        </div>

        <div className="flex items-center space-x-2 w-full sm:w-auto">
          <Filter className="w-4 h-4 text-research-400" />
          <span className="text-xs font-mono text-research-400">Status:</span>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-research-950 text-research-200 border border-research-800 rounded-xl px-3 py-1.5 text-xs font-mono focus:outline-none focus:border-accent-cyan"
          >
            <option value="all">All Verdicts</option>
            <option value="human">Human-Written</option>
            <option value="ai">AI-Generated</option>
            <option value="uncertain">Uncertain / Abstention</option>
          </select>
        </div>
      </div>

      {/* History Records Table */}
      <div className="bg-navy-900 border border-research-800 rounded-2xl overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-sans">
            <thead className="bg-research-950/80 text-research-400 font-mono text-[11px] uppercase tracking-wider border-b border-research-800">
              <tr>
                <th className="py-3 px-4">Date / Time (UTC)</th>
                <th className="py-3 px-4">Language</th>
                <th className="py-3 px-4">Snippet Preview</th>
                <th className="py-3 px-4">Verdict</th>
                <th className="py-3 px-4">Confidence</th>
                <th className="py-3 px-4">Fingerprint</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-research-800/60 text-research-200 font-mono">
              {filteredRecords.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-research-500 text-xs font-sans">
                    {isLoading ? 'Loading history archive...' : 'No analysis records match your filter criteria.'}
                  </td>
                </tr>
              ) : (
                filteredRecords.map((r) => {
                  const dateStr = new Date(r.timestamp).toLocaleString();
                  const isHuman = r.status === 'human';
                  const isAI = r.status === 'ai';
                  const isUncertain = r.status === 'uncertain';

                  return (
                    <tr
                      key={r.id}
                      onClick={() => setSelectedRecord(r)}
                      className="hover:bg-research-850/60 cursor-pointer transition-colors"
                    >
                      <td className="py-3.5 px-4 whitespace-nowrap text-research-400 text-[11px]">
                        {dateStr}
                      </td>
                      <td className="py-3.5 px-4 whitespace-nowrap font-medium text-research-300">
                        {r.language.toUpperCase()}
                      </td>
                      <td className="py-3.5 px-4 max-w-xs truncate text-research-400 text-[11px]">
                        {r.code_snippet.replace(/\n/g, ' ')}
                      </td>
                      <td className="py-3.5 px-4 whitespace-nowrap">
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold ${
                            isHuman
                              ? 'bg-accent-emerald/15 text-accent-emerald border border-accent-emerald/30'
                              : isAI
                              ? 'bg-accent-rose/15 text-accent-rose border border-accent-rose/30'
                              : 'bg-accent-amber/15 text-accent-amber border border-accent-amber/30'
                          }`}
                        >
                          {r.predicted_class}
                        </span>
                      </td>
                      <td className="py-3.5 px-4 whitespace-nowrap font-bold text-research-100">
                        {(r.confidence * 100).toFixed(1)}%
                      </td>
                      <td className="py-3.5 px-4 whitespace-nowrap text-accent-cyan text-[11px]">
                        {r.fingerprint_id || 'DNA-N/A'}
                      </td>
                      <td className="py-3.5 px-4 whitespace-nowrap text-right space-x-2">
                        <a
                          href={getExportJsonUrl(r.id)}
                          download
                          onClick={(e) => e.stopPropagation()}
                          title="Download JSON Report"
                          className="inline-block p-1.5 rounded-lg bg-research-800 hover:bg-research-750 text-research-300 hover:text-white transition-all"
                        >
                          <Download className="w-3.5 h-3.5" />
                        </a>
                        <a
                          href={getExportHtmlUrl(r.id)}
                          target="_blank"
                          rel="noreferrer"
                          onClick={(e) => e.stopPropagation()}
                          title="Print / Save PDF Report"
                          className="inline-block p-1.5 rounded-lg bg-research-800 hover:bg-research-750 text-accent-cyan hover:text-cyan-300 transition-all"
                        >
                          <Printer className="w-3.5 h-3.5" />
                        </a>
                        <button
                          onClick={(e) => handleDelete(r.id, e)}
                          title="Delete Record"
                          className="p-1.5 rounded-lg bg-research-800 hover:bg-accent-rose/20 text-research-400 hover:text-accent-rose transition-all"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Selected Record Detail Modal */}
      {selectedRecord && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-research-900 border border-research-750 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto p-6 space-y-6 shadow-2xl relative">
            <button
              onClick={() => setSelectedRecord(null)}
              className="absolute right-5 top-5 p-2 rounded-lg bg-research-800 text-research-400 hover:text-white"
            >
              <X className="w-4 h-4" />
            </button>

            {/* Modal Title */}
            <div>
              <div className="flex items-center space-x-2 text-xs font-mono text-accent-cyan mb-1">
                <Dna className="w-4 h-4 text-accent-cyan" />
                <span>Forensic Authorship Dossier</span>
              </div>
              <h2 className="text-lg font-bold text-research-50 flex items-center space-x-3">
                <span>Record: {selectedRecord.id.slice(0, 8)}...</span>
                <span
                  className={`text-xs px-2 py-0.5 rounded font-mono font-bold ${
                    selectedRecord.status === 'human'
                      ? 'bg-accent-emerald/20 text-accent-emerald'
                      : selectedRecord.status === 'ai'
                      ? 'bg-accent-rose/20 text-accent-rose'
                      : 'bg-accent-amber/20 text-accent-amber'
                  }`}
                >
                  {selectedRecord.predicted_class}
                </span>
              </h2>
              <span className="text-xs font-mono text-research-400">
                Logged at: {new Date(selectedRecord.timestamp).toUTCString()}
              </span>
            </div>

            {/* Metric Overview */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="p-3 rounded-xl bg-research-950 border border-research-800 font-mono">
                <span className="text-[10px] text-research-400 uppercase block">Calibrated Conf</span>
                <span className="text-base font-bold text-research-100">
                  {(selectedRecord.confidence * 100).toFixed(1)}%
                </span>
              </div>
              <div className="p-3 rounded-xl bg-research-950 border border-research-800 font-mono">
                <span className="text-[10px] text-research-400 uppercase block">Posterior P(AI)</span>
                <span className="text-base font-bold text-accent-rose">
                  {(selectedRecord.p_ai * 100).toFixed(1)}%
                </span>
              </div>
              <div className="p-3 rounded-xl bg-research-950 border border-research-800 font-mono">
                <span className="text-[10px] text-research-400 uppercase block">Shannon Entropy</span>
                <span className="text-base font-bold text-accent-amber">
                  {selectedRecord.entropy.toFixed(3)}
                </span>
              </div>
              <div className="p-3 rounded-xl bg-research-950 border border-research-800 font-mono">
                <span className="text-[10px] text-research-400 uppercase block">Abstention Safety</span>
                <span className="text-base font-bold text-accent-cyan">
                  {(selectedRecord.threshold_used * 100).toFixed(0)}%
                </span>
              </div>
            </div>

            {/* CodeDNA Fingerprint Dimension Breakdown */}
            {selectedRecord.codedna && (
              <div className="p-4 rounded-xl bg-navy-950 border border-research-800 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-research-200 flex items-center space-x-2">
                    <Dna className="w-4 h-4 text-accent-cyan" />
                    <span>CodeDNA Dimension Contributions</span>
                  </span>
                  <span className="text-xs font-mono text-accent-cyan">
                    {selectedRecord.fingerprint_id}
                  </span>
                </div>

                {selectedRecord.codedna.dimension_contributions && (
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2">
                    <div className="p-2.5 rounded-lg bg-research-900 border border-research-800">
                      <span className="text-[10px] font-mono text-research-400 block">Semantic DNA</span>
                      <span className="text-sm font-bold font-mono text-accent-blue">
                        {selectedRecord.codedna.dimension_contributions.semantic}%
                      </span>
                    </div>
                    <div className="p-2.5 rounded-lg bg-research-900 border border-research-800">
                      <span className="text-[10px] font-mono text-research-400 block">Structural DNA</span>
                      <span className="text-sm font-bold font-mono text-accent-cyan">
                        {selectedRecord.codedna.dimension_contributions.structural}%
                      </span>
                    </div>
                    <div className="p-2.5 rounded-lg bg-research-900 border border-research-800">
                      <span className="text-[10px] font-mono text-research-400 block">Stylistic DNA</span>
                      <span className="text-sm font-bold font-mono text-accent-amber">
                        {selectedRecord.codedna.dimension_contributions.stylistic}%
                      </span>
                    </div>
                    <div className="p-2.5 rounded-lg bg-research-900 border border-research-800">
                      <span className="text-[10px] font-mono text-research-400 block">Reliability DNA</span>
                      <span className="text-sm font-bold font-mono text-accent-emerald">
                        {selectedRecord.codedna.dimension_contributions.reliability}%
                      </span>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Code Snippet Box */}
            <div className="space-y-1.5">
              <span className="text-xs font-mono text-research-400">Archived Source Code:</span>
              <pre className="p-4 rounded-xl bg-navy-950 border border-research-800 font-mono text-xs text-research-200 overflow-x-auto max-h-56 leading-relaxed">
                {selectedRecord.code_snippet}
              </pre>
            </div>

            {/* Modal Actions */}
            <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-research-800">
              <span className="text-[11px] font-mono text-research-500">
                Model: {selectedRecord.model_version}
              </span>

              <div className="flex items-center space-x-2">
                <a
                  href={getExportJsonUrl(selectedRecord.id)}
                  download
                  className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-research-800 hover:bg-research-750 text-research-200 text-xs font-mono border border-research-700"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Export JSON</span>
                </a>
                <a
                  href={getExportHtmlUrl(selectedRecord.id)}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-accent-blue hover:bg-blue-600 text-white text-xs font-mono font-medium shadow-sm"
                >
                  <Printer className="w-3.5 h-3.5" />
                  <span>Printable / PDF Report</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
