# API overview

The perms.io API has two services:

| Service | Proto | What it does |
| --- | --- | --- |
| [Permissions](permissions.md) | `permio.permissions.v1.PermissionsService` | Permissions, roles, grants and **checks**. This is the service your application calls. |
| [Organisations](organizations.md) | `permio.organisation.v1.OrganisationService` | Organisations, projects, API keys and team members. Mostly used by the dashboard. |

Both are defined in Permio's protobuf definitions. The same host serves them as REST/JSON, gRPC and gRPC-web.

--8<-- "hosts.md"

## Protocols

| Protocol | How to call it |
| --- | --- |
| **REST/JSON** | The HTTP method and path listed for each RPC in this reference, for example `POST $PERMIO_API/permissions-service/v1/permissions/check`. Request bodies accept the proto field names (`project_name`). Responses use camelCase JSON names (`missingPermissions`) and leave out fields that have default values. |
| **gRPC** | Connect to the host on port 443 with TLS, for example `temp-api.perms.io:443`, and send the key as `authorization` metadata. |
| **gRPC-web** | The protocol the [TypeScript SDK](../sdk/typescript.md) uses. It works from servers, edge runtimes and browsers. |

For `GET` and `DELETE` requests over REST, fields that aren't in the path go in the query string. Nested fields use
dot notation, for example `?project_name=default&pagination.limit=50`.

## Authentication

Every request needs an [API key](../concepts/api-keys.md), sent as a bearer token:

```
Authorization: Bearer perms_...
```

Keys are 44 characters long: `perms_`, 32 random base62 characters and a 6-character checksum. A key is shown once,
when you create it in the dashboard. Only a hash of it is stored, and you can invalidate it at any time. Older JWT
API keys are still accepted.

A key acts within its own **project**. Your organisation is worked out from the key, so permission requests don't
include an organisation ID. A key gets its own grants on its project: by default **check** access, which allows
`Check`, the access queries and the read-only calls. See [Access levels](../concepts/api-keys.md#access-levels).

## Errors

A **denied check is not an error**. `Check` returns success with `passed: false` and a list of
`missing_permissions`. Errors mean that the request itself could not be carried out:

| gRPC status | HTTP | Meaning |
| --- | --- | --- |
| `INVALID_ARGUMENT` (3) | 400 | Malformed input: an invalid resource URI, an empty permissions list, a bad project name, more than 100 items in a check, and so on. |
| `UNAUTHENTICATED` (16) | 401 | The API key is missing, malformed, unknown or invalidated. |
| `PERMISSION_DENIED` (7) | 403 | The **API key** isn't allowed to make this call. For example, a key without `permission.check` calling `Check`, or a check-only key creating a role. The message lists what is missing. |
| `NOT_FOUND` (5) | 404 | The permission, role, group or other entity doesn't exist. Also returned when a `group:<slug>` principal names a group that doesn't exist. |
| `ALREADY_EXISTS` (6) | 409 | A group with this name already exists in the project. |
| `INTERNAL` (13) | 500 | Something went wrong on our side. |
| `UNAVAILABLE` (14) | 503 | The service is temporarily unavailable. Safe to retry for reads. |

Over REST, the error body carries the gRPC code and a message:

```json
{"code": 16, "message": "invalid api key"}
```

Over gRPC and gRPC-web, the code arrives as `grpc-status` and the text as `grpc-message`.

## Clients

=== "TypeScript"

    The [TypeScript SDK](../sdk/typescript.md) (`npm install permio`, pre-release) is the recommended client.
    Besides the check helpers, it exposes every RPC on this page through `permio.permissions` and
    `permio.organisations`.

=== "cURL"

    Every RPC has a REST path, listed with each method in this reference.

    ```bash
    curl -X POST "$PERMIO_API/permissions-service/v1/permissions/check" \
      -H "Authorization: Bearer $PERMIO_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "default", "principal_id": "alice", "resource_uris": ["/documents/42"], "permissions": ["document.read"]}'
    ```

=== "Go"

    Generated gRPC client. It isn't publicly available yet.

    ```go
    import (
        permissionsv1 "github.com/PrivateJAR/permio-go/proto/permissions/v1"
        "google.golang.org/grpc"
        "google.golang.org/grpc/credentials"
        "google.golang.org/grpc/metadata"
    )

    conn, err := grpc.NewClient("temp-api.perms.io:443",
        grpc.WithTransportCredentials(credentials.NewTLS(nil)))
    // handle err
    client := permissionsv1.NewPermissionsServiceClient(conn)
    ctx = metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+apiKey)

    res, err := client.Check(ctx, &permissionsv1.CheckPermissionRequest{
        ProjectName:  "default",
        PrincipalId:  "alice",
        ResourceUris: []string{"/documents/42"},
        Permissions:  []string{"document.read"},
    })
    ```

    Packages: `github.com/PrivateJAR/permio-go/proto/permissions/v1`, `.../proto/organisation/v1`,
    `.../proto/pagination/v1`.

=== "Python"

    Generated gRPC stubs. They aren't publicly available yet.

    ```python
    import grpc
    from permio.permissions.v1 import permissions_pb2, permissions_pb2_grpc

    channel = grpc.secure_channel("temp-api.perms.io:443", grpc.ssl_channel_credentials())
    client = permissions_pb2_grpc.PermissionsServiceStub(channel)

    res = client.Check(
        permissions_pb2.CheckPermissionRequest(
            project_name="default",
            principal_id="alice",
            resource_uris=["/documents/42"],
            permissions=["document.read"],
        ),
        metadata=[("authorization", f"Bearer {api_key}")],
    )
    print(res.passed)
    ```

    Modules: `permio.permissions.v1`, `permio.organisation.v1`, `permio.pagination.v1`.

=== "Rust"

    Generated prost/tonic client. It isn't publicly available yet.

    ```rust
    use permio_rust::permissions::v1::permissions_service_client::PermissionsServiceClient;
    use permio_rust::permissions::v1::CheckPermissionRequest;
    ```

    Send the key as `authorization: Bearer <key>` metadata, for example with a tonic interceptor.

Field names in this reference are the proto names (`project_name`). The generated clients use their language's
convention: `ProjectName` in Go, `project_name` in Python and Rust, and `projectName` in TypeScript.
