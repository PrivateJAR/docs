# Permissions & Roles

Manage permissions, roles, and access control through perms.io's **Resource-Specific Role-Based Access Control (RBAC)** system. Control who can access what resources in your application with fine-grained precision.

## Overview

The permissions system implements a hierarchical RBAC model with the following key components:

- **Permissions**: Individual actions that can be performed (e.g., `read`, `write`, `delete`)
- **Roles**: Collections of permissions that can be assigned as a group
- **Principals**: Users or entities that can be granted permissions
- **Resources**: Specific objects or paths that permissions apply to (e.g., `/project/123`, `/user/456/documents`)

### Key Features

- **Resource-Specific Access**: Permissions apply to specific resource URIs
- **Hierarchical Inheritance**: Permissions on parent resources cascade to child resources
- **Flexible Principal Model**: Support for users, service accounts, and other principal types
- **High-Performance Checks**: Optimized permission checking for real-time applications

## Base URL

```
https://api.perms.io/permissions-service/v1
```

## Permission Management

### Create Permission

Creates a new permission within a project. Permissions are idempotent - creating an existing permission will update it.

**Required Permission**: `permission.create` on `/organisation/{organisation_id}`

=== "HTTP"
    ```http
    POST /permissions
    Content-Type: application/json

    {
      "project_name": "production",
      "name": "document.read",
      "description": "Allows reading documents"
    }
    ```

=== "Go"
    ```go
    package main

    import (
        "context"
        "log"
        
        permissionsv1 "github.com/PrivateJAR/permio-go/proto/permissions/v1"
    )

    func createPermission(client permissionsv1.PermissionsServiceClient) {
        req := &permissionsv1.CreatePermissionRequest{
            ProjectName: "production",
            Name:        "document.read",
            Description: "Allows reading documents",
        }
        
        resp, err := client.CreatePermission(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to create permission: %v", err)
        }
        
        log.Printf("Created permission: %s (ID: %s)", resp.Name, resp.Id)
    }
    ```

=== "Python"
    ```python
    import grpc
    from proto.permissions.v1 import permissions_service_pb2
    from proto.permissions.v1 import permissions_service_pb2_grpc

    def create_permission():
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.CreatePermissionRequest(
            project_name="production",
            name="document.read",
            description="Allows reading documents"
        )
        
        response = client.CreatePermission(request)
        print(f"Created permission: {response.name} (ID: {response.id})")
    ```

