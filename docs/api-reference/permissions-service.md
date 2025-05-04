# Permissions Service API

The Permissions Service is the core of Permio's authorization functionality, allowing you to define permissions, create roles, assign them to resources, and check authorization.

## Permission Operations

### Create a Permission

Create a new permission in your project.

#### gRPC (Go)

```go
permission, err := client.Permissions.CreatePermission(context.Background(), &pb.CreatePermissionRequest{
    ProjectName: "default",
    Name:        "document.read",
    Description: "Permission to read document content",
})
if err != nil {
    log.Fatalf("Failed to create permission: %v", err)
}
log.Printf("Created permission with ID: %v", permission.Id)
```

#### REST API

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

Response:
```json
{
  "id": "perm_1234567890",
  "organisation_id": "org_0987654321",
  "name": "document.read",
  "description": "Permission to read document content",
  "project_name": "default"
}
```

### Get a Permission

Retrieve a permission by its ID.

#### gRPC (Go)

```go
permission, err := client.Permissions.GetPermission(context.Background(), &pb.GetPermissionRequest{
    ProjectName: "default",
    Id:          "perm_1234567890",
})
if err != nil {
    log.Fatalf("Failed to get permission: %v", err)
}
log.Printf("Retrieved permission: %v", permission.Name)
```

#### REST API

```bash
curl -X GET https://api.perms.io/v1/permissions/perm_1234567890?project_name=default \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Update a Permission

Update an existing permission's name or description.

#### gRPC (Go)

```go
permission, err := client.Permissions.UpdatePermission(context.Background(), &pb.UpdatePermissionRequest{
    ProjectName: "default",
    Id:          "perm_1234567890",
    Name:        "document.read.updated",
    Description: "Updated permission description",
})
if err != nil {
    log.Fatalf("Failed to update permission: %v", err)
}
```

#### REST API

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

List all permissions in your project.

#### gRPC (Go)

```go
response, err := client.Permissions.ListPermissions(context.Background(), &pb.ListPermissionsRequest{
    ProjectName: "default",
})
if err != nil {
    log.Fatalf("Failed to list permissions: %v", err)
}

for _, permission := range response.Permissions {
    log.Printf("Permission: %s (%s)", permission.Name, permission.Id)
}
```

#### REST API

```bash
curl -X GET https://api.perms.io/v1/permissions?project_name=default \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Delete a Permission

Delete a permission by its ID.

#### gRPC (Go)

```go
_, err = client.Permissions.DeletePermission(context.Background(), &pb.DeletePermissionRequest{
    ProjectName: "default",
    Id:          "perm_1234567890",
})
if err != nil {
    log.Fatalf("Failed to delete permission: %v", err)
}
```

#### REST API

```bash
curl -X DELETE https://api.perms.io/v1/permissions/perm_1234567890?project_name=default \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Role Operations

### Create a Role

Create a role that bundles multiple permissions together.

#### gRPC (Go)

```go
role, err := client.Permissions.CreateRole(context.Background(), &pb.CreateRoleRequest{
    ProjectName: "default",
    Name:        "Document Editor",
    Description: "Can edit and view documents",
    Permissions: []string{"perm_document_read", "perm_document_write"},
})
if err != nil {
    log.Fatalf("Failed to create role: %v", err)
}
log.Printf("Created role with ID: %v", role.Id)
```

#### REST API

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

Retrieve a role by its ID.

#### gRPC (Go)

```go
role, err := client.Permissions.GetRole(context.Background(), &pb.GetRoleRequest{
    ProjectName: "default",
    Id:          "role_1234567890",
})
if err != nil {
    log.Fatalf("Failed to get role: %v", err)
}
log.Printf("Retrieved role: %v with %d permissions", role.Name, len(role.Permissions))
```

#### REST API

```bash
curl -X GET https://api.perms.io/v1/roles/role_1234567890?project_name=default \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Update a Role

Update an existing role's name, description, or permissions.

#### gRPC (Go)

```go
role, err := client.Permissions.UpdateRole(context.Background(), &pb.UpdateRoleRequest{
    ProjectName: "default",
    Id:          "role_1234567890",
    Name:        "Document Manager",
    Description: "Updated role description",
    Permissions: []string{"perm_document_read", "perm_document_write", "perm_document_delete"},
})
if err != nil {
    log.Fatalf("Failed to update role: %v", err)
}
```

#### REST API

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

### List Roles

List all roles in your project.

#### gRPC (Go)

```go
response, err := client.Permissions.ListRoles(context.Background(), &pb.ListRolesRequest{
    ProjectName: "default",
})
if err != nil {
    log.Fatalf("Failed to list roles: %v", err)
}

for _, role := range response.Roles {
    log.Printf("Role: %s (%s) with %d permissions", role.Name, role.Id, len(role.Permissions))
}
```

