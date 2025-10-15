# E2E Test: Request Current Time Feature

Test the complete end-to-end functionality of requesting current time from TWS through the web interface.

## User Story

As a trader/developer
I want to request the current time from TWS using a web interface
So that I can verify the TWS integration works and build upon this foundation for future trading functionality

## Prerequisites

Before running this test, ensure:

1. **TWS or IB Gateway is running** on your machine
2. **API connections are enabled** in TWS settings:
   - TWS: File → Global Configuration → API → Settings
   - Enable ActiveX and Socket Clients checkbox is checked
   - Socket port is set to 7500 (or your configured port)
   - Trusted IP addresses includes 127.0.0.1
3. **Virtual environment is set up** with all dependencies installed
4. **Backend server is running** on localhost:8000
5. **Frontend development server is running** on localhost:5173

## Test Steps

### Step 1: Verify Prerequisites
1. Confirm TWS or IB Gateway application is running
2. Take a screenshot of the TWS API settings page showing:
   - "Enable ActiveX and Socket Clients" is checked
   - Socket port number (should be 7500 for this test)
   - Trusted IP addresses section
3. **Verify** socket port matches the port configuration
4. **Verify** backend server is running by checking http://localhost:8000/health
5. **Verify** frontend is accessible at http://localhost:5173

### Step 2: Navigate to Application
1. Open browser and navigate to http://localhost:5173
2. **Verify** the page loads without errors
3. **Verify** you see the "TWS Integration Dashboard" header
4. **Verify** you see the "Time Service" section
5. Take a screenshot of the initial application state

### Step 3: Locate Time Request Component
1. **Verify** you can see a card titled "TWS Time Request"
2. **Verify** the card contains a button labeled "Get TWS Time"
3. **Verify** the button displays a clock icon
4. **Verify** help text mentions "Ensure the backend server is running on localhost:8000 and TWS is connected"
5. Take a screenshot of the Time Request component

### Step 4: Test Time Request - Success Path
1. Click the "Get TWS Time" button
2. **Verify** the button immediately shows loading state:
   - Button text changes to "Requesting Time..."
   - Button shows spinning refresh icon
   - Button becomes disabled
3. Wait for the response (should be within 5 seconds)
4. **Verify** success response is displayed:
   - Green success box appears
   - Check circle icon is visible
   - "Time Retrieved Successfully" header is shown
   - Current time is displayed in ISO format (e.g., "2024-01-15T10:30:01")
   - Server version number is shown (if available)
   - Connection time is displayed (if available)
   - Success message is displayed
5. **Verify** the displayed time is approximately current (within 1 minute)
6. Take a screenshot of the successful response

### Step 5: Test Multiple Requests
1. Wait 2 seconds and click "Get TWS Time" button again
2. **Verify** the component handles multiple requests correctly
3. **Verify** the new timestamp is different from the previous one
4. **Verify** both timestamps are logical (new one is later)
5. Take a screenshot of the second successful response

### Step 6: Test Error Handling - Backend Down
1. Stop the backend server (Ctrl+C in the backend terminal)
2. Click the "Get TWS Time" button
3. **Verify** error handling is working:
   - Red error box appears
   - Alert circle icon is visible
   - "Connection Error" header is shown
   - Error message mentions connection failure
   - Network error details are displayed
4. Take a screenshot of the network error state

### Step 7: Test Error Handling - TWS Disconnected (Optional)
1. Restart the backend server
2. Stop TWS or IB Gateway application
3. Click the "Get TWS Time" button
4. **Verify** TWS connection error is handled:
   - Yellow warning box or red error box appears
   - Error message indicates TWS connection failure
   - Appropriate error details are shown
5. Take a screenshot of the TWS connection error

### Step 8: Test Recovery After Errors
1. Restart TWS or IB Gateway (if you stopped it)
2. Wait for TWS to fully load and enable API
3. Click the "Get TWS Time" button again
4. **Verify** the application recovers and shows successful response
5. Take a screenshot of the recovery

### Step 9: Browser Developer Tools Check
1. Open browser developer tools (F12)
2. Go to Console tab
3. Click "Get TWS Time" button
4. **Verify** no JavaScript errors are logged in console
5. Go to Network tab and repeat the request
6. **Verify** the API call to /api/tws/current-time is made correctly
7. **Verify** the response has proper JSON format
8. Take a screenshot of the network tab showing successful API call

### Step 10: Responsive Design Check
1. Resize browser window to mobile size (375px width)
2. **Verify** the component remains usable and properly styled
3. **Verify** all text remains readable
4. **Verify** button remains clickable
5. Take a screenshot of mobile view
6. Resize back to desktop size and verify normal layout

## Success Criteria

- [ ] Application loads without errors at http://localhost:5173
- [ ] TWS Integration Dashboard is displayed with proper styling
- [ ] Time Request component renders correctly with shadcn/ui styling
- [ ] "Get TWS Time" button triggers API request to backend
- [ ] Loading state is properly displayed during request
- [ ] Success response shows current time in multiple formats
- [ ] Timestamp accuracy is within 1 minute of actual time
- [ ] Error states are handled gracefully (network and TWS errors)
- [ ] Application recovers properly after error conditions
- [ ] No JavaScript errors in browser console
- [ ] API calls use correct endpoint and return proper JSON
- [ ] Component is responsive and works on mobile sizes
- [ ] At least 8 screenshots captured documenting the test flow

## Expected API Response Format

Successful response should match:
```json
{
  "success": true,
  "current_time": "2024-01-15T10:30:01",
  "server_version": 123,
  "connection_time": "2024-01-15T10:29:58",
  "error_message": null
}
```

Error response should match:
```json
{
  "success": false,
  "current_time": null,
  "server_version": null,
  "connection_time": null,
  "error_message": "Failed to connect to TWS. Ensure TWS is running on port 7500."
}
```

## Troubleshooting

### Frontend Issues
- If frontend doesn't load: Check that `npm run dev` started successfully
- If API calls fail: Verify backend is running on port 8000
- If styling looks broken: Check that Tailwind CSS is working properly

### Backend Issues
- If backend doesn't start: Check Python dependencies are installed
- If TWS connection fails: Verify TWS API settings and port configuration
- If timeout errors: Check TWS is responding and not overloaded

### TWS Connection Issues
- Verify TWS/Gateway is actually running
- Check that API is enabled in TWS settings
- Verify port number matches configuration (7500 vs 7497)
- Check firewall settings allow local connections
- Ensure no other applications are using the same client_id

## Notes

- This test validates the complete user journey from frontend to TWS
- Test demonstrates both success and error scenarios
- Screenshots provide visual proof of functionality
- Test covers responsive design and browser compatibility
- Component uses shadcn/ui for modern, accessible interface
- API integration follows REST conventions with proper error handling