/**
 * API Service para conectar con ARA Framework Backend
 * URL Base: http://localhost:9090
 */

const API_BASE_URL = 'http://localhost:9090';

// Tipos para las respuestas de la API
export interface BudgetStatus {
  total_budget: number;
  used_budget: number;
  remaining_budget: number;
  percentage_used: number;
  credit_limit: number;
  status: 'healthy' | 'warning' | 'critical';
}

export interface UsageRecord {
  date: string;
  tokens_used: number;
  cost: number;
  model_name: string;
}

export interface ModelInfo {
  id: string;
  name: string;
  provider: string;
  max_tokens: number;
  cost_per_1k: number;
  capabilities: string[];
}

export interface PipelineStatus {
  status: 'idle' | 'running' | 'completed' | 'error';
  current_stage: string;
  progress_percentage: number;
  estimated_time_remaining: string;
  last_run: string | null;
}

/**
 * Cliente API para ARA Framework
 */
class ARAApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  // Helper para hacer requests
  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`Request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // Budget endpoints
  async getBudgetStatus(): Promise<BudgetStatus> {
    return this.request<BudgetStatus>('/api/budget');
  }

  async getBudgetUsage(): Promise<UsageRecord[]> {
    return this.request<UsageRecord[]>('/api/budget/usage');
  }

  async emergencyStop(): Promise<{ success: boolean; message: string }> {
    return this.request('/api/budget/emergency-stop', {
      method: 'POST',
    });
  }

  // Models endpoints
  async getAvailableModels(): Promise<ModelInfo[]> {
    return this.request<ModelInfo[]>('/api/models');
  }

  // Pipeline endpoints
  async getPipelineStatus(): Promise<PipelineStatus> {
    return this.request<PipelineStatus>('/api/pipeline/status');
  }

  async runPipeline(config: any): Promise<{ task_id: string; status: string }> {
    return this.request('/api/pipeline/run', {
      method: 'POST',
      body: JSON.stringify(config),
    });
  }

  // Health check
  async getHealthStatus(): Promise<{ status: string; version: string; uptime: number }> {
    return this.request('/health');
  }

  // Test connectivity
  async testConnection(): Promise<boolean> {
    try {
      await this.request('/');
      return true;
    } catch {
      return false;
    }
  }
}

// Instancia singleton
export const apiClient = new ARAApiClient();

// Hook personalizado para React
export const useAPI = () => {
  return {
    budget: {
      getStatus: () => apiClient.getBudgetStatus(),
      getUsage: () => apiClient.getBudgetUsage(),
      emergencyStop: () => apiClient.emergencyStop(),
    },
    models: {
      getAll: () => apiClient.getAvailableModels(),
    },
    pipeline: {
      getStatus: () => apiClient.getPipelineStatus(),
      run: (config: any) => apiClient.runPipeline(config),
    },
    health: {
      check: () => apiClient.getHealthStatus(),
      testConnection: () => apiClient.testConnection(),
    },
  };
};

export default apiClient;