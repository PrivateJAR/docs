## Key facts

- API host: `https://api.perms.io`.
- Authenticate with an API key (`perms_...`, 44 characters) sent as `Authorization: Bearer <key>`. Keep keys on the server.
- Every Permissions API request names a project (`project_name`); every organisation starts with a `default` project.
- A denied check is a normal response (`passed: false` plus the missing permissions), not an error.
- Groups: grant to the principal ID `group:<slug>` and every member holds the grant; checks include a principal's groups.
- Manage projects, permissions, roles, grants, groups and API keys in the dashboard at https://app.perms.io.

## Docs

- [Home](https://docs.perms.io/): What Permio is and its key features: resource-level RBAC, hierarchical inheritance, groups, bring your own authentication.
- [Quickstart](https://docs.perms.io/quickstart/): From sign-up to a passing permission check: create a permission, a role, a grant and an API key, then check with TypeScript or cURL.
- [How it works](https://docs.perms.io/how-it-works/): The building blocks (organisations, projects, permissions, roles, principals, groups, resources, grants), how checks work and common patterns such as multi-tenancy.
- [Resources and inheritance](https://docs.perms.io/concepts/resources/): Resource URI rules, how grants apply to everything beneath them, the `_` wildcard segment and how a check is decided.
- [Groups](https://docs.perms.io/concepts/groups/): Named sets of principals; granting to `group:<slug>`, members, how checks use groups, deleting groups and the permissions needed to manage them.
- [API keys](https://docs.perms.io/concepts/api-keys/): Key format and checksum, sending keys, check vs full access levels, and invalidating keys.
- [Filtering lists and building share dialogs](https://docs.perms.io/guides/filtering-and-sharing/): Using `listAccess` scopes to filter rows in PostgreSQL, Prisma or MongoDB, `batchCheck` for loaded rows, and `whoHasAccess` for share dialogs.

## API reference

- [API overview](https://docs.perms.io/api-reference/): Services, hosts, REST/JSON vs gRPC vs gRPC-web, authentication, error codes and the available clients.
- [Permissions & Roles](https://docs.perms.io/api-reference/permissions/): `PermissionsService`: Check, BatchCheck, permissions, roles, grants, ListAccess, ListPrincipalsWithAccess and groups, with REST paths, fields and examples.
- [Organisations & Projects](https://docs.perms.io/api-reference/organizations/): `OrganisationService`: organisations, projects, API keys, team members and usage; mostly used by the dashboard.
- [Pagination](https://docs.perms.io/api-reference/pagination/): Cursor-based pagination (`limit`, `cursor`, `next_cursor`) and which endpoints are paginated.

## SDKs

- [TypeScript SDK](https://docs.perms.io/sdk/typescript/): The `permio` package on npm: client options, `check`, `checkDetailed`, `assert`, `checkAny`, `batchCheck`, groups, `listAccess`, `whoHasAccess`, `resource()`, typed errors, retries, iterators, raw clients, and Express and Next.js examples.
- [Go SDK](https://docs.perms.io/sdk/go/): The `github.com/PrivateJAR/permio-go` module: options, checks, batch checks, access queries, grant and revoke, groups, typed errors, retries and rate limits, and the raw gRPC clients.
- [Python SDK](https://docs.perms.io/sdk/python/): The `permio` package on PyPI with sync `Permio` and asyncio `AsyncPermio`: configuration, checks, batch checks, access queries, grant and revoke, groups, exceptions, retries and rate limits, and the raw stubs.
- [Rust SDK](https://docs.perms.io/sdk/rust/): The `permio` crate on crates.io: client builder, checks, batch checks, access queries, grant and revoke, groups, the `Error` enum, retries and rate limits, list streams and the raw tonic clients.
- [Java SDK](https://docs.perms.io/sdk/java/): `io.perms:permio` (coming soon to Maven Central): builder options, checks, batch checks, access queries, async variants, grant and revoke, groups, exceptions, retries and rate limits, and the raw gRPC stubs.

## Optional

- [IAM fundamentals](https://docs.perms.io/iam-basics/): General background on identity and access management: authentication vs authorisation, RBAC, ABAC, inheritance and best practices.
- [Full documentation text](https://docs.perms.io/llms-full.txt): The essential pages above in one Markdown file, for loading into an LLM's context.
