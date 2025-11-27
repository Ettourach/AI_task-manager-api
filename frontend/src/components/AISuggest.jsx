/**
 * AISuggest Component
 * 
 * Provides AI-powered task suggestions using the /api/suggest-task/ endpoint.
 * 
 * Usage:
 * import AISuggest from './components/AISuggest';
 * <AISuggest onSuggestionAccept={handleAddTask} />
 */

import { useState } from 'react';
import apiClient from '../api/apiClient';

const AISuggest = ({ onSuggestionAccept }) => {
  const [prompt, setPrompt] = useState('');
  const [suggestion, setSuggestion] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getSuggestion = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.post('/suggest-task/', { prompt });
      setSuggestion(response.data);
    } catch (err) {
      if (err.response?.status === 429) {
        setError('Rate limit exceeded. Please wait a moment before trying again.');
      } else {
        setError('Failed to get suggestion. Please try again.');
      }
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const acceptSuggestion = () => {
    if (suggestion && onSuggestionAccept) {
      onSuggestionAccept(suggestion.suggestion);
      setSuggestion(null);
      setPrompt('');
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg">
      <div className="flex items-center gap-2 mb-4">
        <svg
          className="w-6 h-6 text-purple-500"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
          />
        </svg>
        <h2 className="text-xl font-semibold text-gray-800">AI Task Suggestions</h2>
      </div>

      <form onSubmit={getSuggestion} className="mb-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="What would you like to do? (e.g., 'study Python', 'exercise more')"
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                Thinking...
              </span>
            ) : (
              'Get Suggestion'
            )}
          </button>
        </div>
      </form>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {suggestion && (
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-start gap-3">
            <div className="flex-1">
              <p className="text-gray-800">{suggestion.suggestion}</p>
              <p className="text-xs text-gray-500 mt-2">
                {suggestion.used_openai ? '✨ Powered by AI' : '📚 Rule-based suggestion'}
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={acceptSuggestion}
                className="px-3 py-1 bg-green-500 text-white text-sm rounded hover:bg-green-600"
              >
                Add as Task
              </button>
              <button
                onClick={() => setSuggestion(null)}
                className="px-3 py-1 bg-gray-300 text-gray-700 text-sm rounded hover:bg-gray-400"
              >
                Dismiss
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AISuggest;
