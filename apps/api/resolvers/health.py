from datetime import datetime, timezone
from typing import Any, Dict

from sqlalchemy import text
from sqlalchemy.orm import Session

from ..database import get_db


class HealthResolver:
    @classmethod
    def get_health_status(cls) -> Dict[str, Any]:
        """Get comprehensive health status including database connectivity"""
        health_data = {
            "status": "ok",
            "timestamp": datetime.now(timezone.utc),
            "api": {"status": "ok"},
            "database": {"status": "unknown", "connection": False, "details": None},
        }

        # Check database connectivity
        try:
            db: Session = next(get_db())
            try:
                # Simple query to test connection
                result = db.execute(text("SELECT 1")).scalar()
                if result == 1:
                    health_data["database"]["status"] = "ok"
                    health_data["database"]["connection"] = True
                    health_data["database"]["details"] = "Connected successfully"
                else:
                    health_data["database"]["status"] = "error"
                    health_data["database"]["details"] = "Unexpected query result"
                    health_data["status"] = "degraded"
            except Exception as db_error:
                health_data["database"]["status"] = "error"
                health_data["database"]["details"] = f"Database error: {str(db_error)}"
                health_data["status"] = "error"
            finally:
                db.close()
        except Exception as connection_error:
            health_data["database"]["status"] = "error"
            health_data["database"][
                "details"
            ] = f"Connection error: {str(connection_error)}"
            health_data["status"] = "error"

        return health_data
