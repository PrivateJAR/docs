# Pagination

List endpoints use cursor-based pagination with two shared messages from the `pagination` proto package.

## PaginationRequest

| Field | Type | Description |
| --- | --- | --- |
| `limit` | int32 | Optional. Items per page, 1–100. Default 10. |
| `cursor` | string | Optional. The `next_cursor` from the previous page. Leave it out to start from the beginning. |

Over REST, send these as query parameters: `?pagination.limit=50&pagination.cursor=…`.

## PaginationResponse

| Field | Type | Description |
| --- | --- | --- |
| `next_cursor` | string | Pass this as `cursor` to get the next page. It's empty when there are no more pages. |

Treat cursors as opaque strings.

## Paginated endpoints

| RPC | Items field |
| --- | --- |
| [ListPermissions](permissions.md#listpermissions) | `permissions` |
| [ListRoles](permissions.md#listroles) | `roles` |
| [ListPrincipals](permissions.md#listprincipals) | `principals` |
| [GetAllAssignmentsForPrincipal](permissions.md#getallassignmentsforprincipal) | `assignments` |
| [ListAccess](permissions.md#listaccess) | `scopes` |
| [ListPrincipalsWithAccess](permissions.md#listprincipalswithaccess) | `principals` |
| [ListGroups](permissions.md#listgroups) | `groups` |
| [ListGroupMembers](permissions.md#listgroupmembers) | `members` |
| [ListGroupsForPrincipal](permissions.md#listgroupsforprincipal) | `groups` |
| [GetProjectsForOrganisation](organizations.md#projects) | `projects` |
| [ListAPIKeys](organizations.md#api-keys) | `api_keys` |

## Examples

=== "TypeScript"

    The SDK's iterators follow cursors for you:

    ```ts
    for await (const p of permio.listPermissions({ pageSize: 50 })) {
      console.log(p.name);
    }
    ```

    For other list RPCs, use `paginate` (see [Listing with iterators](../sdk/typescript.md#listing-with-iterators)).

=== "cURL"

    ```bash
    # First page
    curl "$PERMIO_API/permissions-service/v1/permissions?project_name=default&pagination.limit=50" \
      -H "Authorization: Bearer $PERMIO_API_KEY"

    # Next page: pass the nextCursor value from the previous response
    curl "$PERMIO_API/permissions-service/v1/permissions?project_name=default&pagination.limit=50&pagination.cursor=NEXT_CURSOR" \
      -H "Authorization: Bearer $PERMIO_API_KEY"
    ```

    Responses use camelCase JSON names, so the cursor arrives as `pagination.nextCursor`. When there are no more
    pages it is empty or left out.
