import React from 'react';
import { AlertTriangle, Users, Calendar, FileText, DollarSign, MapPin } from 'lucide-react';
import { AnalysisResult, PainPoint, Entity } from '../../types/contract';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';

interface ResultsSidebarProps {
  analysis: AnalysisResult;
  onPainPointClick: (painPointId: string) => void;
  selectedPainPoint?: string;
}

export const ResultsSidebar: React.FC<ResultsSidebarProps> = ({
  analysis,
  onPainPointClick,
  selectedPainPoint
}) => {
  // Removed unused getSeverityColor

  const getEntityIcon = (type: string) => {
    switch (type) {
      case 'party': return <Users className="h-4 w-4" />;
      case 'date': return <Calendar className="h-4 w-4" />;
      case 'amount': return <DollarSign className="h-4 w-4" />;
      case 'location': return <MapPin className="h-4 w-4" />;
      default: return <FileText className="h-4 w-4" />;
    }
  };

  return (
    <div className="space-y-6 h-full overflow-y-auto">
      {/* Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <FileText className="h-5 w-5 mr-2" />
            Summary
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
            {analysis.summary}
          </p>
          <div className="mt-4 flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Risk Score
            </span>
            <div className="flex items-center space-x-2">
              <div className="w-20 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                <div 
                  className={`h-full ${analysis.riskScore >= 7 ? 'bg-red-500' : analysis.riskScore >= 5 ? 'bg-yellow-500' : 'bg-green-500'}`}
                  style={{ width: `${(analysis.riskScore / 10) * 100}%` }}
                />
              </div>
              <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                {analysis.riskScore}/10
              </span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Pain Points */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <AlertTriangle className="h-5 w-5 mr-2" />
            Pain Points ({analysis.painPoints.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {analysis.painPoints.map((point: PainPoint, idx: number) => (
              <div
                key={idx}
                className={`p-3 rounded-lg border cursor-pointer transition-all ${
                  selectedPainPoint === String(idx)
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                    : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'
                }`}
                onClick={() => onPainPointClick(String(idx))}
              >
                <div className="flex items-start space-x-2">
                  <span className="inline-block px-2 py-1 text-xs font-medium rounded-full bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200">
                    {point.type}
                  </span>
                  <div className="flex-1">
                    <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100">
                      {point.issue}
                    </h4>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      Start: {point.start}, End: {point.end}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Entities */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Users className="h-5 w-5 mr-2" />
            Entities ({analysis.entities.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[...new Set(analysis.entities.map((e: Entity) => e.label))].map((label: string) => {
              const entitiesOfType = analysis.entities.filter((e: Entity) => e.label === label);
              if (entitiesOfType.length === 0) return null;

              return (
                <div key={label as string}>
                  <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-2 flex items-center">
                    {getEntityIcon(label)}
                    <span className="ml-2 capitalize">{label}s</span>
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {entitiesOfType.map((entity: Entity, idx: number) => (
                      <span
                        key={idx}
                        className="inline-block px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-md"
                      >
                        {entity.text}
                      </span>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};