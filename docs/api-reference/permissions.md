# Permissions & Roles

`permio.permissions.v1.PermissionsService` stores permissions, roles and grants, and answers checks. Every request
names a `project_name`. Your organisation comes from the API key.

--8<-- "hosts.md"

In the tables below, **Key access** is the [API key access level](../concepts/api-keys.md#access-levels) needed to
make the call. **Check** is the default for new keys, and **Full** is the level that also allows writes.

| RPC | REST | Key access |
| --- | --- | --- |
| [Check](#check) | `POST /permissions-service/v1/permissions/check` | Check |
| [BatchCheck](#batchcheck) | `POST /permissions-service/v1/permissions/check/batch` | Check |
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
| [ListAccess](#listaccess) | `GET /permissions-service/v1/access` | Check |
| [ListPrincipalsWithAccess](#listprincipalswithaccess) | `GET /permissions-service/v1/access/principals` | Check |
| [CreateGroup](#creategroup) | `POST /permissions-service/v1/groups` | Full |
| [GetGroup](#getgroup) | `GET /permissions-service/v1/groups/{name}` | Check |
| [UpdateGroup](#updategroup) | `PUT /permissions-service/v1/groups/{name}` | Full |
| [DeleteGroup](#deletegroup) | `DELETE /permissions-service/v1/groups/{name}` | Full |
| [ListGroups](#listgroups) | `GET /permissions-service/v1/groups` | Check |
| [AddGroupMembers](#addgroupmembers) | `POST /permissions-service/v1/groups/{name}/members/add` | Full |
| [RemoveGroupMembers](#removegroupmembers) | `POST /permissions-service/v1/groups/{name}/members/remove` | Full |
| [ListGroupMembers](#listgroupmembers) | `GET /permissions-service/v1/groups/{name}/members` | Check |
| [ListGroupsForPrincipal](#listgroupsforprincipal) | `GET /permissions-service/v1/group-memberships/{principal_id=**}` | Check |

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
| Group `name` | 1–64 characters: lowercase letters, digits and `-`. Its principal ID is `group:<name>`. |
| Principal IDs | Any non-empty string. IDs starting with `group:` are reserved for [groups](../concepts/groups.md): such an ID must name a group that exists in the project, or the call fails with `NOT_FOUND` (`INVALID_ARGUMENT` if it isn't a valid group name). Revoking is the exception. |
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
resource count, and so do grants to the [groups](../concepts/groups.md) the principal is a member of. See
[how a check is decided](../concepts/resources.md#how-a-check-is-decided). To get one answer per resource, use
[BatchCheck](#batchcheck).

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

=== "Go"

    ```go
    res, err := client.CheckDetailed(ctx, permio.CheckRequest{
        Principal:   "alice",
        Resources:   []string{"/documents/42", "/invoices/1"},
        Permissions: []string{"document.read"},
    })
    // handle err
    res.Allowed // false
    res.Missing // [{Resource: "/invoices/1", Permissions: ["document.read"]}]
    ```

=== "Python"

    ```python
    result = permio.check_detailed("alice", "document.read", ["/documents/42", "/invoices/1"])
    result.allowed  # False
    result.missing  # [MissingPermission(resource="/invoices/1", permissions=["document.read"])]
    ```

    `check()` returns just the `bool`. See [Checking permissions](../sdk/python.md#checking-permissions).

=== "Rust"

    ```rust
    use permio::Check;

    let result = permio
        .check_detailed(
            Check::new("alice")
                .resources(["/documents/42", "/invoices/1"])
                .permission("document.read"),
        )
        .await?;
    println!("{} {:?}", result.allowed, result.missing);
    ```

    `permio.check("alice", "document.read", "/documents/42")` returns just the `bool`. See
    [Checking permissions](../sdk/rust.md#checking-permissions).

=== "Java"

    ```java
    import io.perms.CheckResult;
    import java.util.List;

    CheckResult result = permio.checkDetailed(
        "alice", List.of("document.read"), List.of("/documents/42", "/invoices/1"));
    result.allowed(); // false
    result.missing(); // [MissingPermission{resource=/invoices/1, permissions=[document.read]}]
    ```

    `check` returns just the boolean. See [Checking permissions](../sdk/java.md#checking-permissions).

---

## BatchCheck

`POST /permissions-service/v1/permissions/check/batch`

Checks a principal's permissions on each resource **separately** and returns one result per resource, in request
order. It is evaluated exactly like [Check](#check): inheritance, stored `_` wildcards, roles and the principal's
[groups](../concepts/groups.md) all count, and it fails closed. A resource is allowed only if the principal holds
**every** requested permission on it.

**Needs:** the same as Check: `permission.check` on every resource and on the principal.

**Request** (`BatchCheckRequest`)

| Field | Type | Description |
| --- | --- | --- |
| `project_name` | string | Required. Project to check in. |
| `principal_id` | string | Required. The principal being checked. |
| `resource_uris` | string[] | Required. 1–100 unique resource URIs, with the same rules as Check. |
| `permissions` | string[] | Required. 1–100 unique permission names. |

**Response** (`BatchCheckResponse`)

| Field | Type | Description |
| --- | --- | --- |
| `results` | BatchCheckResult[] | One per requested resource, in request order. |

**BatchCheckResult**

| Field | Type | Description |
| --- | --- | --- |
| `resource_uri` | string | The resource. |
| `allowed` | bool | `true` if the principal holds every requested permission on it. |
| `missing_permissions` | string[] | The requested permissions not held on it, in request order. |

**Errors:** `INVALID_ARGUMENT` for a malformed request; `PERMISSION_DENIED` if the API key lacks `permission.check`;
`NOT_FOUND` if `principal_id` is `group:<slug>` and that group doesn't exist.

=== "TypeScript"

    ```ts
    const allowed = await permio.batchCheck({
      principal: "alice",
      resources: ["/documents/42", "/invoices/1"],
      permission: "document.read",
    });
    allowed.get("/documents/42"); // true
    ```

    Available from SDK 0.2.0. `batchCheckDetailed` returns the missing permissions too. See
    [Batch checks](../sdk/typescript.md#batch-checks).

=== "cURL"

    ```bash
    curl -X POST "$PERMIO_API/permissions-service/v1/permissions/check/batch" \
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
    {"results": [
      {"resourceUri": "/documents/42", "allowed": true},
      {"resourceUri": "/invoices/1", "missingPermissions": ["document.read"]}
    ]}
    ```

=== "Go"

    ```go
    allowed, err := client.BatchCheck(ctx, "alice",
        []string{"document.read"},
        []string{"/documents/42", "/invoices/1"})
    // handle err
    allowed["/documents/42"] // true
    ```

    `BatchCheckDetailed` returns the missing permissions too. See [Batch checks](../sdk/go.md#batch-checks).

=== "Python"

    ```python
    allowed = permio.batch_check("alice", "document.read", ["/documents/42", "/invoices/1"])
    allowed["/documents/42"]  # True
    ```

    `batch_check_detailed` returns the missing permissions too. See [Batch checks](../sdk/python.md#batch-checks).

=== "Rust"

    ```rust
    use permio::BatchCheck;

    let entries = permio
        .batch_check(
            BatchCheck::new("alice")
                .resources(["/documents/42", "/invoices/1"])
                .permission("document.read"),
        )
        .await?;
    for e in &entries {
        println!("{} {} {:?}", e.resource, e.allowed, e.missing);
    }
    ```

    More than 100 resources are split into concurrent calls. See [`batch_check`](../sdk/rust.md#batch_check).

=== "Java"

    ```java
    import java.util.List;
    import java.util.Map;

    Map<String, Boolean> allowed =
        permio.batchCheck("alice", "document.read", List.of("/documents/42", "/invoices/1"));
    allowed.get("/documents/42"); // true
    ```

    `batchCheckDetailed` returns the missing permissions too. See [Batch checks](../sdk/java.md#batch-checks).

The Go, Python, Rust and Java examples on this page use a client set up as in [Clients](index.md#clients).

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

=== "Go"

    ```go
    perm, err := client.CreatePermission(ctx, "document.read", "Read documents")
    ```

    If the permission already exists with another description, the SDK returns an error of kind `KindAlreadyExists`;
    use `UpdatePermission` to change it.

=== "Python"

    The SDK has no helper for this RPC, so call it through the raw client:

    ```python
    from permio import raw

    perm = permio.permissions.CreatePermission(
        raw.permissions_pb2.CreatePermissionRequest(
            project_name="default", name="document.read", description="Read documents"
        )
    )
    ```

=== "Rust"

    There is no helper for this RPC; use the raw client.

    ```rust
    use permio::raw::permissions::v1::CreatePermissionRequest;

    let perm = permio
        .raw_permissions()
        .create_permission(CreatePermissionRequest {
            project_name: "default".into(),
            name: "document.read".into(),
            description: "Read documents".into(),
        })
        .await?
        .into_inner();
    ```

=== "Java"

    The SDK has no helper for this RPC, so use the generated stub from `permio.raw()`. It sends the API key and applies
    the client's timeout, but not its default project: set `project_name` yourself. See
    [Raw client](../sdk/java.md#raw-client).

    ```java
    import io.perms.proto.permissions.v1.CreatePermissionRequest;
    import io.perms.proto.permissions.v1.Permission;

    Permission perm = permio.raw().permissions().createPermission(
        CreatePermissionRequest.newBuilder()
            .setProjectName("default")
            .setName("document.read")
            .setDescription("Read documents")
            .build());
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

To grant to a [group](../concepts/groups.md), set `user_id` to `group:<slug>`. The group must exist in the project,
or the call fails with `NOT_FOUND`. Every member of the group then holds the grant. Grants to groups don't count
towards your unique principals.

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

=== "Go"

    ```go
    err := client.Grant(ctx, permio.GrantRequest{
        Principal: "alice",
        Resource:  "/documents",
        Roles:     []string{roleID},
    })
    ```

=== "Python"

    ```python
    permio.grant("alice", "/documents", roles="ROLE_ID")
    ```

    `permissions=` and `roles=` each take one value or a list. See
    [Granting and revoking](../sdk/python.md#granting-and-revoking).

=== "Rust"

    ```rust
    use permio::Grant;

    permio
        .grant(Grant::new("alice", "/documents").role("ROLE_ID"))
        .await?;
    ```

    Add `.permission("document.read")` to grant permissions by name. See
    [Granting and revoking](../sdk/rust.md#granting-and-revoking).

=== "Java"

    ```java
    import io.perms.Grant;

    permio.grant(Grant.to("alice").on("/documents").roles("ROLE_ID"));
    ```

    The client's project is used. Grants are never retried automatically.

### RevokeUserPermissionsAndRolesOnResource

`POST /permissions-service/v1/permissions/revoke`

Removes permissions and/or roles from a principal on a resource. It takes the same fields as Grant. Revoking from a
`group:<slug>` principal works even if the group no longer exists, so stray grants can be cleaned up.

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

=== "Go"

    ```go
    err := client.Revoke(ctx, permio.GrantRequest{
        Principal: "alice",
        Resource:  "/documents",
        Roles:     []string{roleID},
    })
    ```

=== "Python"

    ```python
    permio.revoke("alice", "/documents", roles="ROLE_ID")
    ```

=== "Rust"

    ```rust
    use permio::Grant;

    permio
        .revoke(Grant::new("alice", "/documents").role("ROLE_ID"))
        .await?;
    ```

=== "Java"

    ```java
    import io.perms.Grant;

    permio.revoke(Grant.to("alice").on("/documents").roles("ROLE_ID"));
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

---

## Access queries

These answer "where?" and "who?" instead of "may they?", with the same rules as Check. The guide
[Filtering lists and building share dialogs](../guides/filtering-and-sharing.md) shows how to use them.

### ListAccess

`GET /permissions-service/v1/access?project_name=…&principal_id=…&permission=…&under_uri=…`

Answers "where can this principal use this permission, at or below `under_uri`?". It counts grants made to the
principal directly, through roles, and through the groups it is a member of. perms.io doesn't know your records, so
the answer is a list of **scopes** in your URI tree, not a list of objects:

- If the principal holds the permission on `under_uri` itself (through a grant on it, on an ancestor, or on a stored
  `_` wildcard URI that matches it), `covers_all` is `true` and `scopes` is a single `SUBTREE` scope for
  `under_uri`. There are no further pages.
- Otherwise `scopes` lists the URIs of the grants below `under_uri` that confer the permission. A concrete URI is a
  `SUBTREE` scope, because a grant applies to its URI and everything below it. A URI with `_` wildcard segments is a
  `PATTERN` scope. Scopes are ordered by `uri` and paginated.

**Needs:** `permission.check` on `under_uri`, and `principal.assignment.get` on the principal.

**Request** (`ListAccessRequest`)

| Field | Type | Description |
| --- | --- | --- |
| `project_name` | string | Required. |
| `principal_id` | string | Required. |
| `permission` | string | Required. One permission name. |
| `under_uri` | string | Required. Only resources at or below this URI are considered. A `_` segment here is literal. |
| `pagination` | [PaginationRequest](pagination.md) | Optional. |

**Response** (`ListAccessResponse`)

| Field | Type | Description |
| --- | --- | --- |
| `covers_all` | bool | `true` if the principal holds the permission on `under_uri` itself, and so on everything below it. |
| `scopes` | AccessScope[] | The places at or below `under_uri` where the principal holds the permission, ordered by `uri`. |
| `pagination` | PaginationResponse | `next_cursor` for the next page. |

**AccessScope**

| Field | Type | Description |
| --- | --- | --- |
| `uri` | string | A resource URI (`SUBTREE`, `EXACT`) or a URI pattern with `_` segments (`PATTERN`). For a grant below `under_uri`, it is the URI the grant was made on, which may have `_` segments in the part that matches `under_uri`. |
| `scope` | AccessScopeKind | Which resources `uri` stands for. |

**AccessScopeKind**

| Value | Meaning |
| --- | --- |
| `ACCESS_SCOPE_KIND_SUBTREE` | The resource `uri` and every resource below it. |
| `ACCESS_SCOPE_KIND_PATTERN` | Every resource whose leading segments match `uri`, where each `_` segment matches exactly one segment, and every resource below those. |
| `ACCESS_SCOPE_KIND_EXACT` | Exactly the resource `uri`. Reserved: grants are always inherited, so it isn't returned today. |

To filter a database by a `SUBTREE` scope `p`, match `path = p` **or** `path` starting with `p/`. A bare prefix
match on `p` would also match siblings such as `/documents/12` for `/documents/1`.

**Errors:** `INVALID_ARGUMENT` for a malformed request or an invalid cursor; `PERMISSION_DENIED` if the API key lacks
either permission; `NOT_FOUND` if `principal_id` is `group:<slug>` and that group doesn't exist.

=== "TypeScript"

    ```ts
    const access = await permio.listAccess({
      principal: "alice",
      permission: "document.read",
      under: "/documents",
    });
    access.coversAll;    // false
    access.toPrefixes(); // ["/documents/4", "/documents/7"]
    ```

    Available from SDK 0.2.0. It follows every page. See [`listAccess`](../sdk/typescript.md#listaccess).

=== "cURL"

    ```bash
    curl "$PERMIO_API/permissions-service/v1/access?project_name=default&principal_id=alice&permission=document.read&under_uri=/documents" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

    ```json
    {"scopes": [
      {"uri": "/documents/4", "scope": "ACCESS_SCOPE_KIND_SUBTREE"},
      {"uri": "/documents/7", "scope": "ACCESS_SCOPE_KIND_SUBTREE"}
    ]}
    ```

=== "Go"

    ```go
    access, err := client.ListAccess(ctx, "alice", "document.read", "/documents")
    // handle err
    access.CoversAll  // false
    access.Prefixes() // ["/documents/4", "/documents/7"]
    ```

    It follows every page. See [`ListAccess`](../sdk/go.md#listaccess).

=== "Python"

    ```python
    access = permio.list_access("alice", "document.read", "/documents")
    if access.covers_all:
        ...  # no filter needed
    else:
        print(access.to_prefixes())  # ["/documents/4", "/documents/7"]
    ```

    It follows every page. See [`list_access`](../sdk/python.md#list_access).

=== "Rust"

    ```rust
    let access = permio.list_access("alice", "document.read", "/documents").await?;
    access.covers_all;    // false
    access.to_prefixes(); // ["/documents/4", "/documents/7"]
    ```

    It follows every page. See [`list_access`](../sdk/rust.md#list_access).

=== "Java"

    ```java
    import io.perms.AccessScopes;

    AccessScopes access = permio.listAccess("alice", "document.read", "/documents");
    access.coversAll();  // false
    access.toPrefixes(); // [/documents/4, /documents/7]
    ```

    It follows every page. See [`listAccess`](../sdk/java.md#listaccess).

### ListPrincipalsWithAccess

`GET /permissions-service/v1/access/principals?project_name=…&resource_uri=…`

Answers "who has access to `resource_uri`?". It lists the principals with a grant on the resource, on an ancestor
of it, or on a stored `_` wildcard URI that matches it, with the grants that give the access.

- With `permission` set, only grants that confer that permission count, so a principal is listed exactly when a
  Check for it passes through its own grants. Without it, every grant with at least one permission or role counts.
- Groups are listed as principals, with `is_group` set. With `expand_groups`, each group's members are listed too,
  once per group, with `via_group` set.
- Entries are ordered by `principal_id`, then `via_group`, and paginated.

**Needs:** `principal.list` and `principal.assignment.list` on the project.

**Request** (`ListPrincipalsWithAccessRequest`)

| Field | Type | Description |
| --- | --- | --- |
| `project_name` | string | Required. |
| `resource_uri` | string | Required. The resource to look at. A `_` segment here is literal. |
| `permission` | string | Optional. Only count grants that confer this permission. |
| `expand_groups` | bool | Optional. Also list the members of every listed group. |
| `pagination` | [PaginationRequest](pagination.md) | Optional. |

**Response** (`ListPrincipalsWithAccessResponse`): `principals` (PrincipalAccess[]) and `pagination`.

**PrincipalAccess**

| Field | Type | Description |
| --- | --- | --- |
| `principal_id` | string | The principal. A group appears as `group:<slug>`. |
| `is_group` | bool | `true` if `principal_id` is a group. |
| `via_group` | string | For entries added by `expand_groups`: the slug of the group through which the principal holds the grants in `via`. Empty for grants made to the principal itself. |
| `via` | AccessGrant[] | The grants that give the access, most specific first. |

**AccessGrant**

| Field | Type | Description |
| --- | --- | --- |
| `resource_uri` | string | The URI the grant was made on: the resource itself, an ancestor, or a URI with `_` segments that matches it. |
| `inherited` | bool | `true` unless the grant was made on exactly the resource. |
| `match` | AccessGrantMatch | `ACCESS_GRANT_MATCH_EXACT` (on the resource), `ACCESS_GRANT_MATCH_ANCESTOR` (on an ancestor, possibly with `_` segments) or `ACCESS_GRANT_MATCH_WILDCARD` (same depth, with `_` segments). |
| `role` | AccessGrantRole | Set when the access comes through a role: its `id` and `name`. |
| `direct` | AccessGrantDirect | Set (as an empty message) when the access comes from directly granted permissions. |

`role` and `direct` are a `oneof` called `source`: exactly one is set.

**Errors:** `INVALID_ARGUMENT` for a malformed request or an invalid cursor; `PERMISSION_DENIED` if the API key lacks
either permission.

=== "TypeScript"

    ```ts
    const entries = await permio.whoHasAccess({
      resource: "/documents/42",
      permission: "document.read",
      expandGroups: true,
    });
    ```

    Available from SDK 0.2.0. It follows every page. See [`whoHasAccess`](../sdk/typescript.md#whohasaccess).

=== "cURL"

    ```bash
    curl "$PERMIO_API/permissions-service/v1/access/principals?project_name=default&resource_uri=/documents/42&permission=document.read&expand_groups=true" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

    ```json
    {"principals": [
      {"principalId": "alice",
       "via": [{"resourceUri": "/documents", "inherited": true, "match": "ACCESS_GRANT_MATCH_ANCESTOR",
                "role": {"id": "ROLE_ID", "name": "viewer"}}]},
      {"principalId": "bob", "viaGroup": "editors",
       "via": [{"resourceUri": "/documents", "inherited": true, "match": "ACCESS_GRANT_MATCH_ANCESTOR", "direct": {}}]},
      {"principalId": "group:editors", "isGroup": true,
       "via": [{"resourceUri": "/documents", "inherited": true, "match": "ACCESS_GRANT_MATCH_ANCESTOR", "direct": {}}]}
    ]}
    ```

=== "Go"

    ```go
    entries, err := client.WhoHasAccess(ctx, "/documents/42", &permio.WhoHasAccessOptions{
        Permission:   "document.read",
        ExpandGroups: true,
    })
    ```

    It follows every page. See [`WhoHasAccess`](../sdk/go.md#whohasaccess).

=== "Python"

    ```python
    for entry in permio.who_has_access("/documents/42", permission="document.read", expand_groups=True):
        print(entry.principal, entry.via_group, [g.resource for g in entry.via])
    ```

    It follows every page. See [`who_has_access`](../sdk/python.md#who_has_access).

=== "Rust"

    ```rust
    use permio::WhoHasAccess;

    let entries = permio
        .who_has_access(
            WhoHasAccess::new("/documents/42")
                .permission("document.read")
                .expand_groups(true),
        )
        .await?;
    for e in &entries {
        println!("{} {} {:?}", e.principal, e.is_group, e.via_group);
    }
    ```

    It follows every page. See [`who_has_access`](../sdk/rust.md#who_has_access).

=== "Java"

    ```java
    import io.perms.AccessEntry;
    import java.util.List;

    List<AccessEntry> entries = permio.whoHasAccess("/documents/42", "document.read", true);
    ```

    It follows every page. See [`whoHasAccess`](../sdk/java.md#whohasaccess).

---

## Groups

A [group](../concepts/groups.md) is a named set of principals in a project. Grant to its principal ID,
`group:<slug>`, with [GrantUserPermissionsAndRolesOnResource](#grantuserpermissionsandrolesonresource), and every
member holds the grant. Groups can't contain groups.

In the paths below, `{name}` is the group's slug: 1–64 characters, lowercase letters, digits and `-`.

**Group**

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Unique ID. |
| `organisation_id` | string | Owning organisation. |
| `project_name` | string | Owning project. |
| `name` | string | The slug, unique within the project. It can't be changed. |
| `description` | string | Free text, up to 1024 characters. |
| `principal_id` | string | The principal ID grants to the group are made to: `group:<name>`. |
| `created_at`, `updated_at` | Timestamp | |

**GroupMember**: `principal_id` (string) and `created_at` (Timestamp, when the principal was added).

### CreateGroup

`POST /permissions-service/v1/groups`

Creates a group and returns the `Group`. Returns `ALREADY_EXISTS` if the project already has a group with this name.

**Needs:** `group.create` on the project.

| Field | Type | Description |
| --- | --- | --- |
| `project_name` | string | Required. |
| `name` | string | Required. The slug. |
| `description` | string | Optional. Up to 1024 characters. |

=== "TypeScript"

    ```ts
    const g = await permio.groups.create("editors", { description: "Can edit every document" });
    g.principalId; // "group:editors"
    ```

=== "cURL"

    ```bash
    curl -X POST "$PERMIO_API/permissions-service/v1/groups" \
      -H "Authorization: Bearer $PERMIO_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "default", "name": "editors", "description": "Can edit every document"}'
    ```

=== "Go"

    ```go
    g, err := client.Groups().Create(ctx, "editors", "Can edit every document")
    // handle err
    g.PrincipalID // "group:editors"
    ```

=== "Python"

    ```python
    g = permio.groups.create("editors", description="Can edit every document")
    g.principal_id  # "group:editors"
    ```

=== "Rust"

    ```rust
    let g = permio
        .groups()
        .create("editors", Some("Can edit every document"))
        .await?;
    g.principal_id; // "group:editors"
    ```

=== "Java"

    ```java
    import io.perms.proto.permissions.v1.Group;

    Group g = permio.groups().create("editors", "Can edit every document");
    g.getPrincipalId(); // "group:editors"
    ```

### GetGroup

`GET /permissions-service/v1/groups/{name}?project_name=…`

Returns a `Group`, or `NOT_FOUND`.

**Needs:** `group.get` on the group.

=== "TypeScript"

    ```ts
    const g = await permio.groups.get("editors");
    ```

=== "cURL"

    ```bash
    curl "$PERMIO_API/permissions-service/v1/groups/editors?project_name=default" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

### UpdateGroup

`PUT /permissions-service/v1/groups/{name}`

Replaces a group's description and returns the updated `Group`, or `NOT_FOUND`. The name can't be changed, because
`group:<name>` is the principal ID its grants are stored under.

**Needs:** `group.update` on the group.

| Field | Type | Description |
| --- | --- | --- |
| `project_name` | string | Required. |
| `name` | string | Required (path). |
| `description` | string | The new description. Up to 1024 characters. |

=== "TypeScript"

    ```ts
    await permio.groups.update("editors", { description: "Edits documents and comments" });
    ```

=== "cURL"

    ```bash
    curl -X PUT "$PERMIO_API/permissions-service/v1/groups/editors" \
      -H "Authorization: Bearer $PERMIO_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "default", "description": "Edits documents and comments"}'
    ```

### DeleteGroup

`DELETE /permissions-service/v1/groups/{name}?project_name=…`

Deletes a group together with its memberships and every grant made to it, in one transaction. This call is
idempotent: it succeeds whether or not the group existed.

**Needs:** `group.delete` on the group, and `principal.assignment.delete` on the project, because it revokes the
group's grants.

=== "TypeScript"

    ```ts
    await permio.groups.delete("editors");
    ```

=== "cURL"

    ```bash
    curl -X DELETE "$PERMIO_API/permissions-service/v1/groups/editors?project_name=default" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

### ListGroups

`GET /permissions-service/v1/groups?project_name=…`

Lists the groups in a project, ordered by name. The response has `groups` (Group[]) and `pagination`. It takes
`pagination` and `search` (filters by name, up to 128 characters).

**Needs:** `group.list` on the project.

=== "TypeScript"

    ```ts
    for await (const g of permio.groups.list({ search: "edit" })) console.log(g.name);
    ```

=== "cURL"

    ```bash
    curl "$PERMIO_API/permissions-service/v1/groups?project_name=default&search=edit" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

### AddGroupMembers

`POST /permissions-service/v1/groups/{name}/members/add`

Adds up to 100 principals to a group. Principals that are already members are reported, not added again. A
principal that is new to your organisation counts towards its unique principals, exactly as if it had been granted
something, and goes through the same billing check.

**Needs:** `group.member.add` on the group **and** `principal.assignment.create` on the project. A member gets the
group's grants anywhere in the project, so only a caller who could grant that access directly may add members.

| Field | Type | Description |
| --- | --- | --- |
| `project_name` | string | Required. |
| `name` | string | Required (path). |
| `principal_ids` | string[] | Required. 1–100 unique principal IDs. They may not start with `group:`. |

**Response** (`AddGroupMembersResponse`)

| Field | Type | Description |
| --- | --- | --- |
| `added_principal_ids` | string[] | The principals that were added, in request order. |
| `existing_principal_ids` | string[] | The principals that were already members, in request order. |

**Errors:** `INVALID_ARGUMENT` if a principal ID starts with `group:` (groups can't be nested); `NOT_FOUND` if the
group doesn't exist; `PERMISSION_DENIED` if the caller lacks either permission, or if the organisation may not add
new principals.

=== "TypeScript"

    ```ts
    const { added, existing } = await permio.groups.addMembers("editors", ["alice", "bob"]);
    ```

=== "cURL"

    ```bash
    curl -X POST "$PERMIO_API/permissions-service/v1/groups/editors/members/add" \
      -H "Authorization: Bearer $PERMIO_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "default", "principal_ids": ["alice", "bob"]}'
    ```

    ```json
    {"addedPrincipalIds": ["alice", "bob"]}
    ```

=== "Go"

    ```go
    change, err := client.Groups().AddMembers(ctx, "editors", []string{"alice", "bob"})
    // handle err
    change.Changed   // added
    change.Unchanged // already members
    ```

=== "Python"

    ```python
    res = permio.groups.add_members("editors", ["alice", "bob"])
    res.added, res.existing  # (["alice", "bob"], [])
    ```

=== "Rust"

    ```rust
    let res = permio.groups().add_members("editors", ["alice", "bob"]).await?;
    println!("{:?} {:?}", res.added, res.existing);
    ```

=== "Java"

    ```java
    import io.perms.AddMembersResult;
    import java.util.List;

    AddMembersResult res = permio.groups().addMembers("editors", List.of("alice", "bob"));
    res.added();
    res.existing();
    ```

### RemoveGroupMembers

`POST /permissions-service/v1/groups/{name}/members/remove`

Removes up to 100 principals from a group. Principals that aren't members are reported. It takes the same fields as
AddGroupMembers.

**Needs:** `group.member.remove` on the group **and** `principal.assignment.create` on the project.

**Response** (`RemoveGroupMembersResponse`): `removed_principal_ids` and `not_member_principal_ids` (string[], in
request order).

=== "TypeScript"

    ```ts
    const { removed, notMembers } = await permio.groups.removeMembers("editors", ["bob"]);
    ```

=== "cURL"

    ```bash
    curl -X POST "$PERMIO_API/permissions-service/v1/groups/editors/members/remove" \
      -H "Authorization: Bearer $PERMIO_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "default", "principal_ids": ["bob"]}'
    ```

### ListGroupMembers

`GET /permissions-service/v1/groups/{name}/members?project_name=…`

Lists a group's members, ordered by principal ID. The response has `members` (GroupMember[]) and `pagination`. It
takes `pagination`.

**Needs:** `group.member.list` on the group.

=== "TypeScript"

    ```ts
    for await (const m of permio.groups.listMembers("editors")) console.log(m.principalId);
    ```

=== "cURL"

    ```bash
    curl "$PERMIO_API/permissions-service/v1/groups/editors/members?project_name=default" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

### ListGroupsForPrincipal

`GET /permissions-service/v1/group-memberships/{principal_id=**}?project_name=…`

Lists the groups a principal is a member of in the project, ordered by name. The response has `groups` (Group[]) and
`pagination`. It takes `pagination`. Principal IDs may contain slashes.

**Needs:** `group.list` on the project, and `principal.assignment.list` on the principal.

=== "TypeScript"

    ```ts
    for await (const g of permio.groups.listForPrincipal("alice")) console.log(g.name);
    ```

=== "cURL"

    ```bash
    curl "$PERMIO_API/permissions-service/v1/group-memberships/alice?project_name=default" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```
