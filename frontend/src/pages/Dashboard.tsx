import React, { useState } from 'react';
import { ArrowLeft } from 'lucide-react';
import { AnalysisResult } from '../types/contract';
import { Header } from '../components/layout/Header';
import { ContractViewer } from '../components/analysis/ContractViewer';
import { ResultsSidebar } from '../components/analysis/ResultsSidebar';
import { Button } from '../components/ui/Button';

interface DashboardProps {
  analysisResult: AnalysisResult;
  onBack: () => void;
  onBackToHome?: () => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ analysisResult, onBack, onBackToHome }) => {
  const [selectedPainPoint, setSelectedPainPoint] = useState<string | undefined>();

  const handlePainPointClick = (painPointId: string) => {
    setSelectedPainPoint(selectedPainPoint === painPointId ? undefined : painPointId);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header title={`ContractIQ - ${analysisResult.fileName}`} />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6 flex flex-col md:flex-row md:items-center md:space-x-4">
          <Button
            variant="ghost"
            onClick={onBack}
            className="mb-2 md:mb-0"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Upload
          </Button>
          {onBackToHome && (
            <Button
              variant="ghost"
              onClick={onBackToHome}
              className="mb-2 md:mb-0"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Home
            </Button>
          )}
          
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                Contract Analysis Dashboard
              </h1>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {analysisResult.contractType}
                {typeof analysisResult.riskScore === 'number' && ` • Risk Score: ${analysisResult.riskScore}/100`}
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 h-[calc(100vh-200px)]">
          <div className="lg:col-span-2">
            <ContractViewer
              contractText={analysisResult.contractText}
              painPoints={analysisResult.painPoints}
              entities={analysisResult.entities}
              selectedPainPoint={selectedPainPoint}
            />
          </div>
          <div className="lg:col-span-1">
            <ResultsSidebar
              analysis={analysisResult}
              onPainPointClick={handlePainPointClick}
              selectedPainPoint={selectedPainPoint}
            />
          </div>
        </div>
      </main>
    </div>
  );
};