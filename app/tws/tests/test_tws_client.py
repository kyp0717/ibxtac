"""Unit tests for TWSClient class.

This module contains unit tests for the TWS client wrapper,
including initialization, connection handling, and callback methods.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path to import tws_client
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tws_client import TWSClient


class TestTWSClientInitialization(unittest.TestCase):
    """Test cases for TWSClient initialization."""

    def test_client_initialization_with_defaults(self):
        """Test that TWSClient initializes with correct default values."""
        client = TWSClient()

        self.assertEqual(client.host, "localhost")
        self.assertEqual(client.port, 7500)
        self.assertEqual(client.client_id, 1)
        self.assertIsNone(client.current_time)
        self.assertFalse(client.is_connected)
        self.assertIsNone(client.next_valid_order_id)

    def test_client_initialization_with_custom_values(self):
        """Test that TWSClient initializes with custom values."""
        client = TWSClient(host="192.168.1.100", port=7497, client_id=5)

        self.assertEqual(client.host, "192.168.1.100")
        self.assertEqual(client.port, 7497)
        self.assertEqual(client.client_id, 5)

    def test_client_inherits_from_eclient_and_ewrapper(self):
        """Test that TWSClient properly inherits from EClient and EWrapper."""
        from ibapi.client import EClient
        from ibapi.wrapper import EWrapper

        client = TWSClient()

        self.assertIsInstance(client, EClient)
        self.assertIsInstance(client, EWrapper)


class TestTWSClientCallbacks(unittest.TestCase):
    """Test cases for TWSClient callback methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = TWSClient()

    def test_next_valid_id_callback(self):
        """Test nextValidId callback updates state correctly."""
        self.assertFalse(self.client.is_connected)
        self.assertIsNone(self.client.next_valid_order_id)

        # Simulate callback
        self.client.nextValidId(100)

        self.assertTrue(self.client.is_connected)
        self.assertEqual(self.client.next_valid_order_id, 100)

    def test_current_time_callback(self):
        """Test currentTime callback stores time correctly."""
        self.assertIsNone(self.client.current_time)

        # Simulate callback with Unix timestamp
        test_timestamp = 1609459200  # 2021-01-01 00:00:00 UTC
        self.client.currentTime(test_timestamp)

        self.assertEqual(self.client.current_time, test_timestamp)

    def test_error_callback_with_info_code(self):
        """Test error callback handles informational messages."""
        # Should not raise exception for info codes
        try:
            self.client.error(reqId=-1, errorCode=2104, errorString="Market data farm connection is OK")
            self.client.error(reqId=-1, errorCode=2106, errorString="HMDS data farm connection is OK")
            self.client.error(reqId=-1, errorCode=2158, errorString="Sec-def data farm connection is OK")
        except Exception as e:
            self.fail(f"Error callback raised exception for info code: {e}")

    def test_error_callback_with_error_code(self):
        """Test error callback handles actual errors."""
        # Should log error but not raise exception
        try:
            self.client.error(reqId=1, errorCode=502, errorString="Couldn't connect to TWS")
        except Exception as e:
            self.fail(f"Error callback raised unexpected exception: {e}")


class TestTWSClientConnectionMethods(unittest.TestCase):
    """Test cases for TWSClient connection methods."""

    def test_connect_and_run_method_exists(self):
        """Test that connect_and_run method exists and is callable."""
        client = TWSClient()
        self.assertTrue(hasattr(client, 'connect_and_run'))
        self.assertTrue(callable(client.connect_and_run))

    def test_disconnect_gracefully_method_exists(self):
        """Test that disconnect_gracefully method exists and is callable."""
        client = TWSClient()
        self.assertTrue(hasattr(client, 'disconnect_gracefully'))
        self.assertTrue(callable(client.disconnect_gracefully))

    @patch('tws_client.threading.Thread')
    @patch.object(TWSClient, 'connect')
    @patch.object(TWSClient, 'run')
    def test_connect_and_run_starts_thread(self, mock_run, mock_connect, mock_thread):
        """Test that connect_and_run starts a thread for the message loop."""
        client = TWSClient()

        # Mock the thread
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        # Simulate successful connection
        def set_connected(*args, **kwargs):
            client.is_connected = True

        mock_connect.side_effect = set_connected

        result = client.connect_and_run(timeout=1)

        # Verify thread was created and started
        mock_thread.assert_called_once()
        mock_thread_instance.start.assert_called_once()

    @patch.object(TWSClient, 'isConnected')
    @patch.object(TWSClient, 'disconnect')
    def test_disconnect_gracefully_when_connected(self, mock_disconnect, mock_is_connected):
        """Test disconnect_gracefully when client is connected."""
        client = TWSClient()
        client.is_connected = True
        mock_is_connected.return_value = True

        client.disconnect_gracefully()

        mock_disconnect.assert_called_once()
        self.assertFalse(client.is_connected)

    @patch.object(TWSClient, 'isConnected')
    @patch.object(TWSClient, 'disconnect')
    def test_disconnect_gracefully_when_not_connected(self, mock_disconnect, mock_is_connected):
        """Test disconnect_gracefully when client is not connected."""
        client = TWSClient()
        client.is_connected = False
        mock_is_connected.return_value = False

        client.disconnect_gracefully()

        mock_disconnect.assert_not_called()


class TestTWSClientConnectionFailure(unittest.TestCase):
    """Test cases for connection failure scenarios."""

    @patch('tws_client.threading.Thread')
    @patch.object(TWSClient, 'connect')
    def test_connect_and_run_timeout(self, mock_connect, mock_thread):
        """Test that connect_and_run returns False on timeout."""
        client = TWSClient()

        # Mock thread
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        # Don't set is_connected to simulate timeout
        result = client.connect_and_run(timeout=0.1)

        self.assertFalse(result)
        self.assertFalse(client.is_connected)

    @patch('tws_client.threading.Thread')
    @patch.object(TWSClient, 'connect')
    def test_connect_and_run_exception_handling(self, mock_connect, mock_thread):
        """Test that connect_and_run handles exceptions gracefully."""
        client = TWSClient()

        # Simulate connection exception
        mock_connect.side_effect = Exception("Connection refused")

        result = client.connect_and_run(timeout=1)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
