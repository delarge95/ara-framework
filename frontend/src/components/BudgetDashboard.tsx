import React, { useState, useEffect } from 'react';
import { AlertTriangle, DollarSign, TrendingDown, TrendingUp, Zap, Shield } from 'lucide-react';
import GlassCard from './ui/GlassCard';
import { useAPI, BudgetStatus as ApiBudgetStatus, UsageRecord } from '../services/api';

interface BudgetMetric {
  label: string;
  value: string;
  change: string;
  trend: 'up' | 'down' | 'neutral';
  icon: React.ReactNode;
}

const BudgetDashboard: React.FC = () => {
  const [budgetStatus, setBudgetStatus] = useState<ApiBudgetStatus | null>(null);
  const [usageHistory, setUsageHistory] = useState<UsageRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const api = useAPI();

  useEffect(() => {
    const fetchBudgetData = async () => {
      try {
        setIsLoading(true);
        const [status, usage] = await Promise.all([
          api.budget.getStatus(),
          api.budget.getUsage()
        ]);
        
        setBudgetStatus(status);
        setUsageHistory(usage);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error loading budget data');
        console.error('Failed to fetch budget data:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchBudgetData();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchBudgetData, 30000);
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-400';
      case 'warning': return 'text-yellow-400';
      case 'critical': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getProgressBarColor = (percentage: number) => {
    if (percentage < 60) return 'from-green-500 to-emerald-500';
    if (percentage < 80) return 'from-yellow-500 to-orange-500';
    return 'from-red-500 to-pink-500';
  };

  if (isLoading) {
    return (
      <GlassCard>
        <div className="p-6">
          <div className="animate-pulse">
            <div className="h-6 bg-white/20 rounded mb-4"></div>
            <div className="h-32 bg-white/10 rounded"></div>
          </div>
        </div>
      </GlassCard>
    );
  }

  if (error) {
    return (
      <GlassCard>
        <div className="p-6">
          <div className="flex items-center gap-3 text-red-400">
            <AlertTriangle className="w-5 h-5" />
            <span>Error loading budget data: {error}</span>
          </div>
        </div>
      </GlassCard>
    );
  }

  if (!budgetStatus) return null;

  const metrics: BudgetMetric[] = [
    {
      label: 'Total Budget',
      value: `$${budgetStatus.total_budget.toFixed(2)}`,
      change: 'Monthly limit',
      trend: 'neutral',
      icon: <DollarSign className="w-5 h-5" />
    },
    {
      label: 'Used',
      value: `$${budgetStatus.used_budget.toFixed(2)}`,
      change: `${budgetStatus.percentage_used.toFixed(1)}%`,
      trend: budgetStatus.percentage_used > 50 ? 'up' : 'neutral',
      icon: <Zap className="w-5 h-5" />
    },
    {
      label: 'Remaining',
      value: `$${budgetStatus.remaining_budget.toFixed(2)}`,
      change: `${(100 - budgetStatus.percentage_used).toFixed(1)}%`,
      trend: budgetStatus.remaining_budget > budgetStatus.used_budget ? 'down' : 'up',
      icon: <Shield className="w-5 h-5" />
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-white">Budget Dashboard</h2>
        <div className={`flex items-center gap-2 ${getStatusColor(budgetStatus.status)}`}>
          <div className="w-2 h-2 rounded-full bg-current animate-pulse"></div>
          <span className="capitalize font-medium">{budgetStatus.status}</span>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {metrics.map((metric) => (
          <GlassCard key={metric.label}>
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-white/10 rounded-lg text-ara-orange">
                    {metric.icon}
                  </div>
                  <span className="text-gray-300 font-medium">{metric.label}</span>
                </div>
                {metric.trend === 'up' && <TrendingUp className="w-4 h-4 text-red-400" />}
                {metric.trend === 'down' && <TrendingDown className="w-4 h-4 text-green-400" />}
              </div>
              
              <div className="space-y-2">
                <div className="text-2xl font-bold text-white">{metric.value}</div>
                <div className="text-sm text-gray-400">{metric.change}</div>
              </div>
            </div>
          </GlassCard>
        ))}
      </div>

      {/* Progress Bar */}
      <GlassCard>
        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white">Budget Usage</h3>
            <span className="text-sm text-gray-400">
              {budgetStatus.percentage_used.toFixed(1)}% used
            </span>
          </div>
          
          <div className="relative">
            <div className="h-3 bg-white/10 rounded-full overflow-hidden">
              <div 
                className={`h-full bg-gradient-to-r ${getProgressBarColor(budgetStatus.percentage_used)} transition-all duration-1000 ease-out`}
                style={{ width: `${Math.min(budgetStatus.percentage_used, 100)}%` }}
              />
            </div>
            
            {/* Warning threshold markers */}
            <div className="absolute top-0 left-[80%] w-px h-3 bg-yellow-400/60" />
            <div className="absolute top-0 left-[95%] w-px h-3 bg-red-400/60" />
          </div>
          
          <div className="flex justify-between text-xs text-gray-400 mt-2">
            <span>$0</span>
            <span className="text-yellow-400">80% Warning</span>
            <span className="text-red-400">95% Critical</span>
            <span>${budgetStatus.total_budget}</span>
          </div>
        </div>
      </GlassCard>

      {/* Recent Usage */}
      {usageHistory.length > 0 && (
        <GlassCard>
          <div className="p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Recent Usage</h3>
            <div className="space-y-3">
              {usageHistory.slice(-5).map((record, index) => (
                <div key={index} className="flex items-center justify-between py-2 border-b border-white/10 last:border-0">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-ara-orange"></div>
                    <div>
                      <div className="text-white font-medium">{record.model_name}</div>
                      <div className="text-xs text-gray-400">{record.date}</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-white font-medium">${record.cost.toFixed(2)}</div>
                    <div className="text-xs text-gray-400">{record.tokens_used.toLocaleString()} tokens</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </GlassCard>
      )}
    </div>
  );
};

export default BudgetDashboard;
