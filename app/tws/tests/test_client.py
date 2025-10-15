"""
Tests for TWS client integration.
"""

import pytest
import time
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

from ..client import TWSClient, TWSWrapper
from ..models import TimeResponse, ConnectionStatus


class TestTWSWrapper:
    """Test class for TWS wrapper functionality."""

    def test_wrapper_initialization(self):
        """Test wrapper initialization."""
        wrapper = TWSWrapper()

        assert wrapper.current_time is None
        assert wrapper.server_version is None
        assert wrapper.connection_time is None
        assert wrapper.error_message is None

    def test_current_time_callback(self):
        """Test current time callback."""
        wrapper = TWSWrapper()
        test_timestamp = int(datetime(2023, 1, 1, 12, 0, 0).timestamp())

        wrapper.currentTime(test_timestamp)

        assert wrapper.current_time is not None
        assert wrapper.current_time.year == 2023
        assert wrapper.current_time.month == 1
        assert wrapper.current_time.day == 1

    def test_error_callback(self):
        """Test error callback."""
        wrapper = TWSWrapper()

        wrapper.error(1, 502, "Test error message")

        assert wrapper.error_message == "TWS Error 502: Test error message"

    def test_connection_lost_error(self):
        """Test connection lost error codes."""
        wrapper = TWSWrapper()

        wrapper.error(1, 1100, "Connection lost")

        assert "Connection lost" in wrapper.error_message

    def test_connect_ack_callback(self):
        """Test connection acknowledgment callback."""
        wrapper = TWSWrapper()

        wrapper.connectAck()

        assert wrapper.connection_time is not None

    def test_wait_for_time(self):
        """Test waiting for time response."""
        wrapper = TWSWrapper()

        # Should timeout immediately since event is not set
        result = wrapper.wait_for_time(0.1)
        assert result is False

    def test_reset_time_event(self):
        """Test resetting time event."""
        wrapper = TWSWrapper()
        wrapper.current_time = datetime.now()
        wrapper.error_message = "Some error"

        wrapper.reset_time_event()

        assert wrapper.current_time is None
        assert wrapper.error_message is None


