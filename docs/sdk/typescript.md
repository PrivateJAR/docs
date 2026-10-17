# TypeScript SDK

`permio` is the official TypeScript/JavaScript client for the perms.io API. It wraps the API in a few calls for
asking "may this principal do X on this resource?". It also gives you typed errors, retries for idempotent reads
and async iterators over list endpoints. The full generated API is there too, as an escape hatch.

- Runs on Node 18+, edge runtimes and browsers. It talks gRPC-web over `fetch`.
- Ships ESM and CommonJS builds with bundled type definitions.
- Has three runtime dependencies: `@bufbuild/protobuf`, `@connectrpc/connect` and `@connectrpc/connect-web`.

!!! warning "Pre-release"

    The package has not been published to npm yet. The install command below will work once the first version
    (`0.1.0`) is released.

## Install

```bash
npm install permio
```

## Create a client

```ts
import { Permio } from "permio";

const permio = new Permio({
  apiKey: process.env.PERMIO_API_KEY!,
  project: "default", // default project for the helpers below
});
```

The constructor checks the API key's format and checksum straight away. A mistyped or truncated key throws
`PermioConfigError` before any request is sent. See [API keys](../concepts/api-keys.md) for the format.

!!! danger "Keep API keys on the server"

    The SDK works in browsers, but an API key in a browser bundle is visible to anyone who loads the page. Call
    perms.io from your backend, route handlers or middleware.

