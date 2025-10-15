"""
TWS client implementation for connecting to Interactive Brokers TWS.
"""

import logging
import threading
import time
from datetime import datetime
from typing import Optional, Callable

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from .models import TimeResponse, ConnectionStatus

logger = logging.getLogger(__name__)


class TWSWrapper(EWrapper):
    """Wrapper class that handles callbacks from TWS."""

    def __init__(self):
        EWrapper.__init__(self)
        self.current_time: Optional[datetime] = None
        self.server_version: Optional[int] = None
        self.connection_time: Optional[datetime] = None
        self.error_message: Optional[str] = None
        self._time_received_event = threading.Event()

    def currentTime(self, time: int) -> None:
        """Callback for receiving current time from TWS."""
        self.current_time = datetime.fromtimestamp(time)
        logger.info(f"Received current time from TWS: {self.current_time}")
        self._time_received_event.set()

    def error(self, reqId: int, errorCode: int, errorString: str, advancedOrderRejectJson: str = "") -> None:
        """Callback for error messages from TWS."""
        error_msg = f"TWS Error {errorCode}: {errorString}"
        logger.error(error_msg)
        self.error_message = error_msg
        if errorCode in [1100, 1101, 1102]:  # Connection lost errors
            self._time_received_event.set()

    def connectAck(self) -> None:
        """Callback when connection is acknowledged."""
        self.connection_time = datetime.now()
        logger.info("TWS connection acknowledged")

    def nextValidId(self, orderId: int) -> None:
        """Callback when next valid order ID is received."""
        logger.info(f"Next valid order ID: {orderId}")

    def wait_for_time(self, timeout: float = 5.0) -> bool:
        """Wait for time response with timeout."""
        return self._time_received_event.wait(timeout)

    def reset_time_event(self) -> None:
        """Reset the time received event."""
        self._time_received_event.clear()
        self.current_time = None
        self.error_message = None


class TWSClient:
    """Main TWS client for connecting to Interactive Brokers TWS."""

    def __init__(self, host: str = "127.0.0.1", port: int = 7500, client_id: int = 1):
        """
        Initialize TWS client.

        Args:
            host: TWS host address
            port: TWS port number (usually 7496 for live, 7497 for paper)
            client_id: Unique client identifier
        """
        self.host = host
        self.port = port
        self.client_id = client_id

        self.wrapper = TWSWrapper()
        self.client = EClient(self.wrapper)
        self._connection_thread: Optional[threading.Thread] = None
        self._connected = False

    def connect(self) -> bool:
        """
        Connect to TWS.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            logger.info(f"Connecting to TWS at {self.host}:{self.port} with client ID {self.client_id}")
            self.client.connect(self.host, self.port, self.client_id)

            # Start the client in a separate thread
            self._connection_thread = threading.Thread(target=self.client.run, daemon=True)
            self._connection_thread.start()

            # Wait a moment for connection to establish
            time.sleep(1)

            if self.client.isConnected():
                self._connected = True
                logger.info("Successfully connected to TWS")
                return True
            else:
                logger.error("Failed to connect to TWS")
                return False

        except Exception as e:
            logger.error(f"Error connecting to TWS: {e}")
            return False

    def disconnect(self) -> None:
        """Disconnect from TWS."""
        try:
            if self.client.isConnected():
                self.client.disconnect()
                self._connected = False
                logger.info("Disconnected from TWS")

            if self._connection_thread and self._connection_thread.is_alive():
                self._connection_thread.join(timeout=2)

        except Exception as e:
            logger.error(f"Error disconnecting from TWS: {e}")

    def is_connected(self) -> bool:
        """Check if client is connected to TWS."""
        return self._connected and self.client.isConnected()

    def get_connection_status(self) -> ConnectionStatus:
        """Get current connection status."""
        return ConnectionStatus(
            connected=self.is_connected(),
            client_id=self.client_id,
            host=self.host,
            port=self.port,
            connection_time=self.wrapper.connection_time,
            error_message=self.wrapper.error_message
        )

    def request_current_time(self, timeout: float = 5.0) -> Optional[TimeResponse]:
        """
        Request current time from TWS.

        Args:
            timeout: Timeout in seconds for the request

        Returns:
            TimeResponse if successful, None otherwise
        """
        if not self.is_connected():
            logger.error("Not connected to TWS")
            return None

        try:
            # Reset previous time data
            self.wrapper.reset_time_event()

            # Request current time
            logger.info("Requesting current time from TWS")
            self.client.reqCurrentTime()

            # Wait for response
            if self.wrapper.wait_for_time(timeout):
                if self.wrapper.current_time and not self.wrapper.error_message:
                    return TimeResponse(
                        current_time=self.wrapper.current_time,
                        server_version=self.wrapper.server_version,
                        connection_time=self.wrapper.connection_time
                    )
                else:
                    logger.error(f"Error in time request: {self.wrapper.error_message}")
                    return None
            else:
                logger.error("Timeout waiting for time response from TWS")
                return None

        except Exception as e:
            logger.error(f"Error requesting current time: {e}")
            return None

    def __enter__(self):
        """Context manager entry."""
        if not self.connect():
            raise ConnectionError("Failed to connect to TWS")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()