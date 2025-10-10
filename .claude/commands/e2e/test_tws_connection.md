# E2E Test: TWS Connection and Time Request

Test the TWS (Trader Workstation) application's ability to connect to Interactive Brokers TWS/Gateway and retrieve the current server time.

## User Story

As a trader/developer
I want to verify the TWS application can connect to Interactive Brokers
So that I can ensure the integration is working before building trading functionality

## Prerequisites

Before running this test, ensure:

1. **TWS or IB Gateway is running** on your machine
2. **API connections are enabled** in TWS settings:
   - TWS: File → Global Configuration → API → Settings
   - Enable ActiveX and Socket Clients checkbox is checked
   - Socket port is set to 7500 (or your configured port)
   - Trusted IP addresses includes 127.0.0.1
3. **Virtual environment is set up** with ibapi installed
4. **TWS application is built** in `app/server/`

## Test Steps

### Step 1: Verify Prerequisites
1. Confirm TWS or IB Gateway application is running
2. Take a screenshot of the TWS API settings page showing:
   - "Enable ActiveX and Socket Clients" is checked
   - Socket port number (should be 7500 for this test)
   - Trusted IP addresses section
3. **Verify** socket port matches the port you'll use in the test

### Step 2: Run the TWS Application
1. Open a terminal in the project root directory
2. Execute the command:
   ```bash
   bash scripts/start_tws.sh
   ```
3. Take a screenshot of the terminal output showing the startup banner
4. **Verify** you see logs indicating:
   - "TWSClient initialized with localhost:7500, client_id=1"
   - "Connecting to TWS at localhost:7500..."

### Step 3: Verify Connection Establishment
1. Monitor the terminal output for connection messages
2. **Verify** you see:
   - "Connected successfully. Next valid order ID: [number]"
   - "Connection established successfully"
3. Take a screenshot of the connection success messages

### Step 4: Verify Time Request and Response
1. **Verify** you see the log message:
   - "Requesting current time from TWS server..."
2. **Verify** you see the time response logs:
   - "Received current time from TWS: [unix_timestamp]"
   - "Current TWS server time: [readable_timestamp]"
3. Take a screenshot of the time response

### Step 5: Verify Success Summary
1. **Verify** the success summary box is displayed with:
   - "SUCCESS: Connection to TWS established!"
   - TWS Server Time (Unix Timestamp)
   - TWS Server Time (Readable format)
   - Connection Host: localhost
   - Connection Port: 7500
   - Client ID: 1
2. Take a screenshot of the complete success summary
3. **Verify** the readable time format matches approximately current time

### Step 6: Verify Graceful Shutdown
1. Wait for the message: "Connection active. Press Ctrl+C to exit..."
2. Press Ctrl+C to interrupt the application
3. **Verify** you see:
   - "Received interrupt signal, shutting down gracefully..."
   - "Disconnecting from TWS..."
   - "Disconnected successfully"
   - "TWS Application terminated"
4. Take a screenshot of the graceful shutdown messages

### Step 7: Test with Different Ports (Optional)
1. If you have TWS paper trading on port 7497, test with:
   ```bash
   bash scripts/start_tws.sh --port 7497
   ```
2. **Verify** the application connects successfully to the alternate port
3. Take a screenshot if testing alternate ports

### Step 8: Test Help Documentation
1. Run the command:
   ```bash
   bash scripts/start_tws.sh --help
   ```
2. **Verify** the help text displays:
   - Description of the application
   - Usage examples
   - Port options reference
3. Take a screenshot of the help output

## Success Criteria

- [ ] TWS/Gateway is running and API is enabled
- [ ] Application starts without errors
- [ ] Connection to TWS is established successfully
- [ ] Current server time is retrieved and displayed
- [ ] Unix timestamp and readable format are both shown
- [ ] Readable time matches approximate current time (±1 minute)
- [ ] Application shuts down gracefully with Ctrl+C
- [ ] No error messages or exceptions in the output
- [ ] At least 5 screenshots captured documenting the test

## Expected Output Format

The successful test should show output similar to:

```
==========================================
  TWS Application Startup
==========================================

2025-01-15 10:30:00 - tws_client - INFO - TWSClient initialized with localhost:7500, client_id=1
2025-01-15 10:30:00 - tws_client - INFO - Connecting to TWS at localhost:7500...
2025-01-15 10:30:01 - tws_client - INFO - Connected successfully. Next valid order ID: 1
2025-01-15 10:30:01 - tws_client - INFO - Connection established successfully
2025-01-15 10:30:01 - tws_app - INFO - Requesting current time from TWS server...
2025-01-15 10:30:01 - tws_client - INFO - Received current time from TWS: 1736937001
2025-01-15 10:30:01 - tws_client - INFO - Current TWS server time: 2025-01-15 10:30:01

============================================================
SUCCESS: Connection to TWS established!
============================================================
TWS Server Time (Unix Timestamp): 1736937001
TWS Server Time (Readable):       2025-01-15 10:30:01
Connection Host:                   localhost
Connection Port:                   7500
Client ID:                         1
============================================================

2025-01-15 10:30:03 - tws_app - INFO - Connection active. Press Ctrl+C to exit...
```

## Troubleshooting

### Connection Failed
- Verify TWS/Gateway is actually running
- Check that API is enabled in TWS settings
- Verify port number matches TWS configuration
- Check firewall settings
- Ensure no other application is using the same port

### Timeout Errors
- TWS may take a few seconds to accept connections
- Try running the test again
- Check TWS logs for connection attempts
- Verify the client_id is not already in use

### Permission Errors
- Ensure 127.0.0.1 is in the trusted IP addresses list
- Check TWS security settings

## Notes

- This is a basic connectivity test and does not test trading functionality
- The test uses client_id=1 by default; multiple simultaneous connections require unique IDs
- Test can be run multiple times as long as TWS is running
- Connection is intentionally brief (5 seconds) to demonstrate basic functionality
