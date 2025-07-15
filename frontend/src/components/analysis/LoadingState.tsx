import React from 'react';
import { Loader2 } from 'lucide-react';
import { Card, CardContent } from '../ui/Card';

interface LoadingStateProps {
  message?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({ 
  message = 'Analyzing contract...' 
}) => {
  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardContent className="flex flex-col items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600 mb-4" />
        <p className="text-lg font-medium text-gray-900 dark:text-gray-100">
          {message}
        </p>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
          This may take a few moments...
        </p>
      </CardContent>
    </Card>
  );
};