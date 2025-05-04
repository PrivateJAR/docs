# REST API

While Permio is built on gRPC for optimal performance, we provide a complete REST API for broader compatibility. The REST endpoints are automatically generated from our gRPC services using ESPv2 (Extensible Service Proxy).

## API Basics

### Base URL

All REST API requests should be made to:

```
https://api.perms.io/v1/
```

### Authentication

All API requests require authentication with an API key. Include your API key as a bearer token in the Authorization header:

```
Authorization: Bearer YOUR_API_KEY
```

### Request Format

- For GET requests, parameters should be included as query string parameters
- For POST, PUT, PATCH, and DELETE requests, parameters should be included as JSON in the request body
- All requests should include the `Content-Type: application/json` header

### Response Format

All responses are returned as JSON. Successful responses will include the requested data, while error responses will include an error object with details about what went wrong:

```json
{
  "error": {
    "code": 400,
    "message": "Invalid request: Missing required field 'name'",
    "details": [
      {
        "field": "name",
        "description": "This field is required"
      }
    ]
  }
}
```

## Permissions API

### Create a Permission

**POST /v1/permissions**

Create a new permission in your project.

**Request Body:**

```json
{
  "project_name": "default",
  "name": "document.read",
  "description": "Permission to read document content"
}
```

**Response:**

```json
{
  "id": "perm_1234567890",
  "organisation_id": "org_0987654321",
  "name": "document.read",
  "description": "Permission to read document content",
  "project_name": "default"
}
```

**Example:**

```bash
curl -X POST https://api.perms.io/v1/permissions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "name": "document.read",
    "description": "Permission to read document content"
  }'
```

### Get a Permission

**GET /v1/permissions/{permission_id}**

Retrieve a permission by its ID.

**Query Parameters:**

- `project_name` - The name of the project the permission belongs to

**Response:**

```json
{
  "id": "perm_1234567890",
  "organisation_id": "org_0987654321",
  "name": "document.read",
  "description": "Permission to read document content",
  "project_name": "default"
}
```

**Example:**

```bash
curl -X GET https://api.perms.io/v1/permissions/perm_1234567890?project_name=default \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Update a Permission

**PATCH /v1/permissions/{permission_id}**

Update an existing permission's name or description.

**Request Body:**

```json
{
  "project_name": "default",
  "name": "document.read.updated",
  "description": "Updated permission description"
}
```

**Response:**

```json
{
  "id": "perm_1234567890",
  "organisation_id": "org_0987654321",
  "name": "document.read.updated",
  "description": "Updated permission description",
  "project_name": "default"
}
```

**Example:**

```bash
curl -X PATCH https://api.perms.io/v1/permissions/perm_1234567890 \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "name": "document.read.updated",
    "description": "Updated permission description"
  }'
```

### List Permissions

**GET /v1/permissions**

List all permissions in your project.

**Query Parameters:**

- `project_name` - The name of the project to list permissions for

**Response:**

```json
{
  "permissions": [
    {
      "id": "perm_1234567890",
      "organisation_id": "org_0987654321",
      "name": "document.read",
      "description": "Permission to read document content",
      "project_name": "default"
    },
    {
      "id": "perm_0987654321",
      "organisation_id": "org_0987654321",
      "name": "document.write",
      "description": "Permission to write document content",
      "project_name": "default"
    }
  ]
}
```

**Example:**

```bash
curl -X GET https://api.perms.io/v1/permissions?project_name=default \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Delete a Permission

**DELETE /v1/permissions/{permission_id}**

Delete a permission by its ID.

**Query Parameters:**

- `project_name` - The name of the project the permission belongs to

**Response:**

Empty response with status code 200.

**Example:**

```bash
curl -X DELETE https://api.perms.io/v1/permissions/perm_1234567890?project_name=default \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Roles API

### Create a Role

**POST /v1/roles**

Create a role that bundles multiple permissions together.

**Request Body:**

```json
{
  "project_name": "default",
  "name": "Document Editor",
  "description": "Can edit and view documents",
  "permissions": ["perm_document_read", "perm_document_write"]
}
```

**Response:**

```json
{
  "id": "role_1234567890",
  "organisation_id": "org_0987654321",
  "name": "Document Editor",
  "description": "Can edit and view documents",
  "permissions": [
    {
      "id": "perm_document_read",
      "organisation_id": "org_0987654321",
      "name": "document.read",
      "description": "Permission to read document content",
      "project_name": "default"
    },
    {
      "id": "perm_document_write",
      "organisation_id": "org_0987654321",
      "name": "document.write",
      "description": "Permission to write document content",
      "project_name": "default"
    }
  ],
  "project_name": "default"
}
```

**Example:**

```bash
curl -X POST https://api.perms.io/v1/roles \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "name": "Document Editor",
    "description": "Can edit and view documents",
    "permissions": ["perm_document_read", "perm_document_write"]
  }'
