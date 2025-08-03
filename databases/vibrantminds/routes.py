from fastapi import APIRouter, HTTPException
from typing import Dict, List
from databases.vibrantminds.service import VibrantMindsService
from databases.vibrantminds.models import VibrantMindsSessionsDataRequest

router = APIRouter(prefix="/vibrantminds", tags=["vibrantminds"])

@router.get("/users")
def get_vibrantminds_users():
    """Get all users from the VibrantMinds database."""
    try:
        users = VibrantMindsService.get_users()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/sessions")
def get_vibrantminds_sessions():
    """Get raw session data from VibrantMinds database."""
    try:
        rows = VibrantMindsService.get_raw_sessions()
        return {"sessions": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/sessions/readable")
def get_vibrantminds_readable_sessions():
    """Get sessions from VibrantMinds database in a human-readable format without moves."""
    try:
        raw_sessions = VibrantMindsService.get_raw_sessions()
        formatted_sessions = VibrantMindsService.format_session_data_without_moves(raw_sessions)
        readable_summary = VibrantMindsService.create_readable_summary(formatted_sessions, include_moves=False)
        return readable_summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing sessions: {str(e)}")

@router.get("/sessions/readable/extra")
def get_vibrantminds_readable_sessions_with_moves():
    """Get sessions from VibrantMinds database in a human-readable format with moves."""
    try:
        raw_sessions = VibrantMindsService.get_raw_sessions()
        formatted_sessions = VibrantMindsService.format_session_data(raw_sessions)
        readable_summary = VibrantMindsService.create_readable_summary(formatted_sessions, include_moves=True)
        return readable_summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing sessions: {str(e)}")

@router.post("/sessions/format")
def format_vibrantminds_sessions_without_moves(sessions_data: VibrantMindsSessionsDataRequest):
    """Format provided VibrantMinds session data into readable format, ignoring moves data and preserving variable names."""
    try:
        formatted_sessions = VibrantMindsService.format_session_data_without_moves(sessions_data.sessions)
        return {
            "total_sessions": len(formatted_sessions),
            "sessions": formatted_sessions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error formatting sessions: {str(e)}")

@router.post("/sessions/format/extra")
def format_vibrantminds_sessions_with_moves(sessions_data: VibrantMindsSessionsDataRequest):
    """Format provided VibrantMinds session data into readable format with moves."""
    try:
        formatted_sessions = VibrantMindsService.format_session_data(sessions_data.sessions)
        return {
            "total_sessions": len(formatted_sessions),
            "sessions": formatted_sessions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error formatting sessions: {str(e)}") 