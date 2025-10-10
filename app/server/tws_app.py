"""TWS Application - Main entry point for Interactive Brokers TWS integration.

This application connects to Interactive Brokers Trader Workstation (TWS) or
IB Gateway and requests the current server time to demonstrate basic connectivity
and API communication.

Usage:
    python tws_app.py [--host HOST] [--port PORT] [--client-id CLIENT_ID]

Example:
    python tws_app.py --host localhost --port 7500 --client-id 1
"""

import argparse
import logging
import signal
import sys
import time
from datetime import datetime

from tws_client import TWSClient


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Global client instance for signal handling
client_instance = None


def signal_handler(sig, frame):
    """Handle Ctrl+C for graceful shutdown.

    Args:
        sig: Signal number
        frame: Current stack frame
    """
    logger.info("\nReceived interrupt signal, shutting down gracefully...")
    if client_instance:
        client_instance.disconnect_gracefully()
    sys.exit(0)


def main():
    """Main application entry point."""
    global client_instance

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='TWS Application - Connect to Interactive Brokers and request current time',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Connect to localhost:7500 with client_id=1
  %(prog)s --host localhost --port 7497 # Connect to TWS paper trading
  %(prog)s --port 4002                  # Connect to IB Gateway paper trading

Port Options:
  7496 - TWS live trading
  7497 - TWS paper trading
  7500 - Custom port (default)
  4001 - IB Gateway live trading
  4002 - IB Gateway paper trading
        """
    )

    parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='TWS/Gateway host address (default: localhost)'
    )

    parser.add_argument(
        '--port',
        type=int,
        default=7500,
        help='TWS/Gateway port number (default: 7500)'
    )

    parser.add_argument(
        '--client-id',
        type=int,
        default=1,
        help='Client ID for this connection (default: 1)'
    )

    args = parser.parse_args()

    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Create TWS client instance
    logger.info("=" * 60)
    logger.info("TWS Application Starting")
    logger.info("=" * 60)

    client_instance = TWSClient(
        host=args.host,
        port=args.port,
        client_id=args.client_id
    )

    # Connect to TWS
    if not client_instance.connect_and_run():
        logger.error("Failed to connect to TWS. Please ensure:")
        logger.error("  1. TWS or IB Gateway is running")
        logger.error(f"  2. API connections are enabled on port {args.port}")
        logger.error("  3. The port number is correct for your TWS configuration")
        logger.error("  4. No firewall is blocking the connection")
        sys.exit(1)

    try:
        # Request current time from TWS
        logger.info("Requesting current time from TWS server...")
        client_instance.reqCurrentTime()

        # Wait for response (give it a few seconds)
        time.sleep(2)

        # Display results
        if client_instance.current_time:
            print("\n" + "=" * 60)
            print("SUCCESS: Connection to TWS established!")
            print("=" * 60)
            print(f"TWS Server Time (Unix Timestamp): {client_instance.current_time}")
            readable_time = datetime.fromtimestamp(client_instance.current_time).strftime('%Y-%m-%d %H:%M:%S %Z')
            print(f"TWS Server Time (Readable):       {readable_time}")
            print(f"Connection Host:                   {args.host}")
            print(f"Connection Port:                   {args.port}")
            print(f"Client ID:                         {args.client_id}")
            print("=" * 60)
        else:
            logger.warning("No time response received from TWS server")

        # Keep the connection alive for a moment to see any additional messages
        logger.info("Connection active. Press Ctrl+C to exit...")
        time.sleep(3)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

    finally:
        # Graceful disconnect
        client_instance.disconnect_gracefully()
        logger.info("TWS Application terminated")


if __name__ == "__main__":
    main()
