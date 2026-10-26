# Go SDK

`github.com/PrivateJAR/permio-go` is the official Go client for the perms.io API. Its package, `permio`, wraps the
API in a few calls for asking "may this principal do X on this resource?". It also gives you typed errors, retries
for idempotent reads and `iter.Seq2` iterators over list endpoints. The generated gRPC clients ship in the same
module, as an escape hatch to the full API.

- Needs Go 1.24 or later.
- Talks native gRPC over HTTP/2 with TLS (1.2 or later), through `google.golang.org/grpc`.
- Depends on `google.golang.org/grpc`, `google.golang.org/protobuf`, `google.golang.org/genproto` and
  `github.com/envoyproxy/protoc-gen-validate`.

!!! note "Versions"

    The SDK hasn't had a tagged release yet; the first will be **v0.1.0**. Tags up to v0.0.18 contain only the
    generated stubs, without the `permio` package described here. If `go get …@latest` gives you one of those, install
    the default branch with `go get github.com/PrivateJAR/permio-go@main` until v0.1.0 is out.

## Install

```bash
go get github.com/PrivateJAR/permio-go@latest
```

## Quick start

```go
import (
    "context"
    "log"
    "os"

    permio "github.com/PrivateJAR/permio-go"
)

client, err := permio.New(permio.Options{
    APIKey:  os.Getenv("PERMIO_API_KEY"),
    Project: "default", // default project for the helpers below
})
if err != nil {
    log.Fatal(err)
}
defer client.Close()

allowed, err := client.Check(ctx, "alice", "document.read", permio.Resource("documents", "42"))
if err != nil {
    // the check could not be answered (bad key, network...): treat it as not allowed
}
```

A principal that lacks the permission is a normal answer: `allowed` is `false` and `err` is `nil`.

`New` checks the API key's format and checksum straight away, so a mistyped or truncated key fails there with an
error of kind `KindConfig`, before any request is sent. See [API keys](../concepts/api-keys.md) for the format. `New`
doesn't connect: the connection is made on the first call. A `*permio.Client` is safe for concurrent use, so create
one and share it.

## Configuration

