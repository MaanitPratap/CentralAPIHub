import os
import psycopg2
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    """Database configuration and connection management."""
    
    @staticmethod
    def get_vibrantminds_connection():
        """Get connection to VibrantMinds database."""
        return psycopg2.connect(
            host=os.getenv("VIBRANTMINDS_HOST", "localhost"),
            port=int(os.getenv("VIBRANTMINDS_PORT", 5433)),
            database=os.getenv("VIBRANTMINDS_DATABASE", "vibrantminds"),
            user=os.getenv("VIBRANTMINDS_USER", "vm2"),
            password=os.getenv("VIBRANTMINDS_PASSWORD", "BC&i#6h9dLsYA7")
        )
    
    @staticmethod
    def get_other_db_connection():
        """Get connection to other database (for future use)."""
        return psycopg2.connect(
            host=os.getenv("OTHER_DB_HOST", "localhost"),
            port=int(os.getenv("OTHER_DB_PORT", 5432)),
            database=os.getenv("OTHER_DB_DATABASE", "other_db"),
            user=os.getenv("OTHER_DB_USER", "user"),
            password=os.getenv("OTHER_DB_PASSWORD", "password")
        )
    
    @staticmethod
    def get_connection_config(db_type: str = "vibrantminds") -> Dict[str, Any]:
        """Get database configuration for specified database type."""
        if db_type == "vibrantminds":
            return {
                "host": os.getenv("VIBRANTMINDS_HOST", "localhost"),
                "port": int(os.getenv("VIBRANTMINDS_PORT", 5433)),
                "database": os.getenv("VIBRANTMINDS_DATABASE", "vibrantminds"),
                "user": os.getenv("VIBRANTMINDS_USER", "vm2"),
                "password": os.getenv("VIBRANTMINDS_PASSWORD", "BC&i#6h9dLsYA7")
            }
        elif db_type == "other":
            return {
                "host": os.getenv("OTHER_DB_HOST", "localhost"),
                "port": int(os.getenv("OTHER_DB_PORT", 5432)),
                "database": os.getenv("OTHER_DB_DATABASE", "other_db"),
                "user": os.getenv("OTHER_DB_USER", "user"),
                "password": os.getenv("OTHER_DB_PASSWORD", "password")
            }
        else:
            raise ValueError(f"Unknown database type: {db_type}") 