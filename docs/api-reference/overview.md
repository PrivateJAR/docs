# API Reference Overview

Permio offers two primary ways to interact with our API:

1. **gRPC API**: For high-performance, strongly-typed integrations
2. **REST API**: For broader compatibility and ease of use

## Authentication

All API requests require authentication using an API key, which you can create in the Permio dashboard. Include the API key in all requests:

- For gRPC: Use the metadata `authorization: Bearer YOUR_API_KEY`
- For REST: Include the header `Authorization: Bearer YOUR_API_KEY`

## API Services

Permio's API is divided into two main services:

### 1. Permissions Service

The Permissions Service handles all operations related to permissions, roles, and authorization checks.

Key operations:
- Create and manage permissions
- Create and manage roles
- Grant permissions/roles to principals on resources
- Perform permission checks for authorization decisions

[Explore Permissions Service →](permissions-service.md)

### 2. Organisation Service

The Organisation Service manages organization-level operations and project management.

Key operations:
- Create and manage organizations
- Create and manage projects
- Manage API keys
- Handle user invitations and assignments

[Explore Organisation Service →](organisation-service.md)

## Error Handling

API responses use standard HTTP status codes and include detailed error messages in the response body:

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

## Rate Limits

The Permio API implements rate limiting to ensure service stability:

| Plan | Rate Limit |
|------|------------|
| Free | 100 requests per minute |
| Pro  | 1000 requests per minute |
| Enterprise | Custom limits |

If you exceed the limit, you'll receive a `429 Too Many Requests` response.

## SDK Availability

We provide official client libraries for:
- Go (available now)
- Node.js (coming soon)
- Python (coming soon)
- Java (coming soon)

For other languages, you can use our REST API with any HTTP client.

[Go Client SDK Documentation →](../client-sdks/go.md)
[REST API Documentation →](../client-sdks/rest.md)
