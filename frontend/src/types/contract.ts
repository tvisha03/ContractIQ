// Updated to match backend response structure
export interface PainPoint {
  type: string;
  issue: string;
  start: number;
  end: number;
}

export interface Entity {
  text: string;
  label: string;
}

export interface AnalysisResult {
  fileName: string;
  contractText: string;
  contractType: string;
  painPoints: PainPoint[];
  entities: Entity[];
  summary: string;
  riskScore: number;
}