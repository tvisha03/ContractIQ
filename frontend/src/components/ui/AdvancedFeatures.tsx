import React, { useState } from 'react';
import { Settings, GitCompare, Search, Download, MessageCircle, X } from 'lucide-react';
import { Button } from './Button';
import { Card, CardContent } from './Card';

export const AdvancedFeatures: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const features = [
    {
      icon: <GitCompare className="h-5 w-5" />,
      title: 'Compare Contracts',
      description: 'Side-by-side contract comparison',
      action: () => console.log('Compare contracts')
    },
    {
      icon: <Search className="h-5 w-5" />,
      title: 'Search Text',
      description: 'Find specific clauses instantly',
      action: () => console.log('Search text')
    },
    {
      icon: <Download className="h-5 w-5" />,
      title: 'Export Report',
      description: 'Download analysis as PDF',
      action: () => console.log('Export report')
    },
    {
      icon: <MessageCircle className="h-5 w-5" />,
      title: 'AI Assistant',
      description: 'Chat about contract details',
      action: () => console.log('AI Assistant')
    }
  ];

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Floating Button */}
      <Button
        onClick={() => setIsOpen(!isOpen)}
        className="rounded-full w-14 h-14 shadow-lg hover:shadow-xl transition-all duration-300 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white"
        size="lg"
      >
        {isOpen ? (
          <X className="h-6 w-6" />
        ) : (
          <Settings className="h-6 w-6 animate-pulse" />
        )}
      </Button>

      {/* Advanced Features Panel */}
      {isOpen && (
        <div className="absolute bottom-16 right-0 z-40">
          <Card className="w-80 shadow-2xl border-2 border-blue-200 dark:border-blue-800 animate-in slide-in-from-bottom-2 duration-300">
            <CardContent className="p-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center">
                <Settings className="h-5 w-5 mr-2 text-blue-600" />
                Advanced Features
              </h3>
              <div className="space-y-3">
                {features.map((feature, index) => (
                  <button
                    key={index}
                    onClick={feature.action}
                    className="w-full p-3 text-left rounded-lg border border-gray-200 dark:border-gray-600 hover:border-blue-300 dark:hover:border-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all group"
                  >
                    <div className="flex items-start space-x-3">
                      <div className="text-blue-600 dark:text-blue-400 group-hover:scale-110 transition-transform">
                        {feature.icon}
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900 dark:text-gray-100 group-hover:text-blue-600 dark:group-hover:text-blue-400">
                          {feature.title}
                        </h4>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {feature.description}
                        </p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
              <div className="mt-4 pt-3 border-t border-gray-200 dark:border-gray-600">
                <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
                  More features coming soon!
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/20 dark:bg-black/40 z-30"
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  );
};