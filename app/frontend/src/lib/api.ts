import type { TimeResponseAPI, ConnectionStatusAPI, ApiError } from '@/types/api';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  private async fetchWithErrorHandling<T>(url: string, options?: RequestInit): Promise<T> {
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const error: ApiError = {
          error: `HTTP ${response.status}`,
          message: errorData.message || response.statusText,
          status: response.status,
        };
        throw error;
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
          throw {
            error: 'Network Error',
            message: 'Unable to connect to the server. Please ensure the backend is running.',
          } as ApiError;
        }
      }
      throw error;
    }
  }

  async getCurrentTime(): Promise<TimeResponseAPI> {
    return this.fetchWithErrorHandling<TimeResponseAPI>(`${this.baseUrl}/api/tws/current-time`);
  }

  async getConnectionStatus(): Promise<ConnectionStatusAPI> {
    return this.fetchWithErrorHandling<ConnectionStatusAPI>(`${this.baseUrl}/api/tws/connection-status`);
  }

  // Configure base URL (useful for different environments)
  setBaseUrl(baseUrl: string): void {
    this.baseUrl = baseUrl;
  }

  getBaseUrl(): string {
    return this.baseUrl;
  }
}

export const apiClient = new ApiClient();