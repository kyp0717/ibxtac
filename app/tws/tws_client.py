"""TWS Client wrapper class for Interactive Brokers API integration.

This module provides a client wrapper that extends both EClient and EWrapper
from the ibapi library to handle connections and communications with the
Interactive Brokers Trader Workstation (TWS) or IB Gateway.
"""

import logging
import threading
import time
from typing import Optional

from ibapi.client import EClient
from ibapi.wrapper import EWrapper


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TWSClient(EWrapper, EClient):
    """TWS Client that extends EClient and EWrapper for IB API communication.

    This class handles connection management, message processing, and callbacks
    for Interactive Brokers API operations. It implements the required callbacks
    for basic TWS operations including connection handling and time requests.

    Attributes:
        host: The hostname or IP address of the TWS/Gateway instance
        port: The port number for TWS/Gateway connection
        client_id: Unique identifier for this client connection
        current_time: The last received server time (Unix timestamp)
        is_connected: Connection status flag
        next_valid_order_id: Next valid order ID received from TWS
    """

    def __init__(self, host: str = "localhost", port: int = 7500, client_id: int = 1):
        """Initialize the TWS client.

        Args:
            host: TWS/Gateway hostname (default: localhost)
            port: TWS/Gateway port (default: 7500)
            client_id: Unique client identifier (default: 1)
        """
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

        self.host = host
        self.port = port
        self.client_id = client_id

        # State tracking
        self.current_time: Optional[int] = None
        self.is_connected = False
        self.next_valid_order_id: Optional[int] = None

        logger.info(f"TWSClient initialized with {host}:{port}, client_id={client_id}")

    def nextValidId(self, orderId: int):
        """Callback when connection is established and next valid order ID is received.

        This is typically the first callback received after successful connection.
        It indicates that the client is ready to start making requests.

        Args:
            orderId: The next valid order ID from TWS
        """
        self.next_valid_order_id = orderId
        self.is_connected = True
        logger.info(f"Connected successfully. Next valid order ID: {orderId}")

    def currentTime(self, time: int):
        """Callback to receive the current server time from TWS.

        Args:
            time: Unix timestamp of the current server time
        """
        self.current_time = time
        logger.info(f"Received current time from TWS: {time}")
        from datetime import datetime
        readable_time = datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"Current TWS server time: {readable_time}")

    def error(self, reqId: int, errorCode: int, errorString: str, advancedOrderRejectJson: str = ""):
        """Callback for error messages from TWS.

        Args:
            reqId: The request ID that generated the error (-1 for general errors)
            errorCode: The error code
            errorString: Description of the error
            advancedOrderRejectJson: Advanced order rejection details (if applicable)
        """
        # Error codes 2104, 2106, 2158 are informational messages, not actual errors
        if errorCode in [2104, 2106, 2158]:
            logger.info(f"TWS Info [{errorCode}]: {errorString}")
        else:
            logger.error(f"TWS Error [{errorCode}] (Request ID: {reqId}): {errorString}")

    def connect_and_run(self, timeout: int = 10) -> bool:
        """Establish connection to TWS and start the message processing loop.

        This method connects to TWS/Gateway and runs the message processing loop
        in a separate thread to allow for non-blocking operations.

        Args:
            timeout: Maximum seconds to wait for connection (default: 10)

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            logger.info(f"Connecting to TWS at {self.host}:{self.port}...")
            self.connect(self.host, self.port, self.client_id)

            # Start the message processing loop in a separate thread
            api_thread = threading.Thread(target=self.run, daemon=True)
            api_thread.start()

            # Wait for connection to be established
            start_time = time.time()
            while not self.is_connected and (time.time() - start_time) < timeout:
                time.sleep(0.1)

            if self.is_connected:
                logger.info("Connection established successfully")
                return True
            else:
                logger.error(f"Connection timeout after {timeout} seconds")
                return False

        except Exception as e:
            logger.error(f"Failed to connect to TWS: {e}")
            return False

    def disconnect_gracefully(self):
        """Disconnect from TWS gracefully."""
        if self.isConnected():
            logger.info("Disconnecting from TWS...")
            self.disconnect()
            self.is_connected = False
            logger.info("Disconnected successfully")
        else:
            logger.info("Already disconnected")