```

### Get a Role

**GET /v1/roles/{role_id}**

Retrieve a role by its ID.

**Query Parameters:**

- `project_name` - The name of the project the role belongs to

**Response:**

```json
{
  "id": "role_1234567890",
  "organisation_id": "org_0987654321",
  "name": "Document Editor",
  "description": "Can edit and view documents",
  "permissions": [
    {
      "id": "perm_document_read",
      "organisation_id": "org_0987654321",
      "name": "document.read",
      "description": "Permission to read document content",
      "project_name": "default"
    },
    {
      "id": "perm_document_write",
      "organisation_id": "org_0987654321",
      "name": "document.write",
      "description": "Permission to write document content",
      "project_name": "default"
    }
  ],
  "project_name": "default"
}
```

**Example:**

```bash
curl -X GET https://api.perms.io/v1/roles/role_1234567890?project_name=default \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Update a Role

**PATCH /v1/roles/{role_id}**

Update an existing role's name, description, or permissions.

**Request Body:**

```json
{
  "project_name": "default",
  "name": "Document Manager",
  "description": "Updated role description",
  "permissions": ["perm_document_read", "perm_document_write", "perm_document_delete"]
}
```

**Response:**

```json
{
  "id": "role_1234567890",
  "organisation_id": "org_0987654321",
  "name": "Document Manager",
  "description": "Updated role description",
  "permissions": [
    {
      "id": "perm_document_read",
      "name": "document.read",
      "description": "Permission to read document content"
    },
    {
      "id": "perm_document_write",
      "name": "document.write", 
      "description": "Permission to write document content"
    },
    {
      "id": "perm_document_delete",
      "name": "document.delete",
      "description": "Permission to delete documents" 
    }
  ],
  "project_name": "default"
}
```

**Example:**

```bash
curl -X PATCH https://api.perms.io/v1/roles/role_1234567890 \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "name": "Document Manager",
    "description": "Updated role description",
    "permissions": ["perm_document_read", "perm_document_write", "perm_document_delete"]
  }'
```

## Grant Operations

### Grant Permissions and Roles

**POST /v1/grants**

Grant permissions and roles to a principal (user/API key) on a specific resource.

**Request Body:**

```json
{
  "project_name": "default",
  "user_id": "user_1234",
  "resource_uri": "/documents/1234",
  "permissions": ["perm_document_comment"],
  "roles": ["role_document_editor"]
}
```

**Response:**

Empty response with status code 200.

**Example:**

```bash
curl -X POST https://api.perms.io/v1/grants \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "user_id": "user_1234",
    "resource_uri": "/documents/1234",
    "permissions": ["perm_document_comment"],
    "roles": ["role_document_editor"]
  }'
```

### Revoke Permissions and Roles

**DELETE /v1/grants**

Revoke permissions and roles from a principal on a specific resource.

**Request Body:**

```json
{
  "project_name": "default",
  "user_id": "user_1234",
  "resource_uri": "/documents/1234",
  "permissions": ["perm_document_comment"],
  "roles": ["role_document_editor"]
}
```

**Response:**

Empty response with status code 200.

**Example:**

```bash
curl -X DELETE https://api.perms.io/v1/grants \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "user_id": "user_1234",
    "resource_uri": "/documents/1234",
    "permissions": ["perm_document_comment"],
    "roles": ["role_document_editor"]
  }'
```

## Authorization Check

### Check Permission

**POST /v1/check**

Check if a principal has specific permissions on one or more resources.

**Request Body:**

```json
{
  "project_name": "default",
  "principal_id": "user_1234",
  "resource_uris": ["/documents/1234", "/documents/5678"],
  "permissions": ["document.read", "document.write"]
}
```

**Response:**

```json
{
  "passed": false,
  "missing_permissions": [
    {
      "resource_uri": "/documents/5678",
      "missing_permissions": ["document.write"]
    }
  ]
}
```

**Example:**

