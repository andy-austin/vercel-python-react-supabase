import strawberry

from ..resolvers.health import HealthResolver
from ..types.health import DatabaseStatus, HealthStatus, ServiceStatus


@strawberry.type
class HealthQueries:
    @strawberry.field
    def health(self) -> HealthStatus:
        health_data = HealthResolver.get_health_status()

        return HealthStatus(
            status=health_data["status"],
            timestamp=health_data["timestamp"],
            api=ServiceStatus(status=health_data["api"]["status"]),
            database=DatabaseStatus(
                status=health_data["database"]["status"],
                connection=health_data["database"]["connection"],
                details=health_data["database"]["details"],
            ),
        )