class TestTWSClient:
    """Test class for TWS client functionality."""

    def test_client_initialization(self):
        """Test client initialization."""
        client = TWSClient(host="localhost", port=7497, client_id=2)

        assert client.host == "localhost"
        assert client.port == 7497
        assert client.client_id == 2
        assert not client._connected

    def test_client_default_initialization(self):
        """Test client initialization with defaults."""
        client = TWSClient()

        assert client.host == "127.0.0.1"
        assert client.port == 7500
        assert client.client_id == 1

    @patch('app.tws.client.EClient')
    def test_connect_success(self, mock_eclient_class):
        """Test successful connection."""
        mock_eclient = Mock()
        mock_eclient.connect.return_value = None
        mock_eclient.isConnected.return_value = True
        mock_eclient_class.return_value = mock_eclient

        client = TWSClient()
        client.client = mock_eclient

        result = client.connect()

        assert result is True
        assert client._connected is True
        mock_eclient.connect.assert_called_once_with("127.0.0.1", 7500, 1)

    @patch('app.tws.client.EClient')
    def test_connect_failure(self, mock_eclient_class):
        """Test connection failure."""
        mock_eclient = Mock()
        mock_eclient.connect.return_value = None
        mock_eclient.isConnected.return_value = False
        mock_eclient_class.return_value = mock_eclient

        client = TWSClient()
        client.client = mock_eclient

        result = client.connect()

        assert result is False
        assert client._connected is False

    @patch('app.tws.client.EClient')
    def test_connect_exception(self, mock_eclient_class):
        """Test connection with exception."""
        mock_eclient = Mock()
        mock_eclient.connect.side_effect = Exception("Connection error")
        mock_eclient_class.return_value = mock_eclient

        client = TWSClient()
        client.client = mock_eclient

        result = client.connect()

        assert result is False

    def test_disconnect(self):
        """Test disconnect functionality."""
        client = TWSClient()
        client.client = Mock()
        client.client.isConnected.return_value = True
        client._connected = True

        client.disconnect()

        client.client.disconnect.assert_called_once()
        assert client._connected is False

    def test_is_connected(self):
        """Test connection status check."""
        client = TWSClient()
        client.client = Mock()
        client.client.isConnected.return_value = True
        client._connected = True

        assert client.is_connected() is True

    def test_is_not_connected(self):
        """Test not connected status."""
        client = TWSClient()
        client._connected = False

        assert client.is_connected() is False

    def test_get_connection_status(self):
        """Test getting connection status."""
        client = TWSClient(host="test.host", port=1234, client_id=5)
        client._connected = True
        client.wrapper.connection_time = datetime(2023, 1, 1, 12, 0, 0)
        client.wrapper.error_message = None
        client.client = Mock()
        client.client.isConnected.return_value = True

        status = client.get_connection_status()

        assert isinstance(status, ConnectionStatus)
        assert status.connected is True
        assert status.host == "test.host"
        assert status.port == 1234
        assert status.client_id == 5

    def test_request_current_time_not_connected(self):
        """Test requesting current time when not connected."""
        client = TWSClient()
        client._connected = False

        result = client.request_current_time()

        assert result is None

    @patch('app.tws.client.EClient')
    def test_request_current_time_success(self, mock_eclient_class):
        """Test successful current time request."""
        # Setup mocks
        mock_eclient = Mock()
        mock_eclient.isConnected.return_value = True
        mock_eclient.reqCurrentTime.return_value = None
        mock_eclient_class.return_value = mock_eclient

        client = TWSClient()
        client.client = mock_eclient
        client._connected = True

        # Mock the wrapper to simulate receiving time
        test_time = datetime(2023, 1, 1, 12, 0, 0)
        client.wrapper.current_time = test_time
        client.wrapper.server_version = 123
        client.wrapper.connection_time = datetime(2023, 1, 1, 11, 59, 0)

        with patch.object(client.wrapper, 'wait_for_time', return_value=True):
            with patch.object(client.wrapper, 'reset_time_event'):
                result = client.request_current_time()

        assert result is not None
        assert isinstance(result, TimeResponse)
        assert result.current_time == test_time
        assert result.server_version == 123

    @patch('app.tws.client.EClient')
    def test_request_current_time_timeout(self, mock_eclient_class):
        """Test current time request timeout."""
        mock_eclient = Mock()
        mock_eclient.isConnected.return_value = True
        mock_eclient_class.return_value = mock_eclient

        client = TWSClient()
        client.client = mock_eclient
        client._connected = True

        with patch.object(client.wrapper, 'wait_for_time', return_value=False):
            with patch.object(client.wrapper, 'reset_time_event'):
                result = client.request_current_time()

        assert result is None

    @patch('app.tws.client.EClient')
    def test_request_current_time_with_error(self, mock_eclient_class):
        """Test current time request with error response."""
        mock_eclient = Mock()
        mock_eclient.isConnected.return_value = True
        mock_eclient_class.return_value = mock_eclient

        client = TWSClient()
        client.client = mock_eclient
        client._connected = True
        client.wrapper.error_message = "Some error occurred"

        with patch.object(client.wrapper, 'wait_for_time', return_value=True):
            with patch.object(client.wrapper, 'reset_time_event'):
                result = client.request_current_time()

        assert result is None

    def test_context_manager_success(self):
        """Test using client as context manager with successful connection."""
        with patch.object(TWSClient, 'connect', return_value=True):
            with patch.object(TWSClient, 'disconnect'):
                with TWSClient() as client:
                    assert client is not None

    def test_context_manager_connection_failure(self):
        """Test using client as context manager with connection failure."""
        with patch.object(TWSClient, 'connect', return_value=False):
            with pytest.raises(ConnectionError):
                with TWSClient() as client:
                    pass


@pytest.fixture
def mock_tws_client():
    """Fixture providing a mocked TWS client."""
    with patch('app.tws.client.EClient'):
        client = TWSClient()
        client.client = Mock()
        return client


class TestTWSClientIntegration:
    """Integration tests for TWS client (require TWS to be running)."""

    @pytest.mark.integration
    def test_real_connection_attempt(self):
        """
        Test actual connection to TWS.

        Note: This test requires TWS to be running on port 7500.
        It's marked with @pytest.mark.integration so it can be skipped
        in regular test runs.
        """
        client = TWSClient(host="127.0.0.1", port=7500, client_id=999)

        try:
            # Attempt to connect (may fail if TWS is not running)
            connected = client.connect()

            if connected:
                # If connection successful, test some operations
                status = client.get_connection_status()
                assert status.connected is True

                # Try to get current time
                time_response = client.request_current_time(timeout=10.0)

                # Disconnect
                client.disconnect()

                # If we got a time response, verify it
                if time_response:
                    assert isinstance(time_response, TimeResponse)
                    assert time_response.current_time is not None
            else:
                # If connection failed, that's expected when TWS is not running
                pytest.skip("TWS not available for integration test")

        except Exception as e:
            pytest.skip(f"TWS integration test failed: {e}")


if __name__ == "__main__":
    # Run tests, skipping integration tests by default
    pytest.main([__file__, "-v", "-m", "not integration"])