=== "Node.js"
    ```javascript
    const grpc = require('@grpc/grpc-js');
    const protoLoader = require('@grpc/proto-loader');

    const packageDefinition = protoLoader.loadSync('permissions_service.proto');
    const permissionsService = grpc.loadPackageDefinition(packageDefinition).permissions.v1;

    const client = new permissionsService.PermissionsService('api.perms.io:443', 
        grpc.credentials.createSsl());

    function createPermission() {
        const request = {
            project_name: 'production',
            name: 'document.read',
            description: 'Allows reading documents'
        };
        
        client.CreatePermission(request, (error, response) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Created permission: ${response.name} (ID: ${response.id})`);
        });
    }
    ```

### Get Permission

Retrieves details of a specific permission.

**Required Permission**: `permission.get` on `/organisation/{organisation_id}/permission/{id}`

=== "HTTP"
    ```http
    GET /permissions/{id}?project_name=production
    ```

=== "Go"
    ```go
    func getPermission(client permissionsv1.PermissionsServiceClient, projectName, permissionId string) {
        req := &permissionsv1.GetPermissionRequest{
            ProjectName: projectName,
            Id:          permissionId,
        }
        
        resp, err := client.GetPermission(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to get permission: %v", err)
        }
        
        log.Printf("Permission: %s - %s", resp.Name, resp.Description)
    }
    ```

### Update Permission

Updates an existing permission.

**Required Permission**: `permission.update` on `/organisation/{organisation_id}/permission/{id}`

=== "HTTP"
    ```http
    PUT /permissions/{id}
    Content-Type: application/json

    {
      "project_name": "production",
      "name": "document.read",
      "description": "Updated description for reading documents"
    }
    ```

### Delete Permission

Deletes a permission. This operation is idempotent.

**Required Permission**: `permission.delete` on `/organisation/{organisation_id}/permission/{id}`

=== "HTTP"
    ```http
    DELETE /permissions/{id}?project_name=production
    ```

### List Permissions

Lists all permissions within a project with optional search and pagination.

**Required Permission**: `permission.list` on `/organisation/{organisation_id}`

=== "HTTP"
    ```http
    GET /permissions?project_name=production&limit=10&cursor=abc123&search=document
    ```

=== "Go"
    ```go
    func listPermissions(client permissionsv1.PermissionsServiceClient, projectName string) {
        req := &permissionsv1.ListPermissionsRequest{
            ProjectName: projectName,
            Pagination: &paginationv1.PaginationRequest{
                Limit: proto.Int32(10),
            },
            Search: proto.String("document"),
        }
        
        resp, err := client.ListPermissions(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to list permissions: %v", err)
        }
        
        for _, permission := range resp.Permissions {
            log.Printf("Permission: %s - %s", permission.Name, permission.Description)
        }
    }
    ```

## Role Management

### Create Role

Creates a new role with a collection of permissions.

**Required Permissions**: 
- `role.create` on `/organisation/{organisation_id}`
- `permission.get` on `/organisation/{organisation_id}/permission/{permission_id}` for each permission

=== "HTTP"
    ```http
    POST /roles
    Content-Type: application/json

    {
      "project_name": "production",
      "name": "document_editor",
      "description": "Can read and write documents",
      "permissions": ["perm_123", "perm_456"]
    }
    ```

=== "Go"
    ```go
    func createRole(client permissionsv1.PermissionsServiceClient, projectName string, permissionIds []string) {
        req := &permissionsv1.CreateRoleRequest{
            ProjectName: projectName,
            Name:        "document_editor",
            Description: "Can read and write documents",
            Permissions: permissionIds,
        }
        
        resp, err := client.CreateRole(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to create role: %v", err)
        }
        
        log.Printf("Created role: %s (ID: %s)", resp.Name, resp.Id)
    }
    ```

=== "Python"
    ```python
    def create_role(permission_ids: list[str]):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.CreateRoleRequest(
            project_name="production",
            name="document_editor",
            description="Can read and write documents",
            permissions=permission_ids
        )
        
        response = client.CreateRole(request)
        print(f"Created role: {response.name} (ID: {response.id})")
    ```

### Get Role

Retrieves details of a specific role, including all associated permissions.

**Required Permission**: `role.get` on `/organisation/{organisation_id}/role/{id}`

=== "HTTP"
    ```http
    GET /roles/{id}?project_name=production
    ```

### Update Role

Updates an existing role's permissions and metadata.

**Required Permission**: `role.update` on `/organisation/{organisation_id}/role/{id}`

=== "HTTP"
    ```http
    PUT /roles/{id}
    Content-Type: application/json

    {
      "project_name": "production",
      "name": "document_editor",
      "description": "Updated description",
      "permissions": ["perm_123", "perm_456", "perm_789"]
    }
    ```

### Delete Role

Deletes a role. This operation is idempotent.

**Required Permission**: `role.delete` on `/organisation/{organisation_id}/role/{id}`

=== "HTTP"
    ```http
    DELETE /roles/{id}?project_name=production
    ```

### List Roles

Lists all roles within a project with optional search and pagination.

**Required Permission**: `role.list` on `/organisation/{organisation_id}`

=== "HTTP"
    ```http
    GET /roles?project_name=production&limit=10&search=editor
    ```

## Access Control

### Grant Permissions and Roles

Grants permissions and roles to a principal on a specific resource. This operation is additive - it won't remove existing permissions.

**Required Permissions**:
- `permission.get` on `/organisation/{organisation_id}/permission/{permission_id}` for each permission
- `role.get` on `/organisation/{organisation_id}/role/{role_id}` for each role  
- `principal.assignment.create` on `/organisation/{organisation_id}/principal/{user_id}`

=== "HTTP"
    ```http
    POST /permissions/assign
    Content-Type: application/json

    {
      "project_name": "production",
      "user_id": "usr_123",
      "resource_uri": "/project/456/documents/789",
      "permissions": ["perm_123"],
      "roles": ["role_456"]
    }
    ```

=== "Go"
    ```go
    func grantPermissions(client permissionsv1.PermissionsServiceClient, userId, resourceUri string, permissions, roles []string) {
        req := &permissionsv1.GrantUserPermissionsAndRolesOnResourceRequest{
            ProjectName: "production",
            UserId:      userId,
            ResourceUri: resourceUri,
            Permissions: permissions,
            Roles:       roles,
        }
        
        _, err := client.GrantUserPermissionsAndRolesOnResource(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to grant permissions: %v", err)
        }
        
        log.Printf("Granted permissions to user %s on resource %s", userId, resourceUri)
    }
    ```

=== "Python"
    ```python
    def grant_permissions(user_id: str, resource_uri: str, permissions: list[str], roles: list[str]):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.GrantUserPermissionsAndRolesOnResourceRequest(
            project_name="production",
            user_id=user_id,
            resource_uri=resource_uri,
            permissions=permissions,
            roles=roles
        )
        
        client.GrantUserPermissionsAndRolesOnResource(request)
        print(f"Granted permissions to user {user_id} on resource {resource_uri}")
    ```

### Revoke Permissions and Roles

Revokes specific permissions and roles from a principal on a resource.

**Required Permission**: `principal.assignment.delete` on the resource URI

=== "HTTP"
    ```http
    POST /permissions/revoke
    Content-Type: application/json

    {
      "project_name": "production",
      "user_id": "usr_123",
      "resource_uri": "/project/456/documents/789",
      "permissions": ["perm_123"],
      "roles": ["role_456"]
    }
    ```

### Get Principal's Permissions

Retrieves all permissions and roles assigned to a principal on a specific resource.

**Required Permission**: `principal.assignment.get` on the resource URI

=== "HTTP"
    ```http
    GET /permissions/user/{user_id}/resource/{resource_uri}?project_name=production
    ```

=== "Go"
    ```go
    func getUserPermissions(client permissionsv1.PermissionsServiceClient, userId, resourceUri string) {
        req := &permissionsv1.GetUserPermissionsAndRolesOnResourceRequest{
            ProjectName: "production",
            UserId:      userId,
            ResourceUri: resourceUri,
        }
        
        resp, err := client.GetUserPermissionsAndRolesOnResource(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to get user permissions: %v", err)
        }
        
        log.Printf("User has %d permissions and %d roles on resource %s", 
            len(resp.Permissions), len(resp.Roles), resourceUri)
    }
    ```

## User Management

### List Users

Lists all users within a project.

**Required Permission**: `principal.list` on `/organisation/{organisation_id}`

=== "HTTP"
    ```http
    GET /permissions/principals?project_name=production&limit=10&search=user
    ```

=== "Go"
    ```go
    func listPrincipals(client permissionsv1.PermissionsServiceClient, projectName string) {
        req := &permissionsv1.ListPrincipalsRequest{
            ProjectName: projectName,
            Pagination: &paginationv1.PaginationRequest{
                Limit: proto.Int32(10),
            },
        }
        
        resp, err := client.ListPrincipals(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to list principals: %v", err)
        }
        
        for _, principal := range resp.Principals {
            log.Printf("Principal: %s", principal)
        }
    }
    ```

### Get User Permissions

Retrieves all permission assignments for a specific user within an organization.

**Required Permission**: `principal.assignment.list` on `/organisation/{organisation_id}/principal/{principal_id}`

=== "HTTP"
    ```http
    GET /permissions/assignments/principal/{principal_id}?project_name=production
    ```

=== "Go"
    ```go
    func getAllAssignments(client permissionsv1.PermissionsServiceClient, projectName, principalId string) {
        req := &permissionsv1.GetAllAssignmentsForPrincipalRequest{
            ProjectName: projectName,
            PrincipalId: principalId,
        }
        
        resp, err := client.GetAllAssignmentsForPrincipal(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to get assignments: %v", err)
        }
        
        for _, assignment := range resp.Assignments {
            log.Printf("Resource: %s, Permissions: %d, Roles: %d", 
                assignment.ResourceUri, len(assignment.Permissions), len(assignment.Roles))
        }
    }
    ```

## Permission Checking

### Check Permissions

The core permission checking endpoint that determines if a principal has specific permissions on resources.

=== "HTTP"
    ```http
    POST /permissions/check
    Content-Type: application/json

    {
      "project_name": "production",
      "principal_id": "usr_123",
      "resource_uris": ["/project/456/documents/789", "/project/456/documents/101"],
      "permissions": ["read", "write"]
    }
    ```

=== "Go"
    ```go
    func checkPermissions(client permissionsv1.PermissionsServiceClient, principalId string, resourceUris, permissions []string) {
        req := &permissionsv1.CheckPermissionRequest{
            ProjectName:  "production",
            PrincipalId:  principalId,
            ResourceUris: resourceUris,
            Permissions:  permissions,
        }
        
        resp, err := client.Check(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to check permissions: %v", err)
        }
        
        if resp.Passed {
            log.Printf("Permission check passed for principal %s", principalId)
        } else {
            log.Printf("Permission check failed:")
            for _, missing := range resp.MissingPermissions {
                log.Printf("  Resource %s missing: %v", missing.ResourceUri, missing.MissingPermissions)
            }
        }
    }
    ```

=== "Python"
    ```python
    def check_permissions(principal_id: str, resource_uris: list[str], permissions: list[str]):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.CheckPermissionRequest(
            project_name="production",
            principal_id=principal_id,
            resource_uris=resource_uris,
            permissions=permissions
        )
        
        response = client.Check(request)
        
        if response.passed:
            print(f"Permission check passed for principal {principal_id}")
        else:
            print("Permission check failed:")
            for missing in response.missing_permissions:
                print(f"  Resource {missing.resource_uri} missing: {missing.missing_permissions}")
    ```

=== "Node.js"
    ```javascript
    function checkPermissions(principalId, resourceUris, permissions) {
        const request = {
            project_name: 'production',
            principal_id: principalId,
            resource_uris: resourceUris,
            permissions: permissions
        };
        
        client.Check(request, (error, response) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            
            if (response.passed) {
                console.log(`Permission check passed for principal ${principalId}`);
            } else {
                console.log('Permission check failed:');
                response.missing_permissions.forEach(missing => {
                    console.log(`  Resource ${missing.resource_uri} missing: ${missing.missing_permissions}`);
                });
            }
        });
    }
    ```

## Resource URI Patterns

Resource URIs follow a hierarchical pattern that enables inheritance:

### URI Structure

```
/organisation/{org_id}/project/{project_name}/resource/{resource_id}
```

### Examples

- `/project/456` - Top-level project resource
- `/project/456/documents` - All documents in project 456
- `/project/456/documents/789` - Specific document 789
- `/user/123` - User resource
- `/user/123/profile` - User's profile

### Inheritance Rules

Permissions granted on parent resources automatically apply to child resources:

- Permission on `/project/456` applies to `/project/456/documents/789`
- Permission on `/user/123` applies to `/user/123/profile`

## Common RBAC Patterns

### Document Management System

```go
// Create permissions
permissions := []string{"document.read", "document.write", "document.delete"}

