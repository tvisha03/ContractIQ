import React, { useState } from 'react';
import { ThemeProvider } from './contexts/ThemeContext';
import { Homepage } from './pages/Homepage';
import { Dashboard } from './pages/Dashboard';
import { FileUpload } from './components/upload/FileUpload';
import { LoadingState } from './components/analysis/LoadingState';
import { Header } from './components/layout/Header';
import { AdvancedFeatures } from './components/ui/AdvancedFeatures';
import { AnalysisResult } from './types/contract';
import { apiService } from './services/api';

type AppState = 'homepage' | 'upload' | 'loading' | 'analysis';

function App() {
  const [appState, setAppState] = useState<AppState>('homepage');
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [loadingMessage, setLoadingMessage] = useState('');

  const handleGetStarted = () => {
    setAppState('upload');
  };

  const handleFeatureClick = (feature: string) => {
    console.log(`Feature clicked: ${feature}`);
    // You can add specific feature demonstrations here
    setAppState('upload');
  };

  const handleFileUpload = async (file: File) => {
    try {
      setAppState('loading');
      setLoadingMessage('Uploading and analyzing contract...');
      const uploadResult = await apiService.uploadContract(file);
      setAnalysisResult(uploadResult);
      setAppState('analysis');
    } catch (error) {
      console.error('Error analyzing contract:', error);
      setAppState('upload');
    }
  };

  const handleBack = () => {
    setAppState('upload');
    setAnalysisResult(null);
  };

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        {appState === 'homepage' && (
          <Homepage onGetStarted={handleGetStarted} onFeatureClick={handleFeatureClick} />
        )}
        
        {appState === 'upload' && (
          <div>
            <Header />
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">
                  Upload Your Contract
                </h1>
                <p className="text-gray-600 dark:text-gray-400">
                  Select a PDF contract to analyze for risks, entities, and key insights
                </p>
                <button
                  className="mt-4 text-blue-600 underline hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
                  onClick={() => setAppState('homepage')}
                >
                  ← Back to Home
                </button>
              </div>
              <FileUpload onFileSelect={handleFileUpload} />
            </main>
          </div>
        )}
        
        {appState === 'loading' && (
          <div>
            <Header />
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
              <LoadingState message={loadingMessage} />
            </main>
          </div>
        )}
        
        {appState === 'analysis' && analysisResult && (
          <Dashboard 
            analysisResult={analysisResult} 
            onBack={handleBack}
            onBackToHome={() => setAppState('homepage')}
          />
        )}
        
        {/* Advanced Features - Show on analysis page */}
        {appState === 'analysis' && <AdvancedFeatures />}
      </div>
    </ThemeProvider>
  );
}

export default App;