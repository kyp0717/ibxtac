"""
Tests for TWS API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from ..main import app
from ..models import TimeResponseAPI, ConnectionStatusAPI
from ...tws.client import TWSClient
from ...tws.models import TimeResponse, ConnectionStatus


# Create test client
client = TestClient(app)


class TestTWSEndpoints:
    """Test class for TWS API endpoints."""

    def test_health_endpoint(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "timestamp" in data
        assert "tws_connected" in data

    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "version" in data

    @patch('app.backend.routers.tws._tws_client')
    def test_connection_status_success(self, mock_tws_client):
        """Test connection status endpoint with successful connection."""
        # Mock the connection status
        mock_status = ConnectionStatus(
            connected=True,
            client_id=1,
            host="127.0.0.1",
            port=7500,
            connection_time=None,
            error_message=None
        )
        mock_tws_client.get_connection_status.return_value = mock_status

        response = client.get("/api/tws/connection-status")
        assert response.status_code == 200

        data = response.json()
        assert data["connected"] is True
        assert data["client_id"] == 1
        assert data["host"] == "127.0.0.1"
        assert data["port"] == 7500

    @patch('app.backend.routers.tws._tws_client')
    def test_connection_status_failure(self, mock_tws_client):
        """Test connection status endpoint with connection failure."""
        # Mock a connection error
        mock_tws_client.get_connection_status.side_effect = Exception("Connection failed")

        response = client.get("/api/tws/connection-status")
        assert response.status_code == 200

        data = response.json()
        assert data["connected"] is False
        assert "error_message" in data

    @patch('app.backend.routers.tws._tws_client')
    def test_current_time_success(self, mock_tws_client):
        """Test current time endpoint with successful response."""
        from datetime import datetime

        # Mock successful connection and time response
        mock_tws_client.is_connected.return_value = True
        mock_time_response = TimeResponse(
            current_time=datetime(2023, 1, 1, 12, 0, 0),
            server_version=123,
            connection_time=datetime(2023, 1, 1, 11, 59, 0)
        )
        mock_tws_client.request_current_time.return_value = mock_time_response

        response = client.get("/api/tws/current-time")
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "current_time" in data
        assert data["server_version"] == 123

    @patch('app.backend.routers.tws._tws_client')
    def test_current_time_not_connected(self, mock_tws_client):
        """Test current time endpoint when not connected to TWS."""
        # Mock not connected and failed connection attempt
        mock_tws_client.is_connected.return_value = False
        mock_tws_client.connect.return_value = False

        response = client.get("/api/tws/current-time")
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is False
        assert "error_message" in data
        assert "Failed to connect to TWS" in data["error_message"]

    @patch('app.backend.routers.tws._tws_client')
    def test_current_time_request_failed(self, mock_tws_client):
        """Test current time endpoint when time request fails."""
        # Mock connected but failed time request
        mock_tws_client.is_connected.return_value = True
        mock_tws_client.request_current_time.return_value = None

        response = client.get("/api/tws/current-time")
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is False
        assert "error_message" in data

    @patch('app.backend.routers.tws._tws_client')
    def test_connect_endpoint_success(self, mock_tws_client):
        """Test connect endpoint with successful connection."""
        mock_tws_client.is_connected.return_value = False
        mock_tws_client.connect.return_value = True

        response = client.post("/api/tws/connect")
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True

    @patch('app.backend.routers.tws._tws_client')
    def test_connect_endpoint_already_connected(self, mock_tws_client):
        """Test connect endpoint when already connected."""
        mock_tws_client.is_connected.return_value = True

        response = client.post("/api/tws/connect")
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "Already connected" in data["message"]

    @patch('app.backend.routers.tws._tws_client')
    def test_connect_endpoint_failure(self, mock_tws_client):
        """Test connect endpoint with connection failure."""
        mock_tws_client.is_connected.return_value = False
        mock_tws_client.connect.return_value = False

        response = client.post("/api/tws/connect")
        assert response.status_code == 503

        data = response.json()
        assert data["success"] is False

    @patch('app.backend.routers.tws._tws_client')
    def test_disconnect_endpoint(self, mock_tws_client):
        """Test disconnect endpoint."""
        response = client.post("/api/tws/disconnect")
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        mock_tws_client.disconnect.assert_called_once()

    @patch('app.backend.routers.tws._tws_client')
    def test_disconnect_endpoint_with_error(self, mock_tws_client):
        """Test disconnect endpoint when disconnect fails."""
        mock_tws_client.disconnect.side_effect = Exception("Disconnect failed")

        response = client.post("/api/tws/disconnect")
        assert response.status_code == 500

        data = response.json()
        assert data["success"] is False


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment."""
    # Any global test setup can go here
    pass


if __name__ == "__main__":
    pytest.main([__file__])