// Create roles
editorRole := createRole("document_editor", []string{"document.read", "document.write"})
viewerRole := createRole("document_viewer", []string{"document.read"})
adminRole := createRole("document_admin", []string{"document.read", "document.write", "document.delete"})

// Grant permissions
grantPermissions("user_123", "/project/456/documents", []string{}, []string{editorRole.Id})
grantPermissions("user_456", "/project/456/documents/789", []string{}, []string{viewerRole.Id})
```

### Multi-tenant Application

```go
// Organization-level permissions
grantPermissions("user_123", "/organization/789", []string{}, []string{"org_admin"})

// Project-level permissions  
grantPermissions("user_456", "/organization/789/project/456", []string{}, []string{"project_manager"})

// Resource-specific permissions
grantPermissions("user_789", "/organization/789/project/456/resource/123", []string{"read"}, []string{})
```

## Best Practices

### 1. Permission Naming

Use descriptive, hierarchical names:
- `document.read` instead of `read`
- `user.profile.update` instead of `update`
- `billing.invoice.create` instead of `create`

### 2. Resource URI Design

Design URIs to reflect your application's hierarchy:
- Use consistent patterns across resources
- Consider future scalability
- Group related resources under common parents

### 3. Role Management

- Create roles for common permission sets
- Use descriptive role names
- Regularly audit role permissions
- Consider role inheritance patterns

### 4. Performance Optimization

- Batch permission checks when possible
- Cache permission results where appropriate
- Use specific resource URIs rather than wildcards
- Consider permission inheritance in your URI design

### 5. Security Considerations

- Always validate resource URIs
- Use least privilege principle
- Regularly audit permission assignments
- Monitor for permission escalation

## Error Handling

### Common Error Codes

- `INVALID_ARGUMENT` (3): Invalid request parameters
- `NOT_FOUND` (5): Resource not found
- `PERMISSION_DENIED` (7): Insufficient permissions
- `ALREADY_EXISTS` (6): Resource already exists

### Example Error Response

```json
{
  "error": {
    "code": 7,
    "message": "Permission denied: missing required permission 'permission.create' on resource '/organisation/org_123'"
  }
}
```

## Rate Limits

- **Permission Checks**: 10,000 requests per minute
- **Management Operations**: 1,000 requests per minute
- **Bulk Operations**: 100 requests per minute

## Monitoring and Metrics

The service provides metrics for:
- Permission check latency
- Grant/revoke operation counts
- Principal assignment statistics
- Resource access patterns

These metrics are available through the organisation dashboard and usage APIs.