# API keys

Your backend authenticates to the perms.io API with an **API key**. Each key belongs to one project.

## Creating a key

In the [dashboard](https://app.perms.io), pick the project in the project switcher, open **API Keys** and click
**Create New Key**. Give the key a name, ideally after the service or environment that will use it, and click
**Create key**.

!!! warning "Shown once"

    The full key is only shown once, when it is created. Copy it into your secrets manager straight away. perms.io
    only stores a hash of the key, so it can't show it to you again. If you lose a key, create a new one and
    invalidate the old one.

## Format

Keys are opaque, 44-character strings:

```
perms_ + 32 random base62 characters + 6-character checksum
```

- The `perms_` prefix makes leaked keys easy for secret scanners to spot.
- The last 6 characters are a CRC32 checksum of the random part. Clients can use them to reject a mistyped or
  truncated key before sending it. The [TypeScript SDK](../sdk/typescript.md) does this in its constructor.
- The checksum only catches typos. Whether a key exists and is still valid is decided by the API.

Older keys were issued as JWTs. These are still accepted.

## Sending a key

Send the key as a bearer token on every request:

=== "HTTP"

    ```
    Authorization: Bearer perms_...
    ```

=== "gRPC metadata"

    ```
    authorization: Bearer perms_...
    ```

A request with a missing, unknown or invalidated key is rejected with `Unauthenticated` (HTTP 401).

## Access levels

A key is a principal in its own right. When it is created, the key is granted a role on its project, and that role
decides which calls the key may make.

| Access | Role | Allows |
| --- | --- | --- |
| **Check** (default) | `apikey.checker` | `Check`. Reading permissions, roles, principals and assignments (`permission.check`, `permission.get`, `permission.list`, `role.get`, `role.list`, `principal.list`, `principal.assignment.get`, `principal.assignment.list`). |
| **Full access** | `apikey.manager` | Everything above, plus creating, updating and deleting permissions and roles, and granting and revoking (`permission.create/update/delete`, `role.create/update/delete`, `principal.assignment.create/delete`). |

!!! note "Full access is on its way"

    The API defines both levels. The dashboard does not offer a choice yet, so keys created there get **check**
    access. Choosing **full access** in the dashboard is coming. Until then, manage permissions, roles and grants
    in the dashboard and use keys for checks.

To create a key with a given level, you must hold every permission that level grants on the project.

A call the key isn't allowed to make is rejected with `PermissionDenied` (HTTP 403). This is about the key's rights,
not the principal you are checking. For `Check`, the key needs `permission.check` on the checked resources and on
the principal, which the check role gives it across its whole project.

Neither role includes organisation-level permissions. Most [Organisation service](../api-reference/organizations.md)
calls are meant for the dashboard and will be denied for an API key.

## Invalidating a key

On the **API Keys** page, click **Invalidate** next to the key and confirm. The key stops working immediately and
this can't be undone. Its grants on the project are removed too. Invalidated keys stay listed, marked
**Invalidated**.

Keys created in the dashboard don't expire, so invalidate any key you no longer need.

## Good practice

- Use one key per service and environment, so you can invalidate one without affecting the others.
- Keep keys on the server. Never ship a key in browser or mobile code: anyone who loads the page can read it.
- Store keys in a secrets manager or environment variables, not in source control.
