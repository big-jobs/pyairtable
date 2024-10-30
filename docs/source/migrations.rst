.. include:: _warn_latest.rst
.. include:: _substitutions.rst


Migration Guide
*****************


Migrating from 2.x to 3.0
============================

The 3.0 release introduces a number of breaking changes, summarized below.

Updated minimum dependencies
---------------------------------------------

* pyAirtable 3.0 is tested on Python 3.9 or higher. It may continue to work on Python 3.8
  for some time, but bug reports related to Python 3.8 compatibility will not be accepted.
* pyAirtable 3.0 requires Pydantic 2. If your project still uses Pydantic 1,
  you will need to continue to use pyAirtable 2.x until you can upgrade Pydantic.
  Read the `Pydantic v2 migration guide <https://docs.pydantic.dev/latest/migration/>`__
  for more information.

Deprecated metadata module removed
---------------------------------------------

The 3.0 release removed the ``pyairtable.metadata`` module. For supported alternatives,
see :doc:`metadata`.

Changes to generating URLs
---------------------------------------------

The following properties and methods for constructing URLs have been renamed or removed.
These methods now return instances of :class:`~pyairtable.utils.Url`, which is a
subclass of ``str`` that has some overloaded operators. See docs for more details.

.. list-table::
    :header-rows: 1

    * - Building a URL in 2.x
      - Building a URL in 3.0
    * - ``table.url``
      - ``table.urls.records``
    * - ``table.record_url(record_id)``
      - ``table.urls.record(record_id)``
    * - ``table.meta_url("one", "two")``
      - ``table.urls.meta / "one" / "two"``
    * - ``table.meta_url(*parts)``
      - ``table.urls.meta // parts``
    * - ``base.url``
      - (removed; was invalid)
    * - ``base.meta_url("one", "two")``
      - ``base.urls.meta / "one" / "two"``
    * - ``base.webhooks_url()``
      - ``base.urls.webhooks``
    * - ``enterprise.url``
      - ``enterprise.urls.meta``
    * - ``workspace.url``
      - ``workspace.urls.meta``

Changes to the formulas module
---------------------------------------------

Most functions and methods in :mod:`pyairtable.formulas` now return instances of
:class:`~pyairtable.formulas.Formula`, which can be chained, combined, and eventually
passed to the ``formula=`` keyword argument to methods like :meth:`~pyairtable.Table.all`.
Read the module documentation for more details.

The full list of breaking changes is below:

.. list-table::
    :header-rows: 1

    * - Function
      - Changes
    * - :func:`~pyairtable.formulas.match`
      - This now raises ``ValueError`` on empty input,
        instead of returning ``None``.
    * - ``to_airtable_value()``
      - Removed. Use :func:`~pyairtable.formulas.to_formula_str` instead.
    * - ``EQUAL()``
      - Removed. Use :class:`~pyairtable.formulas.EQ` instead.
    * - ``NOT_EQUAL()``
      - Removed. Use :class:`~pyairtable.formulas.NE` instead.
    * - ``LESS()``
      - Removed. Use :class:`~pyairtable.formulas.LT` instead.
    * - ``LESS_EQUAL()``
      - Removed. Use :class:`~pyairtable.formulas.LTE` instead.
    * - ``GREATER()``
      - Removed. Use :class:`~pyairtable.formulas.GT` instead.
    * - ``GREATER_EQUAL()``
      - Removed. Use :class:`~pyairtable.formulas.GTE` instead.
    * - ``FIELD()``
      - Removed. Use :class:`~pyairtable.formulas.Field` or :func:`~pyairtable.formulas.field_name`.
    * - ``STR_VALUE()``
      - Removed. Use :func:`~pyairtable.formulas.quoted` instead.
    * - :func:`~pyairtable.formulas.AND`, :func:`~pyairtable.formulas.OR`
      - These no longer return ``str``, and instead return instances of
        :class:`~pyairtable.formulas.Comparison`.
    * - :func:`~pyairtable.formulas.IF`, :func:`~pyairtable.formulas.FIND`, :func:`~pyairtable.formulas.LOWER`
      - These no longer return ``str``, and instead return instances of
        :class:`~pyairtable.formulas.FunctionCall`.
    * - :func:`~pyairtable.formulas.escape_quotes`
      - Deprecated. Use :func:`~pyairtable.formulas.quoted` instead.

Changes to the ORM in 3.0
---------------------------------------------

* :data:`Model.created_time <pyairtable.orm.Model.created_time>` is now a ``datetime`` (or ``None``)
  instead of ``str``. This change also applies to all timestamp fields used in :ref:`API: pyairtable.models`.

* :meth:`Model.save <pyairtable.orm.Model.save>` now only saves changed fields to the API, which
  means it will sometimes not perform any network traffic (though this behavior can be overridden).
  It also now returns an instance of :class:`~pyairtable.orm.SaveResult` instead of ``bool``.

