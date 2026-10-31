export interface TokenAttribution {
  token: string;
  score: number;
  raw_score: number;
  intensity: 'baseline' | 'low' | 'medium' | 'high';
}

export interface StructuralSignal {
  name: string;
  key: string;
  value: number;
  ai_baseline: number;
  human_baseline: number;
  signal_alignment: string;
  score: number;
}

export interface FeatureCategoryBreakdown {
  category: string;
  importance: number;
  signals: StructuralSignal[];
}

export interface CodeDNADimension {
  dimension: string;
  score: number;
  summary: string;
  indicators: string[];
  norm?: number;
  dispersion?: number;
  variance?: number;
  max_nesting_depth?: number;
  control_flow_nodes?: number;
  cyclomatic_estimate?: number;
  comprehension_ratio?: number;
  type_token_ratio?: number;
  identifier_entropy?: number;
  comment_ratio?: number;
  casing_conformity?: string;
  calibrated_confidence?: number;
  entropy_bits?: number;
  safety_margin?: number;
  abstention_triggered?: boolean;
  threshold_used?: number;
}

export interface CodeDNAProfile {
  fingerprint_id: string;
  semantic_dna: CodeDNADimension;
  structural_dna: CodeDNADimension;
  stylistic_dna: CodeDNADimension;
  reliability_dna: CodeDNADimension;
  dimension_contributions: {
    semantic: number;
    structural: number;
    stylistic: number;
    reliability: number;
  };
  overall_dna_score: number;
}

export interface AnalysisResponse {
  status: 'human' | 'ai' | 'uncertain';
  predicted_class: string;
  confidence: number;
  p_human: number;
  p_ai: number;
  entropy: number;
  is_uncertain: boolean;
  threshold_used: number;
  calibrated_temperature: number;
  code_length_lines: number;
  token_count: number;
  token_attributions: TokenAttribution[];
  feature_breakdown: FeatureCategoryBreakdown[];
  key_findings: string[];
  model_version: string;
  dataset_version: string;
  limitations_notice: string;
  codedna?: CodeDNAProfile;
  history_id?: string;
}

export interface HistoryRecord {
  id: string;
  timestamp: string;
  language: string;
  code_snippet: string;
  code_length_lines: number;
  token_count: number;
  predicted_class: string;
  status: 'human' | 'ai' | 'uncertain';
  confidence: number;
  p_human: number;
  p_ai: number;
  entropy: number;
  threshold_used: number;
  fingerprint_id: string;
  model_version: string;
  codedna: {
    fingerprint_id?: string;
    overall_dna_score?: number;
    semantic_dna?: CodeDNADimension;
    structural_dna?: CodeDNADimension;
    stylistic_dna?: CodeDNADimension;
    reliability_dna?: CodeDNADimension;
    dimension_contributions?: {
      semantic: number;
      structural: number;
      stylistic: number;
      reliability: number;
    };
  };
}

export interface ModelBenchmarkEntry {
  model_key: string;
  model_name: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;
  roc_auc: number;
  ece: number;
  status: string;
}

export interface EvaluationSummary {
  benchmark_comparison: ModelBenchmarkEntry[];
  active_model: string;
  metrics: {
    accuracy: number;
    precision: number;
    recall: number;
    f1: number;
    roc_auc: number;
    ece: number;
    max_calibration_error: number;
    confusion_matrix: {
      matrix: number[][];
      labels: string[];
      true_negatives: number;
      false_positives: number;
      false_negatives: number;
      true_positives: number;
    };
    roc_curve: { fpr: number; tpr: number }[];
    pr_curve: { recall: number; precision: number }[];
    reliability_bins: {
      bin_center: number;
      accuracy: number;
      confidence: number;
      count: number;
    }[];
  };
  ablation_study: {
    configuration: string;
    f1: number;
    accuracy: number;
    ece: number;
    delta_f1: string;
  }[];
  risk_coverage_curve: {
    threshold: number;
    coverage: number;
    selective_risk: number;
    selective_accuracy: number;
    accepted_count: number;
    abstained_count: number;
  }[];
  slice_analysis: {
    by_language: Record<string, { count: number; accuracy: number; f1: number } | null>;
    by_length: Record<string, { count: number; accuracy: number; f1: number } | null>;
  };
  hypotheses_verdicts: {
    id: string;
    statement: string;
    verdict: 'Supported' | 'Unsupported' | 'Inconclusive';
    evidence: string;
  }[];
  calibrated_temperature: number;
  training_loss_history: {
    epoch: number;
    train_loss: number;
    val_loss: number;
    val_accuracy: number;
  }[];
  evaluation_timestamp: string;
}

export interface DatasetSummary {
  total_samples: number;
  train_count: number;
  val_count: number;
  test_count: number;
  class_distribution: Record<string, number>;
  language_distribution: Record<string, number>;
  source_distribution: Record<string, number>;
  avg_code_length_lines: number;
  leakage_info: {
    has_leakage: boolean;
    exact_duplicate_overlap_count: number;
    repository_overlap_count: number;
    overlapping_repositories: string[];
  };
  provenance_notes: string;
  license_info: string;
}

export interface ModelInfo {
  id: string;
  name: string;
  type: string;
  parameters: string;
  is_loaded: boolean;
  has_checkpoint: boolean;
  checkpoint_size: string;
  calibrated_temperature: number;
  abstention_threshold: number;
  description: string;
}

export interface PerturbationResult {
  name: string;
  description: string;
  perturbed_code?: string;
  predicted_class?: string;
  confidence?: number;
  confidence_delta?: number;
  p_ai?: number;
  label_flipped?: boolean;
  supported?: boolean;
  resilience?: string;
  error?: string;
}

export interface RobustnessSummary {
  original: {
    predicted_class: string;
    confidence: number;
    p_ai: number;
  };
  perturbations: Record<string, PerturbationResult>;
  overall_robustness_score: number;
  label_stability_rate: number;
  mean_confidence_drift: number;
}
