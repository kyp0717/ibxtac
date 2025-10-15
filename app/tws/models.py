"""
Data models for TWS responses and structures.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TimeResponse(BaseModel):
    """Response model for current time request from TWS."""

    current_time: datetime
    server_version: Optional[int] = None
    connection_time: Optional[datetime] = None

    model_config = {"json_encoders": {datetime: lambda v: v.isoformat()}}


class ConnectionStatus(BaseModel):
    """Model representing TWS connection status."""

    connected: bool
    client_id: int
    host: str
    port: int
    connection_time: Optional[datetime] = None
    error_message: Optional[str] = None