* Fields which contain lists of values now return instances of ``ChangeTrackingList``, which
  is still a subclass of ``list``. This should not affect most uses, but it does mean that
  some code which relies on exact type checking may need to be updated:

    >>> isinstance(Foo().atts, list)
    True
    >>> type(Foo().atts) is list
    False
    >>> type(Foo().atts)
    <class 'pyairtable.orm.lists.ChangeTrackingList'>

* The 3.0 release has changed the API for retrieving ORM model configuration:

  .. list-table::
      :header-rows: 1

      * - Method in 2.x
        - Method in 3.0
      * - ``Model.get_api()``
        - ``Model.meta.api``
      * - ``Model.get_base()``
        - ``Model.meta.base``
      * - ``Model.get_table()``
        - ``Model.meta.table``
      * - ``Model._get_meta(name)``
        - ``Model.meta.get(name)``

Breaking type changes
---------------------------------------------

* ``pyairtable.api.types.CreateAttachmentDict`` is now a ``Union`` instead of a ``TypedDict``,
  which may change some type checking behavior in code that uses it.

Breaking name changes
---------------------------------------------

    * - | ``pyairtable.api.enterprise.ClaimUsersResponse``
        | has become :class:`pyairtable.api.enterprise.ManageUsersResponse`
    * - | ``pyairtable.formulas.CircularDependency``
        | has become :class:`pyairtable.exceptions.CircularFormulaError`
    * - | ``pyairtable.params.InvalidParamException``
        | has become :class:`pyairtable.exceptions.InvalidParameterError`
    * - | ``pyairtable.orm.fields.MissingValue``
        | has become :class:`pyairtable.exceptions.MissingValueError`
    * - | ``pyairtable.orm.fields.MultipleValues``
        | has become :class:`pyairtable.exceptions.MultipleValuesError`
    * - | ``pyairtable.models.AuditLogEvent.model_id``
        | has become :data:`pyairtable.models.AuditLogEvent.object_id`
    * - | ``pyairtable.models.AuditLogEvent.model_type``
        | has become :data:`pyairtable.models.AuditLogEvent.object_type`


Migrating from 2.2 to 2.3
============================

A breaking API change was accidentally introduced into the 2.3 minor release
by renaming some nested fields of :class:`~pyairtable.models.schema.BaseCollaborators`
and :class:`~pyairtable.models.schema.WorkspaceCollaborators`.

    * - | ``base.collaborators().invite_links.base_invite_links``
        | has become ``base.collaborators().invite_links.via_base``
    * - | ``base.collaborators().invite_links.workspace_invite_links``
        | has become ``base.collaborators().invite_links.via_workspace``
    * - | ``ws.collaborators().invite_links.base_invite_links``
        | has become ``ws.collaborators().invite_links.via_base``
    * - | ``ws.collaborators().invite_links.workspace_invite_links``
        | has become ``ws.collaborators().invite_links.via_workspace``
    * - | ``ws.collaborators().individual_collaborators.base_collaborators``
        | has become ``ws.collaborators().individual_collaborators.via_base``
    * - | ``ws.collaborators().individual_collaborators.workspace_collaborators``
        | has become ``ws.collaborators().individual_collaborators.via_workspace``
    * - | ``ws.collaborators().group_collaborators.base_collaborators``
        | has become ``ws.collaborators().group_collaborators.via_base``
    * - | ``ws.collaborators().group_collaborators.workspace_collaborators``
        | has become ``ws.collaborators().group_collaborators.via_workspace``


Migrating from 1.x to 2.0
============================

With the 2.0 release, we've made some breaking changes to the pyAirtable API. These are summarized below.
You can read more about the rationale behind these changes in `#257 <https://github.com/gtalarico/pyairtable/issues/257>`_,
and you see a list of changes and new features in the :ref:`Changelog`.

ApiAbstract removed
-----------------------

We've removed the ``pyairtable.api.abstract`` module. If you had code which inherited from ``ApiAbstract``,
you will need to refactor it. We recommend taking an instance of :class:`~pyairtable.Api` as a
constructor parameter, and using that to construct :class:`~pyairtable.Table` instances as needed.

Changes to Api, Base, and Table
-----------------------------------

:class:`~pyairtable.Api`, :class:`~pyairtable.Base`, and :class:`~pyairtable.Table`
no longer inherit from the same base class. Each has its own scope of responsibility and has
methods which refer to the other classes as needed. See :ref:`Getting Started`.

For a period of time, the constructor for :class:`~pyairtable.Base` and :class:`~pyairtable.Table`
will remain backwards-compatible with the previous approach (passing in ``str`` values),
but doing so will produce deprecation warnings.

See below for supported and unsupported patterns:

