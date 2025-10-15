// Backend API response interfaces
export interface TimeResponseAPI {
  success: boolean;
  current_time?: string; // ISO datetime string
  server_version?: number;
  connection_time?: string; // ISO datetime string
  error_message?: string;
}

export interface ConnectionStatusAPI {
  connected: boolean;
  client_id: number;
  host: string;
  port: number;
  connection_time?: string;
  error_message?: string;
}

// Frontend error type
export interface ApiError {
  error: string;
  message: string;
  status?: number;
}

// Legacy interface for backward compatibility (if needed)
export interface TimeResponse {
  timestamp: number;
  readable: string;
  success: boolean;
  message: string;
}