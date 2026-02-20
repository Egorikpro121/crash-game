/** API client for backend communication. */
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

class ApiClient {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
    // Try to get token from localStorage
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('auth_token');
    }
  }

  setToken(token: string | null) {
    this.token = token;
    if (token && typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    } else if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    // Add Telegram Mini App init data if available
    if (typeof window !== 'undefined' && (window as any).Telegram?.WebApp?.initData) {
      headers['X-Telegram-Init-Data'] = (window as any).Telegram.WebApp.initData;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          error: data.detail || data.message || 'Request failed',
        };
      }

      return { data };
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  }

  // Auth
  async login(telegramUser: any) {
    return this.request<{ token: string; user: any }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(telegramUser),
    });
  }

  async getMe() {
    return this.request<any>('/auth/me');
  }

  // Game
  async getRoundStatus(roundId?: number) {
    const endpoint = roundId ? `/game/round/${roundId}` : '/game/round/status';
    return this.request<any>(endpoint);
  }

  async placeBet(amount: number, currency: string, autoCashout?: number) {
    return this.request<any>('/game/bet', {
      method: 'POST',
      body: JSON.stringify({ amount, currency, auto_cashout_multiplier: autoCashout }),
    });
  }

  async cashout() {
    return this.request<any>('/game/cashout', {
      method: 'POST',
    });
  }

  async getHistory(limit = 100) {
    return this.request<any[]>(`/game/history?limit=${limit}`);
  }

  // Payments
  async createDeposit(amount: number, currency: string, method: string) {
    return this.request<any>('/payments/deposit', {
      method: 'POST',
      body: JSON.stringify({ amount, currency, payment_method: method }),
    });
  }

  async createWithdrawal(amount: number, currency: string, address: string) {
    return this.request<any>('/payments/withdrawal', {
      method: 'POST',
      body: JSON.stringify({ amount, currency, address }),
    });
  }

  async getPaymentHistory() {
    return this.request<any[]>('/payments/history');
  }

  // User
  async getBalance() {
    return this.request<{ ton: number; stars: number }>('/user/balance');
  }

  async getStatistics() {
    return this.request<any>('/user/statistics');
  }

  // Bonuses
  async getAvailableBonuses(currency: string) {
    return this.request<any>('/bonuses/available', {
      method: 'GET',
    });
  }

  async claimBonuses(currency: string) {
    return this.request<any>('/bonuses/claim', {
      method: 'POST',
      body: JSON.stringify({ currency }),
    });
  }

  // Referrals
  async getReferralCode() {
    return this.request<{ code: string }>('/referrals/code');
  }

  async getReferralStatistics() {
    return this.request<any>('/referrals/statistics');
  }

  // Leaderboard
  async getLeaderboard(limit = 100) {
    return this.request<any[]>('/leaderboard/top', {
      method: 'GET',
    });
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
