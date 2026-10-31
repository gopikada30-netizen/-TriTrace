import {
  AnalysisResponse,
  EvaluationSummary,
  DatasetSummary,
  ModelInfo,
  RobustnessSummary,
  HistoryRecord
} from '../types';

const DIRECT_BACKEND = 'http://127.0.0.1:8000';

async function smartFetch(path: string, init?: RequestInit): Promise<Response> {
  // First attempt via relative proxy path (e.g. /api/...)
  const primaryUrl = path.startsWith('/api') ? path : `/api${path}`;
  try {
    const res = await fetch(primaryUrl, init);
    // If we get an HTTP response (even 4xx/5xx), return it to caller for status handling
    return res;
  } catch (primaryErr: any) {
    // Only on network connection failures (e.g. proxy dropped or cross-port issue), fallback to direct backend
    console.warn(`[TriTrace API] Relative proxy request to ${primaryUrl} failed (${primaryErr.message}). Retrying direct backend at ${DIRECT_BACKEND}...`);
    try {
      const directUrl = `${DIRECT_BACKEND}${primaryUrl}`;
      const fallbackRes = await fetch(directUrl, init);
      return fallbackRes;
    } catch (fallbackErr: any) {
      throw new Error(`Unable to reach TriTrace backend at both ${primaryUrl} and ${DIRECT_BACKEND}${primaryUrl}: ${fallbackErr.message}`);
    }
  }
}

async function extractErrorMessage(res: Response, defaultMsg: string): Promise<string> {
  try {
    const data = await res.json();
    if (typeof data.detail === 'string') {
      return data.detail;
    }
    if (Array.isArray(data.detail)) {
      return data.detail.map((d: any) => `${d.loc?.join('.') || 'field'}: ${d.msg}`).join(', ');
    }
    if (data.message) {
      return data.message;
    }
    return `${defaultMsg} (HTTP ${res.status})`;
  } catch {
    return `${defaultMsg} (HTTP ${res.status} ${res.statusText})`;
  }
}

export async function analyzeCode(
  code: string,
  language: string = 'python',
  threshold: number = 0.70,
  modelName: string = 'tritrace'
): Promise<AnalysisResponse> {
  const payload = {
    code: code.trim(),
    language: language || 'python',
    threshold: Number(threshold) || 0.70,
    model_name: modelName || 'tritrace'
  };

  const res = await smartFetch('/api/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const errMsg = await extractErrorMessage(res, 'Analysis request failed');
    throw new Error(errMsg);
  }

  return res.json();
}

export async function evaluateRobustness(
  code: string,
  language: string = 'python'
): Promise<RobustnessSummary> {
  const res = await smartFetch('/api/robustness/evaluate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code: code.trim(), language: language || 'python' })
  });

  if (!res.ok) {
    const errMsg = await extractErrorMessage(res, 'Robustness stress test failed');
    throw new Error(errMsg);
  }

  return res.json();
}

export async function getAnalysisHistory(
  limit: number = 50,
  status?: string
): Promise<HistoryRecord[]> {
  const query = status && status !== 'all'
    ? `/api/history?limit=${limit}&status=${encodeURIComponent(status)}`
    : `/api/history?limit=${limit}`;

  const res = await smartFetch(query);
  if (!res.ok) {
    const errMsg = await extractErrorMessage(res, 'Failed to load history');
    throw new Error(errMsg);
  }
  return res.json();
}

export async function getHistoryRecord(id: string): Promise<HistoryRecord> {
  const res = await smartFetch(`/api/history/${id}`);
  if (!res.ok) {
    const errMsg = await extractErrorMessage(res, 'Failed to fetch history record');
    throw new Error(errMsg);
  }
  return res.json();
}

export async function deleteHistoryRecord(id: string): Promise<void> {
  const res = await smartFetch(`/api/history/${id}`, { method: 'DELETE' });
  if (!res.ok) {
    const errMsg = await extractErrorMessage(res, 'Failed to delete history record');
    throw new Error(errMsg);
  }
}

export async function clearAllHistory(): Promise<void> {
  const res = await smartFetch(`/api/history/clear`, { method: 'POST' });
  if (!res.ok) {
    const errMsg = await extractErrorMessage(res, 'Failed to clear history');
    throw new Error(errMsg);
  }
}

export function getExportJsonUrl(id: string): string {
  return `/api/history/${id}/export/json`;
}

export function getExportHtmlUrl(id: string): string {
  return `/api/history/${id}/export/html`;
}

export async function getEvaluationSummary(): Promise<EvaluationSummary> {
  const res = await smartFetch('/api/evaluation/summary');
  if (!res.ok) {
    const errMsg = await extractErrorMessage(res, 'Failed to fetch evaluation metrics');
    throw new Error(errMsg);
  }
  return res.json();
}

export async function getDatasetSummary(): Promise<DatasetSummary> {
  const res = await smartFetch('/api/dataset/summary');
  if (!res.ok) {
    const errMsg = await extractErrorMessage(res, 'Failed to fetch dataset summary');
    throw new Error(errMsg);
  }
  return res.json();
}

export async function getAvailableModels(): Promise<ModelInfo[]> {
  const res = await smartFetch('/api/models');
  if (!res.ok) {
    const errMsg = await extractErrorMessage(res, 'Failed to fetch models list');
    throw new Error(errMsg);
  }
  const data = await res.json();
  return data.models || [];
}

export async function triggerTraining(
  epochs: number = 3,
  learningRate: number = 3e-4,
  seed: number = 42
): Promise<any> {
  const res = await smartFetch('/api/training/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      epochs,
      learning_rate: learningRate,
      random_seed: seed
    })
  });

  if (!res.ok) {
    const errMsg = await extractErrorMessage(res, 'Training failed to start');
    throw new Error(errMsg);
  }

  return res.json();
}

export async function getTrainingStatus(): Promise<any> {
  const res = await smartFetch('/api/training/status');
  if (!res.ok) {
    const errMsg = await extractErrorMessage(res, 'Failed to get training status');
    throw new Error(errMsg);
  }
  return res.json();
}

export async function getHealthStatus(): Promise<any> {
  const res = await smartFetch('/api/health');
  if (!res.ok) {
    const errMsg = await extractErrorMessage(res, 'Failed to get health status');
    throw new Error(errMsg);
  }
  return res.json();
}
