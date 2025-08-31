from datetime import datetime
from typing import Optional

import strawberry


@strawberry.type
class ServiceStatus:
    status: str


@strawberry.type
class DatabaseStatus:
    status: str
    connection: bool
    details: Optional[str]


@strawberry.type
class HealthStatus:
    status: str
    timestamp: datetime
    api: ServiceStatus
    database: DatabaseStatus
