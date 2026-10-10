from enum import Enum


class UserRole(str, Enum):
    EMPLOYEE = "employee"
    TECHNICIAN = "technician"
    ADMIN = "admin"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TicketStatus(str, Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REOPENED = "reopened"


class TicketCategory(str, Enum):
    NETWORK = "network"
    HARDWARE = "hardware"
    SOFTWARE = "software"
    IDENTITY = "identity"
    FACILITIES = "facilities"


class CommentVisibility(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"


class AssetStatus(str, Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    UNDER_REPAIR = "under_repair"
    RETIRED = "retired"


class SLAEventType(str, Enum):
    RESPONSE_DEADLINE = "response_deadline"
    RESOLUTION_DEADLINE = "resolution_deadline"
    WARNING = "warning"
    BREACH = "breach"
    COMPLIED = "complied"


class NotificationType(str, Enum):
    INFO = "info"
    SLA_WARNING = "sla_warning"
    SLA_BREACH = "sla_breach"


class HistoryEventType(str, Enum):
    CREATED = "created"
    STATUS_CHANGED = "status_changed"
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    PRIORITY_CHANGED = "priority_changed"
    COMMENT_ADDED = "comment_added"
    RESOLVED = "resolved"
    REOPENED = "reopened"
    CLOSED = "closed"
    EDITED = "edited"