# Permissions & Roles

`permio.permissions.v1.PermissionsService` stores permissions, roles and grants, and answers checks. Every request
names a `project_name`. Your organisation comes from the API key.

--8<-- "hosts.md"

In the tables below, **Key access** is the [API key access level](../concepts/api-keys.md#access-levels) needed to
make the call. **Check** is the default for new keys, and **Full** is the level that also allows writes.

| RPC | REST | Key access |
| --- | --- | --- |
| [Check](#check) | `POST /permissions-service/v1/permissions/check` | Check |
| [CreatePermission](#createpermission) | `POST /permissions-service/v1/permissions` | Full |
| [GetPermission](#getpermission) | `GET /permissions-service/v1/permissions/{name}` | Check |
| [UpdatePermission](#updatepermission) | `PUT /permissions-service/v1/permissions/{name}` | Full |
| [DeletePermission](#deletepermission) | `DELETE /permissions-service/v1/permissions/{name}` | Full |
| [ListPermissions](#listpermissions) | `GET /permissions-service/v1/permissions` | Check |
| [CreateRole](#createrole) | `POST /permissions-service/v1/roles` | Full |
| [GetRole](#getrole) | `GET /permissions-service/v1/roles/{id}` | Check |
| [UpdateRole](#updaterole) | `PUT /permissions-service/v1/roles/{id}` | Full |
| [DeleteRole](#deleterole) | `DELETE /permissions-service/v1/roles/{id}` | Full |
| [ListRoles](#listroles) | `GET /permissions-service/v1/roles` | Check |
| [GrantUserPermissionsAndRolesOnResource](#grantuserpermissionsandrolesonresource) | `POST /permissions-service/v1/permissions/assign` | Full |
| [RevokeUserPermissionsAndRolesOnResource](#revokeuserpermissionsandrolesonresource) | `POST /permissions-service/v1/permissions/revoke` | Full |
| [GetUserPermissionsAndRolesOnResource](#getuserpermissionsandrolesonresource) | `GET /permissions-service/v1/permissions/user/{user_id}/resource/{resource_uri=**}` | Check |
| [ListPrincipals](#listprincipals) | `GET /permissions-service/v1/permissions/principals` | Check |
| [GetAllAssignmentsForPrincipal](#getallassignmentsforprincipal) | `GET /permissions-service/v1/permissions/assignments/principal/{principal_id=**}` | Check |

`GetTotalRolesAndPermissionsForOrganisation` (`GET /permissions-service/v1/permissions/organisation/{organisation_id}/totals`)
is also part of the service. It needs an organisation-level permission that API keys don't have, and the dashboard
uses it.

## Common field rules

| Field | Rule |
| --- | --- |
| `project_name` | 1–32 characters: lowercase letters, digits and `-`. |
| Permission `name` | 1–128 characters: `a-z A-Z 0-9 . _ -`. |
| Role `name` | 1–128 characters, no control characters. |
| Role `id` | 1–128 characters: `a-z A-Z 0-9 . _ -`. |
| Resource URIs | See [Resources and inheritance](../concepts/resources.md#rules-for-uris). |

## Messages

**Permission**

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Unique ID. |
| `organisation_id` | string | Owning organisation. |
| `name` | string | The name your code checks, e.g. `document.read`. |
| `description` | string | Free text. |
| `project_name` | string | Owning project. |

**Role**

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Unique ID. Use it when granting and in the role endpoints. |
| `organisation_id` | string | Owning organisation. |
| `name` | string | Display name. |
| `description` | string | Free text. |
| `permissions` | Permission[] | The permissions in the role. |
| `project_name` | string | Owning project. |

**Assignment**

| Field | Type | Description |
| --- | --- | --- |
| `resource_uri` | string | The resource the grant is on. |
| `permissions` | Permission[] | Permissions granted directly. |
| `roles` | Role[] | Roles granted. |

---

## Check

`POST /permissions-service/v1/permissions/check`

Checks whether a principal holds **every** listed permission on **every** listed resource. Grants on ancestors of a
resource count. See [how a check is decided](../concepts/resources.md#how-a-check-is-decided).

**Request** (`CheckPermissionRequest`)

| Field | Type | Description |
| --- | --- | --- |
| `project_name` | string | Required. Project to check in. |
| `principal_id` | string | Required. The principal being checked. |
| `resource_uris` | string[] | Required. 1–100 unique resource URIs. |
| `permissions` | string[] | Required. 1–100 unique permission names. |

**Response** (`CheckPermissionResponse`)

| Field | Type | Description |
| --- | --- | --- |
| `passed` | bool | `true` if every permission is held on every resource. |
| `missing_permissions` | MissingPermissions[] | For each resource that failed: `resource_uri` and the `missing_permissions` not held there. |

A failed check is a successful response with `passed: false`. `PERMISSION_DENIED` means the **API key** lacks
`permission.check` on the resources or on the principal, not that the principal was denied.

=== "TypeScript"

    ```ts
    const { allowed, missing } = await permio.checkDetailed({
      principal: "alice",
      resources: ["/documents/42", "/invoices/1"],
      permission: "document.read",
    });
    ```

=== "cURL"

    ```bash
    curl -X POST "$PERMIO_API/permissions-service/v1/permissions/check" \
      -H "Authorization: Bearer $PERMIO_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "default",
        "principal_id": "alice",
        "resource_uris": ["/documents/42", "/invoices/1"],
        "permissions": ["document.read"]
      }'
    ```

    ```json
    {"missingPermissions": [{"resourceUri": "/invoices/1", "missingPermissions": ["document.read"]}]}
    ```

---

## Permissions

### CreatePermission

`POST /permissions-service/v1/permissions`

Creates a permission. This call is idempotent: if the permission already exists, it is updated. Returns the
`Permission`.

| Field | Type | Description |
| --- | --- | --- |
| `project_name` | string | Required. |
| `name` | string | Required. |
| `description` | string | Optional. |

=== "TypeScript"

    ```ts
    const perm = await permio.permissions.createPermission({
      projectName: "default",
      name: "document.read",
      description: "Read documents",
    });
    ```

=== "cURL"

    ```bash
    curl -X POST "$PERMIO_API/permissions-service/v1/permissions" \
      -H "Authorization: Bearer $PERMIO_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "default", "name": "document.read", "description": "Read documents"}'
    ```

### GetPermission

`GET /permissions-service/v1/permissions/{name}?project_name=…`

Returns a `Permission` by name, or `NOT_FOUND`.

=== "TypeScript"

    ```ts
    const perm = await permio.permissions.getPermission({ projectName: "default", name: "document.read" });
    ```

=== "cURL"

    ```bash
    curl "$PERMIO_API/permissions-service/v1/permissions/document.read?project_name=default" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

### UpdatePermission

`PUT /permissions-service/v1/permissions/{name}`

Updates a permission, or returns `NOT_FOUND` if it doesn't exist. Returns the updated `Permission`.

| Field | Type | Description |
| --- | --- | --- |
| `project_name` | string | Required. |
| `name` | string | Required (path). The current name. |
| `new_name` | string | Optional. A new name; if omitted, the name stays the same. |
| `description` | string | The new description. |

=== "TypeScript"

    ```ts
    await permio.permissions.updatePermission({
      projectName: "default",
      name: "document.read",
      description: "Read any document",
    });
    ```

=== "cURL"

    ```bash
    curl -X PUT "$PERMIO_API/permissions-service/v1/permissions/document.read" \
      -H "Authorization: Bearer $PERMIO_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "default", "description": "Read any document"}'
    ```

### DeletePermission

`DELETE /permissions-service/v1/permissions/{name}?project_name=…`

Deletes a permission. This call is idempotent: it succeeds whether or not the permission existed.

=== "TypeScript"

    ```ts
    await permio.permissions.deletePermission({ projectName: "default", name: "document.read" });
    ```

=== "cURL"

    ```bash
    curl -X DELETE "$PERMIO_API/permissions-service/v1/permissions/document.read?project_name=default" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

### ListPermissions

`GET /permissions-service/v1/permissions?project_name=…`

Lists permissions in a project. The response has `permissions` (Permission[]) and `pagination`.

| Field | Type | Description |
| --- | --- | --- |
| `project_name` | string | Required. |
| `pagination` | [PaginationRequest](pagination.md) | Optional. `limit` (1–100) and `cursor`. |
| `search` | string | Optional. Filters by name. |

=== "TypeScript"

    ```ts
    for await (const p of permio.listPermissions({ search: "document." })) {
      console.log(p.name);
    }
    ```

=== "cURL"

    ```bash
    curl "$PERMIO_API/permissions-service/v1/permissions?project_name=default&search=document.&pagination.limit=50" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

---

## Roles

### CreateRole

`POST /permissions-service/v1/roles`

Creates a role from existing permissions. This call is idempotent: if the role already exists, it is updated.
Returns the `Role`, including its `id`.

| Field | Type | Description |
| --- | --- | --- |
| `project_name` | string | Required. |
| `name` | string | Required. |
| `description` | string | Optional. |
| `permissions` | string[] | Permission **names**, e.g. `["document.read"]`. |

=== "TypeScript"

    ```ts
    const role = await permio.permissions.createRole({
      projectName: "default",
      name: "viewer",
      description: "Can read documents",
      permissions: ["document.read"],
    });
    console.log(role.id);
    ```

=== "cURL"

    ```bash
    curl -X POST "$PERMIO_API/permissions-service/v1/roles" \
      -H "Authorization: Bearer $PERMIO_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "default", "name": "viewer", "description": "Can read documents", "permissions": ["document.read"]}'
    ```

### GetRole

`GET /permissions-service/v1/roles/{id}?project_name=…`

Returns a `Role` by ID.

=== "TypeScript"

    ```ts
    const role = await permio.permissions.getRole({ projectName: "default", id: roleId });
    ```

=== "cURL"

    ```bash
    curl "$PERMIO_API/permissions-service/v1/roles/ROLE_ID?project_name=default" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

### UpdateRole

`PUT /permissions-service/v1/roles/{id}`

Replaces a role's name, description and permissions, or returns `NOT_FOUND`. Returns the updated `Role`.

| Field | Type | Description |
| --- | --- | --- |
| `project_name` | string | Required. |
| `id` | string | Required (path). |
| `name` | string | Required. |
| `description` | string | Optional. |
| `permissions` | string[] | Permission names. |

=== "TypeScript"

    ```ts
    await permio.permissions.updateRole({
      projectName: "default",
      id: roleId,
      name: "editor",
      permissions: ["document.read", "document.write"],
    });
    ```

=== "cURL"

    ```bash
    curl -X PUT "$PERMIO_API/permissions-service/v1/roles/ROLE_ID" \
      -H "Authorization: Bearer $PERMIO_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "default", "name": "editor", "permissions": ["document.read", "document.write"]}'
    ```

### DeleteRole

`DELETE /permissions-service/v1/roles/{id}?project_name=…`

Deletes a role. This call is idempotent.

=== "TypeScript"

    ```ts
    await permio.permissions.deleteRole({ projectName: "default", id: roleId });
    ```

=== "cURL"

    ```bash
    curl -X DELETE "$PERMIO_API/permissions-service/v1/roles/ROLE_ID?project_name=default" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

### ListRoles

`GET /permissions-service/v1/roles?project_name=…`

Lists roles in a project. The response has `roles` (Role[]) and `pagination`. It takes the same `pagination` and
`search` fields as [ListPermissions](#listpermissions).

=== "TypeScript"

    ```ts
    for await (const role of permio.listRoles()) {
      console.log(role.id, role.name);
    }
    ```

=== "cURL"

    ```bash
    curl "$PERMIO_API/permissions-service/v1/roles?project_name=default&pagination.limit=50" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

---

## Grants

### GrantUserPermissionsAndRolesOnResource

`POST /permissions-service/v1/permissions/assign`

Grants permissions and/or roles to a principal on a resource. Grants are additive: existing grants are kept. The
grant also applies to every resource beneath `resource_uri`. Unknown permissions or roles are rejected with
`INVALID_ARGUMENT`.

| Field | Type | Description |
| --- | --- | --- |
| `project_name` | string | Required. |
| `user_id` | string | Required. The principal ID, the same value you pass as `principal_id` to Check. |
| `resource_uri` | string | Required. |
| `permissions` | string[] | Permission **names**. |
| `roles` | string[] | Role **IDs**. |

=== "TypeScript"

    ```ts
    await permio.permissions.grantUserPermissionsAndRolesOnResource({
      projectName: "default",
      userId: "alice",
      resourceUri: "/documents",
      roles: [roleId],
    });
    ```

=== "cURL"

    ```bash
    curl -X POST "$PERMIO_API/permissions-service/v1/permissions/assign" \
      -H "Authorization: Bearer $PERMIO_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "default", "user_id": "alice", "resource_uri": "/documents", "roles": ["ROLE_ID"]}'
    ```

### RevokeUserPermissionsAndRolesOnResource

`POST /permissions-service/v1/permissions/revoke`

Removes permissions and/or roles from a principal on a resource. It takes the same fields as Grant.

=== "TypeScript"

    ```ts
    await permio.permissions.revokeUserPermissionsAndRolesOnResource({
      projectName: "default",
      userId: "alice",
      resourceUri: "/documents",
      roles: [roleId],
    });
    ```

=== "cURL"

    ```bash
    curl -X POST "$PERMIO_API/permissions-service/v1/permissions/revoke" \
      -H "Authorization: Bearer $PERMIO_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "default", "user_id": "alice", "resource_uri": "/documents", "roles": ["ROLE_ID"]}'
    ```

### GetUserPermissionsAndRolesOnResource

`GET /permissions-service/v1/permissions/user/{user_id}/resource/{resource_uri=**}?project_name=…`<br>
`GET /permissions-service/v1/permissions/user/{user_id}/resource?resource_uri=…&project_name=…`

Returns the permissions and roles assigned to a principal on one resource. The response has `project_name`,
`user_id`, `resource_uri`, `permissions` (names) and `roles` (IDs).

In the first form, send the resource URI **without** its leading slash. The second form passes the URI exactly as a
query parameter.

=== "TypeScript"

    ```ts
    const res = await permio.permissions.getUserPermissionsAndRolesOnResource({
      projectName: "default",
      userId: "alice",
      resourceUri: "/documents",
    });
    ```

=== "cURL"

    ```bash
    curl "$PERMIO_API/permissions-service/v1/permissions/user/alice/resource?resource_uri=/documents&project_name=default" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

### ListPrincipals

`GET /permissions-service/v1/permissions/principals?project_name=…`

Lists the IDs of principals with grants in the project. The response has `principals` (string[]) and `pagination`.
It takes `pagination` and `search`.

=== "TypeScript"

    ```ts
    for await (const id of permio.listPrincipals()) console.log(id);
    ```

=== "cURL"

    ```bash
    curl "$PERMIO_API/permissions-service/v1/permissions/principals?project_name=default" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

### GetAllAssignmentsForPrincipal

`GET /permissions-service/v1/permissions/assignments/principal/{principal_id=**}?project_name=…`

Lists every grant a principal has in the project. The response has `assignments` (Assignment[]) and `pagination`.
Principal IDs may contain slashes.

=== "TypeScript"

    ```ts
    for await (const a of permio.listAssignments({ principal: "alice" })) {
      console.log(a.resourceUri, a.permissions.map((p) => p.name), a.roles.map((r) => r.name));
    }
    ```

=== "cURL"

    ```bash
    curl "$PERMIO_API/permissions-service/v1/permissions/assignments/principal/alice?project_name=default" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```
