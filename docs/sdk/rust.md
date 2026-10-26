# Rust SDK

`permio` is the official Rust client for the perms.io API. It wraps the API in a few calls for asking "may this
principal do X on this resource?". It also gives you one typed error enum, retries for idempotent reads and
`Stream`s over list endpoints. The full generated API is there too, as an escape hatch.

- Needs Rust 1.88 or newer (the minimum for tonic 0.14).
- Async on Tokio. The client must be built inside a Tokio runtime.
- Talks native gRPC over HTTP/2 through [tonic](https://docs.rs/tonic), with prost-generated messages.
- TLS comes from rustls, through the `tls` feature, which is on by default.

!!! note "Not on crates.io yet"

    The crate is version 0.1.0 and isn't published on crates.io yet. Until it is, depend on the Git repository, as
    shown below. Publishing to crates.io is coming.

## Install

```toml
[dependencies]
permio = { git = "https://github.com/PrivateJAR/permio-rust" }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
futures-util = "0.3" # only for the list streams, see Listing with streams
```

### Features

| Feature | Default | Description |
| --- | --- | --- |
| `tls` | on | rustls (with ring) for `https://` endpoints such as `https://api.perms.io`. It trusts the platform's certificates and the bundled webpki roots. |

Without `tls`, only `http://` endpoints work: building a client for an `https://` endpoint fails with
`Error::Config`.

## Quick start

```rust
#[tokio::main]
async fn main() -> Result<(), permio::Error> {
    let permio = permio::Client::builder().project("default").build()?; // key from PERMIO_API_KEY

    let doc = permio::resource!("documents", 42)?; // "/documents/42"
    if permio.check("alice", "document.read", &doc).await? {
        println!("alice may read {doc}");
    }
    Ok(())
}
```

A principal that lacks the permission is a normal answer: `check` returns `Ok(false)`. It only returns `Err` when
the call itself fails, for example because of a bad key, malformed input or network trouble.

## Configuration

```rust
use std::time::Duration;

let permio = permio::Client::builder()
    .api_key(std::env::var("PERMIO_API_KEY").unwrap()) // the default source anyway
    .endpoint(permio::DEFAULT_ENDPOINT)                 // https://api.perms.io
    .project("default")
    .timeout(Duration::from_secs(5))
    .retries(3)
    .build()?;
```

`build()` checks the API key's format and checksum straight away. A mistyped or truncated key returns
`Error::Config` before any request is sent. See [API keys](../concepts/api-keys.md) for the format. The connection
itself is made lazily, on the first call.

### Builder options

| Method | Type | Default | Description |
| --- | --- | --- | --- |
| `api_key` | `impl Into<String>` | `PERMIO_API_KEY` env var | A `perms_…` key from the dashboard, or a legacy JWT key. `Error::Config` if neither is set. |
| `endpoint` | `impl Into<String>` | `DEFAULT_ENDPOINT` | API URL. Must start with `http://` or `https://`; a trailing `/` is dropped. |
| `project` | `impl Into<String>` | none | Default project for every call. Without one, calls that need a project fail with `Error::Config`. |
| `timeout` | `Duration` | 10 s (`DEFAULT_TIMEOUT`) | Timeout for each attempt, also used as the connect timeout. `Duration::ZERO` disables it. |
| `retries` | `u32` | `2` | Retries for idempotent reads. Sets `max_retries` and keeps the other retry settings. |
| `retry_config` | `RetryConfig` | see [Retries and rate limits](#retries-and-rate-limits) | All retry settings at once. |
| `channel` | `tonic::transport::Channel` | none | Advanced: a tonic channel to use instead of connecting to `endpoint`, for example one connected to an in-process test server. Authentication, timeouts and retries still apply. |

`build()` returns `Error::Config` if the key is missing or malformed, the endpoint isn't an http(s) URL, an `https`
endpoint is used without the `tls` feature, or it's called outside a Tokio runtime.

`permio::Client::from_env("default")` is a shorthand for `Client::builder().project("default").build()`: production
endpoint, key from `PERMIO_API_KEY`.

### Production and development

| Constant | URL |
| --- | --- |
| `permio::DEFAULT_ENDPOINT` | `https://api.perms.io` (production, the default) |
| `permio::DEV_ENDPOINT` | `https://dev-api.perms.io` (development) |

```rust
let dev = permio::Client::builder()
    .endpoint(permio::DEV_ENDPOINT)
    .project("default")
    .build()?;
```

An API key only works in the environment and project it was created in.

### Sharing the client and switching project

`Client` is cheap to clone and safe to share between tasks. Clones share one HTTP/2 connection, so create one client
at startup and clone it where you need it.

Most helpers have no per-call project parameter. `with_project` returns a clone with another default project:

```rust
let other = permio.with_project("other-project");
```

The exceptions are `Check` and `BatchCheck`, which take `.project(...)` (see below).

The client also exposes `permio.project()` (`Option<&str>`), `permio.endpoint()` and `permio.api_key_kind()`
(`ApiKeyKind::Opaque` or `ApiKeyKind::Jwt`).

### `who_am_i`

Describes the credential the client uses. It needs no project, so it is a good way to verify a key at startup:

```rust
let me = permio.who_am_i().await?;
println!("{:?} {:?} {:?}", me.kind, me.project, me.api_key_access);
```

`WhoAmI` has `principal_id`, `organisation_id`, `kind` (`PrincipalKind::ApiKey`, `User`, `ServiceAccount` or
`Unknown`), `project` (the project an API key belongs to), `api_key_access` (`Some(ApiKeyAccess::Check)`,
`Some(ApiKeyAccess::Full)` or `Some(ApiKeyAccess::Unknown)` for an API key, otherwise `None`) and `email`. See
[access levels](../concepts/api-keys.md#access-levels).

## Checking permissions

### `check`

Returns `true` when the principal holds the permission on the resource, directly, through a role, through a group,
through an ancestor URI or through a `_` wildcard grant:

```rust
let allowed: bool = permio.check("alice", "document.read", "/documents/42").await?;
```

The arguments are `(principal, permission, resource)`, all `&str`.

### `check_all` and `check_any`

Both take one resource and several permissions, and make a single `Check` call:

```rust
// every permission
permio.check_all("alice", ["document.read", "document.write"], "/documents/42").await?;

// at least one permission
permio.check_any("alice", ["document.admin", "document.write"], "/documents/42").await?;
```

`check_any` works out its answer from the missing list of one `Check`, so it costs the same as `check_all`.

### `check_detailed`

For several resources, several permissions, another project, or to find out what is missing, build a `Check`:

```rust
use permio::Check;

let result = permio
    .check_detailed(
        Check::new("alice")
            .resources(["/documents/1", "/documents/2"])
            .permissions(["document.read", "document.write"]),
    )
    .await?;
// result.allowed: false
// result.missing: [MissingPermission { resource: "/documents/2", permissions: ["document.write"] }]
```

`CheckResult` has `allowed` (the principal holds **every** permission on **every** resource) and `missing`, a
`Vec<MissingPermission>` (`resource`, `permissions`) in request order, empty when `allowed` is `true`.

`Check` builder methods:

| Method | Description |
| --- | --- |
| `Check::new(principal)` | The principal being checked: one of your user or service IDs, or `group:<slug>`. |
| `resource(uri)` / `resources(uris)` | Adds one or several resource URIs. Every resource is checked. |
| `permission(name)` / `permissions(names)` | Adds one or several permission names. |
| `project(name)` | Checks in this project instead of the client's default. |

Duplicates are removed before sending. A check needs 1–100 resources and 1–100 permissions, none of them empty,
or it returns `Error::Validation` without calling the API.

### `assert` and `assert_detailed`

Return `Ok(())` when the principal is allowed and `Err(Error::Denied { .. })` when it is not. The error carries
`principal` and `missing`:

```rust
permio.assert("alice", "document.write", "/documents/1").await?;

permio.assert_detailed(Check::new("alice").permission("document.read").resource("/documents/1")).await?;
```

### `batch_check`

`check_detailed` gives one answer for all its resources together. `batch_check` answers **each resource
separately**, which is what you need to filter a list or decide which rows get an "edit" button:

```rust
use permio::BatchCheck;

let uris = docs
    .iter()
    .map(|d| permio::resource!("documents", d.id))
    .collect::<Result<Vec<_>, _>>()?;

let entries = permio
    .batch_check(BatchCheck::new("alice").resources(uris).permission("document.read"))
    .await?;
let visible: Vec<&str> = entries.iter().filter(|e| e.allowed).map(|e| e.resource.as_str()).collect();
```

It returns a `Vec<BatchCheckEntry>`, one per distinct resource, in request order. Each entry has `resource`,
`allowed` (the principal holds **every** requested permission on it) and `missing` (the requested permissions it
lacks there).

`BatchCheck` has the same builder methods as `Check`. Duplicate resources are sent once. There is no upper limit on
resources: more than 100 are split into several `BatchCheck` calls, sent concurrently. Permissions are limited to
1–100.

The SDK fails closed: if the API's answer doesn't include a result for each requested resource, `batch_check`
returns `Error::Other` instead of guessing.

### `list_access`

Answers "where may this principal use this permission, at or below `under`?". The arguments are
`(principal, permission, under)`. It follows every page and returns an `AccessScopes`:

```rust
let access = permio.list_access("alice", "document.read", "/documents").await?;

if access.covers_all {
    // alice may read everything under /documents
} else {
    let prefixes = access.to_prefixes(); // e.g. ["/documents/4", "/documents/7"]
}
```

The [Filtering lists and building share dialogs](../guides/filtering-and-sharing.md) guide shows it in context.

`AccessScopes`:

| Member | Type | Description |
| --- | --- | --- |
| `under` | `String` | The URI that was asked about. |
| `covers_all` | `bool` | The principal holds the permission on `under` itself, so on everything below it. `scopes` is then a single subtree scope for `under`. |
| `scopes` | `Vec<AccessScope>` | `{ uri, kind }`, ordered by URI. `kind` is `ScopeKind::Subtree`, `Pattern`, `Exact` (reserved, not returned today) or `Unknown` (a kind this SDK version doesn't know; it never matches). |
| `is_empty()` | `bool` | No access anywhere under `under`. |
| `allows(uri)` | `bool` | Whether `uri` is covered. Matches per segment: `/a/b` covers `/a/b/c` but not `/a/bc`. Malformed URIs are never allowed. |
| `to_prefixes()` | `Vec<String>` | The subtree URIs, for prefix filters. Prefixes covered by a shorter one are dropped. Pattern scopes aren't included. |
| `patterns()` | `Vec<String>` | The pattern URIs, with `_` segments. |
| `has_patterns()` | `bool` | Some scope is a pattern, so `to_prefixes()` alone doesn't cover everything. |
| `exact()` | `Vec<String>` | The exact URIs. Empty today. |
| `regex_pattern()` | `String` | One anchored regular expression matching exactly what `allows()` accepts, for PostgreSQL `~`, MongoDB `$regex` or the `regex` crate. With no scopes it is `$.^`, which matches nothing. |

!!! warning

    A prefix `p` from `to_prefixes()` means `p` **and everything below it**. Filter with
    `path = p OR path starts with p + "/"`, never a bare "starts with `p`", which would let `/documents/1` match
    `/documents/12`. In SQL, use `starts_with(path, p || '/')` rather than `LIKE`, where `_` is a wildcard.

For a URI outside `under`, `allows()` returning `false` means "not asked", not "denied". A `_` segment in `under` is
literal. The API key needs `permission.check` on `under` and `principal.assignment.get` on the principal.

### `who_has_access`

Answers "who has access to this resource?". It follows every page and returns a `Vec<AccessEntry>`, ordered by
principal ID:

```rust
use permio::{GrantSource, WhoHasAccess};

let entries = permio
    .who_has_access(
        WhoHasAccess::new("/documents/42")
            .permission("document.read")
            .expand_groups(true),
    )
    .await?;

for e in &entries {
    for g in &e.via {
        let source = match &g.source {
            GrantSource::Role { name, .. } => format!("role {name}"),
            GrantSource::Direct => "direct".to_string(),
            _ => "unknown".to_string(),
        };
        println!("{} on {} ({source})", e.principal, g.resource);
    }
}
```

`WhoHasAccess` builder methods:

| Method | Description |
| --- | --- |
| `WhoHasAccess::new(resource)` | The resource to look at. A `_` segment here is literal. |
| `permission(name)` | Only count grants that confer this permission, so a principal is listed exactly when a check passes for it through its own grants (or, for entries with `via_group`, through that group). Unset, any grant counts. |
| `expand_groups(bool)` | Also list every member of each listed group, once per group, with `via_group` set. |
| `page_size(n)` | Items per page, 1–100. Default 100. |

`AccessEntry` has `principal`, `is_group`, `via_group` (a group slug, or `None`) and `via`, the grants that give the
access, most specific first. Each `AccessGrant` has:

- `resource`: the URI the grant was made on (the resource, an ancestor, or a `_` wildcard URI that matches it);
- `inherited`: `true` unless the grant was made on exactly the resource;
- `match_kind`: `GrantMatch::Exact`, `Ancestor`, `Wildcard` or `Unknown`;
- `source`: `GrantSource::Role { id, name }`, `GrantSource::Direct` for directly granted permissions, or
  `GrantSource::Unknown`.

`GrantMatch` and `GrantSource` are `#[non_exhaustive]`, so a `match` on them needs a `_` arm. The API key needs
`principal.list` and `principal.assignment.list` on the project.

## Granting and revoking

Build a `Grant` with the principal and resource, then add permission names, role IDs or both:

```rust
use permio::Grant;

permio.grant(Grant::new("alice", "/documents").permission("document.read")).await?;
permio.grant(Grant::new("alice", "/documents").role(role_id)).await?; // role IDs, see list_roles
permio
    .grant(Grant::new("alice", "/documents").permissions(["document.read", "document.write"]).roles([role_id]))
    .await?;

permio.revoke(Grant::new("alice", "/documents").permission("document.read")).await?;
```

- `grant` is additive: what the principal already holds there is kept. The grant also applies to every resource
  below the URI. Unknown permissions or roles return `Error::Validation`.
- `revoke` removes names from the principal's grant on **exactly** that URI and ignores names the grant doesn't
  have, so revoking twice is harmless. Grants on ancestor URIs stay, so the principal may still pass a check;
  `who_has_access` shows where access comes from.
- A `Grant` needs at least one permission or role. Empty names return `Error::Validation`.
- Both use the client's default project; use `with_project` for another one.
- Both need a key with full access, and neither is ever retried automatically.

To grant to every member of a group, use `permio::group("editors")?` as the principal (see [Groups](#groups)).

## Groups

A [group](../concepts/groups.md) is a named set of principals in a project. Grant to the group's principal ID,
`group:<slug>`, and every member holds the grant. Checks include the principal's groups automatically.

### `permio::group(slug)`

Returns the group's principal ID. It returns `Error::Validation` unless the slug is 1–64 lower-case letters, digits
and hyphens. `GROUP_PRINCIPAL_PREFIX` is `"group:"`.

```rust
use permio::Grant;

let groups = permio.groups();
groups.create("editors", Some("Can edit every document")).await?;
groups.add_members("editors", ["alice", "bob"]).await?;

permio
    .grant(Grant::new(permio::group("editors")?, "/documents").permission("document.write"))
    .await?;

permio.check("alice", "document.write", "/documents/42").await?; // true, through the group
```

### `permio.groups()`

Returns a `Groups` handle. Every method that takes a group accepts its slug (`"editors"`) or its principal ID
(`"group:editors"`). Calls use the client's default project; use `with_project` for another one.

| Method | Returns |
| --- | --- |
| `create(name, description: Option<&str>)` | `Group`. `Error::Other` with code `AlreadyExists` if the project already has a group with this name. |
| `get(name)` | `Group`. `Error::NotFound` if it doesn't exist. |
| `update(name, description: &str)` | `Group`. Replaces the description; a group can't be renamed. `Error::NotFound` if it doesn't exist. |
| `delete(name)` | `()`. Deletes the group, its memberships and every grant made to it. Succeeds whether or not it existed. |
| `list(ListOptions)` | `ListStream<Group>`, ordered by name. |
| `add_members(name, principals)` | `AddMembersResult { added, existing }`, in request order. |
| `remove_members(name, principals)` | `RemoveMembersResult { removed, not_members }`, in request order. |
| `list_members(name, ListOptions)` | `ListStream<GroupMember>` (`principal_id`, `created_at`), ordered by principal ID. |
| `list_for_principal(principal, ListOptions)` | `ListStream<Group>` of the groups the principal is a member of, ordered by name. |

- `add_members` and `remove_members` take 1–100 principals; duplicates are removed. `add_members` rejects `group:`
  IDs with `Error::Validation`, because groups can't contain groups.
- `Group` is the generated message, re-exported as `permio::Group`. It has `id`, `organisation_id`, `project_name`,
  `name`, `description`, `principal_id` (`"group:<name>"`), `created_at` and `updated_at`.

```rust
use futures_util::TryStreamExt;

let res = permio.groups().add_members("group:editors", ["alice", "carol"]).await?;
println!("added {:?}, already members {:?}", res.added, res.existing);

let mut members = permio.groups().list_members("editors", Default::default());
while let Some(m) = members.try_next().await? {
    println!("{}", m.principal_id);
}
```

Reading groups works with a check-access API key. Creating, updating and deleting groups and changing members needs
a key with full access, and changing members also needs the right to grant across the project. See
[Permissions you need](../concepts/groups.md#permissions-you-need).

## Resource URIs

Resource URIs are paths such as `/projects/p1/documents/42`. A grant on a URI also covers every URI beneath it. See
[Resources and inheritance](../concepts/resources.md) for the full rules.

### `resource!` and `resource()`

Build a URI from raw segments. They add the leading `/` and percent-encode each segment, so an ID that contains
`/`, spaces or other reserved characters stays a single segment. The macro takes segments of mixed `Display` types;
the function takes any iterator of one `Display` type:

```rust
permio::resource!("projects", "p1", "documents", 42)?; // "/projects/p1/documents/42"
permio::resource(["files", "reports/2026.pdf"])?;    // "/files/reports%2F2026.pdf"
```

Everything except ASCII letters, digits and `- _ . ~` is encoded, as UTF-8. Both return `Error::Validation` for an
empty segment or no segments at all.

!!! tip

    Build URIs the same way when you grant and when you check, or they will not match.

### Other helpers

| Item | Description |
| --- | --- |
| `encode_segment(segment)` | Encodes one segment the way `resource()` does. |
| `validate_resource_uri(uri)` | Returns `Error::Validation` unless `uri` has the basic shape the API accepts: a leading `/`, no empty segments (so no `//`, trailing `/` or bare `/`), no whitespace or control characters, and at most 2048 bytes. |
| `MAX_RESOURCE_URI_LENGTH` | `2048`. |
| `WILDCARD_SEGMENT` | `"_"`, the segment that matches exactly one segment in a stored grant. |

Every helper runs `validate_resource_uri` on its URIs before sending. The API enforces the remaining rules, such as
no `( ) [ ] { } * + ? | ^ $ \` in segments, and answers with `InvalidArgument`, which the SDK returns as
`Error::Validation`.

## Errors

Every fallible call returns `Result<_, permio::Error>`. `Error` is an enum with one variant per kind of failure:

| Variant | When |
| --- | --- |
| `Config { message }` | Bad client setup: a missing or malformed API key, no project, an invalid endpoint, `https` without the `tls` feature, or no Tokio runtime. |
| `Auth { .. }` | `Unauthenticated`: the key is missing, unknown or invalidated. |
| `Permission { missing, .. }` | `PermissionDenied`: the **API key** lacks the rights for this call. `missing` lists what it lacks when the API says. |
| `Validation { message, status }` | `InvalidArgument`, or the SDK's own input checks (then `status` is `None`). |
| `NotFound { .. }` | `NotFound`, for example `groups().get` for a group that doesn't exist. |
| `Unavailable { .. }` | `Unavailable`, including connection and TLS failures. |
| `Timeout { .. }` | `DeadlineExceeded`, including the SDK's own per-attempt timeout. |
| `RateLimited { retry_after, .. }` | `ResourceExhausted`: the organisation's rate limit is used up. `retry_after` is the delay the server asked for, if it gave one. |
| `Denied { principal, missing, .. }` | Returned only by `assert` and `assert_detailed`, when the **principal** is not allowed. |
| `Other { message, status }` | Any other gRPC code (for example `AlreadyExists` or `Internal`), or an inconsistent API response (then `status` is `None`). |

Every variant has a `message`. The methods on `Error` are:

- `code()`: the gRPC `Code`, when the error came from the API (`None` for `Config`, `Denied` and local validation);
- `message()`: the message without the `permio: <kind>:` prefix;
- `status()`: the original `tonic::Status`;
- `metadata()`: the response headers and trailers.

`tonic` is re-exported as `permio::tonic`, so you can name `permio::tonic::Code` without adding tonic as a
dependency.

!!! note "Denied is not an error"

    `Error::Permission` is about the *caller*. It means your API key is not allowed to make the call: for `Check`,
    the key needs `permission.check` on the checked resources and on the principal. A principal failing a check is
    a normal result: `check()` returns `Ok(false)` and only `assert()` returns `Error::Denied`.

`Error::Permission`'s `missing` uses the API's fully qualified URIs (`/organisation/{org}/project/{project}/...`),
not the URIs you sent.

`Error` is `#[non_exhaustive]`, so a `match` needs a catch-all arm:

```rust
use permio::Error;

match permio.assert("alice", "document.write", "/documents/1").await {
    Ok(()) => { /* allowed */ }
    Err(Error::Denied { missing, .. }) => {
        // the principal may not do this: respond with 403
    }
    Err(Error::Permission { missing, .. }) => {
        // the API key may not run this check (it needs permission.check)
        eprintln!("API key lacks {missing:?}");
    }
    Err(Error::Auth { .. }) => {
        // the API key is missing, unknown or invalidated
    }
    Err(err) => eprintln!("{:?} {}", err.code(), err.message()),
}
```

`permio::Error::from(status)` converts a `tonic::Status` into the matching variant, for errors from the
[raw clients](#raw-clients-full-api). `parse_missing_permissions(message)` extracts the missing list from a
`PermissionDenied` message. `server_retry_delay(&status)` reads the delay a rate-limited status asks for, and
`rate_limited_status(message, delay)` builds one, for fake servers in tests.

## Retries and rate limits

- **Retries:** idempotent reads are retried on `Unavailable` and `DeadlineExceeded`, including the SDK's own
  per-attempt timeout. They are `Check`, `BatchCheck`, `ListAccess`, `ListPrincipalsWithAccess`, `WhoAmI`, the group
  reads and every other `Get*` and `List*` RPC. `permio::is_idempotent_method(name)` tells you whether a given RPC
  is retried, for example `is_idempotent_method("permio.permissions.v1.PermissionsService.Check")`.
- **Backoff:** exponential with jitter. Before retry *n* (counting from 0), the SDK waits a random time between half
  and all of `min(base_delay × 2ⁿ, max_delay)`: with the defaults, 50–100 ms, then 100–200 ms.
- **Rate limits:** a rate-limited read (`ResourceExhausted`) is retried only when the server says how long to wait,
  through a `google.rpc.RetryInfo` detail or a `retry-after` header in seconds, and only if that delay is at most
  `max_delay`. The SDK then waits at least that long, plus a little jitter. Otherwise, and for every rate-limited
  write, the call returns `Error::RateLimited` with `retry_after` set when the server gave a delay. These retries
  count towards `max_retries`.
- **Writes** (every Create, Update, Delete, Grant, Revoke, adding and removing group members, and so on) are sent
  exactly once and never retried.
- **Timeouts:** the client's `timeout` applies to each attempt (default 10 s). There is no overall deadline across
  retries; wrap the call in `tokio::time::timeout` for one.

`RetryConfig`:

| Field | Default | Description |
| --- | --- | --- |
| `max_retries` | `2` | Retries after the first attempt. |
| `base_delay` | 100 ms | The delay before the first retry, which doubles each time. |
| `max_delay` | 2 s | The cap on a single delay, and on a server-requested delay the SDK will wait for. |

```rust
use std::time::Duration;

let permio = permio::Client::builder()
    .project("default")
    .timeout(Duration::from_secs(5))
    .retry_config(permio::RetryConfig {
        max_retries: 3,
        base_delay: Duration::from_millis(200),
        max_delay: Duration::from_secs(5),
    })
    .build()?;

// an overall deadline of 8 s across all attempts
let allowed = tokio::time::timeout(
    Duration::from_secs(8),
    permio.check("alice", "document.read", "/documents/1"),
)
.await;
```

`RetryConfig::none()` turns retries off.

## Listing with streams

List RPCs are paginated with a cursor (see [Pagination](../api-reference/pagination.md)). The list helpers return a
`permio::ListStream<T>`, a boxed `Stream<Item = Result<T, permio::Error>>` that fetches pages lazily as you poll it.
Dropping the stream stops the listing. Use `futures_util::TryStreamExt` to consume it:

```rust
use futures_util::TryStreamExt;
use permio::ListOptions;

let mut perms = permio.list_permissions(ListOptions::default().search("document."));
while let Some(p) = perms.try_next().await? {
    println!("{}", p.name);
}

let roles: Vec<permio::Role> = permio.list_roles(Default::default()).try_collect().await?;
let principals: Vec<String> = permio.list_principals(Default::default()).try_collect().await?;

let mut assignments = permio.list_assignments("alice", Default::default());
while let Some(a) = assignments.try_next().await? {
    println!("{} {:?}", a.resource_uri, a.roles);
}
```

| Method | Yields |
| --- | --- |
| `list_permissions(options)` | `Permission` |
| `list_roles(options)` | `Role` (with its `permissions`) |
| `list_principals(options)` | `String` principal IDs that have grants in the project |
| `list_assignments(principal, options)` | `Assignment` (`resource_uri`, `permissions`, `roles`) |
| `groups().list(options)` | `Group` (see [Groups](#groups)) |
| `groups().list_members(name, options)` | `GroupMember` |
| `groups().list_for_principal(principal, options)` | `Group` |

`Permission`, `Role`, `Assignment`, `Group` and `GroupMember` are the generated messages, re-exported at the crate
root.

`ListOptions` has two settings:

- `page_size(n)`: items per page, clamped to 1–100 (`MAX_PAGE_SIZE`). Default 100.
- `search(text)`: filters by name, where the RPC supports it (permissions, roles, principals, groups). It is ignored
  elsewhere.

All list helpers use the client's default project; use `with_project` for another one. A configuration or input
error is returned as the stream's first item.

For any other list RPC, use `permio::paginate(page_size, fetch)`, which follows `next_cursor` until the API returns
an empty (or repeated) one:

```rust
use futures_util::TryStreamExt;
use permio::raw::organisation::v1::ListApiKeysRequest;

let raw = permio.raw_organisations();
let keys: Vec<_> = permio::paginate(100, move |pagination| {
    let mut raw = raw.clone();
    async move {
        let res = raw
            .list_api_keys(ListApiKeysRequest {
                project_name: "default".into(),
                pagination: Some(pagination),
                ..Default::default()
            })
            .await?
            .into_inner();
        Ok((res.api_keys, res.pagination))
    }
})
.try_collect()
.await?;
```

## Raw clients (full API)

`permio::raw` holds the generated prost messages and tonic clients for `permio.permissions.v1`
(`permio::raw::permissions::v1`), `permio.organisation.v1` (`permio::raw::organisation::v1`) and `pagination`
(`permio::raw::pagination`). `permio.raw_permissions()` and `permio.raw_organisations()` return a
`PermissionsServiceClient` and an `OrganisationServiceClient` that share the SDK's connection, authentication,
timeouts and retries. Every RPC in the [API reference](../api-reference/index.md) is available. Method names are
the RPC names in snake case, and fields are the proto field names:

```rust
use permio::raw::permissions::v1::{
    CheckPermissionRequest, CreatePermissionRequest, CreateRoleRequest,
    GrantUserPermissionsAndRolesOnResourceRequest,
};

let mut raw = permio.raw_permissions();

raw.create_permission(CreatePermissionRequest {
    project_name: "default".into(),
    name: "document.read".into(),
    description: "Read documents".into(),
})
.await?;

let role = raw
    .create_role(CreateRoleRequest {
        project_name: "default".into(),
        name: "viewer".into(),
        permissions: vec!["document.read".into()], // permission names
        ..Default::default()
    })
    .await?
    .into_inner();

raw.grant_user_permissions_and_roles_on_resource(GrantUserPermissionsAndRolesOnResourceRequest {
    project_name: "default".into(),
    user_id: "alice".into(),
    resource_uri: "/documents".into(),
    roles: vec![role.id], // role IDs
    ..Default::default()
})
.await?;

let res = raw
    .check(CheckPermissionRequest {
        project_name: "default".into(),
        principal_id: "alice".into(),
        resource_uris: vec!["/documents/42".into()],
        permissions: vec!["document.read".into()],
    })
    .await?
    .into_inner();
println!("{} {:?}", res.passed, res.missing_permissions);
```

Raw calls return `Result<tonic::Response<T>, tonic::Status>`. In a function returning `Result<_, permio::Error>`,
`?` converts the status for you; elsewhere use `.map_err(permio::Error::from)`. The raw request types don't take a
default project: set `project_name` on every request.

!!! note "What a key can call"

    By default an API key has **check** access: it can run checks and access queries, and read permissions, roles,
    principals, assignments and groups. Creating, updating or deleting permissions, roles and groups, granting or
    revoking, and changing group members needs a key with full access. See
    [API keys](../concepts/api-keys.md#access-levels).

## API key helpers

| Item | Description |
| --- | --- |
| `validate_api_key(key)` | Returns `ApiKeyKind::Opaque` for `perms_` keys and `ApiKeyKind::Jwt` for legacy JWT keys. Returns `Error::Config` if the key is malformed. |
| `is_valid_api_key(key)` | `true` if `validate_api_key` would pass. |
| `API_KEY_LENGTH` | `44`. |
| `API_KEY_ENV` | `"PERMIO_API_KEY"`, the variable the builder reads. |

These only check the shape and checksum. Only the API can tell you whether a key exists and is still valid; use
`who_am_i` for that.

## How it talks to the API

The SDK speaks native gRPC over HTTP/2 through tonic, not gRPC-web or REST. Every call, from the helpers and the
raw clients alike, goes through one tower service (`permio::Transport`) that adds `authorization: Bearer <key>`,
applies the per-attempt timeout and retries idempotent reads. It sends the user agent `permio-rust/<version>`.
Request and response bodies are buffered, which suits the perms.io API, where every public RPC is unary.