#### REST API

```bash
curl -X GET https://api.perms.io/v1/roles?project_name=default \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Delete a Role

Delete a role by its ID.

#### gRPC (Go)

```go
_, err = client.Permissions.DeleteRole(context.Background(), &pb.DeleteRoleRequest{
    ProjectName: "default",
    Id:          "role_1234567890",
})
if err != nil {
    log.Fatalf("Failed to delete role: %v", err)
}
```

#### REST API

```bash
curl -X DELETE https://api.perms.io/v1/roles/role_1234567890?project_name=default \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Grant Operations

### Grant Permissions and Roles

Grant permissions and roles to a principal (user/API key) on a specific resource.

#### gRPC (Go)

```go
_, err = client.Permissions.GrantUserPermissionsAndRolesOnResource(context.Background(), &pb.GrantUserPermissionsAndRolesOnResourceRequest{
    ProjectName: "default",
    UserId:      "user_1234",
    ResourceUri: "/documents/1234",
    Permissions: []string{"perm_document_comment"},
    Roles:       []string{"role_document_editor"},
})
if err != nil {
    log.Fatalf("Failed to grant permissions and roles: %v", err)
}
```

#### REST API

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

Revoke permissions and roles from a principal on a specific resource.

#### gRPC (Go)

```go
_, err = client.Permissions.RevokeUserPermissionsAndRolesOnResource(context.Background(), &pb.RevokeUserPermissionsAndRolesOnResourceRequest{
    ProjectName: "default",
    UserId:      "user_1234",
    ResourceUri: "/documents/1234",
    Permissions: []string{"perm_document_comment"},
    Roles:       []string{"role_document_editor"},
})
if err != nil {
    log.Fatalf("Failed to revoke permissions and roles: %v", err)
}
```

#### REST API

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

### Get User Permissions and Roles on Resource

Get all permissions and roles a principal has on a specific resource.

#### gRPC (Go)

```go
response, err := client.Permissions.GetUserPermissionsAndRolesOnResource(context.Background(), &pb.GetUserPermissionsAndRolesOnResourceRequest{
    ProjectName: "default",
    UserId:      "user_1234",
    ResourceUri: "/documents/1234",
})
if err != nil {
    log.Fatalf("Failed to get user permissions and roles: %v", err)
}

log.Printf("Permissions: %v", response.Permissions)
log.Printf("Roles: %v", response.Roles)
```

#### REST API

```bash
curl -X GET https://api.perms.io/v1/grants/user_1234?project_name=default&resource_uri=/documents/1234 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Get All Assignments For Principal

Get all resource assignments for a principal across the entire hierarchy.

#### gRPC (Go)

```go
response, err := client.Permissions.GetAllAssignmentsForPrincipal(context.Background(), &pb.GetAllAssignmentsForPrincipalRequest{
    ProjectName: "default",
    PrincipalId: "user_1234",
})
if err != nil {
    log.Fatalf("Failed to get assignments: %v", err)
}

for _, assignment := range response.Assignments {
    log.Printf("Resource: %s", assignment.ResourceUri)
    log.Printf("  Permissions: %d, Roles: %d", len(assignment.Permissions), len(assignment.Roles))
}
```

#### REST API

```bash
curl -X GET https://api.perms.io/v1/principals/user_1234/assignments?project_name=default \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Authorization Check

### Check Permission

Check if a principal has specific permissions on one or more resources.

#### gRPC (Go)

```go
response, err := client.Permissions.Check(context.Background(), &pb.CheckPermissionRequest{
    ProjectName:  "default",
    PrincipalId:  "user_1234",
    ResourceUris: []string{"/documents/1234", "/documents/5678"},
    Permissions:  []string{"document.read", "document.write"},
})
if err != nil {
    log.Fatalf("Failed to check permission: %v", err)
}

if response.Passed {
    log.Println("Access granted: User has all requested permissions")
} else {
    log.Println("Access denied")
    for _, missing := range response.MissingPermissions {
        log.Printf("Resource %s is missing permissions: %v", 
            missing.ResourceUri, missing.MissingPermissions)
    }
}
```

#### REST API

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

Response:
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

## Principals Management

### List Principals

List all principals (users and API keys) in your project.

#### gRPC (Go)

```go
response, err := client.Permissions.ListPrincipals(context.Background(), &pb.ListPrincipalsRequest{
    ProjectName: "default",
})
if err != nil {
    log.Fatalf("Failed to list principals: %v", err)
}

log.Printf("Found %d principals", len(response.Principals))
for _, principalId := range response.Principals {
    log.Printf("Principal: %s", principalId)
}
```

#### REST API

```bash
curl -X GET https://api.perms.io/v1/principals?project_name=default \
  -H "Authorization: Bearer YOUR_API_KEY"
```
