// import { AnalysisResult, PainPoint, Entity } from '../types/contract';

const API_URL = import.meta.env.VITE_API_URL;

export const apiService = {
  async uploadContract(file: File): Promise<{
    fileName: string;
    contractText: string;
    contractType: string;
    painPoints: any[];
    entities: any[];
    summary: string;
    riskScore: number;
  }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/upload/`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to upload contract');
    }

    const data = await response.json();
    return {
      fileName: file.name,
      contractText: data.extracted_text,
      contractType: data.contract_type,
      painPoints: data.pain_points,
      entities: data.entities,
      summary: data.summary,
      riskScore: data.risk_score,
    };
  },
};