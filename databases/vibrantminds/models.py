from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

class GameDetails(BaseModel):
    """Model for game details within a session."""
    tileset: str = "Unknown"
    level: int = 0
    total_levels: int = 0
    package: str = "Unknown"
    layout: str = "Unknown"
    completion_status: str = "Unknown"
    duration_seconds: int = 0
    start_time: int = 0
    end_time: int = 0
    is_level_timeout: bool = False

class PerformanceMetrics(BaseModel):
    """Model for performance metrics within a session."""
    selections: int = 0
    deselections: int = 0
    correct_matches: int = 0
    incorrect_matches: int = 0
    clicked_unselectable: int = 0
    hints_enabled: bool = False
    hints_used: int = 0
    times_shuffled: int = 0
    num_types: int = 0

class Move(BaseModel):
    """Model for individual moves within a session."""
    move_number: str
    type: str
    tiles: Optional[str] = None
    positions: Optional[str] = None
    time: Optional[str] = None
    description: str

class SessionData(BaseModel):
    """Model for formatted session data."""
    session_id: int
    session_date: datetime
    score: int
    activity: str
    organization: str
    participant: str
    game_details: GameDetails
    performance_metrics: PerformanceMetrics
    moves: List[Move]

class SessionSummary(BaseModel):
    """Model for session summary data."""
    total_sessions: int
    total_score: int
    average_score: float
    participant: str
    activity: str

class ReadableSession(BaseModel):
    """Model for human-readable session format."""
    session_info: Dict[str, Any]
    game_details: Dict[str, Any]
    performance: Dict[str, Any]
    moves_summary: Dict[str, Any]

class SessionsResponse(BaseModel):
    """Model for API response containing sessions."""
    summary: SessionSummary
    sessions: List[ReadableSession]

class SessionsDataRequest(BaseModel):
    """Model for incoming session data to be formatted."""
    sessions: List[List] 