### Options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `apiKey` | `string` | required | A `perms_…` key from the dashboard, or a legacy JWT key. |
| `baseUrl` | `string` | `https://temp-api.perms.io` | API host. `DEV_BASE_URL` (`https://dev-api.perms.io`) is exported for the development API. |
| `project` | `string` | none | Default project name for `check*` and `list*` helpers. Each call can override it. |
| `timeoutMs` | `number` | `10000` | Timeout for each attempt, in ms. `0` disables it. |
| `retries` | `number \| RetryOptions` | `2` | Retries for idempotent reads. A number sets `maxRetries`; see [Retries and timeouts](#retries-and-timeouts). |
| `fetch` | `typeof fetch` | `globalThis.fetch` | Custom `fetch`, for example to add an agent, or for tests. |
| `transport` | `Transport` | gRPC-web | Advanced: a Connect transport to use instead, for example `createRouterTransport` in tests. `baseUrl` and `fetch` are then ignored. |

The production default is `https://temp-api.perms.io`, which will move to `https://api.perms.io`. The SDK's
default will follow in a future release.

```ts
import { Permio, DEV_BASE_URL } from "permio";

const devClient = new Permio({ apiKey: process.env.PERMIO_API_KEY!, baseUrl: DEV_BASE_URL, project: "default" });
```

The client also exposes `permio.project`, `permio.baseUrl` and `permio.apiKeyKind` (`"opaque"` or `"jwt"`).

## Checking permissions

All the check helpers take the same parameters (`CheckParams`):

| Parameter | Description |
| --- | --- |
| `principal` | Required. The ID of the user, service or other principal being checked. |
| `resource` / `resources` | One resource URI, or several. Every resource is checked. |
| `permission` / `permissions` | One permission name, or several. |
| `project` | Project to check in. Defaults to the client's `project`. |
| `signal` | An `AbortSignal` that cancels the call. |
| `timeoutMs` | Overall deadline for this call in ms, across retries. |
| `headers` | Extra request headers. |

You can pass both the singular and the plural form; they are merged. Duplicates are removed before sending. A
single check accepts up to 100 resources and 100 permissions.

### `check`

Resolves to `true` when the principal holds **every** permission on **every** resource:

```ts
import { resource } from "permio";

const allowed = await permio.check({
  principal: "alice",
  resource: resource("documents", 42), // "/documents/42"
  permission: "document.read",
});
```

A principal that lacks the permission is a normal answer: `check` resolves to `false`. It only throws when the call
itself fails, for example because of a bad key, malformed input or network trouble.

### `checkDetailed`

Same question, but it also tells you what is missing, per resource and in request order:

```ts
const { allowed, missing } = await permio.checkDetailed({
  principal: "alice",
  resources: ["/documents/1", "/documents/2"],
  permissions: ["document.read", "document.write"],
});
// allowed: false
// missing: [{ resource: "/documents/2", permissions: ["document.write"] }]
```

`missing` is an array of `{ resource: string; permissions: string[] }` (`MissingPermission`), and is empty when
`allowed` is `true`.

### `assert`

Resolves when the principal is allowed and throws `PermioDeniedError` when it is not. The error carries
`principal` and `missing`:

```ts
await permio.assert({ principal: "alice", resource: "/documents/1", permission: "document.write" });
```

### `checkAny`

Resolves to `true` when, **on every resource**, the principal holds **at least one** of the permissions. It is
still a single API call:

```ts
await permio.checkAny({
  principal: "alice",
  resource: "/documents/1",
  permissions: ["document.admin", "document.write"],
});
```

### `checkAll`

An alias of `check`: every permission on every resource.

## Resource URIs

Resource URIs are paths such as `/projects/p1/documents/42`. A grant on a URI also covers every URI beneath it. See
[Resources and inheritance](../concepts/resources.md) for the full rules.

### `resource(...segments)`

Builds a URI from raw segments. It adds the leading `/` and percent-encodes each segment, so an ID that contains
`/`, spaces or other reserved characters stays a single segment:

```ts
import { resource } from "permio";

resource("projects", "p1", "documents", 42); // "/projects/p1/documents/42"
resource("files", "reports/2026.pdf");       // "/files/reports%2F2026.pdf"
```

On top of `encodeURIComponent`, it also encodes `! ' ( ) *`, because the API rejects `( ) *` in segments. Empty
segments throw `PermioValidationError`.

!!! tip

    Build URIs the same way when you grant and when you check, or they will not match.

### Other helpers

| Export | Description |
| --- | --- |
| `encodeSegment(segment)` | Encodes one segment the way `resource()` does. |
| `assertResourceUri(uri)` | Throws `PermioValidationError` unless `uri` has the basic shape the API accepts: a leading `/`, no empty segments, no whitespace or control characters, and at most 2048 bytes. |
| `MAX_RESOURCE_URI_LENGTH` | `2048`. |

Every check runs `assertResourceUri` on its URIs before sending. The API enforces the remaining rules, such as no
`( ) [ ] { } * + ? | ^ $ \` in segments, and answers with `InvalidArgument`, which the SDK raises as
`PermioValidationError`.

## Errors

Every error the SDK throws extends `PermioError`. It has these properties:

- `code`: the gRPC status `Code`. `Code` is re-exported from `permio`.
- `codeName`: the code's name in lower case, for example `"permission_denied"`.
- `metadata`: the response headers and trailers.
- `cause`: the original error, usually a `ConnectError`.

| Class | When |
| --- | --- |
| `PermioConfigError` | Bad client setup: a malformed API key, no `project`, an invalid `baseUrl` or no `fetch`. |
| `PermioAuthError` | `Unauthenticated`: the key is missing, unknown or invalidated. |
| `PermioPermissionError` | `PermissionDenied`: the **API key** lacks the rights for this call. `missing` lists what it lacks when the API says. |
| `PermioValidationError` | `InvalidArgument`, or the SDK's own input checks (for example a URI without a leading `/`). |
| `PermioNotFoundError` | `NotFound`, for example `getPermission` for a name that does not exist. |
| `PermioUnavailableError` | `Unavailable`, including network failures. |
| `PermioTimeoutError` | `DeadlineExceeded`, including the SDK's own timeouts. |
| `PermioDeniedError` | Thrown only by `assert()`, when the **principal** is not allowed. Has `principal` and `missing`. |

Any other status is a plain `PermioError` with the matching `code`.

!!! note "Denied is not an error"

    `PermioPermissionError` is about the *caller*. It means your API key is not allowed to make the call: for
    `Check`, the key needs `permission.check` on the checked resources and on the principal. A principal failing a
    check is a normal result: `check()` returns `false` and `assert()` throws `PermioDeniedError`.

`PermioPermissionError.missing` uses the API's fully qualified URIs (`/organisation/{org}/project/{project}/...`),
not the URIs you sent.

```ts
import { PermioAuthError, PermioDeniedError, PermioError, PermioPermissionError } from "permio";

try {
  await permio.assert({ principal: "alice", resource: "/documents/1", permission: "document.write" });
} catch (err) {
  if (err instanceof PermioDeniedError) {
    // the principal may not do this: respond with 403
  } else if (err instanceof PermioPermissionError) {
    // the API key may not run this check (it needs permission.check)
    console.error(err.missing);
  } else if (err instanceof PermioAuthError) {
    // the API key is missing, unknown or invalidated
  } else if (err instanceof PermioError) {
    console.error(err.codeName, err.message);
  }
}
```

`toPermioError(error)` converts any thrown value into the matching `PermioError` subclass.
`parseMissingPermissions(message)` extracts the missing list from a `PermissionDenied` message. You only need these
if you build your own transport or client.

## Retries and timeouts

- **Retries:** idempotent reads (`Check`, and every `Get*` and `List*` RPC) are retried on `Unavailable` and
  `DeadlineExceeded`. They are retried twice by default, with exponential backoff and jitter. Network failures
  count as `Unavailable`.
- **Writes** (every Create, Update, Delete, Grant, Revoke, Invite and so on) are never retried.
- **Timeouts:**
  - The client's `timeoutMs` applies to each attempt (default 10 s).
  - A call's `timeoutMs` is an overall deadline across all attempts.
  - Aborting `signal` cancels the call and any pending retry.

```ts
const permio = new Permio({
  apiKey: process.env.PERMIO_API_KEY!,
  project: "default",
  timeoutMs: 5_000,
  retries: { maxRetries: 3, baseDelayMs: 100, maxDelayMs: 2_000 },
});

await permio.check({ principal: "alice", resource: "/documents/1", permission: "document.read", timeoutMs: 8_000 });
```

`RetryOptions` has these fields:

- `maxRetries`: retries after the first attempt. Default 2.
- `baseDelayMs`: the first delay, which doubles each time. Default 100.
- `maxDelayMs`: the cap on a single delay. Default 2000.

`isIdempotentMethod("permio.permissions.v1.PermissionsService.Check")` tells you whether the SDK retries a given RPC.

## Listing with iterators

List RPCs are paginated with a cursor (see [Pagination](../api-reference/pagination.md)). The helpers return async
iterators that fetch pages as you go:

```ts
for await (const p of permio.listPermissions({ search: "document." })) console.log(p.name);
for await (const role of permio.listRoles()) console.log(role.name, role.permissions.length);
for await (const id of permio.listPrincipals()) console.log(id);
for await (const a of permio.listAssignments({ principal: "alice" })) console.log(a.resourceUri, a.roles);
```

| Method | Yields |
| --- | --- |
| `listPermissions(params?)` | `Permission` |
| `listRoles(params?)` | `Role` (with its `permissions`) |
| `listPrincipals(params?)` | `string` principal IDs that have grants in the project |
| `listAssignments({ principal, ... })` | `Assignment` (`resourceUri`, `permissions`, `roles`) |

Each method takes these parameters:

- `project`
- `pageSize`: 1–100, default 100
- `signal`: stops iteration and any in-flight request
- `timeoutMs`: per page
- `headers`

`listPermissions`, `listRoles` and `listPrincipals` also take `search`, which filters by name.

For any other list RPC, use `paginate`, which follows `next_cursor` until the API returns an empty one:

```ts
import { paginate } from "permio";

for await (const key of paginate(
  (pagination, signal) =>
    permio.organisations.listAPIKeys({ organisationId: "your-org-id", projectName: "default", pagination }, { signal }),
  (res) => res.apiKeys,
)) {
  console.log(key.name);
}
```

## Raw clients (full API)

`permio.permissions` and `permio.organisations` are the generated [Connect](https://connectrpc.com/docs/web/using-clients)
clients for `permio.permissions.v1.PermissionsService` and `permio.organisation.v1.OrganisationService`.
Authentication, timeouts, retries and error mapping are already applied. Every RPC in the
[API reference](../api-reference/index.md) is available, with request and response types generated from the
protobuf definitions. Method names are the RPC names in lower camel case, and fields are camelCase:

```ts
await permio.permissions.createPermission({
  projectName: "default",
  name: "document.read",
  description: "Read documents",
});

const role = await permio.permissions.createRole({
  projectName: "default",
  name: "viewer",
  permissions: ["document.read"], // permission names
});

await permio.permissions.grantUserPermissionsAndRolesOnResource({
  projectName: "default",
  userId: "alice",
  resourceUri: "/documents",
  roles: [role.id], // role IDs
});

const res = await permio.permissions.check({
  projectName: "default",
  principalId: "alice",
  resourceUris: ["/documents/42"],
  permissions: ["document.read"],
});
console.log(res.passed, res.missingPermissions);
```

!!! note "What a key can call"

    By default an API key has **check** access: it can run checks and read permissions, roles, principals and
    assignments. Creating, updating or deleting permissions and roles, and granting or revoking, needs a key with
    full access. See [API keys](../concepts/api-keys.md#access-levels).

The generated messages are exported as the namespaces `permissionsv1`, `organisationv1` and `paginationv1`. The
service descriptors are exported as `PermissionsService` and `OrganisationService`:

```ts
import { create } from "@bufbuild/protobuf";
import { permissionsv1 } from "permio";

const req = create(permissionsv1.CheckPermissionRequestSchema, { projectName: "default" });
```

## API key helpers

| Export | Description |
| --- | --- |
| `validateApiKey(key)` | Returns `"opaque"` for `perms_` keys and `"jwt"` for legacy JWT keys. Throws `PermioConfigError` if the key is malformed. |
| `isValidApiKey(key)` | `true` if `validateApiKey` would pass. |
| `API_KEY_LENGTH` | `44`. |

These only check the shape and checksum. Only the API can tell you whether a key exists and is still valid.

## Express

```ts
import express, { type RequestHandler } from "express";
import { Permio, PermioDeniedError, resource } from "permio";

const permio = new Permio({ apiKey: process.env.PERMIO_API_KEY!, project: "default" });
const app = express();

const can = (permission: string): RequestHandler => async (req, res, next) => {
  try {
    await permio.assert({
      principal: res.locals.userId, // set by your auth middleware
      resource: resource("documents", req.params.id!),
      permission,
    });
    next();
  } catch (err) {
    if (err instanceof PermioDeniedError) {
      res.status(403).json({ error: "forbidden" });
      return;
    }
    next(err); // any other PermioError: auth, validation, network...
  }
};

app.get("/documents/:id", can("document.read"), (req, res) => {
  res.json({ id: req.params.id });
});
```

## Next.js

Create one client and import it on the server only:

```ts
// lib/permio.ts
import { Permio } from "permio";

export const permio = new Permio({ apiKey: process.env.PERMIO_API_KEY!, project: "default" });
```

### Route handler (App Router)

```ts
// app/documents/[id]/route.ts
import { resource } from "permio";
import { permio } from "@/lib/permio";
import { getUserId } from "@/lib/auth"; // your auth

export async function DELETE(_req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const allowed = await permio.check({
    principal: await getUserId(),
    resource: resource("documents", id),
    permission: "document.delete",
  });
  if (!allowed) return new Response("Forbidden", { status: 403 });
  // ...delete the document
  return new Response(null, { status: 204 });
}
```

### Middleware

The client only needs `fetch`, so it also runs in the Edge runtime and in middleware:

```ts
// middleware.ts
import { NextResponse, type NextRequest } from "next/server";
import { resource } from "permio";
import { permio } from "@/lib/permio";
import { getUserIdFromRequest } from "@/lib/auth"; // your auth

export async function middleware(req: NextRequest) {
  const userId = await getUserIdFromRequest(req);
  if (!userId) return NextResponse.redirect(new URL("/login", req.url));

  const allowed = await permio.check({
    principal: userId,
    resource: resource("admin"),
    permission: "admin.access",
  });
  return allowed ? NextResponse.next() : new NextResponse("Forbidden", { status: 403 });
}

export const config = { matcher: "/admin/:path*" };
```

## How it talks to the API

The SDK uses the gRPC-web protocol over `fetch` (through `@connectrpc/connect-web`). The perms.io gateway accepts
it directly from servers, edge runtimes and browsers. The key is sent as `Authorization: Bearer <key>`. Timeouts are
enforced on the client, so no `grpc-timeout` header is sent.
