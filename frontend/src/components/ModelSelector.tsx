import React, { useState, useEffect } from 'react';
import { Bot, Cloud, HardDrive, Zap, DollarSign, Check, Loader2 } from 'lucide-react';
import GlassCard from './ui/GlassCard';
import { useAPI, ModelInfo } from '../services/api';

interface ModelSelectorProps {
  onModelSelect?: (model: ModelInfo) => void;
  selectedModel?: string;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({ onModelSelect, selectedModel }) => {
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'local' | 'cloud'>('all');
  
  const api = useAPI();

  useEffect(() => {
    const fetchModels = async () => {
      try {
        setIsLoading(true);
        const modelsData = await api.models.getAll();
        setModels(modelsData);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error loading models');
        console.error('Failed to fetch models:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchModels();
  }, []);

  const handleModelSelect = (model: ModelInfo) => {
    onModelSelect?.(model);
  };

  const getProviderIcon = (provider: string) => {
    switch (provider.toLowerCase()) {
      case 'local':
      case 'ollama':
        return <HardDrive className="w-5 h-5" />;
      case 'openai':
      case 'anthropic':
      case 'github':
        return <Cloud className="w-5 h-5" />;
      default:
        return <Bot className="w-5 h-5" />;
    }
  };

  const getProviderColor = (provider: string) => {
    switch (provider.toLowerCase()) {
      case 'local':
      case 'ollama':
        return 'text-green-400 bg-green-400/10';
      case 'openai':
        return 'text-blue-400 bg-blue-400/10';
      case 'anthropic':
        return 'text-purple-400 bg-purple-400/10';
      case 'github':
        return 'text-orange-400 bg-orange-400/10';
      default:
        return 'text-gray-400 bg-gray-400/10';
    }
  };

  const getCapabilityIcon = (capability: string) => {
    switch (capability.toLowerCase()) {
      case 'fast':
        return <Zap className="w-4 h-4" />;
      case 'cheap':
        return <DollarSign className="w-4 h-4" />;
      default:
        return null;
    }
  };

  const filteredModels = models.filter(model => {
    if (filter === 'all') return true;
    if (filter === 'local') return ['local', 'ollama'].includes(model.provider.toLowerCase());
    if (filter === 'cloud') return !['local', 'ollama'].includes(model.provider.toLowerCase());
    return true;
  });

  const filterButtons = [
    { id: 'all', label: 'All Models', icon: Bot },
    { id: 'local', label: 'Local', icon: HardDrive },
    { id: 'cloud', label: 'Cloud', icon: Cloud },
  ];

  if (isLoading) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-white">Model Selection</h2>
        <GlassCard>
          <div className="p-6">
            <div className="flex items-center justify-center space-x-2">
              <Loader2 className="w-6 h-6 animate-spin text-ara-orange" />
              <span className="text-white">Loading models...</span>
            </div>
          </div>
        </GlassCard>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-white">Model Selection</h2>
        <GlassCard>
          <div className="p-6">
            <div className="flex items-center gap-3 text-red-400">
              <Bot className="w-5 h-5" />
              <span>Error loading models: {error}</span>
            </div>
          </div>
        </GlassCard>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-white">Model Selection</h2>
        <span className="text-gray-400">{filteredModels.length} available</span>
      </div>

      {/* Filter Buttons */}
      <div className="flex gap-2">
        {filterButtons.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setFilter(id as any)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
              filter === id
                ? 'bg-ara-orange text-white'
                : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            <Icon className="w-4 h-4" />
            <span>{label}</span>
          </button>
        ))}
      </div>

      {/* Models Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredModels.map((model) => (
          <GlassCard 
            key={model.id} 
            className={`cursor-pointer transition-all hover:scale-105 ${
              selectedModel === model.id ? 'ring-2 ring-ara-orange' : ''
            }`}
            onClick={() => handleModelSelect(model)}
          >
            <div className="p-4">
              {/* Header */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <div className={`p-2 rounded-lg ${getProviderColor(model.provider)}`}>
                    {getProviderIcon(model.provider)}
                  </div>
                  <div>
                    <h3 className="font-semibold text-white text-sm">{model.name}</h3>
                    <p className="text-xs text-gray-400">{model.provider}</p>
                  </div>
                </div>
                {selectedModel === model.id && (
                  <Check className="w-5 h-5 text-ara-orange" />
                )}
              </div>

              {/* Specs */}
              <div className="space-y-2 mb-3">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-400">Max Tokens</span>
                  <span className="text-white">{model.max_tokens.toLocaleString()}</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-400">Cost/1K</span>
                  <span className="text-white">${model.cost_per_1k.toFixed(4)}</span>
                </div>
              </div>

              {/* Capabilities */}
              {model.capabilities.length > 0 && (
                <div className="flex flex-wrap gap-1">
                  {model.capabilities.slice(0, 3).map((capability, index) => (
                    <div 
                      key={index}
                      className="flex items-center gap-1 px-2 py-1 bg-white/10 rounded text-xs text-gray-300"
                    >
                      {getCapabilityIcon(capability)}
                      <span>{capability}</span>
                    </div>
                  ))}
                  {model.capabilities.length > 3 && (
                    <div className="px-2 py-1 bg-white/10 rounded text-xs text-gray-300">
                      +{model.capabilities.length - 3}
                    </div>
                  )}
                </div>
              )}
            </div>
          </GlassCard>
        ))}
      </div>

      {filteredModels.length === 0 && (
        <GlassCard>
          <div className="p-8 text-center">
            <Bot className="w-12 h-12 text-gray-500 mx-auto mb-3" />
            <p className="text-gray-400">No models found for the selected filter</p>
          </div>
        </GlassCard>
      )}

      {/* Selected Model Info */}
      {selectedModel && (
        <GlassCard>
          <div className="p-4">
            <h3 className="text-lg font-semibold text-white mb-2">Selected Model</h3>
            {(() => {
              const model = models.find(m => m.id === selectedModel);
              return model ? (
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-lg ${getProviderColor(model.provider)}`}>
                      {getProviderIcon(model.provider)}
                    </div>
                    <div>
                      <div className="text-white font-medium">{model.name}</div>
                      <div className="text-sm text-gray-400">{model.provider}</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-white">${model.cost_per_1k.toFixed(4)}/1K</div>
                    <div className="text-sm text-gray-400">{model.max_tokens.toLocaleString()} tokens</div>
                  </div>
                </div>
              ) : null;
            })()}
          </div>
        </GlassCard>
      )}
    </div>
  );
};

export default ModelSelector;
