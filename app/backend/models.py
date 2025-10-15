"""
Pydantic models for API requests and responses.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TimeResponseAPI(BaseModel):
    """API response model for current time request."""

    success: bool
    current_time: Optional[datetime] = None
    server_version: Optional[int] = None
    connection_time: Optional[datetime] = None
    error_message: Optional[str] = None

    model_config = {"json_encoders": {datetime: lambda v: v.isoformat()}}


class ConnectionStatusAPI(BaseModel):
    """API response model for connection status."""

    connected: bool
    client_id: int
    host: str
    port: int
    connection_time: Optional[datetime] = None
    error_message: Optional[str] = None


class HealthResponse(BaseModel):
    """API response model for health check."""

    status: str
    version: str
    timestamp: datetime
    tws_connected: bool