`permio.New` takes an `Options` struct. Only an API key is required:

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `APIKey` | `string` | `$PERMIO_API_KEY` | A `perms_…` key from the dashboard, or a legacy JWT key. When empty, the `PERMIO_API_KEY` environment variable is used. |
| `Endpoint` | `string` | `permio.DefaultEndpoint` | API host, as `host:port`, a bare host (port 443) or a URL such as `https://dev-api.perms.io`. An `http://` URL dials without TLS. |
| `Project` | `string` | none | Default project for every helper. Helpers fail with `KindConfig` when it is empty. |
| `Timeout` | `time.Duration` | `10 * time.Second` | Timeout for each attempt. Zero means the default; a negative value disables it. |
| `Retry` | `permio.RetryOptions` | 2 retries | Retries for idempotent reads. See [Retries and rate limits](#retries-and-rate-limits). |
| `Insecure` | `bool` | `false` | Dial without TLS. Only for local servers. |
| `UserAgent` | `string` | none | Prepended to grpc-go's user agent. |
| `DialOptions` | `[]grpc.DialOption` | none | Appended to the SDK's dial options. |
| `Conn` | `grpc.ClientConnInterface` | none | Advanced: a connection to use instead of dialling `Endpoint`, for example a bufconn connection in tests. Auth, timeouts, retries and error mapping still apply. You own it: `Close` doesn't close it. |

The host constants are:

| Constant | Value |
| --- | --- |
| `permio.DefaultEndpoint` | `api.perms.io:443`, the production API (`https://api.perms.io`). |
| `permio.DevEndpoint` | `dev-api.perms.io:443`, the development API (`https://dev-api.perms.io`). |

```go
client, err := permio.New(permio.Options{
    APIKey:   os.Getenv("PERMIO_API_KEY"),
    Endpoint: permio.DevEndpoint,
    Project:  "default",
    Timeout:  5 * time.Second,
    Retry:    permio.RetryOptions{MaxRetries: 3},
})
```

There are no per-call options. Instead:

- **Project:** `client.WithProject("other")` returns a client for another project that shares the same connection.
  Close only the original client.
- **Deadline and cancellation:** use the `context.Context` you pass to each call. Its deadline is an overall deadline
  across all attempts; `Options.Timeout` applies to each attempt.

The client also has `client.Project()`, `client.APIKeyKind()` (`permio.APIKeyOpaque` or `permio.APIKeyJWT`) and
`client.Close()`.

### Verifying the key

Only the API can tell you whether a key exists and is still valid. `client.WhoAmI(ctx)` describes the credential and
needs no project, so you can call it at startup:

```go
id, err := client.WhoAmI(ctx)
if err != nil {
    log.Fatal(err) // KindAuth if the key is unknown or invalidated
}
if id.APIKeyAccess != permio.APIKeyAccessFull {
    log.Fatal("this service needs a full-access API key")
}
```

`Identity` has `PrincipalID` (the key's ID), `OrganisationID`, `Kind` (`PrincipalAPIKey`, `PrincipalUser`,
`PrincipalServiceAccount` or `PrincipalUnknown`), `Project` (the project the key belongs to), `APIKeyAccess`
(`APIKeyAccessCheck`, `APIKeyAccessFull` or `APIKeyAccessUnknown`, for API keys only) and `Email` (for users). See
[Access levels](../concepts/api-keys.md#access-levels).

## Checking permissions

Every check helper validates its input before sending: the principal must not be empty, there must be at least one
resource and one permission, and every resource URI must pass `ValidateResourceURI` (see
[Resource URIs](#resource-uris)). Duplicates are removed. A single check takes up to 100 resources and 100
permissions (`permio.MaxBatch`). Input errors are of kind `KindValidation`.

| Method | Returns |
| --- | --- |
| `Check(ctx, principal, permission, resource)` | `(bool, error)`. `true` when the principal holds the permission on the resource. |
| `CheckAll(ctx, principal, permissions, resource)` | `(bool, error)`. `true` when it holds **every** permission. |
| `CheckAny(ctx, principal, permissions, resource)` | `(bool, error)`. `true` when it holds **at least one**. Still a single API call. |
| `CheckDetailed(ctx, permio.CheckRequest)` | `(*permio.CheckResult, error)`. Several resources, with what is missing. |
| `Assert(ctx, principal, permission, resource)` | `error`. `nil` when allowed; an error of kind `KindDenied` when not. |
| `AssertAll(ctx, permio.CheckRequest)` | `error`. As `Assert`, for every permission on every resource. |

### `Check`, `CheckAll` and `CheckAny`

```go
ok, err := client.Check(ctx, "alice", "document.read", "/documents/42")

ok, err = client.CheckAll(ctx, "alice", []string{"document.read", "document.write"}, "/documents/42")

ok, err = client.CheckAny(ctx, "alice", []string{"document.admin", "document.write"}, "/documents/42")
```

A denial is `false` with a `nil` error. These only return an error when the call itself fails, for example because
of a bad key, malformed input or network trouble. `CheckAny` fails closed: if the API denies without saying what is
missing, it returns `false`.

### `CheckDetailed`

Checks every permission on every resource and tells you what is missing, per resource:

```go
res, err := client.CheckDetailed(ctx, permio.CheckRequest{
    Principal:   "alice",
    Resources:   []string{"/documents/1", "/documents/2"},
    Permissions: []string{"document.read", "document.write"},
})
if err != nil {
    return err
}
// res.Allowed: false
// res.Missing: []permio.MissingPermission{{Resource: "/documents/2", Permissions: []string{"document.write"}}}
```

`CheckResult` has `Allowed` and `Missing`, a `[]MissingPermission` (`Resource`, `Permissions`) that is empty when
`Allowed` is `true`.

### `Assert` and `AssertAll`

Return `nil` when the principal is allowed, and a `*permio.Error` of kind `KindDenied` when it is not. The error
carries `Principal` and `Missing`:

```go
err := client.Assert(ctx, "alice", "document.write", "/documents/1")
if errors.Is(err, permio.ErrDenied) {
    // respond with 403
}
```

`AssertAll` takes a `CheckRequest`, like `CheckDetailed`.

### Batch checks

`CheckAll` gives one answer for all its resources together. `BatchCheck` answers **each resource separately**,
which is what you need to filter a list or decide which rows get an "edit" button. It returns a `map[string]bool`
from resource URI to allowed:

```go
uris := make([]string, len(docs))
for i, d := range docs {
    uris[i] = permio.Resource("documents", d.ID)
}
allowed, err := client.BatchCheck(ctx, "alice", []string{"document.read"}, uris)
if err != nil {
    return err
}
var visible []Document
for _, d := range docs {
    if allowed[permio.Resource("documents", d.ID)] {
        visible = append(visible, d)
    }
}
```

`BatchCheckDetailed` takes the same arguments and returns a `[]permio.BatchResult`, one per distinct resource, in
request order:

```go
entries, err := client.BatchCheckDetailed(ctx, "alice",
    []string{"document.read", "document.write"},
    []string{"/documents/1", "/documents/2"})
// [{Resource: "/documents/1", Allowed: true, Missing: []},
//  {Resource: "/documents/2", Allowed: false, Missing: ["document.write"]}]
```

- A resource is allowed only with **all** the permissions (up to 100).
- Duplicate resources are sent once. More than 100 resources are split into several calls, made one after another.
- The SDK fails closed: if the API's answer doesn't have a result for every requested resource, it returns an error
  instead of guessing.

### `ListAccess`

Answers "where may this principal use this permission, at or below `under`?". Access through roles and groups
counts. It follows every page and returns an `*AccessScopes`. The
[Filtering lists and building share dialogs](../guides/filtering-and-sharing.md) guide shows it in context.

```go
access, err := client.ListAccess(ctx, "alice", "document.read", "/documents")
if err != nil {
    return err
}
switch {
case access.CoversAll:
    // alice may read everything under /documents: no filter needed
case !access.HasPatterns():
    fmt.Println(access.Prefixes()) // e.g. [/documents/4 /documents/7]
default:
    fmt.Println(access.RegexpSource()) // one regex covering prefixes and patterns
}
```

| Member | Type | Description |
| --- | --- | --- |
| `Under` | `string` | The URI that was asked about. A `_` segment here is literal. |
| `CoversAll` | `bool` | The principal holds the permission on `Under` itself, so on everything below it. |
| `Scopes` | `[]AccessScope` | `{URI, Kind}`, ordered by URI. `Kind` is `permio.ScopeSubtree`, `ScopePattern`, `ScopeExact` (reserved, not returned today) or `ScopeUnknown` (a kind this SDK version doesn't know; it never matches). |
| `IsEmpty()` | `bool` | No access anywhere under `Under`. |
| `Allows(uri)` | `bool` | Whether `uri` is covered. Matches per segment: `/a/b` covers `/a/b/c` but not `/a/bc`. Malformed URIs are never allowed. |
| `Prefixes()` | `[]string` | The subtree URIs, for prefix filters. Prefixes covered by a shorter one are dropped. Pattern scopes aren't included. |
| `Patterns()` | `[]string` | The pattern URIs, with `_` segments. |
| `HasPatterns()` | `bool` | Some scope is a pattern, so `Prefixes()` alone doesn't cover everything. |
| `Exact()` | `[]string` | The exact URIs. Empty today. |
| `RegexpSource()` | `string` | One anchored regular expression matching exactly what `Allows` accepts, in syntax common to RE2, PCRE and POSIX ERE, so usable in PostgreSQL `~` and MongoDB `$regex`. Matches nothing when there are no scopes. |
| `Regexp()` | `*regexp.Regexp` | `RegexpSource()`, compiled. |

!!! warning

    A prefix `p` from `Prefixes()` means `p` **and everything below it**. Filter with
    `path = p OR path starts with p + "/"`, never a bare "starts with `p`", which would let `/documents/1` match
    `/documents/12`. In SQL, use `starts_with(path, p || '/')` rather than `LIKE`, where `_` is a wildcard.

For a URI outside `Under`, `Allows` returning `false` means "not asked", not "denied". The API key needs
`permission.check` on `under` and `principal.assignment.get` on the principal.

### `WhoHasAccess`

Answers "who has access to this resource?" (the `ListPrincipalsWithAccess` RPC). It follows every page and returns
an `[]AccessEntry`, ordered by principal ID. The options may be `nil`:

```go
entries, err := client.WhoHasAccess(ctx, "/documents/42", &permio.WhoHasAccessOptions{
    Permission:   "document.read",
    ExpandGroups: true,
})
if err != nil {
    return err
}
// [
//   {Principal: "alice", Via: [{Resource: "/documents", Inherited: true, Match: "ancestor",
//                               Source: "role", RoleID: "ROLE_ID", RoleName: "viewer"}]},
//   {Principal: "bob", ViaGroup: "editors", Via: [...]},
//   {Principal: "group:editors", IsGroup: true, Via: [...]},
// ]
```

`WhoHasAccessOptions`:

| Field | Description |
| --- | --- |
| `Permission` | Only count grants that confer this permission, so a principal is listed exactly when a check passes for it through its own grants (or, for entries with `ViaGroup`, through that group). Empty: any grant counts. |
| `ExpandGroups` | Also list every member of each listed group, once per group, with `ViaGroup` set. |

`AccessEntry` has `Principal`, `IsGroup`, `ViaGroup` (a group slug, or `""`) and `Via`, the grants that give the
access, most specific first. Each `AccessVia` has:

- `Resource`: the URI the grant was made on (the resource, an ancestor, or a `_` wildcard URI that matches it);
- `Inherited`: `true` unless the grant was made on exactly the resource;
- `Match`: `"exact"`, `"ancestor"`, `"wildcard"` or `"unknown"`;
- `Source`: `"role"` (with `RoleID` and `RoleName`), `"direct"` for directly granted permissions, or `"unknown"`.

The API key needs `principal.list` and `principal.assignment.list` on the project.

## Granting and revoking

Grants and revokes need a key with full access. See [API keys](../concepts/api-keys.md#access-levels).

```go
err := client.Grant(ctx, permio.GrantRequest{
    Principal:   "alice",
    Resource:    "/documents",          // also covers everything below it
    Permissions: []string{"document.read"},
    Roles:       []string{roleID},      // role IDs, not names
})

err = client.Revoke(ctx, permio.GrantRequest{
    Principal: "alice",
    Resource:  "/documents",
    Roles:     []string{roleID},
})
```

`GrantRequest` has `Principal`, `Resource`, `Permissions` (permission names) and `Roles` (role IDs). It needs at
least one permission or role.

- `Grant` is additive: what the principal already holds there is kept. Unknown permissions or roles fail with
  `KindValidation`.
- `Revoke` applies to exactly `Resource`. Names the grant doesn't hold are ignored, so revoking twice is harmless.
  Grants on ancestor URIs aren't touched, so the principal may still pass a check afterwards; `WhoHasAccess` shows
  where access comes from.
- Both are sent once and never retried automatically (see [Retries and rate limits](#retries-and-rate-limits)).
- `client.GetGrant(ctx, principal, resource)` returns the `*Grant` made on exactly that URI, not inherited ones. The
  API returns role IDs only, so `RoleRef.Name` is empty there.

### Permissions and roles

| Method | Returns |
| --- | --- |
| `CreatePermission(ctx, name, description)` | `*Permission`. Creating one that already exists with the same description succeeds; with another description it fails with `KindAlreadyExists`. |
| `GetPermission(ctx, name)` | `*Permission`, or an error of kind `KindNotFound`. |
| `UpdatePermission(ctx, name, newName, description)` | `*Permission`. Replaces the description and, when `newName` isn't empty, renames it. |
| `DeletePermission(ctx, name)` | `error`. Also deletes every grant of it. Succeeds if it doesn't exist. |
| `CreateRole(ctx, name, description, permissions)` | `*Role`, with its `ID`. Fails with `KindAlreadyExists` if a role with this name has other permissions or another description. |
| `GetRole(ctx, id)` | `*Role`. |
| `UpdateRole(ctx, id, name, description, permissions)` | `*Role`. Replaces the name, description and permissions. |
| `DeleteRole(ctx, id)` | `error`. |

`Permission` has `Name` and `Description`. `Role` has `ID`, `Name`, `Description` and `Permissions` (names, sorted).

```go
role, err := client.CreateRole(ctx, "viewer", "Read documents", []string{"document.read"})
if err != nil {
    return err
}
err = client.Grant(ctx, permio.GrantRequest{Principal: "alice", Resource: "/documents", Roles: []string{role.ID}})
```

## Groups

A [group](../concepts/groups.md) is a named set of principals in a project. Grant to the group's principal ID,
`group:<slug>`, and every member holds the grant. Checks include the principal's groups automatically.

`permio.GroupPrincipal(slug)` returns the group's principal ID. `client.Groups()` returns the group operations, in
the client's project:

```go
groups := client.Groups()

if _, err := groups.Create(ctx, "editors", "Can edit every document"); err != nil {
    return err
}
if _, err := groups.AddMembers(ctx, "editors", []string{"alice", "bob"}); err != nil {
    return err
}
err := client.Grant(ctx, permio.GrantRequest{
    Principal:   permio.GroupPrincipal("editors"), // "group:editors"
    Resource:    "/documents",
    Permissions: []string{"document.write"},
})

ok, err := client.Check(ctx, "alice", "document.write", "/documents/42") // true
```

Every method that takes a group accepts its slug (`"editors"`) or its principal ID (`"group:editors"`). The slug
must be 1–64 lower-case letters, digits and hyphens, or the call fails with `KindValidation` before anything is
sent (`permio.ValidateGroupName` runs the same check).

| Method | Returns |
| --- | --- |
| `Create(ctx, name, description)` | `*Group`. Fails with `KindAlreadyExists` if the project already has a group with this name. |
| `Get(ctx, name)` | `*Group`, or an error of kind `KindNotFound`. |
| `Update(ctx, name, description)` | `*Group`. Replaces the description; a group can't be renamed. |
| `Delete(ctx, name)` | `error`. Deletes the group, its memberships and every grant made to it. Succeeds whether or not it existed. |
| `List(ctx, opts)` | `iter.Seq2[Group, error]`, ordered by name. `opts.Search` filters by name. |
| `AddMembers(ctx, name, principals)` | `*MembershipChange`: `Changed` (added) and `Unchanged` (already members), in request order. |
| `RemoveMembers(ctx, name, principals)` | `*MembershipChange`: `Changed` (removed) and `Unchanged` (weren't members), in request order. |
| `ListMembers(ctx, name, opts)` | `iter.Seq2[GroupMember, error]` (`PrincipalID`, `CreatedAt`), ordered by principal ID. |
| `ListForPrincipal(ctx, principal, opts)` | `iter.Seq2[Group, error]`: the groups the principal is a member of, ordered by name. |

- `AddMembers` and `RemoveMembers` remove duplicates and send 100 principals per call. If a later call fails, the
  result holds the changes made by the calls that succeeded, alongside the error.
- `AddMembers` rejects `group:` IDs with `KindValidation`, because groups can't contain groups.
- `Group` has `Name`, `Description`, `PrincipalID` (`"group:<name>"`), `CreatedAt` and `UpdatedAt`.

```go
change, err := groups.AddMembers(ctx, "group:editors", []string{"alice", "carol"})
// change.Changed: [carol], change.Unchanged: [alice]

for m, err := range groups.ListMembers(ctx, "editors", nil) {
    if err != nil {
        return err
    }
    fmt.Println(m.PrincipalID)
}
```

Reading groups works with a check-access API key. Creating, updating and deleting groups and changing members needs
a key with full access, and changing members also needs the right to grant across the project. See
[Permissions you need](../concepts/groups.md#permissions-you-need).

## Resource URIs

Resource URIs are paths such as `/projects/p1/documents/42`. A grant on a URI also covers every URI beneath it. See
[Resources and inheritance](../concepts/resources.md) for the full rules.

### `Resource(segments...)`

Builds a URI from raw segments. It adds the leading `/` and percent-encodes each segment, so an ID that contains
`/`, spaces or other reserved characters stays a single segment:

```go
permio.Resource("projects", "p1", "documents", "42") // "/projects/p1/documents/42"
permio.Resource("files", "reports/2026.pdf")         // "/files/reports%2F2026.pdf"
```

Only `A–Z`, `a–z`, `0–9` and `- _ . ~` are left as they are. Segments are strings, so convert numeric IDs yourself
(`strconv.Itoa`). An empty segment produces a URI that every call rejects.

!!! tip

    Build URIs the same way when you grant and when you check, or they will not match.

### Other helpers

| Export | Description |
| --- | --- |
| `EncodeSegment(segment)` | Encodes one segment the way `Resource` does. |
| `ValidateResourceURI(uri)` | Returns an error of kind `KindValidation` unless `uri` has the basic shape the API accepts: a leading `/`, no empty segments, no whitespace or control characters, no regular-expression metacharacters (below) and at most 2048 bytes. |
| `MaxResourceURILength` | `2048`. |
| `GroupPrincipal(slug)` | `"group:" + slug`. |
| `GroupPrefix` | `"group:"`. |
| `ValidateGroupName(slug)` | Returns an error of kind `KindValidation` unless the slug is 1–64 lower-case letters, digits and hyphens. |
| `WildcardSegment` | `"_"`, which in a stored grant URI or a pattern scope matches exactly one segment. |

The metacharacters `ValidateResourceURI` rejects are `( ) [ ] { } * + ? | ^ $ \`. Every helper that takes a resource
URI runs it before sending; the API enforces the remaining rules and answers with `InvalidArgument`
(`KindValidation`).

## Errors

Every call that fails returns a `*permio.Error`, including calls made through the
[raw clients](#raw-clients-full-api). It has these fields:

| Field | Description |
| --- | --- |
| `Kind` | A `permio.Kind` that classifies the error (below). |
| `Code` | The gRPC `codes.Code`. `codes.OK` for errors the SDK raises itself (`KindConfig`, `KindDenied`), `codes.InvalidArgument` for its own input checks. |
| `Message` | The server's or the SDK's message. |
| `Missing` | For `KindPermission`, what the API key lacks; for `KindDenied`, what the principal lacks. |
| `Principal` | The checked principal, for `KindDenied`. |
| `RetryAfter` | The delay the server asked for, for `KindRateLimited` and sometimes `KindUnavailable`. Zero when it gave none. |
| `Metadata` | The response headers and trailers. |

Match a kind with `errors.Is` and the `Err…` sentinel, and read the fields with `errors.As`:

| Kind | Sentinel | When |
| --- | --- | --- |
| `KindConfig` | `ErrConfig` | Bad client setup: a malformed API key, an invalid endpoint or no project. |
| `KindAuth` | `ErrAuth` | `Unauthenticated`: the key is missing, unknown or invalidated. |
| `KindPermission` | `ErrPermission` | `PermissionDenied`: the **API key** lacks the rights for this call. |
| `KindValidation` | `ErrValidation` | `InvalidArgument`, or the SDK's own input checks. |
| `KindNotFound` | `ErrNotFound` | `NotFound`, for example `GetPermission` for a name that doesn't exist. |
| `KindAlreadyExists` | `ErrAlreadyExists` | `AlreadyExists`. |
| `KindUnavailable` | `ErrUnavailable` | `Unavailable`, including network failures. |
| `KindTimeout` | `ErrTimeout` | `DeadlineExceeded`, from `Options.Timeout` or the context's deadline. |
| `KindRateLimited` | `ErrRateLimited` | `ResourceExhausted`: the organisation's rate limit is used up. |
| `KindDenied` | `ErrDenied` | Returned only by `Assert` and `AssertAll`, when the **principal** is not allowed. |
| `KindOther` | none | Anything else, including cancellation of the context. |

`permio.KindOf(err)` returns the kind (or `""` for other errors), and `permio.IsNotFound(err)` is a shortcut.
`*Error` also implements `GRPCStatus()`, so `status.Code(err)` works, and `Unwrap()` returns the underlying gRPC or
context error.

!!! note "Denied is not an error"

    `KindPermission` is about the *caller*. It means your API key is not allowed to make the call: for `Check`, the
    key needs `permission.check` on the checked resources and on the principal. A principal failing a check is a
    normal result: `Check` returns `false` with a `nil` error, and only `Assert` returns an error, of kind
    `KindDenied`.

For `KindPermission`, `Missing` uses the API's fully qualified URIs (`/organisation/{org}/project/{project}/...`),
not the URIs you sent.

```go
err := client.Assert(ctx, "alice", "document.write", "/documents/1")

var perr *permio.Error
switch {
case err == nil:
    // allowed
case errors.Is(err, permio.ErrDenied):
    // the principal may not do this: respond with 403
case errors.Is(err, permio.ErrPermission):
    // the API key may not run this check (it needs permission.check)
    errors.As(err, &perr)
    log.Println(perr.Missing)
case errors.Is(err, permio.ErrAuth):
    // the API key is missing, unknown or invalidated
case errors.As(err, &perr):
    log.Println(perr.Kind, perr.Code, perr.Message)
}
```

`permio.ParseMissingPermissions(message)` extracts the missing list from a `PermissionDenied` message. You only need
it if you call the API without the SDK's connection.

## Retries and rate limits

- **Retried:** idempotent reads (`Check`, `BatchCheck`, `WhoAmI`, and every `Get*` and `List*` RPC, including
  `ListAccess`, `ListPrincipalsWithAccess` and the group reads) are retried on `Unavailable` and
  `DeadlineExceeded`. They are retried twice by default, with exponential backoff and jitter.
- **Never retried:** writes (every Create, Update, Delete, Grant, Revoke, adding and removing group members, and so
  on) are sent exactly once. Grant and revoke converge on the server, so you can repeat them yourself after a
  timeout, as long as nobody else is changing that grant in the meantime.
- **Rate limits:** a rate-limited read (`ResourceExhausted`) is retried after the delay the server asks for (a
  `google.rpc.RetryInfo` detail, else a `retry-after` header), when that delay is within `RetryOptions.MaxDelay`.
  Otherwise, and for writes, the call fails with `KindRateLimited` and `RetryAfter` set. `ResourceExhausted` without
  a delay is not retried. A `retry-after` on `Unavailable` is used as the minimum backoff.
- **Timeouts:** `Options.Timeout` applies to each attempt (default 10 s). The context's deadline is an overall
  deadline across all attempts, and cancelling the context stops any pending retry.

```go
client, err := permio.New(permio.Options{
    APIKey:  os.Getenv("PERMIO_API_KEY"),
    Project: "default",
    Timeout: 5 * time.Second,
    Retry: permio.RetryOptions{
        MaxRetries: 3,
        BaseDelay:  100 * time.Millisecond,
        MaxDelay:   2 * time.Second,
    },
})

ctx, cancel := context.WithTimeout(ctx, 8*time.Second) // overall deadline for this call
defer cancel()
ok, err := client.Check(ctx, "alice", "document.read", "/documents/1")
```

`RetryOptions` has these fields:

- `MaxRetries`: retries after the first attempt. Zero means the default, 2; a negative value disables retries.
- `BaseDelay`: the first delay, which doubles each time. Default 100 ms.
- `MaxDelay`: the cap on a single delay, and the longest server-requested delay the SDK will wait for. Default 2 s.

If you handle rate limiting yourself, wait for `RetryAfter`:

```go
var perr *permio.Error
if errors.As(err, &perr) && perr.Kind == permio.KindRateLimited {
    time.Sleep(perr.RetryAfter)
}
```

`permio.IsIdempotent("/permio.permissions.v1.PermissionsService/Check")` tells you whether the SDK retries a given
RPC.

## Listing with iterators

List RPCs are paginated with a cursor (see [Pagination](../api-reference/pagination.md)). The list helpers return
`iter.Seq2[T, error]` iterators that fetch pages as you go. Breaking out of the loop stops fetching:

```go
for p, err := range client.ListPermissions(ctx, &permio.ListOptions{Search: "document."}) {
    if err != nil {
        return err
    }
    fmt.Println(p.Name)
}

roles, err := permio.Collect(client.ListRoles(ctx, nil))
```

A failing page yields the error once and ends the iteration. `permio.Collect` gathers a listing into a slice and
stops at the first error.

| Method | Yields |
| --- | --- |
| `ListPermissions(ctx, opts)` | `Permission` |
| `ListRoles(ctx, opts)` | `Role` (with its `Permissions`) |
| `ListPrincipals(ctx, opts)` | `string` principal IDs that have grants in the project, groups included as `group:<slug>` |
| `ListAssignments(ctx, principal, opts)` | `Grant` (`Principal`, `Resource`, `Roles`, `Permissions`), one per resource URI |
| `Groups().List(ctx, opts)` | `Group` |
| `Groups().ListMembers(ctx, name, opts)` | `GroupMember` |
| `Groups().ListForPrincipal(ctx, principal, opts)` | `Group` |

`opts` is a `*permio.ListOptions` and may be `nil`:

- `PageSize`: 1–100, default 100 (`permio.MaxPageSize`).
- `Search`: filters by name. `ListPermissions`, `ListRoles`, `ListPrincipals` and `Groups().List` use it; the others
  ignore it.

There is no public helper for other list RPCs. Follow `next_cursor` yourself through the raw clients, as in the
example below.

## Raw clients (full API)

`client.Permissions()` and `client.Organisations()` return the generated gRPC clients for
`permio.permissions.v1.PermissionsService` and `permio.organisation.v1.OrganisationService`. Authentication,
timeouts, retries and error mapping are already applied. Every RPC in the [API reference](../api-reference/index.md)
is available, with request and response types generated from the protobuf definitions. Method names are the RPC
names, and fields are in Go's CamelCase. Set `ProjectName` on requests yourself; the client's default project isn't
applied:

```go
import (
    permissionsv1 "github.com/PrivateJAR/permio-go/proto/permissions/v1"
)

perm, err := client.Permissions().CreatePermission(ctx, &permissionsv1.CreatePermissionRequest{
    ProjectName: "default",
    Name:        "document.read",
    Description: "Read documents",
})

res, err := client.Permissions().Check(ctx, &permissionsv1.CheckPermissionRequest{
    ProjectName:  "default",
    PrincipalId:  "alice",
    ResourceUris: []string{"/documents/42"},
    Permissions:  []string{"document.read"},
})
if err != nil {
    return err
}
fmt.Println(res.GetPassed(), res.GetMissingPermissions())
```

A list RPC without a helper, following the cursor by hand:

```go
import (
    organisationv1 "github.com/PrivateJAR/permio-go/proto/organisation/v1"
    paginationv1 "github.com/PrivateJAR/permio-go/proto/pagination/v1"
    "google.golang.org/protobuf/proto"
)

var cursor *string
for {
    page, err := client.Organisations().ListAPIKeys(ctx, &organisationv1.ListAPIKeysRequest{
        OrganisationId: "your-org-id",
        ProjectName:    "default",
        Pagination:     &paginationv1.PaginationRequest{Limit: proto.Int32(100), Cursor: cursor},
    })
    if err != nil {
        return err
    }
    for _, k := range page.GetApiKeys() {
        fmt.Println(k.GetName())
    }
    next := page.GetPagination().GetNextCursor()
    if next == "" {
        break
    }
    cursor = proto.String(next)
}
```

`client.Conn()` returns the wrapped `grpc.ClientConnInterface`, for any other generated client.

| Import path | Package | Contents |
| --- | --- | --- |
| `github.com/PrivateJAR/permio-go/proto/permissions/v1` | `permissionsv1` | `PermissionsService` client; permission, role, check, access and group messages |
| `github.com/PrivateJAR/permio-go/proto/organisation/v1` | `organisationv1` | `OrganisationService` client; organisation, project and API key messages |
| `github.com/PrivateJAR/permio-go/proto/pagination/v1` | `paginationv1` | Pagination request and response messages |

!!! note "What a key can call"

    By default an API key has **check** access: it can run checks and access queries, and read permissions, roles,
    principals, assignments and groups. Creating, updating or deleting permissions, roles and groups, granting or
    revoking, and changing group members needs a key with full access. See
    [API keys](../concepts/api-keys.md#access-levels).

## API key helpers

| Export | Description |
| --- | --- |
| `ValidateAPIKey(key)` | Returns `APIKeyOpaque` for `perms_` keys and `APIKeyJWT` for legacy JWT keys, or an error of kind `KindConfig` if the key is malformed. |
| `APIKeyLength` | `44`, the length of a `perms_` key. |
| `EnvAPIKey` | `"PERMIO_API_KEY"`. |

These only check the shape and checksum. Only the API can tell you whether a key exists and is still valid: use
[`WhoAmI`](#verifying-the-key).

## net/http

```go
func requirePermission(client *permio.Client, permission string, next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        userID := userIDFrom(r.Context()) // set by your auth middleware
        err := client.Assert(r.Context(), userID, permission, permio.Resource("documents", r.PathValue("id")))
        switch {
        case err == nil:
            next.ServeHTTP(w, r)
        case errors.Is(err, permio.ErrDenied):
            http.Error(w, "forbidden", http.StatusForbidden)
        default:
            // any other error: auth, validation, network...
            http.Error(w, "authorisation unavailable", http.StatusServiceUnavailable)
        }
    })
}

mux := http.NewServeMux()
mux.Handle("GET /documents/{id}", requirePermission(client, "document.read", http.HandlerFunc(getDocument)))
```

## How it talks to the API

The SDK uses native gRPC over HTTP/2 with TLS, through `google.golang.org/grpc`. The key is sent as
`authorization: Bearer <key>` metadata on every call. Timeouts are applied as context deadlines on each attempt.