```bash
curl -X POST https://api.perms.io/v1/check \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "principal_id": "user_1234",
    "resource_uris": ["/documents/1234", "/documents/5678"],
    "permissions": ["document.read", "document.write"]
  }'
```

## Organization Management

### Create an Organization

**POST /v1/organisations**

Create a new organization.

**Request Body:**

```json
{
  "name": "Acme Inc.",
  "user_id": "user_1234567890"
}
```

**Response:**

```json
{
  "organisation": {
    "id": "org_1234567890",
    "name": "Acme Inc.",
    "users": [
      {
        "id": "user_1234567890",
        "email": "user@example.com"
      }
    ],
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
    "billing_customer": {
      "id": "cus_1234567890",
      "organisation_id": "org_1234567890",
      "name": "Acme Inc.",
      "email": "billing@example.com"
    }
  }
}
```

### Project Management

**POST /v1/organisations/{organisation_id}/projects**

Create a new project within an organization.

**Request Body:**

```json
{
  "name": "mobile-app"
}
```

**Response:**

```json
{
  "project": {
    "organisation_id": "org_1234567890",
    "name": "mobile-app",
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

## API Keys

**POST /v1/organisations/{organisation_id}/apikeys**

Create a new API key for accessing the Permio API programmatically.

**Request Body:**

```json
{
  "project_name": "default",
  "name": "Production Service Key"
}
```

**Response:**

```json
{
  "api_key": {
    "id": "apikey_1234567890",
    "name": "Production Service Key",
    "key": "perms_api_1234567890abcdef",
    "created_at": "2025-01-01T00:00:00Z",
    "invalidated": false
  }
}
```

> ⚠️ **Important**: The full API key is only returned once upon creation. Make sure to securely store this key as you won't be able to retrieve it again.

## Error Handling

The API uses standard HTTP response codes to indicate the success or failure of an API request:

- `200 OK` - The request was successful
- `400 Bad Request` - The request was invalid or cannot be served
- `401 Unauthorized` - The API key is missing or invalid
- `403 Forbidden` - The API key does not have permission to perform the requested action
- `404 Not Found` - The requested resource does not exist
- `429 Too Many Requests` - The request was rate limited
- `500 Internal Server Error` - An error occurred on the server

Error responses will include an error object with details:

```json
{
  "error": {
    "code": 403,
    "message": "Permission denied: No permission to view resource",
    "details": [
      {
        "missing_permissions": ["customer.info.view"],
        "resource_uri": "/customer/1234"
      }
    ]
  }
}
```

## Pagination

For endpoints that return collections, results are paginated:

**Request:**

```
GET /v1/permissions?project_name=default&page_size=10&page_token=next_page_token
```

**Response:**

```json
{
  "permissions": [...],
  "next_page_token": "token_for_next_page",
  "total_items": 157
}
```

To get the next page, include the `next_page_token` from the previous response:

```
GET /v1/permissions?project_name=default&page_size=10&page_token=token_for_next_page
```

## Rate Limits

The API enforces rate limits to ensure service stability:

| Plan | Rate Limit |
|------|------------|
| Free | 100 requests per minute |
| Pro  | 1000 requests per minute |
| Enterprise | Custom limits |

Rate limit headers are included in each response:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 55
```

When a rate limit is exceeded, a `429 Too Many Requests` response will be returned:

```json
{
  "error": {
    "code": 429,
    "message": "Rate limit exceeded. Please retry after 45 seconds."
  }
}
```

## Common Request Patterns

### Resource Hierarchy Authorization

Permio's hierarchical design allows you to define permissions at parent levels that automatically propagate to child resources. This is particularly useful for building complex applications.

For example, if you want to grant admin access to all projects within a team:

```bash
curl -X POST https://api.perms.io/v1/grants \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "user_id": "user_1234",
    "resource_uri": "/teams/engineering",
    "roles": ["team_admin"]
  }'
```

Now the user has admin access to `/teams/engineering` and any child resources, such as `/teams/engineering/projects/app1`.

### Batch Permission Checks

You can efficiently check multiple permissions across multiple resources in a single API call:

```bash
curl -X POST https://api.perms.io/v1/check \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "principal_id": "user_1234",
    "resource_uris": [
      "/projects/123",
      "/projects/456",
      "/projects/789"
    ],
    "permissions": [
      "project.view",
      "project.edit"
    ]
  }'
```

This will check if the user has both view and edit permissions on all three project resources in a single request.
