from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

class VibrantMindsGameDetails(BaseModel):
    """Model for VibrantMinds game details within a session."""
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

class VibrantMindsPerformanceMetrics(BaseModel):
    """Model for VibrantMinds performance metrics within a session."""
    selections: int = 0
    deselections: int = 0
    correct_matches: int = 0
    incorrect_matches: int = 0
    clicked_unselectable: int = 0
    hints_enabled: bool = False
    hints_used: int = 0
    times_shuffled: int = 0
    num_types: int = 0

class VibrantMindsMove(BaseModel):
    """Model for individual VibrantMinds moves within a session."""
    move_number: str
    type: str
    tiles: Optional[str] = None
    positions: Optional[str] = None
    time: Optional[str] = None
    description: str

class VibrantMindsSessionData(BaseModel):
    """Model for formatted VibrantMinds session data."""
    session_id: int
    session_date: datetime
    score: int
    activity: str
    organization: str
    participant: str
    game_details: VibrantMindsGameDetails
    performance_metrics: VibrantMindsPerformanceMetrics
    moves: List[VibrantMindsMove]

class VibrantMindsSessionSummary(BaseModel):
    """Model for VibrantMinds session summary data."""
    total_sessions: int
    total_score: int
    average_score: float
    participant: str
    activity: str

class VibrantMindsReadableSession(BaseModel):
    """Model for human-readable VibrantMinds session format."""
    session_info: Dict[str, Any]
    game_details: Dict[str, Any]
    performance: Dict[str, Any]
    moves_summary: Dict[str, Any]

class VibrantMindsSessionsResponse(BaseModel):
    """Model for VibrantMinds API response containing sessions."""
    summary: VibrantMindsSessionSummary
    sessions: List[VibrantMindsReadableSession]

class VibrantMindsSessionsDataRequest(BaseModel):
    """Model for incoming VibrantMinds session data to be formatted."""
    sessions: List[List] 