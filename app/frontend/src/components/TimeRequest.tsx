import React, { useState, useEffect } from 'react';
import { Clock, RefreshCw, AlertCircle, CheckCircle, Wifi, WifiOff } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { apiClient } from '@/lib/api';
import type { TimeResponseAPI, ConnectionStatusAPI, ApiError } from '@/types/api';

interface TimeRequestState {
  timeData: TimeResponseAPI | null;
  connectionData: ConnectionStatusAPI | null;
  loading: boolean;
  error: ApiError | null;
  connectionLoading: boolean;
  connectionError: ApiError | null;
}

export const TimeRequest: React.FC = () => {
  const [state, setState] = useState<TimeRequestState>({
    timeData: null,
    connectionData: null,
    loading: false,
    error: null,
    connectionLoading: false,
    connectionError: null,
  });

  // Fetch connection status on component mount
  useEffect(() => {
    checkConnectionStatus();
  }, []);

  const checkConnectionStatus = async () => {
    setState(prev => ({ ...prev, connectionLoading: true, connectionError: null }));

    try {
      const connectionData = await apiClient.getConnectionStatus();
      setState(prev => ({
        ...prev,
        connectionData,
        connectionLoading: false,
        connectionError: null,
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        connectionData: null,
        connectionLoading: false,
        connectionError: error as ApiError,
      }));
    }
  };

  const handleTimeRequest = async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const timeData = await apiClient.getCurrentTime();
      setState(prev => ({
        ...prev,
        timeData,
        loading: false,
        error: null,
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        timeData: null,
        loading: false,
        error: error as ApiError,
      }));
    }
  };

  const formatISODate = (isoString: string): string => {
    return new Date(isoString).toLocaleString();
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <CardTitle className="flex items-center justify-center gap-2">
          <Clock className="h-5 w-5" />
          TWS Time Request
        </CardTitle>
        <CardDescription>
          Request current time from the Trader Workstation
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Connection Status */}
        <div className="p-3 border rounded-lg bg-gray-50">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {state.connectionLoading ? (
                <RefreshCw className="h-4 w-4 animate-spin text-gray-500" />
              ) : state.connectionData?.connected ? (
                <Wifi className="h-4 w-4 text-green-600" />
              ) : (
                <WifiOff className="h-4 w-4 text-red-600" />
              )}
              <span className="text-sm font-medium">
                TWS Connection
              </span>
            </div>
            <Button
              onClick={checkConnectionStatus}
              disabled={state.connectionLoading}
              variant="outline"
              size="sm"
            >
              Refresh
            </Button>
          </div>

          {state.connectionData && (
            <div className="mt-2 text-xs text-gray-600">
              <div>Status: {state.connectionData.connected ? 'Connected' : 'Disconnected'}</div>
              <div>Host: {state.connectionData.host}:{state.connectionData.port}</div>
              <div>Client ID: {state.connectionData.client_id}</div>
              {state.connectionData.connection_time && (
                <div>Connected at: {formatISODate(state.connectionData.connection_time)}</div>
              )}
            </div>
          )}

          {state.connectionError && (
            <div className="mt-2 text-xs text-red-600">
              Error: {state.connectionError.message}
            </div>
          )}
        </div>

        <Button
          onClick={handleTimeRequest}
          disabled={state.loading}
          className="w-full"
          size="lg"
        >
          {state.loading ? (
            <>
              <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
              Requesting Time...
            </>
          ) : (
            <>
              <Clock className="mr-2 h-4 w-4" />
              Get TWS Time
            </>
          )}
        </Button>

        {/* Success Display */}
        {state.timeData && state.timeData.success && (
          <div className="p-4 border rounded-lg bg-green-50 border-green-200">
            <div className="flex items-start gap-2">
              <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
              <div className="space-y-2 min-w-0 flex-1">
                <h3 className="font-semibold text-green-800">Time Retrieved Successfully</h3>
                <div className="space-y-1 text-sm text-green-700">
                  {state.timeData.current_time && (
                    <>
                      <div>
                        <span className="font-medium">Current Time:</span> {state.timeData.current_time}
                      </div>
                      <div>
                        <span className="font-medium">Local Time:</span> {formatISODate(state.timeData.current_time)}
                      </div>
                    </>
                  )}
                  {state.timeData.server_version && (
                    <div>
                      <span className="font-medium">Server Version:</span> {state.timeData.server_version}
                    </div>
                  )}
                  {state.timeData.connection_time && (
                    <div>
                      <span className="font-medium">Connection Time:</span> {formatISODate(state.timeData.connection_time)}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* API Success but TWS Error */}
        {state.timeData && !state.timeData.success && (
          <div className="p-4 border rounded-lg bg-yellow-50 border-yellow-200">
            <div className="flex items-start gap-2">
              <AlertCircle className="h-5 w-5 text-yellow-600 flex-shrink-0 mt-0.5" />
              <div className="space-y-2 min-w-0 flex-1">
                <h3 className="font-semibold text-yellow-800">TWS Request Failed</h3>
                <div className="text-sm text-yellow-700">
                  {state.timeData.error_message && (
                    <div>
                      <span className="font-medium">Error:</span> {state.timeData.error_message}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Network/API Error */}
        {state.error && (
          <div className="p-4 border rounded-lg bg-red-50 border-red-200">
            <div className="flex items-start gap-2">
              <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
              <div className="space-y-2 min-w-0 flex-1">
                <h3 className="font-semibold text-red-800">Connection Error</h3>
                <div className="space-y-1 text-sm text-red-700">
                  <div>
                    <span className="font-medium">Error:</span> {state.error.error}
                  </div>
                  <div>
                    <span className="font-medium">Message:</span> {state.error.message}
                  </div>
                  {state.error.status && (
                    <div>
                      <span className="font-medium">Status:</span> {state.error.status}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Help Text */}
        <div className="text-xs text-muted-foreground text-center">
          Ensure the backend server is running on localhost:8000 and TWS is connected
        </div>
      </CardContent>
    </Card>
  );
};