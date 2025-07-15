import React from 'react';
import { FileText, Shield, Users, Zap, ChevronRight } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card, CardContent } from '../components/ui/Card';
import { Header } from '../components/layout/Header';

interface HomepageProps {
  onGetStarted: () => void;
  onFeatureClick: (feature: string) => void;
}

export const Homepage: React.FC<HomepageProps> = ({ onGetStarted, onFeatureClick }) => {
  const features = [
    {
      id: 'smart-analysis',
      icon: <FileText className="h-8 w-8 text-blue-600" />,
      title: 'Smart Contract Analysis',
      description: 'AI-powered analysis of contract terms, clauses, and potential risks'
    },
    {
      id: 'risk-detection',
      icon: <Shield className="h-8 w-8 text-red-600" />,
      title: 'Risk Detection',
      description: 'Identify problematic clauses, unfair terms, and potential legal issues'
    },
    {
      id: 'entity-extraction',
      icon: <Users className="h-8 w-8 text-green-600" />,
      title: 'Entity Extraction',
      description: 'Automatically extract parties, dates, amounts, and key contract elements'
    },
    {
      id: 'instant-insights',
      icon: <Zap className="h-8 w-8 text-yellow-600" />,
      title: 'Instant Insights',
      description: 'Get comprehensive summaries and actionable recommendations in seconds'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-gray-100 mb-6">
            <span className="text-blue-600">ContractIQ</span>
            <span className="block text-gray-700 dark:text-gray-300 text-3xl md:text-4xl mt-2">AI-Powered Contract Analysis</span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto mb-8">
            Upload your contracts and get instant AI-powered analysis. Identify risks, 
            extract key information, and understand complex legal documents in minutes.
          </p>
          <Button
            size="lg"
            onClick={onGetStarted}
            className="text-lg px-8 py-4"
          >
            <FileText className="h-5 w-5 mr-2" />
            Upload Contract to Analyze
          </Button>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {features.map((feature, index) => (
            <Card 
              key={index} 
              className="text-center hover:shadow-lg transition-all cursor-pointer group hover:scale-105 hover:border-blue-300 dark:hover:border-blue-600"
              onClick={() => onFeatureClick(feature.id)}
            >
              <CardContent className="pt-6">
                <div className="flex justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                  {feature.title}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {feature.description}
                </p>
                <div className="mt-4 flex items-center justify-center text-blue-600 dark:text-blue-400 opacity-0 group-hover:opacity-100 transition-opacity">
                  <span className="text-sm font-medium mr-1">Learn More</span>
                  <ChevronRight className="h-4 w-4" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* How It Works */}
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-8">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { step: '1', title: 'Upload', description: 'Upload your contract PDF' },
              { step: '2', title: 'Analyze', description: 'AI processes and analyzes the document' },
              { step: '3', title: 'Review', description: 'Get detailed insights and recommendations' }
            ].map((step, index) => (
              <div key={index} className="flex flex-col items-center">
                <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold text-lg mb-4">
                  {step.step}
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
                  {step.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {step.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};