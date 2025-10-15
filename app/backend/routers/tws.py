"""
TWS API router for Interactive Brokers operations.
"""

import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from ..models import TimeResponseAPI, ConnectionStatusAPI
from ...tws.client import TWSClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tws", tags=["TWS"])

# Global TWS client instance
_tws_client: TWSClient = None


def get_tws_client() -> TWSClient:
    """Dependency to get the TWS client instance."""
    global _tws_client
    if _tws_client is None:
        _tws_client = TWSClient(host="127.0.0.1", port=7500, client_id=1)
    return _tws_client


@router.get("/current-time", response_model=TimeResponseAPI)
async def get_current_time(tws_client: TWSClient = Depends(get_tws_client)) -> TimeResponseAPI:
    """
    Request current time from TWS.

    Returns:
        TimeResponseAPI: Response containing current time or error information
    """
    try:
        logger.info("Processing current time request")

        # Connect if not already connected
        if not tws_client.is_connected():
            logger.info("TWS not connected, attempting to connect...")
            if not tws_client.connect():
                logger.error("Failed to connect to TWS")
                return TimeResponseAPI(
                    success=False,
                    error_message="Failed to connect to TWS. Ensure TWS is running on port 7500."
                )

        # Request current time
        time_response = tws_client.request_current_time()

        if time_response:
            logger.info(f"Successfully retrieved time: {time_response.current_time}")
            return TimeResponseAPI(
                success=True,
                current_time=time_response.current_time,
                server_version=time_response.server_version,
                connection_time=time_response.connection_time
            )
        else:
            logger.error("Failed to retrieve current time from TWS")
            return TimeResponseAPI(
                success=False,
                error_message="Failed to retrieve current time from TWS"
            )

    except Exception as e:
        logger.error(f"Error in get_current_time: {e}")
        return TimeResponseAPI(
            success=False,
            error_message=f"Internal server error: {str(e)}"
        )


@router.get("/connection-status", response_model=ConnectionStatusAPI)
async def get_connection_status(tws_client: TWSClient = Depends(get_tws_client)) -> ConnectionStatusAPI:
    """
    Get TWS connection status.

    Returns:
        ConnectionStatusAPI: Current connection status
    """
    try:
        status = tws_client.get_connection_status()
        return ConnectionStatusAPI(
            connected=status.connected,
            client_id=status.client_id,
            host=status.host,
            port=status.port,
            connection_time=status.connection_time,
            error_message=status.error_message
        )
    except Exception as e:
        logger.error(f"Error getting connection status: {e}")
        return ConnectionStatusAPI(
            connected=False,
            client_id=0,
            host="unknown",
            port=0,
            error_message=f"Error getting status: {str(e)}"
        )


@router.post("/connect")
async def connect_to_tws(tws_client: TWSClient = Depends(get_tws_client)) -> JSONResponse:
    """
    Connect to TWS.

    Returns:
        JSONResponse: Connection result
    """
    try:
        if tws_client.is_connected():
            return JSONResponse(
                content={"success": True, "message": "Already connected to TWS"},
                status_code=200
            )

        logger.info("Attempting to connect to TWS...")
        if tws_client.connect():
            logger.info("Successfully connected to TWS")
            return JSONResponse(
                content={"success": True, "message": "Successfully connected to TWS"},
                status_code=200
            )
        else:
            logger.error("Failed to connect to TWS")
            return JSONResponse(
                content={"success": False, "message": "Failed to connect to TWS"},
                status_code=503
            )

    except Exception as e:
        logger.error(f"Error connecting to TWS: {e}")
        return JSONResponse(
            content={"success": False, "message": f"Error connecting: {str(e)}"},
            status_code=500
        )


@router.post("/disconnect")
async def disconnect_from_tws(tws_client: TWSClient = Depends(get_tws_client)) -> JSONResponse:
    """
    Disconnect from TWS.

    Returns:
        JSONResponse: Disconnection result
    """
    try:
        tws_client.disconnect()
        logger.info("Disconnected from TWS")
        return JSONResponse(
            content={"success": True, "message": "Disconnected from TWS"},
            status_code=200
        )

    except Exception as e:
        logger.error(f"Error disconnecting from TWS: {e}")
        return JSONResponse(
            content={"success": False, "message": f"Error disconnecting: {str(e)}"},
            status_code=500
        )