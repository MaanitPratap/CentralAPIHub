import json
from typing import List, Dict, Any
from config.database import DatabaseConfig

class Service:
    """Service class for handling session data operations."""
    
    @staticmethod
    def get_raw_sessions() -> List[List]:
        """Get raw session data from database."""
        conn = DatabaseConfig.get_vibrantminds_connection()
        cur = conn.cursor()

        query = """
        SELECT 
            s.id AS session_id,
            s.session_date,
            s.score,
            s.session_info,
            s.settings,
            a.name AS activity_name,
            o.name AS organization_name,
            p.email AS participant_name
        FROM 
            public.vm2_backend_session s
        LEFT JOIN public.vm2_backend_activity a ON s.activity_id = a.id
        JOIN public.vm2_backend_organization o ON s.organization_id = o.user_id
        JOIN public.vm2_backend_participant p ON s.participant_id = p.user_id;
        """

        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return rows

    @staticmethod
    def get_users() -> List[List]:
        """Get users from database."""
        conn = DatabaseConfig.get_vibrantminds_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users;")
        users = cur.fetchall()
        cur.close()
        conn.close()
        return users

    @staticmethod
    def parse_session_info(session_info_str: str) -> Dict[str, Any]:
        """Parse the session_info JSON string into a structured format."""
        try:
            return json.loads(session_info_str)
        except (json.JSONDecodeError, TypeError):
            return {"error": "Could not parse session info"}

    @staticmethod
    def format_moves(moves_dict: Dict[str, str]) -> List[Dict[str, str]]:
        """Format moves into a more readable structure."""
        formatted_moves = []
        for move_key, move_description in moves_dict.items():
            # Extract move number from key (e.g., "selection 2" -> 2)
            move_num = move_key.split()[-1] if " " in move_key else move_key
            
            # Parse the move description more carefully
            if "SUCCESSFUL MATCH" in move_description:
                try:
                    # Split by ": " to get the part after "SUCCESSFUL MATCH: "
                    match_part = move_description.split("SUCCESSFUL MATCH: ")[1]
                    # Split by ", " to separate tiles, positions, and time
                    parts = match_part.split(", ")
                    
                    tiles = parts[0] if len(parts) > 0 else ""
                    positions = parts[1] if len(parts) > 1 else ""
                    time = parts[2] if len(parts) > 2 else ""
                    
                    formatted_moves.append({
                        "move_number": move_num,
                        "type": "successful_match",
                        "tiles": tiles,
                        "positions": positions,
                        "time": time,
                        "description": move_description
                    })
                except (IndexError, AttributeError):
                    formatted_moves.append({
                        "move_number": move_num,
                        "type": "successful_match",
                        "description": move_description
                    })
            elif "Mismatch" in move_description:
                try:
                    # Split by ": " to get the part after "Mismatch: "
                    mismatch_part = move_description.split("Mismatch: ")[1]
                    # Split by ", " to separate tiles, positions, and time
                    parts = mismatch_part.split(", ")
                    
                    tiles = parts[0] if len(parts) > 0 else ""
                    positions = parts[1] if len(parts) > 1 else ""
                    time = parts[2] if len(parts) > 2 else ""
                    
                    formatted_moves.append({
                        "move_number": move_num,
                        "type": "mismatch",
                        "tiles": tiles,
                        "positions": positions,
                        "time": time,
                        "description": move_description
                    })
                except (IndexError, AttributeError):
                    formatted_moves.append({
                        "move_number": move_num,
                        "type": "mismatch",
                        "description": move_description
                    })
            else:
                formatted_moves.append({
                    "move_number": move_num,
                    "type": "other",
                    "description": move_description
                })
        
        return formatted_moves

    @staticmethod
    def format_session_data(raw_sessions: List[List]) -> List[Dict[str, Any]]:
        """Convert raw session data into a nicely formatted structure."""
        formatted_sessions = []
        
        for session in raw_sessions:
            session_id, session_date, score, session_info_str, settings, activity_name, organization_name, participant_email = session
            
            # Parse session info
            session_info = Service.parse_session_info(session_info_str)
            
            # Format the session data
            formatted_session = {
                "session_id": session_id,
                "session_date": session_date,
                "score": score,
                "activity": activity_name,
                "organization": organization_name,
                "participant": participant_email,
                "game_details": {
                    "tileset": session_info.get("tileset", "Unknown"),
                    "level": session_info.get("level", 0),
                    "total_levels": session_info.get("totalLevels", 0),
                    "package": session_info.get("package", "Unknown"),
                    "layout": session_info.get("layout", "Unknown"),
                    "completion_status": session_info.get("completion", "Unknown"),
                    "duration_seconds": session_info.get("duration", 0),
                    "start_time": session_info.get("startGameTime", 0),
                    "end_time": session_info.get("endGameTime", 0),
                    "is_level_timeout": session_info.get("isLevelTimeout", False)
                },
                "performance_metrics": {
                    "selections": session_info.get("selections", 0),
                    "deselections": session_info.get("deselections", 0),
                    "correct_matches": session_info.get("correctMatches", 0),
                    "incorrect_matches": session_info.get("incorrectMatches", 0),
                    "clicked_unselectable": session_info.get("clicked_unselectable", 0),
                    "hints_enabled": session_info.get("hintsEnabled", False),
                    "hints_used": session_info.get("hintsUsed", 0),
                    "times_shuffled": session_info.get("timesShuffled", 0),
                    "num_types": session_info.get("numTypes", 0)
                },
                "moves": Service.format_moves(session_info.get("moves", {}))
            }
            
            formatted_sessions.append(formatted_session)
        
        return formatted_sessions

    @staticmethod
    def format_session_data_without_moves(raw_sessions: List[List]) -> List[Dict[str, Any]]:
        """Convert raw session data into a nicely formatted structure, ignoring moves data and preserving all variable names."""
        formatted_sessions = []
        
        for session in raw_sessions:
            session_id, session_date, score, session_info_str, settings, activity_name, organization_name, participant_email = session
            
            # Parse session info
            session_info = Service.parse_session_info(session_info_str)
            
            # Create a copy of session_info without the moves data
            session_info_without_moves = {}
            for key, value in session_info.items():
                if key != "moves":  # Ignore moves data
                    session_info_without_moves[key] = value
            
            # Format the session data while preserving all original variable names
            formatted_session = {
                "session_id": session_id,
                "session_date": session_date,
                "score": score,
                "activity": activity_name,
                "organization": organization_name,
                "participant": participant_email,
                "session_info": session_info_without_moves  # Include all session info except moves
            }
            
            formatted_sessions.append(formatted_session)
        
        return formatted_sessions

    @staticmethod
    def create_readable_summary(formatted_sessions: List[Dict[str, Any]], include_moves: bool = True) -> Dict[str, Any]:
        """Create a readable summary from formatted sessions."""
        if not formatted_sessions:
            return {
                "summary": {
                    "total_sessions": 0,
                    "total_score": 0,
                    "average_score": 0,
                    "participant": "Unknown",
                    "activity": "Unknown"
                },
                "sessions": []
            }

        # Create a more readable summary
        readable_summary = {
            "summary": {
                "total_sessions": len(formatted_sessions),
                "total_score": sum(session["score"] for session in formatted_sessions),
                "average_score": round(sum(session["score"] for session in formatted_sessions) / len(formatted_sessions), 2),
                "participant": formatted_sessions[0]["participant"],
                "activity": formatted_sessions[0]["activity"]
            },
            "sessions": []
        }
        
        for session in formatted_sessions:
            if include_moves:
                # Create a more readable session format with moves
                readable_session = {
                    "session_info": {
                        "id": session["session_id"],
                        "date": session["session_date"],
                        "score": session["score"],
                        "activity": session["activity"],
                        "participant": session["participant"]
                    },
                    "game_details": {
                        "level": f"Level {session['game_details']['level']} of {session['game_details']['total_levels']}",
                        "tileset": session["game_details"]["tileset"],
                        "package": session["game_details"]["package"],
                        "layout": session["game_details"]["layout"],
                        "status": session["game_details"]["completion_status"],
                        "duration": f"{session['game_details']['duration_seconds']} seconds"
                    },
                    "performance": {
                        "matches": {
                            "correct": session["performance_metrics"]["correct_matches"],
                            "incorrect": session["performance_metrics"]["incorrect_matches"],
                            "accuracy": f"{round(session['performance_metrics']['correct_matches'] / (session['performance_metrics']['correct_matches'] + session['performance_metrics']['incorrect_matches']) * 100, 1)}%" if (session['performance_metrics']['correct_matches'] + session['performance_metrics']['incorrect_matches']) > 0 else "0%"
                        },
                        "actions": {
                            "selections": session["performance_metrics"]["selections"],
                            "deselections": session["performance_metrics"]["deselections"],
                            "hints_used": session["performance_metrics"]["hints_used"],
                            "shuffles": session["performance_metrics"]["times_shuffled"]
                        }
                    },
                    "moves_summary": {
                        "total_moves": len(session["moves"]),
                        "successful_matches": len([move for move in session["moves"] if move["type"] == "successful_match"]),
                        "mismatches": len([move for move in session["moves"] if move["type"] == "mismatch"]),
                    }
                }
            else:
                # Create a readable session format without moves
                readable_session = {
                    "session_info": {
                        "id": session["session_id"],
                        "date": session["session_date"],
                        "score": session["score"],
                        "activity": session["activity"],
                        "participant": session["participant"],
                        "organization": session["organization"]
                    },
                    "game_data": session["session_info"]  # Include all session info except moves
                }
            
            readable_summary["sessions"].append(readable_session)
        
        return readable_summary 