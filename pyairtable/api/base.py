import warnings
from typing import Any, Dict, List, Optional, Sequence, Union

import pyairtable.api.api
import pyairtable.api.table
from pyairtable.models.schema import BaseInfo, BaseSchema, BaseShare, PermissionLevel
from pyairtable.models.webhook import (
    CreateWebhook,
    CreateWebhookResponse,
    Webhook,
    WebhookSpecification,
)
from pyairtable.utils import enterprise_only


class Base:
    """
    Represents an Airtable base.
    """

    #: The connection to the Airtable API.
    api: "pyairtable.api.api.Api"

    #: The base ID, in the format ``appXXXXXXXXXXXXXX``
    id: str

    #: The permission level the current user has on the base
    permission_level: Optional[PermissionLevel]

    # Cached metadata to reduce API calls
    _info: Optional[BaseInfo] = None
    _schema: Optional[BaseSchema] = None
    _shares: Optional[List[BaseShare]] = None

    def __init__(
        self,
        api: Union["pyairtable.api.api.Api", str],
        base_id: str,
        *,
        name: Optional[str] = None,
        permission_level: Optional[PermissionLevel] = None,
    ):
        """
        Old style constructor takes ``str`` arguments, and will create its own
        instance of :class:`Api`.

        This approach is deprecated, and will likely be removed in the future.

            >>> Base("access_token", "base_id")

        New style constructor takes an instance of :class:`Api`:

            >>> Base(api, "table_name")

        Args:
            api: An instance of :class:`Api` or an Airtable access token.
            base_id: |arg_base_id|
        """
        if isinstance(api, str):
            warnings.warn(
                "Passing API keys to pyairtable.Base is deprecated; use Api.base() instead."
                " See https://pyairtable.rtfd.org/en/latest/migrations.html for details.",
                category=DeprecationWarning,
                stacklevel=2,
            )
            api = pyairtable.api.api.Api(api)

        self.api = api
        self.id = base_id
        self.permission_level = permission_level
        self._name = name

    @property
    def name(self) -> Optional[str]:
        """
        The name of the base, if provided to the constructor
        or available in cached base information.
        """
        if self._info:
            return self._info.name
        return self._name

    def __repr__(self) -> str:
        repr = f"<Base id={self.id!r}"
        if name := self.name:
            repr += f" {name=}"
        if permission_level := self.permission_level:
            repr += f" {permission_level=}"
        return repr + ">"

    def table(
        self,
        id_or_name: str,
        *,
        validate: bool = False,
    ) -> "pyairtable.api.table.Table":
        """
        Returns a new :class:`Table` instance using this instance of :class:`Base`.

        Args:
            id_or_name: An Airtable table ID or name. Table name should be unencoded,
                as shown on browser.
            validate: |kwarg_validate_metadata|

        Usage:
            >>> base.table('Apartments')
            <Table base='appLkNDICXNqxSDhG' name='Apartments'>
        """
        if validate:
            schema = self.schema(force=True).table(id_or_name)
            return pyairtable.api.table.Table(None, self, schema)
        return pyairtable.api.table.Table(None, self, id_or_name)

    def tables(self, *, force: bool = False) -> List["pyairtable.api.table.Table"]:
        """
        Retrieves the base's schema and returns a list of :class:`Table` instances.

        Args:
            force: |kwarg_force_metadata|

        Usage:
            >>> base.tables()
            [
                <Table base='appLkNDICXNqxSDhG' id='tbltp8DGLhqbUmjK1' name='Apartments'>,
                <Table base='appLkNDICXNqxSDhG' id='tblK6MZHez0ZvBChZ' name='Districts'>
            ]
        """
        return [
            pyairtable.api.table.Table(None, self, table_schema)
            for table_schema in self.schema(force=force).tables
        ]

    def create_table(
        self,
        name: str,
        fields: Sequence[Dict[str, Any]],
        description: Optional[str] = None,
    ) -> "pyairtable.api.table.Table":
        """
        Creates a table in the given base.

        Args:
            name: The unique table name.
            fields: A list of ``dict`` objects that conform to Airtable's
                `Field model <https://airtable.com/developers/web/api/model/field-model>`__.
            description: The table description. Must be no longer than 20k characters.
        """
        url = self.meta_url("tables")
        payload = {"name": name, "fields": fields}
        if description:
            payload["description"] = description
        response = self.api.request("POST", url, json=payload)
        return self.table(response["id"], validate=True)

    @property
    def url(self) -> str:
        return self.api.build_url(self.id)

    def meta_url(self, *components: Any) -> str:
        """
        Builds a URL to a metadata endpoint for this base.
        """
        return self.api.build_url("meta/bases", self.id, *components)

    def schema(self, *, force: bool = False) -> BaseSchema:
        """
        Retrieves the schema of all tables in the base and caches it.

        Args:
            force: |kwarg_force_metadata|

        Usage:
            >>> base.schema().tables
            [TableSchema(...), TableSchema(...), ...]
            >>> base.schema().table("tblXXXXXXXXXXXXXX")
            TableSchema(id="tblXXXXXXXXXXXXXX", ...)
            >>> base.schema().table("My Table")
            TableSchema(id="...", name="My Table", ...)
        """
        if force or not self._schema:
            url = self.meta_url("tables")
            params = {"include": ["visibleFieldIds"]}
            data = self.api.request("GET", url, params=params)
            self._schema = BaseSchema.parse_obj(data)
        return self._schema

    @property
    def webhooks_url(self) -> str:
        return self.api.build_url("bases", self.id, "webhooks")

    def webhooks(self) -> List[Webhook]:
        """
        Retrieves all the base's webhooks
        (see: `List webhooks <https://airtable.com/developers/web/api/list-webhooks>`_).

        Usage:
            >>> base.webhooks()
            [
                Webhook(
                    id='ach00000000000001',
                    are_notifications_enabled=True,
                    cursor_for_next_payload=1,
                    is_hook_enabled=True,
                    last_successful_notification_time=None,
                    notification_url="https://example.com",
                    last_notification_result=None,
                    expiration_time="2023-07-01T00:00:00.000Z",
                    specification: WebhookSpecification(...)
                )
            ]
        """
        response = self.api.request("GET", self.webhooks_url)
        return [
            Webhook.from_api(
                api=self.api,
                url=f"{self.webhooks_url}/{data['id']}",
                obj=data,
            )
            for data in response["webhooks"]
        ]

    def webhook(self, webhook_id: str) -> Webhook:
        """
        Returns a single webhook or raises ``KeyError`` if the given ID is invalid.

        Airtable's API does not permit retrieving a single webhook, so this function
        will call :meth:`~webhooks` and simply return one item from the list.
        """
        for webhook in self.webhooks():
            if webhook.id == webhook_id:
                return webhook
        raise KeyError(f"webhook not found: {webhook_id!r}")

    def add_webhook(
        self,
        notify_url: str,
        spec: Union[WebhookSpecification, Dict[Any, Any]],
    ) -> CreateWebhookResponse:
        """
        Creates a webhook on the base with the given
        `webhooks specification <https://airtable.com/developers/web/api/model/webhooks-specification>`_.

        The return value will contain a unique secret that must be saved
        in order to validate payloads as they are sent to your notification
        endpoint. If you do not save this, you will have no way of confirming
        that payloads you receive did, in fact, come from Airtable.

        For more on how to validate notifications to your webhook, see
        :meth:`WebhookNotification.from_request() <pyairtable.models.WebhookNotification.from_request>`.

        Usage:
            >>> base.add_webhook(
            ...     "https://example.com",
            ...     {
            ...         "options": {
            ...             "filters": {
            ...                 "dataTypes": ["tableData"],
            ...             }
            ...         }
            ...     }
            ... )
            CreateWebhookResponse(
                id='ach00000000000001',
                mac_secret_base64='c3VwZXIgZHVwZXIgc2VjcmV0',
                expiration_time='2023-07-01T00:00:00.000Z'
            )

        Raises:
            pydantic.ValidationError: If the dict provided is invalid.

        Args:
            notify_url: The URL where Airtable will POST all event notifications.
            spec: The configuration for the webhook. It is easiest to pass a dict
                that conforms to the `webhooks specification`_ but you
                can also provide :class:`~pyairtable.models.webhook.WebhookSpecification`.
        """
        if isinstance(spec, dict):
            spec = WebhookSpecification.parse_obj(spec)

        create = CreateWebhook(notification_url=notify_url, specification=spec)
        request = create.dict(by_alias=True, exclude_unset=True)
        response = self.api.request("POST", self.webhooks_url, json=request)
        return CreateWebhookResponse.parse_obj(response)

    @enterprise_only
    def info(self, *, force: bool = False) -> "BaseInfo":
        """
        Retrieves `base collaborators <https://airtable.com/developers/web/api/get-base-collaborators>`__.

        Args:
            force: |kwarg_force_metadata|
        """
        if force or not self._info:
            params = {"include": ["collaborators", "inviteLinks", "interfaces"]}
            data = self.api.request("GET", self.meta_url(), params=params)
            self._info = BaseInfo.parse_obj(data)
        return self._info

    @enterprise_only
    def shares(self, *, force: bool = False) -> List[BaseShare]:
        """
        Retrieves `base shares <https://airtable.com/developers/web/api/list-shares>`__.

        Args:
            force: |kwarg_force_metadata|
        """
        if force or not self._shares:
            data = self.api.request("GET", self.meta_url("shares"))
            self._shares = [BaseShare.parse_obj(share) for share in data["shares"]]
        return self._shares
