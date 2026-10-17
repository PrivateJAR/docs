# How it works

Permio implements **resource-level role-based access control**. Your application keeps handling sign-in. perms.io
stores who may do what, on which resources, and answers permission checks.

## The building blocks

### Organisations and projects

Your **organisation** holds your team, billing and projects. A **project** is a separate space for permissions,
roles, grants and API keys. Every organisation starts with a project called `default`. You might add others, for
example to separate environments (`staging`, `production`) or products.

Nothing is shared between projects. A check in one project never sees another project's grants.

### Permissions

A **permission** is a named action that your code checks, for example:

- `document.read`
- `document.write`
- `invoice.pay`

Names can use letters, digits, `.`, `_` and `-`, up to 128 characters. A `resource.action` style works well.

### Roles

A **role** is a named set of permissions, such as `viewer` = `document.read`, or `editor` = `document.read` and
`document.write`. Granting a role grants all of its permissions.

### Principals

A **principal** is whoever you check: usually a user, but it could be a service, a device or anything else. It is
identified by a string that **you** choose, typically the user ID from your auth provider. You don't register
principals in advance. A principal appears in perms.io once it has a grant.

API keys are principals too. Each key is granted a role on its own project, which decides what it may call. See
[API keys](concepts/api-keys.md).

### Resources

A **resource** is anything you protect, identified by a URI path such as `/documents/42`. See
[Resources and inheritance](concepts/resources.md) for the rules.

### Grants

A **grant** gives a principal some permissions and/or roles on one resource URI. A grant applies to that resource
and to everything beneath it:

```
grant viewer to alice on /documents

check alice document.read /documents/42   → passed
check alice document.read /invoices/1     → failed, missing document.read on /invoices/1
```

## Checks

A check asks: does a principal hold **every** listed permission on **every** listed resource? You can check up to
100 resources and 100 permissions in one call.

The answer is `passed: true`, or `passed: false` with the missing permissions per resource. A denial is a normal
response, not an error. API errors mean the request itself couldn't be carried out, for example because the key is
invalid or the input is malformed.

## Where perms.io fits in

perms.io only does authorisation. It doesn't do authentication.

```
1. Client ──────────→ Your app: request with a session or token
2. Your app ────────→ Your auth provider: who is this?      → user ID "alice"
3. Your app ────────→ perms.io: may alice do document.read on /documents/42?
4. perms.io ────────→ Your app: passed / missing permissions
5. Your app ────────→ Client: the data, or 403
```

Your backend calls perms.io with an API key. Keep the key on the server; never ship it to browsers or mobile apps.

## Managing access

- **Dashboard** ([app.perms.io](https://app.perms.io)): create projects, permissions and roles, grant and revoke
  access on the **Principals** page, and manage API keys and your team.
- **API**: every dashboard action is also an RPC. See the [API reference](api-reference/index.md). Writes need an
  API key with full access, which is [on its way](concepts/api-keys.md#access-levels).

## Patterns

### Multi-tenant applications

Put the tenant at the top of every URI and grant tenant admins on the tenant:

```
/tenants/acme                          ← grant tenant_admin to the Acme admin
/tenants/acme/projects/web-app         ← grant editor to project members
/tenants/acme/projects/web-app/documents/42
```

A grant under `/tenants/acme` can never reach `/tenants/globex`.

### Per-object sharing

Grant on the exact object to share one document with one user:

```
grant viewer to bob on /documents/42
```

### The same rule at every level

Use `_` in a grant to match any single segment, for example to let a moderator manage the comments on every
document:

```
grant comment_moderator to carol on /documents/_/comments
```

## Next steps

- Follow the [Quickstart](quickstart.md).
- Add checks to your app with the [TypeScript SDK](sdk/typescript.md), including Express and Next.js examples.
