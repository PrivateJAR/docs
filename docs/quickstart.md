# Quickstart

This guide takes you from a new account to a passing permission check in about five minutes. You'll use the
dashboard to set things up, then make the check from code.

## 1. Sign up

Go to [app.perms.io](https://app.perms.io) and click **Sign up**. You can sign up with email and password or with
Google.

Next, name your organisation and click **Create organisation**. The organisation holds your projects, API keys,
billing and team.

## 2. Use the `default` project

A project called `default` is created with your organisation, and the dashboard selects it for you. Permissions,
roles, grants and API keys all belong to a project. You can switch projects, or create more, from the project
switcher at the top of the dashboard.

This guide uses `default` throughout.

## 3. Create a permission and a role

A **permission** is an action your code checks, such as `document.read`. A **role** is a named set of permissions.

1. Open **Permissions** and click **Create Permission**. Enter the name `document.read`, optionally add a
   description, and click **Create permission**.
2. Open **Roles** and click **Create New Role**. Enter the name `viewer`, tick `document.read` under
   **Permissions**, and click **Create role**.

!!! tip

    A permission's name is the string your code checks, and it can't be renamed later. A `resource.action` style
    such as `document.read` works well.

## 4. Grant the role to a principal on a resource

A **principal** is whoever you are checking: usually one of your users, identified by the ID your app already
uses. perms.io doesn't need to know about the principal in advance.

1. Open **Principals** and click **Grant Access**.
2. Fill in:
    - **Principal ID**: `alice`
    - **Resource URI**: `/documents`
    - **Roles**: `viewer`
3. Click **Grant access**.

Alice can now read `/documents` and **everything beneath it**.

## 5. Create an API key

1. Open **API Keys** and click **Create New Key**.
2. Name it, for example `quickstart`, and click **Create key**.
3. Copy the key. **It is only shown once.**

Keys look like `perms_` followed by 38 letters and digits. Keep the key on your server. See
[API keys](concepts/api-keys.md) for details.

## 6. Make a check

Ask whether `alice` may read document 42:

--8<-- "hosts.md"

=== "TypeScript"

    ```bash
    npm install permio
    ```

    !!! warning "Pre-release"

        The `permio` package isn't on npm yet. Use the cURL tab until the first release is published.

    ```ts
    import { Permio, resource } from "permio";

    const permio = new Permio({
      apiKey: process.env.PERMIO_API_KEY!,
      project: "default",
    });

    const allowed = await permio.check({
      principal: "alice",
      resource: resource("documents", 42), // "/documents/42"
      permission: "document.read",
    });

    console.log(allowed); // true
    ```

=== "cURL"

    ```bash
    curl -X POST "$PERMIO_API/permissions-service/v1/permissions/check" \
      -H "Authorization: Bearer $PERMIO_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "default",
        "principal_id": "alice",
        "resource_uris": ["/documents/42"],
        "permissions": ["document.read"]
      }'
    ```

    ```json
    {"passed": true}
    ```

The check passes even though you never granted anything on `/documents/42`. The grant on `/documents` is inherited
by every resource beneath it.

### A denied check

Now check a resource outside `/documents`:

=== "TypeScript"

    ```ts
    const result = await permio.checkDetailed({
      principal: "alice",
      resource: "/invoices/1",
      permission: "document.read",
    });

    console.log(result);
    // { allowed: false, missing: [{ resource: "/invoices/1", permissions: ["document.read"] }] }
    ```

=== "cURL"

    ```bash
    curl -X POST "$PERMIO_API/permissions-service/v1/permissions/check" \
      -H "Authorization: Bearer $PERMIO_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "default",
        "principal_id": "alice",
        "resource_uris": ["/invoices/1"],
        "permissions": ["document.read"]
      }'
    ```

    ```json
    {"missingPermissions": [{"resourceUri": "/invoices/1", "missingPermissions": ["document.read"]}]}
    ```

    JSON responses use camelCase field names and leave out fields with default values, so `"passed": false` is
    not printed.

A denial is a normal answer, not an error. You get a successful response with `passed` false and a list of what is
missing. Errors are kept for problems with the request itself: a bad key, malformed input or a key that isn't allowed
to check. See [Errors](api-reference/index.md#errors).

## Next steps

- [Resources and inheritance](concepts/resources.md): design your resource URIs, and use the `_` wildcard.
- [TypeScript SDK](sdk/typescript.md): `assert`, `checkAny`, error handling, and Express and Next.js examples.
- [API reference](api-reference/index.md): every endpoint, for cURL, gRPC and the generated clients.