.. code-block:: python

    # The following are supported:
    >>> api = Api(api_key, timeout=..., retry_strategy=..., endpoint_url=...)
    >>> base = api.base(base_id)  # [str]
    >>> base = Base(api, base_id)  # [Api, str]
    >>> table = base.table(table_name)  # [str]
    >>> table = api.table(base_id, table_name)  # [str, str]
    >>> table = Table(None, base, table_name)  # [None, Base, str]

    # The following are still supported but will issue a DeprecationWarning:
    >>> base = Base(api_key, base_id)  # [str, str]
    >>> table = Table(api_key, base_id, table_name)  # [str, str, str]

    # The following will raise a TypeError for mixing str & instances:
    >>> table = Table(api_key, base, table_name)  # [str, Base, str]
    >>> table = Table(api, base_id, table_name)  # [Api, str, str]

    # The following will raise a TypeError. We do this proactively
    # to avoid situations where self.api and self.base don't align.
    >>> table = Table(api, base, table_name)  # [Api, Base, str]

You may need to change how your code looks up some pieces of connection metadata; for example:

.. list-table::
    :header-rows: 1

    * - Method/attribute in 1.5
      - Method/attribute in 2.0
    * - ``base.base_id``
      - :data:`base.id <pyairtable.Base.id>`
    * - ``table.table_name``
      - :data:`table.name <pyairtable.Table.name>`
    * - ``table.get_base()``
      - :data:`table.base <pyairtable.Table.base>`
    * - ``table.base_id``
      - :data:`table.base.id <pyairtable.Base.id>`
    * - ``table.table_url``
      - :meth:`table.url <pyairtable.Table.url>`
    * - ``table.get_record_url()``
      - :meth:`table.record_url() <pyairtable.Table.record_url>`

There is no fully exhaustive list of changes; please refer to
:ref:`the API documentation <API: pyairtable>` for a list of available methods and attributes.

Retry by default
----------------

* By default, the library will retry requests up to five times if it receives
  a 429 status code from Airtable, indicating the base has exceeded its QPS limit.

Changes to the ORM
------------------

* :meth:`Model.all <pyairtable.orm.Model.all>` and :meth:`Model.first <pyairtable.orm.Model.first>`
  return instances of the model class instead of returning dicts.
* :class:`~pyairtable.orm.fields.LinkField` now defaults to ``lazy=False``. The first time your code
  accesses the field, it will perform one or more API calls to retrieve field data for linked records.
  You can disable this by passing ``lazy=True`` when creating the field.

Changes to types
----------------

* All functions and methods in this library have full type annotations that will pass ``mypy --strict``.
  See the :mod:`pyairtable.api.types` module for more information on the types this library accepts and returns.

batch_upsert has a different return type
--------------------------------------------

* :meth:`~pyairtable.Table.batch_upsert` now returns the full payload from the Airtable API,
  as opposed to just the list of records (with no indication of which were created or updated).
  See :class:`~pyairtable.api.types.UpsertResultDict` for more details.


Found a problem?
--------------------

While these breaking changes were intentional, it is very possible that the 2.0 release has bugs.
Please take a moment to :ref:`read our contribution guidelines <contributing>` before submitting an issue.


------


Migrating from 0.x to 1.0
============================

**Airtable Python Wrapper** was renamed to **pyAirtable** starting on its first major release, ``1.0.0``.
The docs for the older release will remain `on Read the Docs <https://airtable-python-wrapper.readthedocs.io/>`__,
the source code on `this branch <https://github.com/gtalarico/airtable-python-wrapper>`__.
The last ``0.x`` release will remain available on `PyPI <https://pypi.org/project/airtable-python-wrapper/>`__.

You can read about the reasons behind the renaming `here <https://github.com/gtalarico/airtable-python-wrapper/issues/125#issuecomment-891439661>`__.


New Features in 1.0
-------------------

* Type Annotations
* Simpler API
* Formulas
* ORM Models

API Changes in 1.0
------------------

We used this new major release to make a few breaking changes:

* Introduced a simpler API that's more closely aligned with Airtable API's patterns.
* Created more a flexible API (:class:`~pyairtable.Api`, :class:`~pyairtable.Base`, :class:`~pyairtable.Table`)


.. list-table:: Changes
   :widths: 35 65
   :header-rows: 1

   * - 0.x (airtable-python-wrapper)
     - 1.0 (pyAirtable)
   * - ``Airtable()``
     - :class:`~pyairtable.Api`, :class:`~pyairtable.Base`, :class:`~pyairtable.Table`
   * - ``get()``
     - ``get()``
   * - ``get_iter()``
     - ``iterate()``
   * - ``get_all()``
     - ``all()``
   * - ``search()``
     - ``all(formula=match({"Name" : "X"})``
   * - ``match(**kwargs)``
     - ``first(formula=match({"Name" : "X"})``
   * - ``insert()``
     - ``create()``
   * - ``update()``
     - ``update()``
   * - ``replace()``
     - use ``update(replace=True)``
   * - ``delete()``
     - ``delete()``
