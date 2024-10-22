from datetime import datetime
from typing import Any, Dict, List, Optional

import pydantic
from typing_extensions import TypeAlias

from pyairtable.models._base import AirtableModel, rebuild_models


class AuditLogResponse(AirtableModel):
    """
    Represents a page of audit log events.

    See `Audit log events <https://airtable.com/developers/web/api/audit-log-events>`__
    for more information on how to interpret this data structure.
    """

    events: List["AuditLogEvent"]
    pagination: Optional["AuditLogResponse.Pagination"] = None

    class Pagination(AirtableModel):
        next: Optional[str] = None
        previous: Optional[str] = None


class AuditLogEvent(AirtableModel):
    """
    Represents a single audit log event.

    See `Audit log events <https://airtable.com/developers/web/api/audit-log-events>`__
    for more information on how to interpret this data structure.

    To avoid namespace conflicts with the Pydantic library, the
    ``modelId`` and ``modelType`` fields from the Airtable API are
    represented as fields named ``object_id`` and ``object_type``.
    """

    id: str
    timestamp: datetime
    action: str
    actor: "AuditLogActor"
    object_id: str = pydantic.Field(alias="modelId")
    object_type: str = pydantic.Field(alias="modelType")
    payload: "AuditLogPayload"
    payload_version: str
    context: "AuditLogEvent.Context"
    origin: "AuditLogEvent.Origin"

    class Context(AirtableModel):
        base_id: Optional[str] = None
        action_id: str
        enterprise_account_id: str
        descendant_enterprise_account_id: Optional[str] = None
        interface_id: Optional[str] = None
        workspace_id: Optional[str] = None

    class Origin(AirtableModel):
        ip_address: str
        user_agent: str
        oauth_access_token_id: Optional[str] = None
        personal_access_token_id: Optional[str] = None
        session_id: Optional[str] = None


class AuditLogActor(AirtableModel):
    type: str
    user: Optional["AuditLogActor.UserInfo"] = None
    view_id: Optional[str] = None
    automation_id: Optional[str] = None

    class UserInfo(AirtableModel):
        id: str
        email: str
        name: Optional[str] = None


# Placeholder until we can parse https://airtable.com/developers/web/api/audit-log-event-types
AuditLogPayload: TypeAlias = Dict[str, Any]


rebuild_models(vars())
